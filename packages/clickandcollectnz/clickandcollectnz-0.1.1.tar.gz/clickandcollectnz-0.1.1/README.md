# Click and Collect NZ

![PyPI](https://img.shields.io/pypi/v/clickandcollectnz)

## Usage

```
usage: python -m clickandcollectnz [-h] [--json] [{Countdown,NewWorld,PakNSave}] [store_id]

NZ Click and Collect time slots.

positional arguments:
  {Countdown,NewWorld,PakNSave}
  store_id

optional arguments:
  -h, --help            show this help message and exit
  --json                output in JSON format
```

## Examples

```bash
$ python -m clickandcollectnz Countdown --json | jq

[
  {
    "id": "951739", 
    "name": "Countdown Hawera", 
    "available": 0, 
    "next_available": null, 
    "days": []
  }, 
  ... 
]
```


```bash
$ python -m clickandcollectnz Countdown 951739 --json | jq

{
  "id": "951739",
  "name": "Countdown Hawera",
  "available": 43,
  "next_available": {
    "time": "09:00AM - 10:00AM",
    "available": true,
    "raw_status": "Closing Soon"
  },
  "days": [
    {
      "date": "2020-04-06",
      "slots": [
        {
          "time": "09:00AM - 10:00AM",
          "available": false,
          "raw_status": "Closed"
        },
        ...
      ]
    },
    ...
  ]
}
```
