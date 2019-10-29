#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import json

parser = ArgumentParser(description='Marks watched episodes')
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', '--folder', help='Scan the specified folder for media')
group.add_argument('-m', '--mark', action='store_true', help='Mark watched episodes')
group.add_argument('-l', '--list', action='store_true', help='List all scanned media')
args = parser.parse_args()

folder = args.folder
VALID_FORMATS = ['mp4', 'rmvb']
DATA_FILE = 'data.json'

def walk(path):
	contents = {
		'name': path.name,
		'files': list(),
		'folders': list()
	}

	try:
		for entry in path.iterdir():
			if entry.is_file():
				fragmented = entry.name.split(sep='.')
				if len(fragmented) > 1:
					extension = fragmented[1]
					if extension in VALID_FORMATS:
						contents['files'].append({
							'name': entry.name,
							'watched': False
						})

			if entry.is_dir():
				contents['folders'].append(walk(entry))
	except Exception as e:
		print(e)

	return contents

def rwalk(data):
	result = '## ' + data.get('name', 'Empty') + '\n'

	for key in data:
		if key == 'folders':
			folders = data[key]
			if len(folders) > 0:
				folders = sorted(folders, key=lambda folder: folder['name'].lower())

				for folder in folders:
					result += rwalk(folder)

		elif key == 'files':
			files = data[key]
			if len(files) > 0:
				files = sorted(files, key=lambda episode: episode['name'].lower())

				for file in files:
					result += '****** ' + file['name'] + (' -- (Watched)' if file['watched'] else '') + '\n' 

	return result

def scan(data):
	for key in data:
		if key == 'files':
			files = data[key]
			if len(files) > 0:
				files = sorted(files, key=lambda episode: episode['name'].lower())
				
				for file in files:
					if not file['watched']:
						print(file['name'])
						
						answer = input('Mark? (y/n, q to quit): ')
						
						if answer.lower() == 'y':
							file['watched'] = True
						elif answer.lower() == 'n':
							pass
						elif answer.lower() == 'q':
							break

		elif key == 'folders':
			folders = data[key]
			if len(folders) > 0:
				folders = sorted(folders, key=lambda folder: folder['name'].lower())

				for folder in folders:
					scan(folder)

	return data

if folder:
	path = Path(folder)
	if not path.exists():
		print(f'Error: folder {folder} does not exist')
	else:
		contents = dict()

		try:
			contents = walk(path)
		except Exception as e:
			print(e)

		with open(DATA_FILE, 'w') as file:
			json.dump(contents, file, indent='\t')

elif args.mark:
	with open(DATA_FILE, 'r') as file:
		contents = json.load(file)

	contents = scan(contents)

	with open(DATA_FILE, 'w') as file:
		json.dump(contents, file, indent='\t')

elif args.list:
	with open(DATA_FILE, 'r') as file:
		contents = json.load(file)

	print(rwalk(contents))
