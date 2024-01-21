# fornova_home_task
In this homework task, I used Selenium. The Request library was not able to retrieve data that was dynamically loaded to the website, via JS scripts. Additionally, the Request library extension 'requests_html' proved to be insufficient, since the website loads data dynamically as the user scrolls, necessitating the emulation of user activity. During the solving process, I attempted to retrieve all links through the HAR file, but it appears that only the website itself can do that
![image](https://github.com/C1l1r/fornova_home_task/assets/55895013/8cfb7251-6281-4037-bfd3-9628e1b8b0f3)\
HTML file without JS added data
![image](https://github.com/C1l1r/fornova_home_task/assets/55895013/e06ed116-a026-49d3-83e2-9ad07f0f19d0)\
Review of the outgoing traffic
![image](https://github.com/C1l1r/fornova_home_task/assets/55895013/0c8fc5d5-f846-4156-9c74-b340609229c2)
Almost succeeded. But not quite.

## Structure of the output data

[
  {
    "room_name": "Premium Room, 1 King Bed, Park View",
    "data": [
      {
        "rate_name": "Premium Room, 1 King Bed, Park View",
        "price": "759",
        "currency": "AUD",
        "topdeal": true,
        "guests": "2"
      },
      {
        "rate_name": "Internet Included",
        "price": "884",
        "currency": "AUD",
        "topdeal": false,
        "guests": "2"
      },
      {
        "rate_name": "Internet Included",
        "price": "893",
        "currency": "AUD",
        "topdeal": false,
        "guests": "2"
      },
      {
        "rate_name": "Internet Included, Breakfast Included",
        "price": "967",
        "currency": "AUD",
        "topdeal": false,
        "guests": "2"
      }
    ]
  },
  {
    "room_name": "Premium Room, 1 King Bed, Corner (Panorama)",
    "data": [
      {
        "rate_name": "Premium Room, 1 King Bed, Corner (Panorama)",
        "price": "773",
        "currency": "AUD",
        "topdeal": true,
        "guests": "2"
      },
      {
        "rate_name": "Internet Included",
        "price": "900",
        "currency": "AUD",
        "topdeal": false,
        "guests": "2"
      },
      {
        "rate_name": "Internet Included",
        "price": "910",
        "currency": "AUD",
        "topdeal": false,
        "guests": "2"
      },
