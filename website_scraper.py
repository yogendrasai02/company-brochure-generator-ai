import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Common phrases and patterns that indicate JavaScript is disabled or not supported.
# Ordered roughly from most specific/common to more generic.
# _JS_DISABLED_PATTERNS: list[str] = [
#     # Explicit JS disabled/unavailable messages
#     r"javascript\s+is\s+(currently\s+)?(disabled|not\s+enabled|turned\s+off|unavailable|not\s+supported|blocked|required)",
#     r"(please\s+)?(enable|turn\s+on|allow)\s+javascript",
#     r"you\s+(need\s+to\s+|must\s+)?enable\s+javascript",
#     r"requires?\s+javascript\s+to\s+(be\s+)?(enabled|run|work|function|load)",
#     r"javascript\s+must\s+be\s+enabled",
#     r"javascript\s+has\s+been\s+(disabled|blocked|turned\s+off)",
#     r"javascript\s+is\s+not\s+(running|loading|active|working)",
#     r"javascript\s+support\s+is\s+(disabled|unavailable|required|not\s+detected)",
 
#     # "This app/site/page needs JS"
#     r"this\s+(app|site|page|application|web\s+app)\s+(needs?|requires?|uses?|depends?\s+on)\s+javascript",
#     r"(this\s+)?(site|app|page)\s+(does\s+not\s+work|won'?t\s+work|cannot\s+run)\s+without\s+javascript",
 
#     # Noscript / fallback block signatures
#     r"<noscript",
#     r"to\s+use\s+this\s+(site|app|page|service|application)[^.]{0,60}(enable|turn\s+on)\s+javascript",
#     r"for\s+the\s+best\s+experience[^.]{0,60}enable\s+javascript",
 
#     # Generic "no JS" shorthand
#     r"\bno[\s\-]?js\b",
#     r"\bjavascript[\s\-]?disabled\b",
#     r"(do\s+not|don'?t|never)\s+disable\s+javascript",  # e.g. "do not disable javascript"
 
#     # Browser instruction patterns
#     r"(your\s+)?browser\s+(does\s+not\s+support|has\s+disabled|is\s+blocking)\s+javascript",
#     r"(update|upgrade)\s+your\s+browser\s+to\s+(support|enable)\s+javascript",
 
#     # React / Next.js / Angular default noscript messages
#     r"you\s+need\s+to\s+enable\s+javascript\s+to\s+run\s+this\s+app",
#     r"please\s+enable\s+js\s+(in|on)\s+your\s+browser",
 
#     # Twitter / X style
#     r"javascript\s+is\s+not\s+available",
 
#     # Generic fallback — "without javascript" in a warning context
#     r"without\s+javascript[^.]{0,80}(work|function|display|load|run|use)",
# ]

# # Pre-compile all patterns once for efficiency
# _COMPILED_PATTERNS: list[re.Pattern] = [
#     re.compile(p, re.IGNORECASE | re.DOTALL) for p in _JS_DISABLED_PATTERNS
# ]
 
# # helper function which determines whether a web page indicates that JavaScript is disabled
# def is_javascript_disabled_page(content: str) -> bool:
#     """
#     Detect whether website content indicates that JavaScript is disabled,
#     unavailable, or required but not present.
 
#     Parameters
#     ----------
#     content : str
#         Raw HTML (or plain text) from a web page.
 
#     Returns
#     -------
#     bool
#         True  – the page is telling the user that JS is not enabled.
#         False – no such signal was found.
 
#     Examples
#     --------
#     >>> is_javascript_disabled_page("You need to enable JavaScript to run this app.")
#     True
#     >>> is_javascript_disabled_page("Welcome to our homepage!")
#     False
#     """
#     if not content or not isinstance(content, str):
#         return False
 
#     for pattern in _COMPILED_PATTERNS:
#         if pattern.search(content):
#             return True
 
#     return False

def fetch_website_links(website_url: str) -> list[str]:
    """
    Scrape a website and return a list of all links found in the webpage.
    
    Args:
        website_url (str): The URL of the website to scrape.
    
    Returns:
        list: A list of absolute URLs found in the webpage.
    """
    try:
        response = requests.get(website_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(website_url, a_tag['href'])
            links.append(link)
        return links
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
# function to scrape content of a given link
def fetch_website_content(website_url):
    """
    Scrape a website (single provided url) and return its content as text.
    
    Args:
        website_url (str): The URL of the website to scrape.
    
    Returns:
        str: The text content of the website.
    """
    print("Scraping website content at URL:", website_url)
    try:
        response = requests.get(website_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        # Get text
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    finally:
        print("Finished scraping website content at URL:", website_url)
    
def generate_website_content_context(website_name: str, links: list) -> str:
  """
  Input: website_name - string
  Output: links - list of dictionaries with fields: name, url
  """

  print("Starting to generate website context by scraping all its relevant links")

  content = f"""
  Website Name: {website_name}

  Relavant Links & their Content:\n
  """

  # loop over all the relevant links and scrape their content
  for link in links:
    link_content = fetch_website_content(link['url'])

    # if javascript is not enabled then skip this link
    # if is_javascript_disabled_page(link_content) == False:
    #     print("Skipping link because JS is not enabled:", link['url'])
    #     continue

    content += f"""
    --------------

    Link Name: {link['name']}
    Link URL: {link['url']}
    Link Content: 
    {link_content}

    """

  print("Finished generating website context by scraping all its relevant links")
  return content