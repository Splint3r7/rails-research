#!/usr/bin/env python
#GemScanner

import requests
from bs4 import BeautifulSoup
from colorama import init , Style, Back,Fore
import argparse
import sys,os
import concurrent.futures
import re
from bs4 import BeautifulSoup

if os.name == 'nt':
	os.system('cls')
else:
	os.system('clear')

def logo():
	print("""
 	 ____                ____
 	/ ___| ___ _ __ ___ / ___|  ___ __ _ _ __  _ __   ___ _ __
	| |  _ / _ | '_ ` _ \\___ \ / __/ _` | '_ \| '_ \ / _ | '__|
	| |_| |  __| | | | | |___) | (_| (_| | | | | | | |  __| |
 	\____|\___|_| |_| |_|____/ \___\__,_|_| |_|_| |_|\___|_|

 	GemScanner - Finds Vulnerable/Claimable RubyGems!.
 	Author: Splint3r7 - ( https://github.com/Splint3r7 )

		""")

parser = argparse.ArgumentParser(description="Script to find vulnerable GEMS")

parser.add_argument('-f','--file',
                            help = "Path to Gemfile.lock",
                            type = str,
                            required = False)

parser.add_argument('-u','--url',
                            help = "URL to Gemfile.lock",
                            type = str,
                            required = False)

parser.add_argument('-o','--output',
                            help = "Output file",
                            type = str,
                            required = True)

args = parser.parse_args()


def versions_f(_gemname_):


	print(Style.DIM+Fore.GREEN+"[-]"+Style.RESET_ALL+Style.DIM+Fore.WHITE+" TESTING | "+Style.RESET_ALL+Style.BRIGHT+Fore.BLUE+"{}".format(_gemname_)+Style.RESET_ALL)
	try:
		req = requests.get("https://rubygems.org/gems/"+_gemname_, timeout=7, allow_redirects=False)
		if req.status_code == 404:
			print(Style.DIM+Fore.YELLOW+"["+Style.BRIGHT+Fore.GREEN+"+"+Style.RESET_ALL+Style.DIM+Fore.YELLOW+"]"+Style.RESET_ALL+Style.BRIGHT+Fore.RED+" Claimable gem found |"+Style.BRIGHT+Fore.RED+" {}".format(_gemname_)+Style.RESET_ALL)
			filew.write(_gemname_+"\n")
		else:
			pass
	except:
		pass


def GemParser(_array_):

	for line in _array_:
		line = line.strip()
		if "(" in line:
			fullname = line
			line_arr = line.split(" ", 1)
			# To get the gem name from gem (version) basically from lock files
			gem_name = line_arr[0]
			gem_version = line_arr[1]
			_lista_.append(gem_name)

				# to read gem 'gem_name'	
		elif ":" not in line and not "source" in line and not "GEM" in line and "gem" in line:
			line = line.split("'")
			linex = line[0:2]
			for y in linex:
				y = y.strip()
				if not "gem" in y:
					_lista_.append(y)

				# to read rest of the dependencies
		elif "https://rubygems.org" not in line and "#" not in line and "GEM" not in line and ":" not in line and "PLATFORMS" not in line and "DEPENDENCIES" not in line and "1.16.0" not in line and "BUNDLED WITH" not in line and "1.11.2" not in line and "VERSION" not in line and "ruby 2." not in line and "PATH" not in line and "2.1.4" not in line and "1.17.3" not in line and "1.14.6" not in line and "GIT" not in line and "1.10.3" not in line and "1.13.3" not in line and "1.16.5" not in line and "1.14.5" not in line and "1.12.5" not in line and "ruby 3." not in line and "2.2.6" not in line and "1.10.6" not in line and "1.16.4" not in line:
			_lista_.append(line)


if __name__ == "__main__":

	out_file = args.output
	_lista_ = []
	unique_list = []
	filew = open(out_file, "a+")

	if args.file:
		file_path = args.file
		logo()
		with open(file_path, "r") as f:
			lines = f.readlines()
			GemParser(lines)


	elif args.url:

		logo()
		f2 = open("temp.txt", "w")
		url = args.url
		req = requests.get(url, timeout=10)
		soup = BeautifulSoup(req.content, 'html.parser')
		f2.write(str(soup))
		f2.close()
		with open("temp.txt", "r") as f:
			lines = f.readlines()
			GemParser(lines)

	for x in _lista_:
		if x not in unique_list:
			# To filter '' in array
			if len(x) > 1:
				unique_list.append(x)

	with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
		executor.map(versions_f, unique_list)

	filew.close()