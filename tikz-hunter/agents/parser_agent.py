# tikz-hunter/agents/parser_agent.py
import time
import os
import grpc
import google.generativeai as genai
from google.protobuf.json_format import ParseDict
import json

from proto import a2a_pb2, a2a_pb2_grpc

class ParserAgent:
    def __init__(self, broker_address, api_key, model_name="gemini-1.5-pro-latest"):
        self.broker_address = broker_address
        self.channel = grpc.insecure_channel(self.broker_address)
        self.stub = a2a_pb2_grpc.A2ABrokerStub(self.channel)
        self.agent_id = f"parser-{os.getpid()}"
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY must be provided.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        self.running = True
        print(f"Parser Agent ({self.agent_id}) initialized with model {model_name}, connecting to broker at {self.broker_address}")

    def start(self):
        print("Parser Agent started, waiting for jobs...")
        while self.running:
            try:
                get_job_request = a2a_pb2.GetJobRequest(agent_id=self.agent_id)
                harvest_job = self.stub.GetHarvestJob(get_job_request)

                if harvest_job.source_url:
                    print(f"Processing job for: {harvest_job.source_url}")
                    parsed_snippet = self.parse_code_with_llm(harvest_job)
                    if parsed_snippet:
                        response = self.stub.SubmitParsedSnippet(parsed_snippet)
                        if response.success:
                            print(f"Successfully submitted parsed snippet for {harvest_job.source_url}")
                        else:
                            print(f"Failed to submit parsed snippet for {harvest_job.source_url}: {response.message}")
                else:
                    # No job was available
                    print("No harvest jobs available, sleeping for 10 seconds...")
                    time.sleep(10)

            except grpc.RpcError as e:
                print(f"gRPC Error while getting job: {e.status()}. Retrying in 15s.")
                time.sleep(15)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                self.stop()

    def _build_prompt(self, tikz_code):
        return f"""
Analyze the following TikZ-Feynman code and extract structured information.
Your output MUST be a valid JSON object. Do not add any text before or after the JSON.

**TikZ Code:**
```latex
{tikz_code}
```

**JSON Output Format:**
{{
  "topic": "A concise, descriptive title for the physics process.",
  "reaction": "The reaction formula in LaTeX format (e.g., e- e+ -> Z^0).",
  "particles": ["List", "of", "particle", "names", "or", "symbols"],
  "description": "A brief, one-sentence explanation of the diagram.",
  "process_type": "One of: 'decay', 'scattering', 'production', 'loop', 'annihilation', or 'other'."
}}

**Your JSON output:**
"""

    def parse_code_with_llm(self, harvest_job: a2a_pb2.HarvestJob) -> a2a_pb2.ParsedSnippet:
        prompt = self._build_prompt(harvest_job.tikz_code)
        try:
            print("Sending request to LLM for parsing...")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            
            # Clean up the response from the LLM before parsing
            cleaned_json_str = response.text.strip()
            if cleaned_json_str.startswith("```json"):
                cleaned_json_str = cleaned_json_str[7:]
            if cleaned_json_str.endswith("```"):
                cleaned_json_str = cleaned_json_str[:-3]
            
            print(f"LLM response received and cleaned:\n{cleaned_json_str}")
            
            # Parse the JSON string from LLM into a dictionary
            data = json.loads(cleaned_json_str)
            
            # Add the fields that are not from the LLM
            data['tikz_code'] = harvest_job.tikz_code
            data['source_url'] = harvest_job.source_url
            data['source_type'] = "github" # Or determine from URL
            
            # Convert dictionary to protobuf message
            parsed_snippet = a2a_pb2.ParsedSnippet()
            ParseDict(data, parsed_snippet)
            
            return parsed_snippet

        except Exception as e:
            print(f"Error parsing with LLM: {e}")
            return None

    def stop(self):
        print("Parser Agent shutting down.")
        self.running = False
        if self.channel:
            self.channel.close()

if __name__ == '__main__':
    broker_addr = os.getenv("BROKER_ADDRESS", "localhost:50051")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set.")
    else:
        agent = ParserAgent(broker_address=broker_addr, api_key=api_key)
        try:
            agent.start()
        except KeyboardInterrupt:
            agent.stop()