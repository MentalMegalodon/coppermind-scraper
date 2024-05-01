import requests
from bs4 import BeautifulSoup
from sys import argv
from urllib.parse import urljoin


def process_section(section):
    result = []
    for a in section.find_all("a"):
        href = a.get("href")
        # Ignore the section edit links.
        if "edit" not in href:
            result.append(a.text)
            result.extend(scrape_url(href))
            return result
    # The page is a one-section page.
    if section.text == "Plot Summary[edit]":
        next_sibling = section.findNextSibling()
        while next_sibling.name == "p":
            result.append(next_sibling.text.strip())
            next_sibling = next_sibling.findNextSibling()
    elif section.text in (
        "Setting[edit]",
        "Notes[edit]",
        "Characters[edit]",
        "Navigation menu",
        "Epigraph[edit]",
        "Chapter Header[edit]",
        "Notable[edit]",
        "See Also[edit]",
    ):
        return result
    else:
        result.append(section.find("span").text)
        next_sibling = section.findNextSibling()
        while next_sibling and next_sibling.name != "h2":
            if next_sibling.name == "h3":
                result.append(next_sibling.find("span").text)
            if next_sibling.name == "p":
                text = next_sibling.text.strip()
                if text:
                    result.append(text)
            next_sibling = next_sibling.findNextSibling()
    return result


def scrape_url(url):
    main_page = requests.get(urljoin("https://coppermind.net", url))
    soup = BeautifulSoup(main_page.text, "html.parser")
    sections = soup.find_all("h2")
    # Skip the first section as it's the list of contents.
    sections = sections[1:]
    result = [item for section in sections for item in process_section(section)]
    return result


def scrape_summaries(base_url, book):
    print(f"Scraping from {base_url}")
    result = scrape_url(base_url)
    with open(f"output/{book}.txt", "w") as f:
        f.write("\n\n".join(result))


if __name__ == "__main__":
    assert len(argv) == 3, "Must pass one URL and one book."
    base_url = argv[1]
    book = argv[2]
    scrape_summaries(base_url, book)
