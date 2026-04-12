# Company Sales Brochure Generator AI

Builds a short brochure for a company using its website content.

The notebook `brochure-generator-experimentation.ipynb` demonstrates an end-to-end workflow:

- Scrape the main website and collect all anchor links.
- Use an LLM to filter and select relevant pages for a brochure (About, Products, Careers, etc.).
- Scrape text content from the relevant pages.
- Combine the content into a single context prompt.
- Generate a brochure in Markdown format using the OpenAI API.

## Setup

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install openai python-dotenv requests beautifulsoup4 tiktoken ipython
```

3. Add your OpenAI key to a `.env` file in this folder:

```env
OPENAI_TUTORIALS_API_KEY=sk-...
```

4. Open and run the notebook:

- `brochure-generator-experimentation.ipynb`
