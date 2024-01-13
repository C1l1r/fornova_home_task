import re
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from lxml import etree
import argparse
import sys

parser = argparse.ArgumentParser(prog='web_scraper_lxml', description="Takes data from qantas.com. No beautiful soup")

parser.add_argument('-o', '--out', nargs='?', help='Optional out file', default=None)
parser.add_argument('links', nargs='+', help='List of links')

args = parser.parse_args(sys.argv[1:])



def scrape_url(url):
    number_of_scrolls = 5
    scroll_pause_time = 3  # in seconds

    # Initialize the WebDriver (this example uses Firefox)
    driver = webdriver.Firefox()

    # Open the URL
    driver.get(url)

    # Scroll down the page
    for i in range(number_of_scrolls):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(scroll_pause_time)

    # Get the page source and close the browser
    html_content = driver.page_source
    driver.quit()


    # Parse the HTML content
    tree = etree.HTML(html_content)

    hotel_accomodations = []
    processed_rooms = set()  # Set to keep track of processed room names

    # Find buttons with specific text
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

                # Skip if this room has already been processed
                if room_name in processed_rooms:
                    continue
                processed_rooms.add(room_name)

                price_elements = box.xpath(".//span[@data-testid='amount']")
                price = price_elements[0].text.strip() if price_elements else None

                rooms = []
                guests = None

                for heading in box.xpath(".//h3[contains(@class, 'Heading-Heading-Text')]"):
                    mini_box = heading.getparent()
                    for _ in range(2):  # Adjust as necessary
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

    #print(json.dumps(hotel_accomodations, indent=2))
    return hotel_accomodations
#%%

hotel_accomodations = []
for url in args.links:
    hotel_accomodations += scrape_url(url)

output = json.dumps(hotel_accomodations, indent=2)

if args.out == None:
    print(output)
else:
    with open(args.out, 'w') as file:
        print(output, file = file)
