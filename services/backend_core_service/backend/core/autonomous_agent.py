import os
"""
autonomous_agent.py: Unified Royal Diadem Backend—explicitly integrates 'silver', 'gold', 'cinnabar', 'combined' (decision/logic and logging)
Each action is logged to 'backend_core_service/logs/autonomy_log.log' with explicit tags and rationales, and to 'backend_core_service/logs/autonomy_enhancements.log' for Sophic Mercury reasoning.

Fine-tuned model integration: default model is now 'ft:gpt-4o-2024-08-06:churchofadeptus:sonny-philosophersstone-v1:BlRr0kpo'. To override, pass 'model=...' explicitly.
"""
import os
import logging
from datetime import datetime
import subprocess
from services.backend_core_service.backend.cinnabar.base import LLMClient
from services.backend_core_service.backend.core.core_agent import symbolic_state
# Sophic Mercury advanced reasoning integration
try:
    from services.backend_core_service.backend.cinnabar.advanced import analyze_text, plan_tasks
except (ImportError, SystemError, ValueError):
    from services.backend_core_service.backend.cinnabar.advanced import analyze_text, plan_tasks
# Log explicit integration steps
_autonomy_enhancements_log = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs/autonomy_enhancements.log'))
def log_sophic_autonomy(message: str):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(_autonomy_enhancements_log, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] {message}\n")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUTONOMY_LOG = os.path.abspath(os.path.join(BASE_DIR, "../../logs/autonomy_log.log"))
CMD_LOG = os.path.abspath(os.path.join(BASE_DIR, "../../logs/cmd_execution.log"))

ERROR_LOG = os.path.abspath(os.path.join(BASE_DIR, "../../logs/error_handling.log"))
logger = logging.getLogger(__name__)

def log_error(message: str, exc: Exception = None):
    dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    err_line = f"[{dt}] [ERROR] {message}"
    if exc is not None:
        err_detail = f" Exception: {str(exc)}"
        err_line += err_detail
    try:
        with open(ERROR_LOG, "a", encoding="utf-8") as f:
            f.write(err_line + "\n")
    except Exception:
        logger.error(f"Severe error: Unable to write to error_handling.log")
    logger.error(err_line)

