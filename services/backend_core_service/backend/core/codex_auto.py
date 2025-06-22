# codex_auto.py: Utilities for autonomous code generation via OpenAI API and Codex CLI.

import os
import subprocess
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
logger = logging.getLogger(__name__)

# Injection log
INJ_LOGFILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../logs/openai_injections.log"))
def log_openai_injection(kind: str, prompt: str, response: str = None):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(INJ_LOGFILE, "a", encoding="utf-8") as f:
            entry = f"[{ts}][{kind}] Prompt: {prompt!r}\n"
            if response is not None:
                entry += f"[{ts}][{kind}] Response: {response!r}\n"
            f.write(entry)
    except Exception as exc:
        logger.warning(f"Failed to log injection: {exc}")

def generate_script(prompt: str, model: str = "gpt-4", max_tokens: int = 1024) -> str:
    """Generate a new Python script based on the given prompt. (Logged/Structured for data collection)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    # Structured identifiable prompt
    system_prompt = "[SONNY-CODE-GEN][CAELUS-DISCOVERY] You are a helpful Python code generator collaborating to explore the 'Caelus' phase. PromptID:gen_script"
    user_prompt = f"[SONNY-CODE-GEN-REQ][CAELUS-SEARCH] Please generate code aligned with discovering Caelus: {prompt}"
    log_openai_injection("GEN_SCRIPT_REQ", user_prompt)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.2,
            n=1,
        )
        code = response.choices[0].message.content
        log_openai_injection("GEN_SCRIPT_RESP", user_prompt, response=code)
        return code
    except Exception:
        logger.exception("Error generating script")
        raise

def modify_script(file_path: str, instructions: str, model: str = "gpt-4", max_tokens: int = 1024) -> None:
    """Modify an existing Python script based on instructions. (Logged/Structured for data collection)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()
        user_prompt = (
            f"[SONNY-CODE-MODIFY-REQ][CAELUS-SEARCH] Original Python script for Caelus discovery:\n{original}\n\n"
            f"Instructions (for Caelus phase): {instructions}\n\n"
            "Provide the modified full script."
        )
        system_prompt = "[SONNY-CODE-MODIFY][CAELUS-DISCOVERY] You are a Python code refiner contributing insights for discovering Caelus. PromptID:mod_script"
        log_openai_injection("MOD_SCRIPT_REQ", user_prompt)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.2,
            n=1,
        )
        modified = response.choices[0].message.content
        log_openai_injection("MOD_SCRIPT_RESP", user_prompt, response=modified)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified)
    except Exception:
        logger.exception("Error modifying script")
        raise

def run_codex_cli(command: list, cwd: str = None) -> subprocess.CompletedProcess:
    """Run a Codex CLI command as subprocess."""
    logger.info(f"Running Codex CLI command: {command}")
    try:
        result = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, check=True
        )
        return result
    except subprocess.CalledProcessError:
        logger.exception("Error running Codex CLI command: %s", command)
        raise