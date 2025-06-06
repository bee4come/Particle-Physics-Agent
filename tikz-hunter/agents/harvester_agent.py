# tikz-hunter/agents/harvester_agent.py
import time
import os
import grpc
from github import Github, RateLimitExceededException, GithubException
import base64
import re

from proto import a2a_pb2, a2a_pb2_grpc

class HarvesterAgent:
    def __init__(self, broker_address, github_token):
        self.broker_address = broker_address
        self.channel = grpc.insecure_channel(self.broker_address)
        self.stub = a2a_pb2_grpc.A2ABrokerStub(self.channel)
        self.agent_id = f"harvester-{os.getpid()}"
        self.github = Github(github_token)
        # Regex to find TikZ blocks
        self.tikz_block_regex = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)
        print(f"Harvester Agent ({self.agent_id}) initialized, connecting to broker at {self.broker_address}")

    def start(self, query="feynman diagram tikz language:latex", max_repos=50, max_files_per_repo=10):
        print(f"Harvester Agent starting job with query: '{query}'")
        try:
            repositories = self.github.search_code(query, sort="indexed", order="desc")
            print(f"Found {repositories.totalCount} code results. Processing up to {max_repos} repos.")
            
            repo_count = 0
            for repo_file in repositories:
                if repo_count >= max_repos:
                    break
                try:
                    # To avoid hitting rate limits too quickly, we can add a small delay
                    time.sleep(1) 
                    
                    repo = repo_file.repository
                    print(f"\n[Repo] {repo.full_name}")

                    # Search for files within this specific repository
                    contents = repo.get_contents("")
                    files_processed = 0
                    while contents and files_processed < max_files_per_repo:
                        file_content = contents.pop(0)
                        if file_content.type == "dir":
                            # Add directory contents to the list to search, respecting max_files limit
                            if files_processed + len(repo.get_contents(file_content.path)) <= max_files_per_repo:
                                contents.extend(repo.get_contents(file_content.path))
                        elif file_content.name.endswith((".tex", ".tikz")) and files_processed < max_files_per_repo:
                            files_processed += 1
                            print(f"  - [File] {file_content.path}")
                            self._process_file_content(file_content)
                
                except GithubException as e:
                    print(f"  - Error processing repo {repo.full_name}: {e}")
                
                repo_count += 1

        except RateLimitExceededException:
            print("GitHub API rate limit exceeded. Please wait and try again later, or use an authenticated token.")
        except Exception as e:
            print(f"An unexpected error occurred during GitHub search: {e}")

        print("Harvester Agent job finished.")

    def _process_file_content(self, file_content):
        try:
            decoded_content = base64.b64decode(file_content.content).decode('utf-8')
            found_blocks = self.tikz_block_regex.findall(decoded_content)
            
            if found_blocks:
                print(f"    Found {len(found_blocks)} TikZ block(s).")
                for block in found_blocks:
                    job = a2a_pb2.HarvestJob(
                        source_url=file_content.html_url,
                        tikz_code=block,
                        harvester_id=self.agent_id
                    )
                    self._submit_job(job)
        except (UnicodeDecodeError, binascii.Error) as e:
            print(f"    - Could not decode file {file_content.path}: {e}")
        except Exception as e:
            print(f"    - An error occurred processing file content: {e}")

    def _submit_job(self, job):
        try:
            response = self.stub.SubmitHarvestJob(job)
            if response.success:
                print(f"    -> Successfully submitted job for {job.source_url}")
            else:
                print(f"    -> Failed to submit job for {job.source_url}: {response.message}")
        except grpc.RpcError as e:
            print(f"    -> gRPC Error submitting job for {job.source_url}: {e.status()}")


if __name__ == '__main__':
    broker_addr = os.getenv("BROKER_ADDRESS", "localhost:50051")
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("Warning: GITHUB_TOKEN environment variable not set. Using unauthenticated requests, which have lower rate limits.")

    agent = HarvesterAgent(broker_address=broker_addr, github_token=github_token)
    
    # Example query
    # For more targeted searches, you can add filters like `language:latex` or `extension:tex`
    search_query = '"feynmandiagram" "begin{tikzpicture}"'
    
    agent.start(query=search_query, max_repos=30)