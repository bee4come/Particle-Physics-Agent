#!/usr/bin/env python3
"""
Simple test runner for FeynmanCraft ADK agents.
This allows us to test our multi-agent system without requiring the full ADK CLI.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to Python path
# This assumes the script is run from the project root (feynmancraft-adk/)
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
    sys.exit(1)

# Import our agent
try:
    # This is the main orchestrator agent
    from feynmancraft_adk.agent import root_agent
    # Import sub-agents for individual testing
    from feynmancraft_adk.sub_agents.kb_retriever_agent import KBRetrieverAgent
    from feynmancraft_adk.sub_agents.physics_validator_agent import PhysicsValidatorAgent
    from feynmancraft_adk.sub_agents.code_agent import CodeAgent
    print(f"✅ Root agent and sub-agents imported successfully.")
except ImportError as e:
    print(f"❌ Failed to import agents: {e}")
    sys.exit(1)

async def test_individual_agents():
    """Test individual agents to verify their core functionality."""
    print("\n🧪 Testing individual agents...")

    # Test KBRetrieverAgent with local search
    try:
        print("\n📚 Testing KBRetrieverAgent (local search)...")
        # To trigger local search, the prompt must contain "local search"
        # as defined in the agent's instructions.
        query = "beta decay local search"
        # LlmAgents expect a Message object, a simple string is fine for this agent.
        result = await KBRetrieverAgent.run_async(message=query)

        print(f"Retrieval query: '{query}'")
        # The result from an LlmAgent is a message object, its body contains the data.
        retrieved_data = result.body
        print(f"Retrieval result: {retrieved_data}")
        # A simple assertion to check if it returned a list of results
        assert isinstance(retrieved_data, list)
        assert len(retrieved_data) > 0
        assert "Beta decay" in retrieved_data[0].get("topic")
        print("✅ KBRetrieverAgent local search test PASSED.")

    except Exception as e:
        print(f"❌ KBRetrieverAgent test FAILED: {e}")
        import traceback
        traceback.print_exc()

    # Test CodeAgent
    try:
        print("\n💻 Testing CodeAgent...")
        # This task simulates a request from the PhysicsValidatorAgent
        task = {
            "code_spec": {
                "inputs": ["m_e_GeV", "m_mu_GeV"],
                "output": "branching_ratio",
                "template": "branching_ratio = ({m_e_GeV} / {m_mu_GeV})**2\\nprint(branching_ratio)"
            },
            "inputs": {"m_e_GeV": 0.000511, "m_mu_GeV": 0.1057}
        }
        # For LlmAgents, we now pass the structured data as a JSON string.
        import json
        message_str = json.dumps(task)
        result = await CodeAgent.run_async(message=message_str)
        result_body = result.body
        print(f"CodeAgent result: {result_body}")
        assert result_body.get("success") is True
        assert "output" in result_body
        assert abs(result_body["output"] - 2.34e-5) < 1e-7
        print("✅ CodeAgent test PASSED.")

    except Exception as e:
        print(f"❌ CodeAgent test FAILED: {e}")
        import traceback
        traceback.print_exc()

async def test_with_adk_runner():
    """Test the full multi-agent workflow with the ADK InMemoryRunner."""
    print("\n🚀 Testing with full ADK Runner...")

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

        # --- Test Case 1: A query that should use local search ---
        # The prompt includes "local search" to guide the KBRetrieverAgent
        print("\n▶️ Running test case 1: 'neutron decay local search'")
        test_message_local = types.Content(parts=[
            types.TextPart(text="Draw a diagram for neutron decay using a local search")
        ])

        local_events = []
        local_tool_called = False
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.session_id,
            new_message=test_message_local,
            run_config=RunConfig()
        ):
            local_events.append(event)
            # Find the tool call to the KB retriever
            if event.event_type == "tool_code" and "search_local_tikz_examples" in event.event_data.get("code", ""):
                 local_tool_called = True
        
        if local_tool_called:
            print("✅ Correctly called 'search_local_tikz_examples' tool.")
        else:
            print("❌ FAILED to call 'search_local_tikz_examples' tool.")

        print(f"✅ ADK runner (local search) test completed. Generated {len(local_events)} events.")
        
        # --- Test Case 2: A query that would default to BigQuery ---
        # Note: This will fail if BigQuery credentials/project are not set up.
        # We expect it to try and call the bigquery tool.
        print("\n▶️ Running test case 2: 'Z boson decay' (will attempt BigQuery search)")
        test_message_bq = types.Content(parts=[
            types.TextPart(text="Generate a TikZ diagram for Z boson decay to leptons")
        ])

        bq_events = []
        bigquery_tool_called = False
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.session_id,
            new_message=test_message_bq,
            run_config=RunConfig()
        ):
            bq_events.append(event)
            if event.event_type == "tool_code" and "search_bigquery_tikz_examples" in event.event_data.get("code", ""):
                 bigquery_tool_called = True
        
        if bigquery_tool_called:
            print("✅ Correctly attempted to call 'search_bigquery_tikz_examples' tool.")
        else:
            print("⚠️ 'search_bigquery_tikz_examples' was not called. The agent may have chosen the local search tool instead. This is acceptable if it found a good local match first.")


        print(f"✅ ADK runner (BigQuery attempt) test completed. Generated {len(bq_events)} events.")

    except Exception as e:
        print(f"❌ ADK runner test FAILED: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function."""
    print("🔬 FeynmanCraft ADK Agent Test Runner")
    print("=" * 50)
    
    # Test 1: Individual agents
    await test_individual_agents()

    # Test 2: Full ADK runner for the whole system
    await test_with_adk_runner()

    print("\n🎉 Test session completed!")
    print("\nNext steps:")
    print("1. If tests pass, your agents are working correctly.")
    print("2. The BigQuery test may show an error if you haven't configured authentication, which is expected.")
    print("3. To run just this test script: `python test_runner.py`")


if __name__ == "__main__":
    # The ADK uses asyncio, so we run our main function in an event loop.
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n💥 An error occurred during the test run: {e}")
        import traceback
        traceback.print_exc() 