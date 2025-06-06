# tikz-hunter/agents/validator_agent.py
import time
import os
import grpc
import hashlib
from pydantic import BaseModel, ValidationError, Field
from typing import List
from enum import Enum

from proto import a2a_pb2, a2a_pb2_grpc
from google.protobuf.json_format import MessageToDict

# Enum for allowed process types for stricter validation
class ProcessType(str, Enum):
    DECAY = "decay"
    SCATTERING = "scattering"
    PRODUCTION = "production"
    LOOP = "loop"
    ANNIHILATION = "annihilation"
    OTHER = "other"

# Pydantic model for robust validation of a parsed snippet's structure
class SnippetValidator(BaseModel):
    topic: str = Field(..., min_length=3)
    reaction: str = Field(..., min_length=1)
    particles: List[str] = Field(..., min_items=1)
    description: str = Field(..., min_length=10)
    tikz_code: str = Field(..., min_length=20)
    source_url: str = Field(..., min_length=10)
    process_type: ProcessType
    source_type: str

class ValidatorAgent:
    def __init__(self, broker_address):
        self.broker_address = broker_address
        self.channel = grpc.insecure_channel(self.broker_address)
        self.stub = a2a_pb2_grpc.A2ABrokerStub(self.channel)
        self.agent_id = f"validator-{os.getpid()}"
        self.running = True
        print(f"Validator Agent ({self.agent_id}) initialized, connecting to broker at {self.broker_address}")

    def start(self):
        print("Validator Agent started, waiting for parsed snippets...")
        while self.running:
            try:
                get_job_request = a2a_pb2.GetJobRequest(agent_id=self.agent_id)
                parsed_snippet = self.stub.GetParsedSnippet(get_job_request)

                if parsed_snippet.source_url:
                    print(f"Validating snippet from: {parsed_snippet.source_url}")
                    is_valid, error_message = self.validate_snippet(parsed_snippet)
                    
                    if is_valid:
                        validated_snippet = self.hash_snippet(parsed_snippet)
                        response = self.stub.SubmitValidatedSnippet(validated_snippet)
                        if response.success:
                            print(f"  -> Successfully submitted validated snippet (hash: {validated_snippet.hash[:8]}...)")
                        else:
                            print(f"  -> Failed to submit validated snippet: {response.message}")
                    else:
                        # Handle invalid snippet, e.g., log it or send to a 'needs_review' queue
                        print(f"  -> Validation Failed: {error_message}. Snippet from {parsed_snippet.source_url} rejected.")

                else:
                    print("No parsed snippets available, sleeping for 10 seconds...")
                    time.sleep(10)

            except grpc.RpcError as e:
                print(f"gRPC Error while getting snippet: {e.status()}. Retrying in 15s.")
                time.sleep(15)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                self.stop()

    def validate_snippet(self, snippet_proto: a2a_pb2.ParsedSnippet) -> (bool, str):
        """Validates the snippet using a Pydantic model."""
        try:
            # Convert protobuf message to a dictionary for Pydantic validation
            snippet_dict = MessageToDict(snippet_proto, preserving_proto_field_name=True)
            SnippetValidator(**snippet_dict)
            print("  - Pydantic validation successful.")
            return True, ""
        except ValidationError as e:
            return False, str(e)
        except Exception as e:
            return False, f"An unexpected error occurred during validation: {e}"

    def hash_snippet(self, snippet: a2a_pb2.ParsedSnippet) -> a2a_pb2.ValidatedSnippet:
        """Creates a unique hash for the snippet."""
        # Use a combination of the TikZ code and source URL for a more unique hash
        unique_string = f"{snippet.tikz_code.strip()}+{snippet.source_url.strip()}"
        sha256_hash = hashlib.sha256(unique_string.encode()).hexdigest()
        print(f"  - Generated hash: {sha256_hash}")

        return a2a_pb2.ValidatedSnippet(
            hash=sha256_hash,
            snippet=snippet
        )

    def stop(self):
        print("Validator Agent shutting down.")
        self.running = False
        self.channel.close()

if __name__ == '__main__':
    broker_addr = os.getenv("BROKER_ADDRESS", "localhost:50051")
    agent = ValidatorAgent(broker_address=broker_addr)
    try:
        agent.start()
    except KeyboardInterrupt:
        agent.stop()