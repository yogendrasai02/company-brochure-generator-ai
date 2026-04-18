from dotenv import load_dotenv
import os
import json
from litellm import completion_cost

def get_openai_api_key():
  """
  Returns the OpenAI API key from the environment variable.
  """
  load_dotenv()
  OPENAI_API_KEY = os.getenv("OPENAI_TUTORIALS_API_KEY")
  if not OPENAI_API_KEY or "sk-proj" not in OPENAI_API_KEY:
    raise ValueError("Please set your OpenAI API key in the .env file or environment variable OPENAI_TUTORIALS_API_KEY")
  return OPENAI_API_KEY

def construct_llm_messages(system_msg: str, user_msg: str):
  return [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_msg}
  ]

def log_llm_token_cost_usage(response):
    """Log token usage and cost from a normal (non-streamed) LiteLLM response."""

    u = response.usage

    input_tokens     = getattr(u, "prompt_tokens",     "N/A")
    output_tokens    = getattr(u, "completion_tokens", "N/A")
    total_tokens     = getattr(u, "total_tokens",      "N/A")
    reasoning_tokens = getattr(u.completion_tokens_details, "reasoning_tokens", "N/A") if u.completion_tokens_details else "N/A"

    try:
        cost = f"${completion_cost(completion_response=response):.6f}"
    except Exception:
        cost = "N/A"

    print("=" * 40)
    print(" " * 10, "TOKEN USAGE & COST")
    print("=" * 40)
    print(f"Input tokens    : {input_tokens}")
    print(f"Output tokens   : {output_tokens}")
    print(f"Reasoning tokens: {reasoning_tokens}")
    print(f"Total tokens    : {total_tokens}")
    print(f"Cost            : {cost}")
    print("=" * 40)


def log_llm_token_cost_usage_streamed(final_chunk):
    """Log token usage and cost from the final chunk of a streamed LiteLLM response."""

    u = getattr(final_chunk, "usage", None)

    if u is None:
        print("No usage data found. Ensure stream_options={'include_usage': True} is set.")
        return

    input_tokens     = getattr(u, "prompt_tokens",     "N/A")
    output_tokens    = getattr(u, "completion_tokens", "N/A")
    total_tokens     = getattr(u, "total_tokens",      "N/A")
    reasoning_tokens = getattr(u.completion_tokens_details, "reasoning_tokens", "N/A") if u.completion_tokens_details else "N/A"

    try:
        cost = f"${completion_cost(completion_response=final_chunk):.6f}"
    except Exception:
        cost = "N/A"

    print("=" * 40)
    print(" " * 10, "TOKEN USAGE & COST")
    print("=" * 40)
    print(f"Input tokens    : {input_tokens}")
    print(f"Output tokens   : {output_tokens}")
    print(f"Reasoning tokens: {reasoning_tokens}")
    print(f"Total tokens    : {total_tokens}")
    print(f"Cost            : {cost}")
    print("=" * 40)