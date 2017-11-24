#!/usr/bin/env python

import sys
import os
import re
from collections import namedtuple
from argparse import ArgumentParser
from PIL import Image


DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024
DEFAULT_MAX_DEPTH = 10
FORMATS = ["jpg", "png"]
IMAGE_REGEX = re.compile("\.({})$".format("|".join(FORMATS)), re.IGNORECASE)


def process_image(file_info, width, height):
	image = Image.open(file_info.path)
	if image.width > width or image.height > height:
		print("Resizing {}".format(file_info.path))
		image.thumbnail((width, height))
		image.save(file_info.path)
	else:
		print("Skipping {}".format(file_info.path))


def process_dir(dir, width, height, recurse, max_depth, depth=0):
	if depth >= max_depth:
		return
	with os.scandir(dir) as entries:
		for e in entries:
			if recurse and e.is_dir():
				process_dir(e.path, width, height, recurse, max_depth, depth + 1)
			elif e.is_file() and re.search(IMAGE_REGEX, e.path):
				process_image(e, width, height)


def main():
	p = ArgumentParser()
	p.add_argument("directory")
	p.add_argument("--recursive", "-r", action="store_true")
	p.add_argument("--width", "-w", type=int, default=DEFAULT_WIDTH)
	p.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
	p.add_argument("--max-depth", "-d", type=int, default=DEFAULT_MAX_DEPTH)
	args = p.parse_args()

	print("Thumbnail size {}x{}".format(args.width, args.height))
	print("Starting scan from", args.directory)
	process_dir(args.directory, args.width, args.height, args.recursive, args.max_depth)


if __name__ == "__main__":
	main()
