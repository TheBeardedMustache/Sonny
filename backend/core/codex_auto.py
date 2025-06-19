# codex_auto.py: Utilities for autonomous code generation via OpenAI API and Codex CLI.
import os
from dotenv import load_dotenv
import logging
import subprocess
import openai

load_dotenv()

logger = logging.getLogger(__name__)

def generate_script(prompt: str, model: str = "gpt-4", max_tokens: int = 1024) -> str:
    """Generate a new Python script based on the given prompt."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful Python code generator."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.2,
            n=1,
        )
        code = response.choices[0].message.content
        return code
    except Exception:
        logger.exception("Error generating script")
        raise

def modify_script(file_path: str, instructions: str, model: str = "gpt-4", max_tokens: int = 1024) -> None:
    """Modify an existing Python script based on instructions."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()
        prompt = (
            f"Original Python script:\n{original}\n\n"
            f"Instructions: {instructions}\n\n"
            "Provide the modified full script."
        )
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Python code refiner."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.2,
            n=1,
        )
        modified = response.choices[0].message.content
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