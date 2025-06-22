"""
autonomous_agent.py: Advanced Autonomous Agent for proactive coding and symbolic intelligence.
"""
import logging
from backend.cinnabar.base import LLMClient
from backend.core.core_agent import symbolic_state

logger = logging.getLogger(__name__)


class AutonomousAgent:
    """Sophic Mercury: Explicit, step-by-step autonomous reasoning agent with logs and tool hierarchy."""
    def __init__(self, system_prompt: str = "You are an autonomous Python code engineer."):
        self.llm = LLMClient(
            system_prompt=system_prompt,
            model="gpt-4",
            max_tokens=1024,
            temperature=0.5,
            symbolic_state=symbolic_state,
        )
        self.state = symbolic_state

    def reason_decide_act(self, user_input: str = None, **kwargs):
        """
        Unified reasoning: Reason about user request, explicitly log steps, decide the right tool, act and record.
        Returns dict with 'log', 'decision', 'result', and updated symbolic state.
        """
        log = []
        log.append(f"Received user input: {user_input}")
        # Step 1: Parse or reinterpret input/nature
        if not user_input or not user_input.strip():
            log.append("Input empty: rejecting as invalid.")
            self.state.update("autonomous_agent_last_reasoning", log)
            return {"log": log, "decision": "invalid", "result": None, "symbolic_state": self.state.get_state()}

        # Step 2: Classify request type
        llm_decision_prompt = (
            "Classify this request as one of: CMD, CODEX, SYMBOLIC."
            "\nCMD: direct shell/system action."
            "\nCODEX: requires code generation or script edit."
            "\nSYMBOLIC: natural language or knowledge reasoning."
            f"\nRequest: {user_input}\nType:"
        )
        decision_type = self.llm.chat(llm_decision_prompt).strip().upper()
        log.append(f"Decision type by LLM: {decision_type}")

        # Step 3: Decide and act
        result = None
        if "CMD" in decision_type:
            log.append("Selected CMD tool: running shell/system interaction.")
            # Simulate shell command result (actual implementation may vary)
            result = f"[CMD] Would execute: {user_input}"
        elif "CODEX" in decision_type:
            log.append("Selected Codex CLI: generating/modifying code.")
            code_prompt = f"As Codex, write or modify code for this: {user_input}"
            result = self.llm.chat(code_prompt)
        elif "SYMBOLIC" in decision_type:
            log.append("Selected Symbolic AI: NLU/LLM-based reasoning.")
            symbolic_prompt = f"As Symbolic AI, answer or analyze: {user_input}"
            result = self.llm.chat(symbolic_prompt)
        else:
            log.append("Unrecognized decision type. Using fallback symbolic LLM.")
            result = self.llm.chat(user_input)

        self.state.update("autonomous_agent_last_reasoning", log)
        self.state.update("autonomous_agent_last_decision", decision_type)
        self.state.update("autonomous_agent_last_result", result)
        return {
            "log": log,
            "decision": decision_type,
            "result": result,
            "symbolic_state": self.state.get_state(),
        }

    @staticmethod
    def process_chat(chat: str):
        """
        Unified Chat API: Log steps, reason, pick tool, return reply string.
        Returns assistant response string, logs explicit steps in symbolic_state.
        """
        agent = AutonomousAgent(system_prompt="You are Sonny, a transparent, step-wise, explicit autonomous agent. Explain your steps as you act.")
        output = agent.reason_decide_act(chat)
        response = "\n".join([
            f"[log] {step}" for step in output["log"]
        ])
        # Response summary
        response += f"\n\n[Sonny Action: {output['decision']}]\n{output['result']}"
        return response