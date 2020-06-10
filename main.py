import argparse
import sys
import json
from io import open
from src import FBCrawler

def usage():
    return """
    python main.py
  """

def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()

def create_group(username, password, filepath):
  fb_crawler = FBCrawler()
  return fb_crawler.create_group(username, password, filepath)

def output(data, filepath):
    out = json.dumps(data, ensure_ascii=False)
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        print(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="facebook automation", usage=usage())
    parser.add_argument(
        "mode", help="options: [create_group]"
    )
    parser.add_argument("-u", "--username", help="facebook's username")
    parser.add_argument("-p", "--password", help="facebook's password")
    parser.add_argument("-i", "--input", help="input file name(json format)")
    parser.add_argument("-o", "--output", help="output file name(json format)")

    args = parser.parse_args()

    if args.mode == "create_group":
        arg_required(args, ["username", "password"])
        output(
          create_group(args.username, args.password, args.input), args.output
        )
    else:
        usage()
