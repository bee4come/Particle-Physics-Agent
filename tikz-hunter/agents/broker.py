# tikz-hunter/agents/broker.py
import os
import grpc
from concurrent import futures
from collections import deque
import threading
import time

from proto import a2a_pb2, a2a_pb2_grpc
from google.protobuf.json_format import MessageToJson
import psycopg2
from psycopg2.extras import Json

class A2ABroker(a2a_pb2_grpc.A2ABrokerServicer):
    def __init__(self, db_conn_str):
        self.db_conn_str = db_conn_str
        self.harvest_queue = deque()
        self.parsed_queue = deque()
        self.lock = threading.Lock()
        self.active_streams = []
        print("A2A Broker initialized.")

    def _get_db_connection(self):
        return psycopg2.connect(self.db_conn_str)

    def SubmitHarvestJob(self, request, context):
        with self.lock:
            self.harvest_queue.append(request)
        print(f"Received HarvestJob from {request.harvester_id} for {request.source_url}")
        return a2a_pb2.BrokerResponse(success=True, message="HarvestJob received")

    def GetHarvestJob(self, request, context):
        with self.lock:
            if self.harvest_queue:
                job = self.harvest_queue.popleft()
                print(f"Sending HarvestJob to {request.agent_id}")
                return job
        return a2a_pb2.HarvestJob() # Return empty job if queue is empty

    def SubmitParsedSnippet(self, request, context):
        with self.lock:
            self.parsed_queue.append(request)
        print(f"Received ParsedSnippet for {request.source_url}")
        return a2a_pb2.BrokerResponse(success=True, message="ParsedSnippet received")

    def GetParsedSnippet(self, request, context):
        with self.lock:
            if self.parsed_queue:
                snippet = self.parsed_queue.popleft()
                print(f"Sending ParsedSnippet to {request.agent_id}")
                return snippet
        return a2a_pb2.ParsedSnippet()

    def SubmitValidatedSnippet(self, request, context):
        print(f"Received ValidatedSnippet with hash {request.hash[:8]}...")
        try:
            with self._get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Convert protobuf to a dictionary, then to JSON string for db
                    snippet_json = MessageToJson(request.snippet, preserving_proto_field_name=True)
                    
                    # Using ON CONFLICT to prevent duplicates based on the unique hash
                    cur.execute(
                        """
                        INSERT INTO tikz_snippets (hash, snippet, source_url)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (hash) DO NOTHING;
                        """,
                        (request.hash, snippet_json, request.snippet.source_url)
                    )
                    conn.commit()
                    if cur.rowcount > 0:
                        print(f"Stored snippet with hash {request.hash[:8]} in database.")
                        # Broadcast to active streams
                        self._broadcast(request)
                    else:
                        print(f"Snippet with hash {request.hash[:8]} already exists. Ignored.")

            return a2a_pb2.BrokerResponse(success=True, message="ValidatedSnippet processed")
        except Exception as e:
            print(f"Error storing ValidatedSnippet: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {e}")
            return a2a_pb2.BrokerResponse(success=False, message=str(e))

    def StreamValidatedSnippets(self, request, context):
        print(f"Client {request.client_id} connected for streaming.")
        stream_queue = deque()
        with self.lock:
            self.active_streams.append(stream_queue)
        
        try:
            while context.is_active():
                if stream_queue:
                    yield stream_queue.popleft()
                else:
                    time.sleep(0.5) # Wait for new snippets
        finally:
            with self.lock:
                self.active_streams.remove(stream_queue)
            print(f"Client {request.client_id} disconnected.")

    def _broadcast(self, snippet):
        with self.lock:
            print(f"Broadcasting snippet {snippet.hash[:8]} to {len(self.active_streams)} clients.")
            for q in self.active_streams:
                q.append(snippet)


def serve():
    db_url = os.getenv("POSTGRES_URL")
    if not db_url:
        raise ValueError("POSTGRES_URL environment variable not set.")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    a2a_pb2_grpc.add_A2ABrokerServicer_to_server(A2ABroker(db_conn_str=db_url), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Broker server started on port 50051.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()