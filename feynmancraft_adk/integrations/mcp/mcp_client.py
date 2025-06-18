"""
MCP Client for ParticlePhysics MCP Server
Connects to the external server at https://github.com/uzerone/ParticlePhysics-MCP-Server
Uses the standard MCP protocol for communication
"""

import json
import asyncio
import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
import os
import math

from .particle_name_mappings import normalize_particle_name, PARTICLE_NAME_MAPPINGS

logger = logging.getLogger(__name__)


def sanitize_for_json(obj: Any) -> Any:
    """Recursively sanitize an object to be JSON-serializable."""
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, float):
        if math.isinf(obj):
            return "infinity" if obj > 0 else "-infinity"
        elif math.isnan(obj):
            return "NaN"
        else:
            return obj
    else:
        return obj


class ParticlePhysicsMCPClient:
    """Client for the ParticlePhysics MCP Server using standard MCP protocol."""
    
    def __init__(self):
        """Initialize the MCP client."""
        self.process = None
        self._reader = None
        self._writer = None
        self._request_id = 0
        self._connected = False
        self._lock = asyncio.Lock()
        
    async def connect(self):
        """Connect to the MCP server."""
        async with self._lock:
            if self._connected and self.process and self.process.returncode is None:
                return True
                
            try:
                # Start the MCP server process
                cmd = [
                    "uv", "tool", "run", "--from",
                    "git+https://github.com/uzerone/ParticlePhysics-MCP-Server.git",
                    "pp-mcp-server"
                ]
                
                logger.info(f"Starting MCP server with command: {' '.join(cmd)}")
                
                self.process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env={**os.environ, "PYTHONUNBUFFERED": "1"}
                )
                
                self._reader = self.process.stdout
                self._writer = self.process.stdin
                
                # Wait a moment for server to start
                await asyncio.sleep(1)
                
                # Initialize connection
                await self._initialize()
                
                self._connected = True
                logger.info("Connected to ParticlePhysics MCP Server")
                return True
                
            except Exception as e:
                logger.error(f"Failed to connect to MCP server: {e}")
                await self.disconnect()
                return False
    
    async def _initialize(self):
        """Initialize the MCP connection."""
        # Send initialize request with correct protocol version
        init_request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",  # Updated protocol version
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "feynmancraft-adk",
                    "version": "1.0.0"
                }
            }
        }
        
        logger.debug(f"Sending initialize request: {init_request}")
        response = await self._send_request(init_request)
        
        if not response:
            raise Exception("No response to initialize request")
        
        if "error" in response:
            raise Exception(f"Initialize error: {response['error']}")
            
        logger.debug(f"Initialize response: {response}")
        
        # Send initialized notification
        initialized = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"  # Updated method name
        }
        
        await self._send_notification(initialized)
        logger.info("MCP initialization complete")
    
    def _get_next_id(self) -> int:
        """Get next request ID."""
        self._request_id += 1
        return self._request_id
    
    async def _send_notification(self, notification: Dict[str, Any]):
        """Send a notification (no response expected)."""
        if not self._writer:
            return
            
        try:
            notification_str = json.dumps(notification) + '\n'
            self._writer.write(notification_str.encode())
            await self._writer.drain()
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
    
    async def _send_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a request and wait for response."""
        if not self._writer or not self._reader:
            return None
            
        try:
            # Send request
            request_str = json.dumps(request) + '\n'
            self._writer.write(request_str.encode())
            await self._writer.drain()
            
            # Read response with timeout
            try:
                response_line = await asyncio.wait_for(
                    self._reader.readline(), 
                    timeout=10.0
                )
                if response_line:
                    response = json.loads(response_line.decode())
                    logger.debug(f"Received response: {response}")
                    return response
                else:
                    logger.error("Empty response from server")
                    
            except asyncio.TimeoutError:
                logger.error("Timeout waiting for server response")
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            self._connected = False
            
        return None
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server."""
        # Ensure connected
        if not self._connected:
            success = await self.connect()
            if not success:
                return {"error": "Failed to connect to MCP server"}
        
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        logger.debug(f"Calling tool {tool_name} with args: {arguments}")
        response = await self._send_request(request)
        
        if not response:
            # Try reconnecting once
            logger.warning("No response, attempting reconnection...")
            await self.disconnect()
            success = await self.connect()
            if success:
                response = await self._send_request(request)
            else:
                return {"error": "MCP server connection lost"}
        
        if response and "result" in response:
            result = response["result"]
            # The result contains content array with text
            if isinstance(result, dict) and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    first_content = content[0]
                    if isinstance(first_content, dict) and "text" in first_content:
                        # Parse the JSON text response
                        try:
                            parsed_result = json.loads(first_content["text"])
                            # Sanitize the result to handle Infinity values
                            return sanitize_for_json(parsed_result)
                        except json.JSONDecodeError:
                            return {"text": first_content["text"]}
            return sanitize_for_json(result)
        elif response and "error" in response:
            return {"error": response["error"].get("message", "Unknown error")}
        else:
            return {"error": "Invalid response from server"}
    
    async def disconnect(self):
        """Disconnect from the MCP server."""
        self._connected = False
        if self.process:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")
            finally:
                self.process = None
                self._reader = None
                self._writer = None


# Global client instance
_mcp_client = None
_client_lock = asyncio.Lock()

