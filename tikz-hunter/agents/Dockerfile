# tikz-hunter/agents/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install git for github access if needed byHarvester
RUN apt-get update && apt-get install -y git

COPY requirements.txt .

# Install python dependencies
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Install gRPC tools
RUN python -m pip install grpcio-tools

# Copy the rest of the application code
COPY ./agents /app/agents
COPY ./proto /app/proto
COPY ./config /app/config

# Compile protobuf definitions
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/a2a.proto

# The command to run the services will be specified in the docker-compose.yml
# e.g., CMD ["python", "-m", "agents.broker"]