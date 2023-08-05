import json

class Store:
  def __init__(self, id, name, slot_finder):
    self._id = id
    self._name = name
    self._slot_finder = slot_finder
    self._days = []

  @property
  def name(self):
    return self._name

  @property
  def id(self):
    return self._id

  def get_slots(self):
    self._slot_finder(self)

  @property
  def next_available(self):
    for d in self._days:
      for s in d.slots:
        if s.available:
          return s

  @property
  def available(self):
    count = 0
    for d in self._days:
      for s in d.slots:
        if s.available:
          count += 1
    return count

  @property
  def days(self):
    return self._days

  @days.setter
  def days(self, days):
    self._days = days

  def __str__(self):
    return f'{self._id} - {self._name}'

  def to_json(self):
    data = {
      "id": self._id,
      "name": self._name,
      "available": self.available,
      "next_available": self.next_available,
      "days": self._days
    }
    return data


class StoreDay:
  def __init__(self, date, slots=[]):
    self._date = date
    self._slots = slots

  @property
  def date(self):
    return self._date.strftime("%Y-%m-%d")

  @property
  def slots(self):
    return self._slots

  @slots.setter
  def slots(self, slots):
    self._slots = slots

  def __str__(self):
    return self.date

  def to_json(self):
    return {"date": self.date, "slots": self._slots}


class StoreSlot:
  def __init__(self, day, from_time, to_time, available, raw_status):
    self._day = day
    self._from_time = from_time
    self._to_time = to_time
    self._available = available
    self._raw_status = raw_status

  @property
  def time(self):
    return f'{self._from_time.strftime("%I:%M%p")} - {self._to_time.strftime("%I:%M%p")}'

  @property
  def available(self):
    return self._available

  @property
  def raw_status(self):
    return self._raw_status

  def __str__(self):
    return f"{self._raw_status} @ {self.time} on {self._day.date}"

  def to_json(self):
    data = {
      "time": self.time,
      "available": self._available,
      "raw_status": self._raw_status
    }
    return data