async def get_mcp_client() -> ParticlePhysicsMCPClient:
    """Get or create the MCP client instance."""
    global _mcp_client
    async with _client_lock:
        if _mcp_client is None:
            _mcp_client = ParticlePhysicsMCPClient()
            await _mcp_client.connect()
    return _mcp_client


# MCP tool functions that map to the 64 tools available in the server
async def search_particle_mcp(query: str, **kwargs) -> Dict[str, Any]:
    """Search for particles using the MCP server."""
    try:
        # Normalize query using centralized mappings
        normalized_query = normalize_particle_name(query)
        if normalized_query != query:
            logger.debug(f"Mapped '{query}' to '{normalized_query}'")
            query = normalized_query
        
        client = await get_mcp_client()
        params = {'query': query}
        params.update(kwargs)
        result = await client.call_tool('search_particle', params)
        
        # Handle the response
        if isinstance(result, dict) and "results" in result:
            # Convert to expected format
            particles = []
            for r in result.get("results", []):
                if isinstance(r, dict) and "name" in r:
                    particles.append(r)
            
            return {
                "particles": particles,
                "total_found": result.get("total_found", len(particles))
            }
        
        return result
    except Exception as e:
        logger.error(f"search_particle_mcp failed: {e}")
        return {"error": str(e)}


async def get_particle_properties_mcp(particle_name: str, **kwargs) -> Dict[str, Any]:
    """Get particle properties using the MCP server."""
    try:
        # Normalize particle name using centralized mappings
        normalized_name = normalize_particle_name(particle_name)
        if normalized_name != particle_name:
            logger.debug(f"Mapped '{particle_name}' to '{normalized_name}'")
            particle_name = normalized_name
        
        client = await get_mcp_client()
        params = {'particle_name': particle_name}
        params.update(kwargs)
        result = await client.call_tool('get_particle_properties', params)
        
        # Format response
        if isinstance(result, dict) and "particle" in result:
            return result
        elif isinstance(result, dict) and "name" in result:
            # Wrap in expected format
            return {"particle": result}
        
        return result
    except Exception as e:
        logger.error(f"get_particle_properties_mcp failed: {e}")
        return {"error": str(e)}


async def validate_quantum_numbers_mcp(particle_name: str, **kwargs) -> Dict[str, Any]:
    """Get quantum numbers using the MCP server."""
    try:
        # Normalize particle name using centralized mappings
        normalized_name = normalize_particle_name(particle_name)
        if normalized_name != particle_name:
            logger.debug(f"Mapped '{particle_name}' to '{normalized_name}'")
            particle_name = normalized_name
            
        client = await get_mcp_client()
        params = {'particle_name': particle_name}
        params.update(kwargs)
        return await client.call_tool('get_particle_quantum_numbers', params)
    except Exception as e:
        logger.error(f"validate_quantum_numbers_mcp failed: {e}")
        return {"error": str(e)}


async def get_branching_fractions_mcp(particle_name: str, **kwargs) -> Dict[str, Any]:
    """Get branching fractions using the MCP server."""
    try:
        # Normalize particle name using centralized mappings
        normalized_name = normalize_particle_name(particle_name)
        if normalized_name != particle_name:
            logger.debug(f"Mapped '{particle_name}' to '{normalized_name}'")
            particle_name = normalized_name
            
        client = await get_mcp_client()
        params = {'particle_name': particle_name}
        params.update(kwargs)
        return await client.call_tool('get_branching_fractions', params)
    except Exception as e:
        logger.error(f"get_branching_fractions_mcp failed: {e}")
        return {"error": str(e)}


async def compare_particles_mcp(particle_names: List[str], **kwargs) -> Dict[str, Any]:
    """Compare particles using the MCP server."""
    try:
        # Map each particle name using centralized mappings
        mapped_names = []
        for name in particle_names:
            normalized = normalize_particle_name(name)
            if normalized != name:
                logger.debug(f"Mapped '{name}' to '{normalized}'")
            mapped_names.append(normalized)
        
        client = await get_mcp_client()
        params = {'particle_names': mapped_names}
        params.update(kwargs)
        return await client.call_tool('compare_particles', params)
    except Exception as e:
        logger.error(f"compare_particles_mcp failed: {e}")
        return {"error": str(e)}


async def convert_units_mcp(value: float, from_units: str, to_units: str, **kwargs) -> Dict[str, Any]:
    """Convert units using the MCP server."""
    try:
        client = await get_mcp_client()
        params = {
            'value': value,
            'from_units': from_units,
            'to_units': to_units
        }
        params.update(kwargs)
        return await client.call_tool('convert_units_advanced', params)
    except Exception as e:
        logger.error(f"convert_units_mcp failed: {e}")
        return {"error": str(e)}


async def check_particle_properties_mcp(particle_name: str, **kwargs) -> Dict[str, Any]:
    """Check particle properties using the MCP server."""
    try:
        # Normalize particle name using centralized mappings
        normalized_name = normalize_particle_name(particle_name)
        if normalized_name != particle_name:
            logger.debug(f"Mapped '{particle_name}' to '{normalized_name}'")
            particle_name = normalized_name
            
        client = await get_mcp_client()
        params = {'particle_name': particle_name}
        params.update(kwargs)
        return await client.call_tool('check_particle_properties', params)
    except Exception as e:
        logger.error(f"check_particle_properties_mcp failed: {e}")
        return {"error": str(e)} 