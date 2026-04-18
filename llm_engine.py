import json
from litellm import completion
from website_scraper import fetch_website_links, generate_website_content_context
from utils import construct_llm_messages, log_llm_token_cost_usage, log_llm_token_cost_usage_streamed

def filter_relevant_links_from_llm(website_name: str, website_url: str, llm_api_key: str, llm_model: str):
  """
  Input: website name and its primary url, along with API key and model

  Processing: uses an LLM to filter out the relavant link for brochure generation
  (using one-shot prompting)

  Output: a structure json in the format specified in the system prompt
  """

  # get all links
  all_links = fetch_website_links(website_url)

  # system prompt to give instructions to the LLM
  system_prompt = """
  You are an expert AI agent who can look at a given set of links, and decide which ones are relevant to be included in a brochure to a company where the target audience could be prospective clients, investors, recruits, etc.

  The useful links could be like the about page, careers page, products page, etc.

  The links should be returned in a JSON format as follows:
  {
    "links": [
      {"name": "About Us", "url": "https://example.com/about"},
      {"name": "Careers", "url": "https://example.com/careers"},
      {"name": "Products", "url": "https://example.com/products"}
    ]
  }
  """

  # user prompt which asks LLM to filter out the relavant links
  user_prompt = f"""
  Below are the list of links found in the website of {website_name} at the URL {website_url}.
  Your task is to decide what links are relavant to create a brochure for the company, where the potential stake holders are prospective clients, investors, recruits, etc.
  Do not include links about non-relavant items like Terms of Service, Privacy Policy, etc. But links to other social media like Twitter, LinkedIn, Instagram might be relavant ones.
  
  Links:
  {"\n".join(all_links)}
  """

  print("Preparing LLM call to filter the relavant links for website:", website_name)

  response = completion(
    api_key=llm_api_key,
    model=llm_model,
    messages=construct_llm_messages(system_prompt, user_prompt)
  )

  print("Done with LLM call to filter the relavant links for website:", website_name)
  log_llm_token_cost_usage(response)

  links_json = json.loads(response.choices[0].message.content)

  return links_json


def generate_brochure_from_llm(website_name: str, relevant_links: dict, llm_api_key: str, llm_model: str):
  brochure_gen_system_prompt = """
  You are a digital marketing expert in creating engaging & energetic short brochures for companies (for prospective clients, investors, recruits, etc.) based on information in relavant pages of the company's website.

  Create the brochure and respond in Markdown format.

  Include emojis to keep content engaging.
  """

  # create the user prompt: which includes the content of the relevant links fo the website
  company_context = generate_website_content_context(website_name, relevant_links['links'])
  user_prompt = f"""
  You are looking at a company called: {website_name}

  Below is the content of various relavant links of the company.
  
  Based on this knowledge, create a short brochure and output in Markdown format. Do not include additional chat messages.

  Company Details:
  {company_context}
  """

  print("Preparing LLM call (with streaming) to generate brochure for website:", website_name)

  stream = completion(
    api_key=llm_api_key,
    model=llm_model,
    messages=construct_llm_messages(brochure_gen_system_prompt, user_prompt),
    stream=True,
  )

  response_accumulator = ""
  final_chunk = None
  for chunk in stream:
    final_chunk = chunk
    delta = chunk.choices[0].delta.content if chunk.choices else None
    if delta:
      response_accumulator += delta
      yield response_accumulator

  print("Done with LLM call (with streaming) to generate brochure for website:", website_name)
  log_llm_token_cost_usage_streamed(final_chunk=final_chunk)

  yield response_accumulator