"""
autonomous_agent.py: Simplified Autonomous Agent for explicit text-task reasoning.
"""
import os
import logging
from datetime import datetime
from backend.cinnabar.base import LLMClient
from backend.core.core_agent import symbolic_state
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUTONOMY_LOG = os.path.abspath(os.path.join(BASE_DIR, "../../logs/autonomy.log"))
CMD_LOG = os.path.abspath(os.path.join(BASE_DIR, "../../logs/cmd_execution.log"))

logger = logging.getLogger(__name__)

def log_autonomy(message: str, level: str = "INFO"):
    """Structured log for all backend autonomy decisions and tool actions."""
    dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{dt}] [AUTONOMY|{level}] {message}\n"
    try:
        with open(AUTONOMY_LOG, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as exc:
        logger.warning(f"Could not write to autonomy.log: {exc}")
    logger.info(message)

def log_cmd(command, output, error, returncode):
    dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(CMD_LOG, "a", encoding="utf-8") as f:
            f.write(
                f"[{dt}] [AUTONOMY|CMD] EXECUTE: {command}\n"
                f"[{dt}] [AUTONOMY|CMD] OUTPUT: {output}\n"
                f"[{dt}] [AUTONOMY|CMD] ERROR: {error}\n"
                f"[{dt}] [AUTONOMY|CMD] RETURNCODE: {returncode}\n"
            )
    except Exception as exc:
        logger.warning(f"Could not write to cmd_execution.log: {exc}")

def run_cmd(command_str):
    """Safely execute shell command and log it. Returns output string or error."""
    cmd = command_str if isinstance(command_str, list) else command_str.strip()
    log_autonomy(f"CMD Execution requested: {cmd}")
    # Recommend shell-interpreter parsing only if genuinely required
    try:
        # Prefer splits/simple parsing if command_str is str
        if isinstance(cmd, str):
            # Use shlex.split for real security, but here basic split
            import shlex
            cmd = shlex.split(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = (result.stdout or "").strip()
        error = (result.stderr or "").strip()
        log_cmd(" ".join(cmd), output, error, result.returncode)
        if result.returncode == 0:
            return output
        else:
            return f"[CMD ERROR]\nERROR: {error}\nOUTPUT: {output}\nRC: {result.returncode}"
    except Exception as e:
        log_cmd(command_str, "", f"Exception: {str(e)}", -999)
        return f"[CMD EXCEPTION] {e}"

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

        # Step 2: Classifier prompt and tool autonomous selection (Gold, Silver, Cinnabar, Combined logic unified)
        decision_prompt = (
            "Classify this request explicitly as one and only one tool: \n"
            "CMD: Run a shell/system command when user intent is to interact with the OS or files directly. \n"
            "CODEX: For any code generation, editing, refactoring, or code completion.\n"
            f"Request: {user_input}\nType:"
        )
        decision_type = self.llm.chat(decision_prompt).strip().upper()
        log.append(f"LLM tool decision: {decision_type}")
        log_autonomy(f"LLM tool decision for '{user_input}': {decision_type}")

        # Step 3: Unified explicit action and logging
        result = None
        if "CMD" in decision_type:
            log.append("Tool: CMD. Invoking securely.")
            log_autonomy(f"Tool: CMD. Executing '{user_input}'")
            result = run_cmd(user_input)
            log_autonomy(f"CMD execution done. Result: {result[:200]}", level="RESULT")
        elif "CODEX" in decision_type:
            log.append("Tool: CODEX CLI. Generating code.")
            log_autonomy("Tool: CODEX CLI. Generating or editing code.")
            # Use Codex module for generation or modification
            from backend.core import codex_auto
            code_result = codex_auto.generate_script(user_input)
            result = f"[CODEX OUTPUT]\n{code_result}"
            log_autonomy(f"CODEX result: {code_result[:200]}", level="RESULT")
        else:
            # Default to symbolic LLM reasoning path (Cinnabar/Cinnabar Response)
            log.append("Tool: LLM fallback - responding as symbolic/assistant.")
            log_autonomy("Tool: SYMBOLIC/LLM fallback (responding as assistant)")
            symbolic_result = self.llm.chat(user_input)
            result = f"[SYMBOLIC/LLM RESULT]\n{symbolic_result}"
            log_autonomy(f"LLM result: {symbolic_result[:200]}", level="RESULT")

        # Log outcome and update symbolic state
        log.append(f"Outcome: {result}")
        log_autonomy(f"Outcome: {result[:120]}", level="OUTCOME")
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