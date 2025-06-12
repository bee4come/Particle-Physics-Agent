#!/usr/bin/env python3
"""
Simple test runner for FeynmanCraft ADK agents.
This allows us to test our multi-agent system without requiring the full ADK CLI.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import required ADK components
try:
    from google.adk.agents.run_config import RunConfig
    from google.adk.runners import InMemoryRunner
    from google.adk.sessions import InMemorySessionService
    from google.adk.artifacts import InMemoryArtifactService
    from google.genai import types
    print("✅ ADK imports successful")
except ImportError as e:
    print(f"❌ ADK import failed: {e}")
    print("This might be due to the early version of google-adk installed.")
    print("Let's try a simpler test approach...")

# Import our agent
try:
    from app.agent import root_agent
    print(f"✅ Root agent imported: {root_agent.name}")
except ImportError as e:
    print(f"❌ Failed to import root agent: {e}")
    sys.exit(1)

# Test individual agents first
def test_individual_agents():
    """Test individual agents without the full ADK runner."""
    print("\n🧪 Testing individual agents...")
    
    # Test TikzValidatorAgent first (since it has the most complete implementation)
    try:
        from agents.tikz_validator_agent import TikZValidatorAgent
        from google.adk.messages import JSONMessage
        
        print("\n📝 Testing TikZValidatorAgent...")
        validator = TikZValidatorAgent()
        
        # Test with valid TikZ code
        test_tikz = {
            "code": "\\begin{tikzpicture}\\node{Hello World};\\end{tikzpicture}",
            "description": "A simple test diagram"
        }
        message = JSONMessage(body=test_tikz)
        result = validator.run(message)
        print(f"Validation result: {result.body}")
        
    except Exception as e:
        print(f"❌ TikZValidatorAgent test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test other stub agents
    try:
        from agents.planner_agent import PlannerAgent
        from google.adk.messages import JSONMessage
        
        print("\n📋 Testing PlannerAgent...")
        planner = PlannerAgent()
        
        test_request = {"user_prompt": "electron positron annihilation"}
        message = JSONMessage(body=test_request)
        result = planner.run(message)
        print(f"Planning result: {result.body}")
        
    except Exception as e:
        print(f"❌ PlannerAgent test failed: {e}")

def test_simple_orchestrator():
    """Test the orchestrator with a simple mock setup."""
    print("\n🎭 Testing OrchestratorAgent with simplified setup...")
    
    try:
        # Import individual agents for direct testing
        from agents.planner_agent import PlannerAgent
        from agents.kb_retriever_agent import KBRetrieverAgent
        from agents.diagram_generator_agent import DiagramGeneratorAgent
        from agents.tikz_validator_agent import TikZValidatorAgent
        from google.adk.messages import JSONMessage
        
        # Create a simple workflow manually
        print("Creating agent instances...")
        planner = PlannerAgent()
        retriever = KBRetrieverAgent()
        generator = DiagramGeneratorAgent()
        validator = TikZValidatorAgent()
        
        print("Testing workflow step by step...")
        
        # Step 1: Planning
        request = {"user_prompt": "electron positron annihilation to two photons"}
        plan_result = planner.run(JSONMessage(body=request))
        print(f"1. Planning: {plan_result.body}")
        
        # Step 2: Knowledge Retrieval  
        retrieval_result = retriever.run(JSONMessage(body={}))
        print(f"2. Knowledge Retrieval: Found {len(retrieval_result.body.get('examples', []))} examples")
        
        # Step 3: Generation
        gen_input = {
            "description": request["user_prompt"],
            "examples": retrieval_result.body.get("examples", [])
        }
        generation_result = generator.run(JSONMessage(body=gen_input))
        print(f"3. Generation: {generation_result.body}")
        
        # Step 4: Validation
        validation_result = validator.run(generation_result)
        print(f"4. Validation: {validation_result.body}")
        
        print("\n✅ Simple workflow test completed successfully!")
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_with_adk_runner():
    """Test with proper ADK runner if available."""
    print("\n🚀 Testing with ADK Runner...")
    
    try:
        # Create ADK services
        artifact_service = InMemoryArtifactService()
        session_service = InMemorySessionService()
        
        # Create session
        user_id = 'test_user'
        session = await session_service.create_session(
            app_name="feynmancraft", user_id=user_id
        )
        
        # Create runner
        runner = InMemoryRunner(
            app_name="feynmancraft",
            agent=root_agent,
            artifact_service=artifact_service,
            session_service=session_service
        )
        
        # Test message
        test_message = types.Content(parts=[
            types.TextPart(text="Generate a TikZ diagram for electron positron annihilation")
        ])
        
        print("Running agent with ADK runner...")
        events = []
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.session_id,
            new_message=test_message,
            run_config=RunConfig()
        ):
            events.append(event)
            print(f"Event: {event}")
        
        print(f"✅ ADK runner test completed. Generated {len(events)} events.")
        
    except Exception as e:
        print(f"❌ ADK runner test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function."""
    print("🔬 FeynmanCraft ADK Agent Test Runner")
    print("=" * 50)
    
    # Test 1: Individual agents
    test_individual_agents()
    
    # Test 2: Simple orchestrator workflow
    test_simple_orchestrator()
    
    # Test 3: ADK runner (if available)
    try:
        asyncio.run(test_with_adk_runner())
    except Exception as e:
        print(f"⚠️  ADK runner test skipped: {e}")
    
    print("\n🎉 Test session completed!")
    print("\nNext steps:")
    print("1. If tests pass, your agents are working correctly")
    print("2. You can use 'python test_runner.py' for quick testing")
    print("3. For web UI, try: python -m http.server 8000 (for static files)")
    print("4. Consider upgrading google-adk to a newer version for full CLI support")

if __name__ == "__main__":
    main() 