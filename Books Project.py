import requests
from bs4 import BeautifulSoup
import json
import time
import configparser
import logging
from urllib.parse import urljoin

config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
book_selector = config['settings']['book_selector']
next_button_selector = config['settings']['next_button_selector']
wait_time = int(config['settings']['wait_time'])

books_data = []

def get_category_name(soup):
    category_element = soup.find('h1')
    if category_element:
        return category_element.text.strip().replace(' ', '_').lower()
    return 'nezinoma_kategorija'


def get_book_details(book_link):
    full_url = urljoin('https://www.knygos.lt', book_link)

    try:
        response = requests.get(full_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        author_elements = soup.select("a.book-author span[itemprop='name']")
        if not author_elements:
            author_elements = soup.select("span[itemprop='author'] span[itemprop='name']")

        if author_elements:
            book_authors = ', '.join([author.text.strip() for author in author_elements])
        else:
            book_authors = 'Autorius nerastas'

        all_text = soup.get_text(separator=' ').strip()
        year_text = None

        if 'Metai:' in all_text:
            year_text = all_text.split('Metai:')[-1].strip().split(' ')[0]

        if year_text:
            book_year = year_text
        else:
            book_year = 'Metai nerasti'

        logging.info(f"Sėkmingai surasta informacija apie knygą {full_url}")
        return book_authors, book_year

    except Exception as e:
        logging.error(f"Klaida naršant knygą {full_url}: {e}")
        return "Autorius nerastas", "Metai nerasti"


def scrape_page(url, category_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_elements = soup.select(book_selector)

    for book in book_elements:
        book_link = book['href'].strip()
        book_title = book.get('title', 'Pavadinimas nerastas').upper()
        book_price = book.get('data-cta-price', 'Kaina nerasta')
        full_book_link = urljoin('https://www.knygos.lt', book_link)
        book_author, book_year = get_book_details(full_book_link)

        books_data.append({
            'title': book_title,
            'link': full_book_link,
            'author': book_author,
            'year': book_year,
            'price': book_price
        })

        logging.info(
            f"Pavadinimas: {book_title}, Nuoroda: {full_book_link}, Autorius: {book_author}, Metai: {book_year}")


def save_to_json(category_name):
    with open(f'{category_name}_books_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_data, json_file, ensure_ascii=False, indent=4)
    logging.info(f"Duomenys sėkmingai išsaugoti į {category_name}_books_data.json")


def pagination(url, category_name, max_pages):
    page_count = 1
    while url and page_count <= max_pages:
        print(f"Pereinamas į kitą puslapį: {url}")

        scrape_page(url, category_name)
        time.sleep(wait_time)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        next_button = soup.select_one(next_button_selector)
        if next_button:
            next_page = next_button.get('href')
            if next_page:
                url = urljoin('https://www.knygos.lt', next_page)
                page_count += 1
            else:
                break
        else:
            break


def process_category(category_url, max_pages):
    global books_data
    books_data = []

    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_name = get_category_name(soup)
    pagination(category_url, category_name, max_pages)
    save_to_json(category_name)


def main():
    categories = [section for section in config.sections() if section.startswith('category_')]

    for category in categories:
        category_url = config[category]['url']
        max_pages = int(config[category]['max_pages'])
        process_category(category_url, max_pages)


if __name__ == "__main__":
    main()


