# tikz-hunter/web/api/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install gRPC tools and compile protobufs
# The proto files are copied from the project root
RUN pip install grpcio-tools
COPY proto /app/proto
RUN python -m grpc_tools.protoc -I/app/proto --python_out=. --grpc_python_out=. /app/proto/a2a.proto

# Copy the API source code
COPY web/api /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]