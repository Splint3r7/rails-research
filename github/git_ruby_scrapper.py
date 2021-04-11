import requests
from colorama import init , Style, Back,Fore
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import sys
import re
import requests
import argparse
import concurrent.futures

parser = argparse.ArgumentParser(description="Extract Github Projects via Organization Name / Specfic Langauage")

parser.add_argument('-f','--file',
                            help = "List of Organization",
                            type = str,
                            required = True)

parser.add_argument('-o','--output',
                            help = "Output file",
                            type = str,
                            required = True)

parser.add_argument('-l','--lang',
                            help = "Language of project",
                            type = str,
                            required = False)

args = parser.parse_args()

#organization = str(sys.argv[1])
#git_urls = sys.argv[2]


headers = {
	'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
}

def getpages(_org_):

	em = 0

	#if args.lang:
	_url_ = "https://github.com/"+_org_+"?q=&type=&language=ruby&sort="
	#else:
	#	_url_ = "https://github.com/"+_org_
	req = requests.get(_url_, headers=headers)

	if req.status_code == 200:
		soup = BeautifulSoup(req.content, 'html.parser')
		try:
			em = soup.find("em", {"class": "current"}).attrs['data-total-pages']
			em = int(em)
			em = em+1
		except:
			em = 2
	
	return em

def Getting_all_git_repos(_Organization_):

	for pages in range(1,getpages(_Organization_)):

		#if args.lang:
		
		_url_ = "https://github.com/"+_Organization_+"/?q=&type=&language=ruby&sort=&page={}".format(pages)
		#else:
		#	_url_ = "https://github.com/"+_Organization_+"/?page={}".format(pages)

		req = requests.get(_url_, headers=headers)

		if req.status_code == 200:
			soup = BeautifulSoup(req.content, 'html.parser')
			for link in soup.findAll('a', attrs={'href': re.compile("^/{}/.*".format(_Organization_))}):
				urls = link.get('href')
				if not urls.endswith("stargazers") and not urls.endswith("members") and not "/issues" in urls and not "/pulls" in urls:
					#print(urls)
					resutls_not_use = "https://github.com/"+urls+".git"
					resutls = "https://raw.githubusercontent.com/"+urls+"/master/Gemfile.lock"
					git_urls_output.write(resutls+"\n")
					print(resutls_not_use)
	
	#print("\n"+"[+] Fetched All github urls in "+args.output+" file")


def ValidateGemfiles(_Url_):

	req = requests.get(_Url_, timeout=15)
	if req.status_code == 200:
		print(_Url_)
		gemfiles_f.write(args.output)

if __name__ == "__main__":

	git_urls_output = open("temp.txt", "w")

	with open(args.file, "r") as orgs:
		orgss = orgs.read().splitlines()

	#for org in orgss:
	#	org = org.strip()
	with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
		executor.map(Getting_all_git_repos, orgss)
		#print("\n"+"[+] Fetching {} github projects".format(org)+"\n")
		#Getting_all_git_repos(org)

	git_urls_output.close()

	gemfiles_f = open(args.output, "w")
	with open("temp.txt", "r") as gemfile:
		gemfiles = gemfile.read().splitlines()

	print ("[+] Valid Gemfilie.lock files found In All projects!"+"\n")
	with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
		executor.map(ValidateGemfiles, gemfiles)

	gemfiles_f.close()
	

