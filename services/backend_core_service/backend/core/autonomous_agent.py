"""
autonomous_agent.py: Simplified Autonomous Agent for explicit text-task reasoning.
"""
import os
import logging
from datetime import datetime
from backend.cinnabar.base import LLMClient
from backend.core.core_agent import symbolic_state

# Log file for explicit autonomy decisions and actions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GLOBAL_LOG_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../logs/autonomy_log.log")
)

logger = logging.getLogger(__name__)

def log_autonomy(message: str):
    """Append to the autonomy log file and logger."""
    dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{dt}] {message}\n"
    try:
        with open(GLOBAL_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as exc:
        logger.warning(f"Could not write to autonomy log: {exc}")
    logger.info(message)

class AutonomousAgent:
    """Simplified explicit, step-by-step autonomous agent (text command only, clear tool-chain)."""
    def __init__(self, system_prompt: str = "You are an explicit autonomous Python agent."):
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
        Accept text command, reason explicitly to use CMD or Codex, act, and log all steps and outcomes.
        """
        log = []
        log.append(f"Received user input: {user_input}")
        log_autonomy(f"Received input: {user_input}")

        # Step 1: Validate input
        if not user_input or not user_input.strip():
            log.append("Input empty: rejecting as invalid.")
            log_autonomy("Rejected as invalid: input empty.")
            self.state.update("autonomous_agent_last_reasoning", log)
            return {"log": log, "decision": "invalid", "result": None, "symbolic_state": self.state.get_state()}

        # Step 2: Explicitly classify as CMD or CODEX via LLM
        decision_prompt = (
            "Classify the following user request explicitly as one of:\n"
            "CMD: For direct shell/system command or OS interaction.\n"
            "CODEX: For any code generation, code editing, or code-related file operations.\n"
            "SYMBOLIC: For questions, general reasoning, or natural language tasks.\n"
            f"Request: {user_input}\nType:"
        )
        decision_type = self.llm.chat(decision_prompt).strip().upper()
        log.append(f"LLM decision: {decision_type}")
        log_autonomy(f"LLM classified input as: {decision_type}")

        # Step 3: Act and explicitly document reasoning
        result = None
        if "CMD" in decision_type:
            log.append("Tool selected: CMD. Preparing to execute as shell/system command.")
            log_autonomy(f"Tool selected: CMD (Shell) for '{user_input}'")
            # Simulate actual CMD; real implementation would run safely via subprocess
            result = f"[SIMULATED CMD] Would run: {user_input}"
            log_autonomy(f"Simulated CMD execution: '{user_input}'")
        elif "CODEX" in decision_type:
            log.append("Tool selected: CODEX CLI. Generating code with Codex (simulated).")
            log_autonomy("Tool selected: CODEX CLI")
            code_task = f"Write or edit code as per: {user_input}"
            code_result = self.llm.chat(code_task)
            result = f"[SIMULATED CODEX] Codex output:\n{code_result}"
            log_autonomy(f"Simulated Codex CLI output: {code_result[:100]}...")
        elif "SYMBOLIC" in decision_type:
            log.append("Tool selected: SYMBOLIC (LLM). Performing reasoning/answer.")
            log_autonomy("Tool selected: SYMBOLIC (LLM)")
            symbolic_result = self.llm.chat(f"Answer or analyze: {user_input}")
            result = f"[SYMBOLIC RESULT]\n{symbolic_result}"
            log_autonomy(f"Symbolic result: {symbolic_result[:100]}...")
        else:
            log.append(f"Unknown tool class '{decision_type}' - fallback to LLM symbolic.")
            log_autonomy(f"Unknown tool type. Fallback to LLM.")
            fallback = self.llm.chat(user_input)
            result = f"[FALLBACK SYMBOLIC]\n{fallback}"

        # Log outcome and update symbolic state
        log.append(f"Outcome: {result}")
        log_autonomy(f"Outcome: {result[:120]}")
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
        Unified Chat API: Accept user text, reason step-by-step, select explicit tool, act, and log all steps.
        Returns: string (assistant response with internal step logs, outcome, and tool rationale).
        Explicitly logs everything to 'backend_core_service/logs/autonomy_log.log'.
        """
        agent = AutonomousAgent(system_prompt="You are Sonny, an explicit backend autonomy agent. Always log and explain your steps and tool choices as you process a user text task. Clearly state if you select CMD or Codex.")
        output = agent.reason_decide_act(chat)
        # Format logs for response
        response = "\n".join([f"[log] {step}" for step in output["log"]])
        response += f"\n\n[Sonny Action: {output['decision']}]\n{output['result']}"
        return response