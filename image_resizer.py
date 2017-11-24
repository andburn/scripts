#!/usr/bin/env python

"""Runs over a directory tree searching for supported image files. Resizes any
images larger than the required width and height.
"""

import os
import re
from shutil import copyfile
from argparse import ArgumentParser
from PIL import Image


DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024
DEFAULT_MAX_DEPTH = 10
FORMATS = ["jpg", "png"]
IMAGE_REGEX = re.compile("\.({})$".format("|".join(FORMATS)), re.IGNORECASE)


def image_message(name, message):
	print("{} {}{}".format(message, "..." if len(name) > 50 else "", name[-50:]))


def process_image(file_info, width, height, dry_run, backup):
	image = Image.open(file_info.path)
	if image.width > width or image.height > height:
		image_message(file_info.path, "Resizing")
		if not dry_run:
			if backup:
				copyfile(file_info.path, file_info.path + ".bak")
			image.thumbnail((width, height))
			image.save(file_info.path)
	else:
		image_message(file_info.path, "Skipping")


def process_dir(dir, width, height, recurse, max_depth, dry_run, backup, depth=0):
	if depth >= max_depth:
		return
	with os.scandir(dir) as entries:
		for e in entries:
			if recurse and e.is_dir():
				process_dir(e.path, width, height, recurse, max_depth,
							depth + 1, dry_run, backup)
			elif e.is_file() and re.search(IMAGE_REGEX, e.path):
				process_image(e, width, height, dry_run, backup)


def main():
	p = ArgumentParser()
	p.add_argument("directory")
	p.add_argument("--recursive", "-r", action="store_true")
	p.add_argument("--width", "-w", type=int, default=DEFAULT_WIDTH)
	p.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
	p.add_argument("--max-depth", "-d", type=int, default=DEFAULT_MAX_DEPTH)
	p.add_argument("--dry-run", "-n", action="store_true")
	p.add_argument("--backup", "-b", action="store_true")
	args = p.parse_args()

	if args.dry_run:
		print("--- DRY RUN ---")
	print("Thumbnail size {}x{}".format(args.width, args.height))
	print("Starting scan from", args.directory)
	process_dir(args.directory, args.width, args.height, args.recursive,
				args.max_depth, args.dry_run, args.backup)


if __name__ == "__main__":
	main()
