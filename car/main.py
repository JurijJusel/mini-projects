import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from rich import print
from rich.progress import track
from pathlib import Path
from constants import BASE_URL, OUTPUT_DIR
import re


def get_soup(page_url):
    """
    Fetches and parses a webpage into a BeautifulSoup object.
    Args:
        page_url (str): The full URL of the page to fetch.
    Returns:
        BeautifulSoup: Parsed HTML content of the page.
    """
    req= requests.get(page_url, headers={"User-Agent":"Mozilla/5.0"})
    req.raise_for_status()
    soup = BeautifulSoup(req.text, "html.parser")
    return soup


def get_links_from_page(soup, page_url):
    """
    Extracts all car listing URLs from a single listing page.
    Args:
        soup (BeautifulSoup): Parsed HTML content of a listing page.
        page_url (str): URL of the current page (for reference/logging).
    Returns:
        list[str]: A list of full URLs to individual car detail pages.
    """
    print("Fetching:", page_url)
    links = []
    for a in soup.find_all("a", class_="car--list-item-element", href=True):
        full_url = urljoin(BASE_URL, a["href"])
        links.append(full_url)
    return links


def get_all_pages_links():
    """
    Iterates through all paginated listing pages and collects all car detail links.
    Returns:
        list[str]: A complete list of all car detail page URLs.
        out:
        [
            'https://www.mkauto.lt/lt/lengvieji-automobiliai/406476/toyota-avensis-verso-2.0',
            'https://www.mkauto.lt/lt/lengvieji-automobiliai/406778/hyundai-santa-fe-2.0',
            'https://www.mkauto.lt/lt/lengvieji-automobiliai/404558/ford-mondeo-2.0',
            'https://www.mkauto.lt/lt/lengvieji-automobiliai/404833/hyundai-accent-1.5'
        ]
    """
    all_links = []
    page = 1
    while True:
        url = BASE_URL + f"/lengvieji-automobiliai?page_id={page}"
        soup = get_soup(url)
        page_links = get_links_from_page(soup, url)
        if not page_links:
            print("No more links found. Stopping at page", page)
            break
        print(f"Found {len(page_links)} links on page {page}")
        for link in page_links:
            all_links.append(link)
        page += 1
        time.sleep(1)

    return all_links


def images_urls_each_car_detail_page(all_links):
    """
    Extracts all image URLs for each car detail page.
    Args:
        all_links (list[str]): List of car detail page URLs.
    Returns:
        list[str]: List of all image URLs found across all car pages.
    """
    images_urls = []
    for link in all_links:
        soup = get_soup(link)
        found = False
        for a in soup.find_all("a", href=True, attrs={"data-lightbox": True}):
            car_image_full_url = urljoin(BASE_URL, a["href"])
            images_urls.append(car_image_full_url)
            found = True
        if not found:
            print("No matching <a> tag found.")
    return images_urls


def save_photos_from_urls(all_cars_urls, output_dir):
    """
    Downloads and saves images from a list of URLs.
    Args:
        all_cars_urls (list[str]): List of image URLs to download.
        output_dir (str | Path): Directory path to save downloaded images.
    Notes:
        Filenames are generated based on the image ID from the URL,
        with an incremented index appended to avoid duplicates.
    """
    base_path = Path(output_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    for img_index, image_url in track(
        enumerate(all_cars_urls, start=1),
        description="Downloading car images ..."):

        try:
            req = requests.get(image_url, timeout=1.5)
            req.raise_for_status()
            match = re.search(r'i\.(\d+)', image_url)
            image_url_id = match.group(1)
            filename = base_path / f"{image_url_id}_image_{img_index}.jpg"

            with open(filename, "wb") as f:
                f.write(req.content)

        except Exception as e:
            print(f"Failed {image_url}: {e}")


def main():
    all_links = get_all_pages_links()
    print("Fetching images urls links ...")
    all_images_url = images_urls_each_car_detail_page(all_links)
    save_photos_from_urls(all_images_url, OUTPUT_DIR)
    print("Done!")


if __name__ == "__main__":
    main()
