import requests
from bs4 import BeautifulSoup


def parse_meta(soup):
    title = soup.find_all("title")[0].text
    description = ""
    image = ""
    for tag in soup.find_all("meta"):
        if tag.get("name", None) == "description":
            description = tag.get("content", description)
        if tag.get("property", None) == "og:title":
            title = tag.get("content", title)
        if tag.get("property", None) == "og:description":
            description = tag.get("content", description)
        if tag.get("property", None) == "og:image":
            image = tag.get("content", image)
    return {
        "title": title,
        "description": description,
        "image": image
    }


def fetch_url_meta(url):
    headers = {'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        responseText = response.text
        soup = BeautifulSoup(responseText, features="lxml")
        meta = parse_meta(soup)
        return meta
    return None
