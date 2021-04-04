# Author: @Splint3r7

import subprocess
import concurrent.futures
import sys
import argparse
import json
from colorama import init , Style, Back,Fore

parser = argparse.ArgumentParser(description="Detect Rails Site using wappalyzer-cli")

parser.add_argument('-f','--file',
                            help = "file with list of domains",
                            type = str,
                            required = True)

parser.add_argument('-o','--output',
                            help = "output file",
                            type = str,
                            required = True)

args = parser.parse_args()

def installation():
	result = subprocess.Popen(['which', 'wappalyzer'], stdout=subprocess.PIPE)
	output = result.stdout.read()
	out = output.decode('utf-8')
	if "not found" in out:
		sys.exit()


def waplizer(_url_):

	print(Style.DIM+Fore.GREEN+"[-]"+Style.RESET_ALL+Style.DIM+Fore.WHITE+" TESTING | "+Style.RESET_ALL+Style.BRIGHT+Fore.BLUE+"{}".format(_url_)+Style.RESET_ALL)
	result = subprocess.Popen(['wappalyzer', '{}'.format(_url_)], stdout=subprocess.PIPE)
	output = result.stdout.read()

	out = json.loads(output)

	for i in out['technologies']:
		slug = i['slug']
		if "ruby-on-rails" in slug:
			print(Style.DIM+Fore.YELLOW+"["+Style.BRIGHT+Fore.GREEN+"+"+Style.RESET_ALL+Style.DIM+Fore.YELLOW+"]"+Style.RESET_ALL+Style.BRIGHT+Fore.RED+" Rails Site Found! |"+Style.BRIGHT+Fore.RED+" {}".format(_url_)+Style.RESET_ALL)
			f2.write(_url_+"\n")


if __name__ == "__main__":

	installation()
	_listUrls_ = []
	f = open(args.file, "r")
	for line in f:
		line = line.strip()
		_listUrls_.append(line)
	f.close()
	f2 = open(args.output, "w")
	with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
		executor.map(waplizer, _listUrls_)
	f2.close()
