from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import json
import argparse
import sys

parser = argparse.ArgumentParser(prog='web_scraper', description="Takes data from qantas.com")

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


    soup = BeautifulSoup(html_content, 'html.parser')
    buttons = soup.find('button', string='View room details')

    hotel_accomodations = []

    boxes_container = list(buttons.parents)[5] # Getting html boxes of rooms by going 5 parents up the tree
    for box in boxes_container:
        room_name = box.find('h3')
        if room_name:
            room_name = room_name.get_text(strip=True)

            # Find the price within the same container
            price = box.find_next('span', {'data-testid': 'amount'})
            if price:
                price = price.get_text(strip=True)

            rooms  = []
            guests = None
            for i in box.find_all('h3', class_= lambda x: x and "Heading-Heading-Text" in x):
                minibox = i.parent.parent.parent
                price = minibox.find('span',  {'data-testid': 'amount'})



                topdeal = minibox.find('span', string = 'Top Deal') is not None
                if price is None: # adding rooms to list if the boxes have both prices and correct names.
                    continue
                guests = guests or minibox.find('span', string = re.compile('guests'))
                currency_element = next(price.parent.parent.parent.find_next_sibling().children)
                rooms.append({
                    'rate_name': i.text,
                    "price": price.text,
                    'currency': currency_element.text,
                    'topdeal':topdeal,
                    'guests': guests.text.split(" ")[0],
                })
            hotel_accomodations.append({'room_name': room_name,
                                        'data': rooms
                                        })
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

#%%

#%%
