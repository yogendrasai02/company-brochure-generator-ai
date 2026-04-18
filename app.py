import gradio as gr
from llm_engine import filter_relevant_links_from_llm, generate_brochure_from_llm
from utils import get_openai_api_key

LLM_MODEL = "openai/gpt-5-mini"

def generate_brochure_ui(website_name: str, website_url: str):
  """Generator function that yields brochure text chunks for Gradio streaming."""

  # validate that website name and url are not empty
  if not website_name or not website_url:
    yield "**Please enter the website name and URL before generating a brochure.**", ""
    return

  # load the openai api key
  OPENAI_API_KEY = get_openai_api_key()
  
  # small inline spinner HTML to show while processing
  spinner_on = """
  <div style='display:inline-block;vertical-align:middle'>
    <style>@keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}</style>
    <div style='width:18px;height:18px;border:3px solid #eee;border-top:3px solid #007bff;border-radius:50%;animation:spin 1s linear infinite;display:inline-block;margin-right:8px;'></div>
  </div>
  """

  # indicate first step to the user
  yield "", "Gathering relevant links...", ""

  # LLM Call 1: filter out relevant links from the primary url of the company
  relevant_links = filter_relevant_links_from_llm(
    website_name,
    website_url,
    llm_api_key=OPENAI_API_KEY,
    llm_model=LLM_MODEL,
  )

  # LLM Call 2: generate brochure from the filtered links, using streaming
  try:
    yield "", "Creating brochure...", spinner_on

    brochure_stream = generate_brochure_from_llm(
      website_name,
      relevant_links,
      llm_api_key=OPENAI_API_KEY,
      llm_model=LLM_MODEL,
    )

    # Stream each incremental chunk to the UI and keep status updated
    accummulated_brochure = None
    for chunk in brochure_stream:
      # chunk is the incremental/accumulated markdown string
      accummulated_brochure = chunk
      yield accummulated_brochure, "Creating brochure...", spinner_on

    # Final status update — keep brochure content, hide spinner
    yield accummulated_brochure, "Done — Brochure generated ✅", ""
  except Exception as e:
    yield None, f"Error: {e}", ""


if __name__ == "__main__":
  with gr.Blocks(title="Company Brochure Generator") as demo:
    gr.Markdown("# 📝 Company Brochure Generator")
    gr.Markdown("Enter a website name and URL, then click **Generate Brochure** to produce brochure content in Markdown.")

    with gr.Row():
      website_name_input = gr.Textbox(label="Website Name", info="e.g. Sarvam AI", lines=1)
      website_url_input = gr.Textbox(label="Website URL", info="e.g. https://sarvam.ai", lines=1)

    generate_button = gr.Button("Generate Brochure")
    brochure_output = gr.Markdown(label="Brochure Output")
    status_output = gr.Markdown(label="Status")
    # simple inline spinner (hidden when empty string is returned)
    spinner_html = gr.HTML("", elem_id="loading-spinner")

    generate_button.click(
      fn=generate_brochure_ui,
      inputs=[website_name_input, website_url_input],
      outputs=[brochure_output, status_output, spinner_html],
    )

  demo.launch(server_port=3000)
