from dotenv import load_dotenv
import os
import json

def get_openai_api_key():
  """
  Returns the OpenAI API key from the environment variable.
  """
  OPENAI_API_KEY = os.getenv("OPENAI_TUTORIALS_API_KEY")
  if not "sk-proj" in OPENAI_API_KEY:
    raise ValueError("Please set your OpenAI API key in the .env file")
  return OPENAI_API_KEY

def construct_llm_messages(system_msg: str, user_msg: str):
  return [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_msg}
  ]


def log_llm_token_cost_usage(completion_result: dict):
  """Log detailed token and cost usage from a litellm completion result."""
  try:
    usage = completion_result.get("usage", {})
    if not usage:
      print("No token usage information available in the completion result.")
      return

    # Handle different token field names across providers
    input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens")
    output_tokens = usage.get("output_tokens") or usage.get("completion_tokens")
    total_tokens = usage.get("total_tokens")

    # Reasoning tokens may be nested in completion_tokens_details (Pydantic object)
    reasoning_tokens = (
        usage.get("reasoning_tokens") or
        usage.get("intermediate_tokens")
    )
    if reasoning_tokens is None and hasattr(usage, "completion_tokens_details"):
      try:
        reasoning_tokens = getattr(usage.completion_tokens_details, "reasoning_tokens", None)
      except AttributeError:
        pass

    print("LLM Token Usage:")
    print(f"  input_tokens: {input_tokens}")
    print(f"  reasoning_tokens: {reasoning_tokens}")
    print(f"  output_tokens: {output_tokens}")
    print(f"  total_tokens: {total_tokens}")

    # Cost from _hidden_params (LiteLLM standard)
    hidden_params = completion_result.get("_hidden_params", {})
    response_cost = hidden_params.get("response_cost")

    if response_cost is not None:
      print(f"LLM Cost: ${response_cost:.6f}")
    else:
      print("LLM Cost: Not available in the response.")
  except Exception as e:
    print(f"Error logging token and cost usage: {e}")
    print("Continuing without logging usage details.")