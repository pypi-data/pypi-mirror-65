import requests
import json
import sys

from abc import ABC
from dateutil import parser

from clickandcollectnz.store import Store, StoreDay, StoreSlot

store_list_url = "https://{}/CommonApi/Store/GetStoreList"
store_slot_list_url = "https://{}/CommonApi/Delivery/GetClickCollectTimeSlot?id="

class Foodstuffs(ABC):
  domain = ""

  @classmethod
  def get_store_slots(cls, store):
    response = requests.request("GET", f"{store_slot_list_url.format(cls.domain)}{store.id}")
    slots_json = response.json()["slots"]
    days = []
    for day_json in slots_json:
      date_string = day_json["date"]
      date = parser.parse(date_string)
      slots = []
      day = StoreDay(date)
      for slot_json in day_json["timeSlots"]:
        time_string = slot_json["slot"]
        from_time = parser.parse(f'{time_string.split("-")[0]} {date_string}')
        to_time = parser.parse(f'{time_string.split("-")[1]} {date_string}')

        status = f"{slot_json['available']} available"
        available = slot_json["available"] > 0

        slot = StoreSlot(day, from_time, to_time, available, status)
        slots.append(slot)
      day.slots = slots
      days.append(day)

    store.days = days

  @classmethod
  def get_store_list(cls):
    response = requests.request("GET", store_list_url.format(cls.domain))
    stores_json = response.json()["stores"]
    stores = []
    for store_json in stores_json:
      stores.append(Store(store_json["id"], store_json["name"], cls.get_store_slots))
    return stores


class PakNSave(Foodstuffs):
  domain = "www.paknsaveonline.co.nz"


class NewWorld(Foodstuffs):
  domain = "www.ishopnewworld.co.nz"
