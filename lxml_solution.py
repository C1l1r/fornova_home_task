import re
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from lxml import etree



def scrape_url(url):
    NUMBER_OF_SCROLLS = 5
    SCROLL_PAUSE_TIME = 3  # in seconds

    # We use them to gather dynamically loaded hotel rooms info
    driver = webdriver.Firefox()

    driver.get(url)

    # Scroll down the page
    for i in range(NUMBER_OF_SCROLLS):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)

    html_content = driver.page_source
    driver.quit()

    """
    1. Search for the boxes by h3 tag, "View room details" button and contain price tag
    2. Iterate through chlid boxes and gather needed info
    """

    tree = etree.HTML(html_content)

    hotel_accomodations = []

    buttons = tree.xpath("//button[contains(text(), 'View room details')]")

    # Navigate to the container that holds the room details
    for button in buttons:
        box_container = button.getparent()
        for _ in range(5):  # Adjust the range as needed to reach the correct parent
            box_container = box_container.getparent()

        for box in box_container:
            room_elements = box.xpath(".//h3")
            if room_elements:
                room_name = room_elements[0].text.strip()

                rooms = []
                guests = None

                for heading in box.xpath(".//h3[contains(@class, 'Heading-Heading-Text')]"):
                    mini_box = heading.getparent()
                    for _ in range(2):
                        mini_box = mini_box.getparent()

                    price_elements = mini_box.xpath(".//span[@data-testid='amount']")
                    top_deal_elements = mini_box.xpath(".//span[contains(text(), 'Top Deal')]")

                    if price_elements == []:
                        continue

                    price_elements = price_elements[0]

                    guests_elements = mini_box.xpath(".//span[contains(text(), 'guests')]")
                    guests = guests or (guests_elements[0].text.split(" ")[0] if guests_elements else None)

                    currency_elements = price_elements.xpath("../../../following-sibling::*[1]/*")
                    currency = currency_elements[0].text.strip() if currency_elements else "Unknown"

                    rooms.append({
                        'rate_name': heading.text.strip(),
                        'price': "".join (price_elements.itertext()).strip(),
                        'currency': currency,
                        'topdeal': bool(top_deal_elements),
                        'guests': guests
                    })

                hotel_accomodations.append({'room_name': room_name, 'data': rooms})

    return hotel_accomodations


if __name__ == "__main__":

    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='web_scraper_lxml', description="Takes data from qantas.com. No beautiful soup")

    parser.add_argument('-o', '--out', nargs='?', help='Optional out file', default=None)
    parser.add_argument('links', nargs='+', help='List of links')

    args = parser.parse_args(sys.argv[1:])

    hotel_accomodations = []
    for url in args.links:
        hotel_accomodations += scrape_url(url)

    output = json.dumps(hotel_accomodations, indent=2)

    if args.out == None:
        print(output)
    else:
        with open(args.out, 'w') as file:
            print(output, file = file)
