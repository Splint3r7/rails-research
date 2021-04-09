#!/usr/bin/env python
#GemScanner

import requests
from bs4 import BeautifulSoup
from colorama import init , Style, Back,Fore
import argparse
import sys,os
import concurrent.futures
import re

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

 	GemScanner - Finds depreciated versions of your gems.
 	Author: Splint3r7 - ( https://github.com/Splint3r7 )

		""")

parser = argparse.ArgumentParser(description="Script to find vulnerable GEMSs")

parser.add_argument('-f','--file',
                            help = "Path to Gemfile.lock",
                            type = str,
                            required = True)

parser.add_argument('-o','--output',
                            help = "Output file",
                            type = str,
                            required = True)

args = parser.parse_args()

file_path = args.file
out_file = args.output

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


if __name__ == "__main__":

	logo()
	_lista_ = []
	unique_list = []

	filew = open(out_file, "a+")
	with open(file_path, "r") as f:
		lines = f.readlines()
		for line in lines:
			line = line.strip()
			if "(" in line:
				fullname = line
				line_arr = line.split(" ", 1)
				gem_name = line_arr[0]
				gem_version = line_arr[1]
				_lista_.append(gem_name)

			elif ":" not in line and not "source" in line and not "GEM" in line and "gem" in line:
				line = line.split("'")
				linex = line[0:2]
				for y in linex:
					y = y.strip()
					if not "gem" in y:
						_lista_.append(y)

	for x in _lista_:
		if x not in unique_list:
			unique_list.append(x)

	with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
		executor.map(versions_f, unique_list)

	filew.close()