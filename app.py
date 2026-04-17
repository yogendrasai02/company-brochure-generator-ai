from llm_engine import filter_relevant_links_from_llm, generate_brochure_from_llm
from utils import get_openai_api_key

if __name__ == "__main__":
  OPENAI_API_KEY = get_openai_api_key()
  LLM_MODEL = "openai/gpt-5-mini"

  WEBSITE_NAME = "Sarvam.AI"
  WEBSITE_URL = "https://sarvam.ai"

  relevant_links = filter_relevant_links_from_llm(WEBSITE_NAME, WEBSITE_URL, llm_api_key=OPENAI_API_KEY, llm_model=LLM_MODEL)
  
  llm_brochure_generation_response_markdown = generate_brochure_from_llm(website_name=WEBSITE_NAME, relevant_links=relevant_links, llm_api_key=OPENAI_API_KEY, llm_model=LLM_MODEL)