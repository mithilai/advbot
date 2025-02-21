import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
from vectorstore import add_to_pinecone

# Load environment variables
load_dotenv()
ADVAIDH_WEBSITE_URL = "https://www.advaidh.in"

# Set to track visited links (to avoid duplicates)
visited_links = set()

def scrape_page(url):
    """Scrapes a single page, extracting all meaningful text content."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if request was successful

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title, headings, and text content
        title = soup.title.string.strip() if soup.title else "No Title"
        headings = " ".join([h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])])
        paragraphs = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])

        content = f"{title}\n\n{headings}\n\n{paragraphs}"

        if not paragraphs:  # Skip empty pages
            print(f"⚠️ No meaningful content found on {url}, skipping.")
            return None

        return {"url": url, "content": content}

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None

def get_all_links(url):
    """Finds all internal links on a webpage to crawl more pages."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urljoin(url, href)

            # Ensure it's an internal link
            if urlparse(full_url).netloc == urlparse(ADVAIDH_WEBSITE_URL).netloc:
                links.add(full_url)

        return links

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Could not fetch links from {url}: {e}")
        return set()

def crawl_website(start_url):
    """Crawls the entire website, scraping all linked pages."""
    to_visit = {start_url}  # Queue of links to visit
    all_docs = []

    while to_visit:
        url = to_visit.pop()

        if url in visited_links:
            continue

        print(f"🔍 Scraping: {url}")
        visited_links.add(url)

        page_data = scrape_page(url)
        if page_data:
            all_docs.append(page_data)

        # Find new links and add them to the queue
        new_links = get_all_links(url) - visited_links
        to_visit.update(new_links)

    # Store scraped data in Pinecone
    if all_docs:
        print("🚀 Storing scraped data in Pinecone...")
        add_to_pinecone(all_docs)
    else:
        print("⚠️ No data found to store.")

if __name__ == "__main__":
    crawl_website(ADVAIDH_WEBSITE_URL)
