#!/usr/bin/env python

import sys
import os
import re
from collections import namedtuple
from argparse import ArgumentParser


Dimension = namedtuple("Dimension", "width height")
DEFAULT_THRESHOLD = Dimension(1024, 768)
DEFAULT_RESIZE = Dimension(800, 600)
DEFAULT_MAX_DEPTH = 10
FORMATS = ["jpg", "png"]
IMAGE_REGEX = re.compile("\.({})$".format("|".join(FORMATS)), re.IGNORECASE)


def process_image(file_info, width, height):
	print("resize {} {}x{}".format(file_info.name, width, height))


def process_dir(dir, width, height, recurse, max_depth, depth=0):
	if depth >= max_depth:
		return
	with os.scandir(dir) as it:
		for e in it:
			if recurse and e.is_dir():
				process_dir(e.path, width, height, recurse, max_depth, depth + 1)
			elif e.is_file() and re.search(IMAGE_REGEX, e.path):
				process_image(e, width, height)


def main():
	p = ArgumentParser()
	p.add_argument("directory")
	p.add_argument("--recursive", "-r", action="store_true")
	p.add_argument("--width", "-w", type=int, default=DEFAULT_RESIZE.width)
	p.add_argument("--height", type=int, default=DEFAULT_RESIZE.height)
	p.add_argument("--max-depth", "-d", type=int, default=DEFAULT_MAX_DEPTH)
	args = p.parse_args()
	process_dir(args.directory, args.width, args.height, args.recursive, args.max_depth)


if __name__ == "__main__":
	main()
