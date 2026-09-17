import cowsay
import argparse

parser = argparse.ArgumentParser(
    prog="cowsay",
    description="Make animals say things",
)
parser.add_argument("--animal", choices=cowsay.char_names, help="The animal to be saying things.", default="cow")
parser.add_argument("message", nargs="+", help="The message to say.")
args = parser.parse_args()

getattr(cowsay, args.animal)(" ".join(args.message))