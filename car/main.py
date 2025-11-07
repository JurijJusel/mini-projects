import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from rich import print
from rich.progress import track
from pathlib import Path
from constants import BASE_URL, OUTPUT_DIR, JSON_FILE_PATH
from file import create_data_json_file, open_json_file


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


def get_each_car_detail_page_data(all_links):
    """
    Extracts image URLs and basic metadata (car model, page URL)
    for each car detail page.
    Args:
        all_links (list[str]): List of car detail page URLs.
    Returns:
        list[dict]: A list of dictionaries with keys:
                    - car_model
                    - car_page_url
                    - car_image_full_url
    """
    result = []
    for _ , link in track(
        enumerate(all_links, start=1),
        description="Scanning car detail pages...",
        total=len(all_links)):

        soup = get_soup(link)
        car_page_url = link
        car_model = soup.title.text.strip() if soup.title else "Unknown"

        for a in soup.find_all("a", href=True, attrs={"data-lightbox": True}):
            car_image_full_url = urljoin(BASE_URL, a["href"])

            data = {
                "car_model" : car_model,
                "car_page_url" : car_page_url,
                "car_image_full_url" : car_image_full_url
            }
            result.append(data)
    return result


def save_photos_from_urls(json_data: list[dict], output_dir: str):
    """
    Downloads car images from a list of dictionaries and saves them to a folder.
    Each dictionary in `json_data` should contain:
        - 'car_model': Name of the car (used in the filename)
        - 'car_image_full_url': URL of the car image to download
        - 'car_page_url' :  URL of the car page
    The filename is created by joining the first two words of the car model
    (lowercased) with an underscore, followed by an index number.
    Args:
        json_data (list[dict]): List of dictionaries containing car info and image URLs.
        output_dir (str): Path to the folder where images will be saved.
    Returns:
        None
    Notes:
        - The function automatically creates the output directory if it does not exist.
        - Downloads are done sequentially; if a download fails, it prints an error and continues.
        - Output File names: "toyota_avensis_1.jpg"
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for index, item in track(
        enumerate(json_data, start=1),
        description="Downloading car images ...",
        total=len(json_data)):


        car_model = item.get("car_model", "unknown_model").lower().split()
        model = "_".join(car_model[:2])
        image_url = item.get("car_image_full_url")

        filename = out_dir / f"{model}_{index}.jpg"

        try:
            resp = requests.get(image_url, timeout=5)
            resp.raise_for_status()

            with open(filename, "wb") as f_out:
                f_out.write(resp.content)

        except Exception as e:
            print(f"Failed to download {image_url}: {e}")



def main():
    all_links = get_all_pages_links()
    print("Fetching images urls links and data...")
    all_images_url = get_each_car_detail_page_data(all_links)
    print("Done get all images urls links and data!")

    print("Write data to json file ...")
    create_data_json_file(all_images_url, JSON_FILE_PATH)

    print("Open json file load data ...")
    open_json_data = open_json_file(JSON_FILE_PATH)

    print("Save prhotos from links ...")
    save_photos_from_urls(open_json_data, OUTPUT_DIR)
    print("Done!")


if __name__ == "__main__":
    main()
