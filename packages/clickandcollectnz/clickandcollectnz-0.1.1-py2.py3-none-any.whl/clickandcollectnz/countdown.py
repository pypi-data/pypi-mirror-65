import requests
from bs4 import BeautifulSoup
import json
import sys
from dateutil import parser
from clickandcollectnz.store import Store, StoreDay, StoreSlot

store_list_url = "https://shop.countdown.co.nz/shop/changeaddress"
set_store_url = "https://shop.countdown.co.nz/shop/setdeliveryaddressanddeliverymethod?_mode=ajax"
store_slot_list_url = "https://shop.countdown.co.nz/shop/schedulereserve?DeliveryMethod=Pickup"

class Countdown:

  @classmethod
  def get_store_slots(cls, store):
    s = requests.Session()
    list_page = s.get(store_list_url)
    form_token = BeautifulSoup(list_page.text, "html.parser") \
      .find(class_="manage-delivery-buttons") \
      .find("input", attrs={"name": "__RequestVerificationToken"}) \
      .get("value")

    headers = {
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    s.post(
      set_store_url,
      headers=headers,
      data=f"__RequestVerificationToken={form_token}&addressIdString={store.id}&deliveryMethod=Pickup"
    )

    response = s.get(store_slot_list_url)

    page = response.text

    soup = BeautifulSoup(page, "html.parser")

    # store_name = soup.find(class_="show-pickup-address-link").string

    days = []
    for day_column in soup.find_all(class_="window-day"):
      date_string = day_column.find(class_="day-name").string
      date = parser.parse(date_string)
      slots = []
      day = StoreDay(date)
      for time_box in day_column.find(class_="toggle-children").find_all(class_="text-center"):
        time_string = time_box.find(class_="time-duration-text").string.strip()
        from_time = parser.parse(f'{time_string.split("-")[0]} {date_string}')
        to_time = parser.parse(f'{time_string.split("-")[1]} {date_string}')

        status = time_box.find(class_="status-text").string.strip()
        available = status != "Closed" and status != "Full"

        slot = StoreSlot(day, from_time, to_time, available, status)
        slots.append(slot)
      day.slots = slots
      days.append(day)

    store.days = days

  @classmethod
  def get_store_list(cls):
    response = requests.request("GET", store_list_url)
    page = response.text

    soup = BeautifulSoup(page, "html.parser")
    stores = []
    ids = []
    for select in soup.find_all(class_="_stateFilter"):
      for store_option in select.find_all("option"):
        store_id = store_option.get("value")
        if store_id not in ids:
          stores.append(Store(store_id, store_option.string.strip(), cls.get_store_slots))
          ids.append(store_id)

    return stores
