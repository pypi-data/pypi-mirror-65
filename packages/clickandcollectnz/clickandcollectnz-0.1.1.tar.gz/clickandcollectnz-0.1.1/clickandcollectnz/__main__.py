import sys
import json
import argparse

from clickandcollectnz.countdown import Countdown
from clickandcollectnz.foodstuffs import NewWorld, PakNSave

classes = ['Countdown', 'NewWorld', 'PakNSave']

def print_usage():
  print("Usage: python -m clickandcollectnz [chain] [store_id]")
  print()
  print("    chain:  Countdown | PakNSave | NewWorld")

if __name__ == "__main__":

  parser = argparse.ArgumentParser(prog='python -m clickandcollectnz', description='NZ Click and Collect time slots.')
  parser.add_argument('chain', nargs="?", choices=classes)
  parser.add_argument('store_id', nargs="?")
  parser.add_argument('--json', dest='json', action='store_const',
                    const=True, default=False,
                    help='output in JSON format')

  args = parser.parse_args()

  if not args.chain:
    parser.print_help()
    sys.exit(0)

  if args.chain and not args.store_id:
    cls = eval(args.chain)
    stores = cls.get_store_list()
    if args.json:
      print(json.dumps(stores, default=lambda o: o.to_json()))
    else:
      print("ID - Store Name")
      for store in stores:
        print(store)
    sys.exit(0)

  if args.chain and args.store_id:
    cls = eval(args.chain)
    stores = cls.get_store_list()
    store = next((x for x in stores if x.id == args.store_id), None)
    store.get_slots()
    if args.json:
      print(json.dumps(store, default=lambda o: o.to_json()))
    else:
      print("Not Implemented")
