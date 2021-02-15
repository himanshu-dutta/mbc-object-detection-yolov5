import io
import os
import time
import math
import hashlib
import logging
import requests
from tqdm import *
from PIL import Image
import urllib.request
from typing import Union, List
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def init_driver(fetcher):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    tab = webdriver.Chrome(ChromeDriverManager(
        log_level=logging.WARNING).install(), options=options)

    def fetcher_with_tab(*args, **kwargs):
        return fetcher(*args, **kwargs, driver=tab)

    return fetcher_with_tab


@init_driver
def google_images_scraper(search_term: str, min_image_count: int = 10, driver: webdriver.chrome.webdriver.WebDriver = None) -> list:
    base_url = "https://www.google.com/imghp?hl=en"
    driver.get(base_url)
    search_form = driver.find_element_by_name("q")
    search_form.send_keys(search_term)
    search_form.submit()
    urls = []
    while len(urls) < min_image_count:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        urls = driver.execute_script(
            "return Array.from(document.querySelectorAll(\'.rg_i\')).map(el=> el.hasAttribute(\'data-src\')?el.getAttribute(\'data-src\'):el.getAttribute(\'data-iurl\'));")

        while None in urls:
            urls.remove(None)
    return urls


def download_images_from_url(urls: Union[str, List[str]], image_tag: str, format: str = 'png',  save_location: str = ".") -> None:
    dir = os.path.join(save_location, image_tag)
    if not os.path.exists(dir):
        os.mkdir(dir)
    else:
        print("Already Exists")
        return

    if isinstance(urls, str):
        try:
            urllib.request.urlretrieve(urls, os.path.join(
                dir, "0001" + "." + format))
            print(f"Downloaded 1 image in {dir}.")
        except:
            print("Error encountered")

    elif isinstance(urls, list):
        pad = math.ceil(math.log10(len(urls)))
        na = 0
        for idx in tqdm(range(len(urls))):
            try:
                urllib.request.urlretrieve(urls[idx], os.path.join(
                    dir, str(idx+1).zfill(pad) + "." + format))
            except:
                na += 1
        print(f"Downloaded {len(urls)-na} images in {dir}.")

    else:
        raise Exception("Invalid argument type for \"urls\"")


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(
            f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls),
                  "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path: str, file_name: str, url: str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path, file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path, hashlib.sha1(
                image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path, hashlib.sha1(
                image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


if __name__ == '__main__':
    wd = webdriver.Chrome(ChromeDriverManager().install())
    queries = ['rice',
               'saffron',
               'cardamom',
               'semolina',
               'clarified butter',
               'mustard seeds',
               'yogurt',
               'garlic',
               'lemon juice',
               'baking soda']

  # change your set of querries here
    for query in queries:
        wd.get('https://google.com')
        search_box = wd.find_element_by_css_selector('input.gLFyf')
        search_box.send_keys(query)
        links = fetch_image_urls(query, 50, wd)
        # images_path = '/Users/anand/Desktop/contri/images'  #enter your desired image path
        images_path = 'indian-food-ingredients/top_30'
        for i in links:
            persist_image(images_path, query, i)
    wd.quit()