# ---- Explicit Logging Utils ----
def log_autonomy(message: str, level: str = "INFO"):
    dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{dt}] [AUTONOMY|{level}] {message}\n"
    try:
        with open(AUTONOMY_LOG, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as exc:
        logger.warning(f"Could not write to autonomy_log.log: {exc}")
    logger.info(line.strip())

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
            import shlex
            cmd = shlex.split(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = (result.stdout or "").strip()
        error = (result.stderr or "").strip()
        log_cmd(" ".join(cmd), output, error, result.returncode)
        if result.returncode == 0:
            return output
        else:
            log_error(f"CMD ERROR\nERROR: {error}\nOUTPUT: {output}\nRC: {result.returncode}")
            return f"[CMD ERROR]\nERROR: {error}\nOUTPUT: {output}\nRC: {result.returncode}"
    except Exception as e:
        log_error(f"Exception running CMD: {command_str}", e)
        log_cmd(command_str, "", f"Exception: {str(e)}", -999)
        return f"[CMD EXCEPTION] {e}"

class AutonomousAgent:
    """
    Unified Royal Diadem Autonomous Agent (backend)
    - Explicitly integrates Silver (CMD), Gold (Codex/code-gen), Cinnabar (NLU/Response), Combined (decision logic)
    Sophic Mercury: Each step now uses explicit symbolic/log_sophic_autonomy reasoning
    - Tool selection and result, as well as all actions, are logged to autonomy_log.log and autonomy_enhancements.log
    """
    def __init__(self, system_prompt: str = "You are an explicit autonomous Python agent.", model: str = "ft:gpt-4o-2024-08-06:churchofadeptus:sonny-philosophersstone-v1:BlRr0kpo"): 
        # Use fine-tuned model by default for all LLM calls.
        self.llm = LLMClient(
            system_prompt=system_prompt,
            model=model,
            max_tokens=1024,
            temperature=0.5,
            symbolic_state=symbolic_state,
        )
        self.state = symbolic_state

    def reason_decide_act(self, user_input: str = None, **kwargs):
        """
        Sophic Mercury: Accept text command, reason step-by-step with deep symbolic/chain-of-thought context.
        - Advanced symbolic planning and analysis are included for decision/context.
        - All reasoning steps, tool decisions, and plans are logged to both autonomy log files.
        """
        log = []
        log.append(f"Received user input: {user_input}")
        log_autonomy(f"[COMBINED] Received input: {user_input}")

        if not user_input or not user_input.strip():
            log.append("Input empty: rejecting as invalid.")
            log_autonomy("[COMBINED] Rejected as invalid: input empty.", level="WARNING")
            log_sophic_autonomy("Input empty: rejecting as invalid.")
            self.state.update("autonomous_agent_last_reasoning", log)
            return {"log": log, "decision": "invalid", "result": None, "symbolic_state": self.state.get_state()}

        # --- Step 2: Sophic Mercury symbolic reasoning pipeline ---
        analysis = analyze_text(user_input)
        log_sophic_autonomy(f"Sophic Mercury analysis: {analysis}")
        log.append(f"[SOPHIC] Deep analysis: {analysis.get('analysis','')}")
        log_autonomy(f"[SOPHIC] Deep analysis: {analysis.get('analysis','')}")

        context = self.state.get_state()
        plans = plan_tasks(context)
        log_sophic_autonomy(f"Sophic Mercury plans: {plans}")
        log.append(f"[SOPHIC] Proactive plan suggestion(s): {plans}")
        log_autonomy(f"[SOPHIC] Proactive plan suggestion(s): {plans}")

        # --- Step 3: Enhanced tool decision with Sophic context ---
        decision_prompt = (
            "Analyze the following request with symbolic, philosophical, and practical context. \n"
            "Which path should an autonomous agent select to maximize wisdom, virtue, and efficacy, given this symbolic state?\n"
            f"Sophic Mercury analysis - chain of thought: {analysis.get('chain_of_thought', [])}\n"
            f"Sophic Mercury plans: {plans}\n"
            "SILVER: Run a shell/system command to control the OS or files.\n"
            "GOLD: Generate, edit, or refactor code (Codex/codex_auto).\n"
            "CINNABAR: Interpret/respond as pure LLM/assistant.\n"
            f"Symbolic state summary: {context}\n"
            f"User Request: {user_input}\nType (SILVER/GOLD/CINNABAR):"
        )
        decision_type = self.llm.with_history_context(decision_prompt).strip().upper()
        log.append(f"[SOPHIC] LLM tool decision: {decision_type}")
        log_autonomy(f"[SOPHIC] LLM tool decision (Sophic context) for '{user_input}': {decision_type}")
        log_sophic_autonomy(f"Sophic Mercury tool decision: {decision_type}")

        # --- Step 4: Dispatch to tool
        result = None
        philosophical_explanation = None
        if "SILVER" in decision_type or "CMD" in decision_type:
            log.append(f"[SILVER] Tool selected: CMD. Invoking '{user_input}' with context-sensitive rationale.")
            log_autonomy(f"[SILVER] CMD execution (Virtue) starting: {user_input}")
            log_sophic_autonomy(f"CMD execution (Sophic): {user_input}")
            result = run_cmd(user_input)
            log_autonomy(f"[SILVER] CMD execution done. Result: {result[:200]}", level="RESULT")
            log_sophic_autonomy(f"CMD execution result (Sophic): {result[:200]}")
        elif "GOLD" in decision_type or "CODEX" in decision_type:
            try:
                log.append(f"[GOLD] Tool selected: CODEX CLI (Virtue code-gen)")
                log_autonomy("[GOLD] Using Codex/Codex-auto for code generation (Virtue mode).")
                log_sophic_autonomy("GOLD (CODEX) tool selected, generating script.")
                from services.backend_core_service.backend.core import codex_auto
                code_result = codex_auto.generate_script(user_input)
                result = f"[GOLD][CODEX OUTPUT]\n{code_result}"
                log_autonomy(f"[GOLD] CODEX result: {code_result[:200]}", level="RESULT")
                log_sophic_autonomy(f"CODEX result (Sophic): {code_result[:200]}")
            except Exception as gold_exc:
                log_error("Exception in GOLD/Codex tool selection", gold_exc)
                log_sophic_autonomy(f"Exception in GOLD/Codex: {gold_exc}")
                result = f"[GOLD][EXCEPTION] {gold_exc}"
        else:
            try:
                log.append(f"[CINNABAR] Tool selected: LLM/Assistant/Response (Virtue philosophical fallback).")
                log_autonomy("[CINNABAR] LLM fallback (Virtue philosophical reasoning)")
                log_sophic_autonomy("LLM fallback, symbolic reasoning/response (Sophic)")
                symbolic_result = self.llm.with_history_context(user_input)
                result = f"[CINNABAR][LLM RESULT]\n{symbolic_result}"
                log_autonomy(f"[CINNABAR] LLM result: {symbolic_result[:200]}", level="RESULT")
                log_sophic_autonomy(f"LLM result (Sophic): {symbolic_result[:200]}")
            except Exception as cinnabar_exc:
                log_error("Exception in CINNABAR/LLM tool selection", cinnabar_exc)
                log_sophic_autonomy(f"Exception in CINNABAR/LLM: {cinnabar_exc}")
                result = f"[CINNABAR][EXCEPTION] {cinnabar_exc}"
        # --- Step 5: Final logging, symbolic update ---
        log.append(f"Outcome: {result}")
        log_autonomy(f"[COMBINED] Outcome: {result[:120]}", level="OUTCOME")
        log_sophic_autonomy(f"Outcome (Sophic): {result[:120]}")
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
        Unified Chat API: Accept user text, reason via explicit unified tool-logic,
        select SILVER (CMD), GOLD (Codex), or CINNABAR (LLM), act, and log each step to autonomy_log.log
        The action log includes clear tool tags and outcomes for transparency.
        """
        agent = AutonomousAgent(system_prompt="You are Sonny, the unified backend Royal Diadem agent. For every step, log your explicit tool choices and their result. Clearly state if you pick SILVER, GOLD, or CINNABAR.")
        output = agent.reason_decide_act(chat)
        response = "\n".join([f"[log] {step}" for step in output["log"]])
        response += f"\n\n[Sonny Action: {output['decision']}]\n{output['result']}"
        return response
