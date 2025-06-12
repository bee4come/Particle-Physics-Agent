from google.adk.agents import Agent
from google.adk.messages import JSONMessage
from feynmancraft_adk.schemas import DiagramRequest, Plan, PlanStep
import json

class PlannerAgent(Agent):
    """
    将用户 prompt 解析为执行步骤列表。
    首版直接返回固定步骤；后续可接 Gemini function‑calling 优化。
    """
    def __init__(self):
        super().__init__(name="PlannerAgent")
        print(f"{self.name} initialized.")

    def run(self, message: JSONMessage) -> JSONMessage:
        print(f"{self.name} received input: {message.body}")
        req = DiagramRequest(**message.body)
        # 简化：全部步骤都跑
        plan = Plan(steps=[
            PlanStep.RETRIEVE_EXAMPLES,
            PlanStep.GENERATE_TIKZ,
            PlanStep.VALIDATE_TIKZ,
            PlanStep.VALIDATE_PHYSICS,
            PlanStep.FEEDBACK,
        ])
        print(f"{self.name} generated plan: {plan.dict()}")
        return JSONMessage(body=json.loads(plan.json()))

if __name__ == '__main__':
    # This is for local testing of the agent if needed
    planner = PlannerAgent()
    sample_request_body = {"user_prompt": "e+ e- to Z gamma"}
    # ADK messages are typically JSONMessages with a body that is a dict/JSON-serializable
    sample_message = JSONMessage(body=sample_request_body)
    output_message = planner.run(sample_message)
    print(f"PlannerAgent output: {output_message.body}") 