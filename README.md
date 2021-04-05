# rails-research

RAILS RESEARCH:

TODO-list:

1) Reverse engineer bundle-audit and https://github.com/rubysec/ruby-advisory-db to create:
   - Wordlist for GET-based vulnerabilities
   - Nuclei templates for POST-based vulnerabilities (don't forget to add the 3 ones of https://github.com/jaeles-project/jaeles-signatures/tree/master/cves)
   - Burp Bounty profile to detect magic-bytes of serialized ruby code?

2) Remaining vulns for the blog post:
   -Unmarshalling
   -Open redirect
3) Search again in Google to make sure we did find all the dangerous functions for each type of vulnerability and include them in the blog post

4) Create tool to detect Rails for a big list of subdomains:
   -Easiest option: use wappalyzer-cli with bash/python
   -Other option: with Python make a request to all the subdomains and detect cookies/headers/csrf token name

5) Create wordlist via Google dorking:
  -We can use some dork like site:github.com inurl:/config/routes.rb  with tools like dorks-eye (view in Github) to get all those files
  - Parse them to get routes. Check if there is a tool that already exists for this (it is likely to exist) or write a tool to parse that ourselves
- Clean the wordlist -> all the endpoints with more than 1 hit (idk /api/users appears twice in the wordlist, then it remains, but if only appears once it gets removed or moved to a secondary wordlist)
   
5) Create tool to check for dependency confusion vulns:
   Having this post in mind: https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610
   -It must check all the sites where code is hosted (ex: Github, and other alternatives, search for more)
   -Crawl their projects looking for the Gemfile
   -Check if the Gem is internal (like, if its a module which is already defined locally)
   -Query to the main Gem repo (idk what is called) to check if that Gem exists
   -Create gem with TCP reverse shell both for windows and linux (encode it just in case the guys of the Gem repo check for malware)
   -Upload malicious gem (maybe manually)
   -Set up VPS or something to receive shells
                                                                                                                                                                                                                                      

6) Get Ruby on Rails site’s from the shodan Dork:
https://www.shodan.io/search?query=title%3A%22Ruby+on+Rails%22

7) Recon for Gemfile.lock

1) 

site:github.com inurl:gemfile
Parse to googDorker and get all github urls

2)
site:github.com inurl:gemfile
Find .lock from gemfiles 
Parse to googdorker and find all urls
                                                                                                                                                                                                                                           
BUG BOUNTY WORKFLOW:                                                                                                                                                                                                                       
                                                                                                                                                                                                                                           
1-Subdomain enum                                                                                                                                                                                                                           
2-Launch rails instances detection script                                                                                                                                                                                                  
3-Launch public wordlists (listed in the blog) and the one created via bundler-audit,ruby-advisory-db against Rails sites                                                                                                                  
4-Launch nuclei templates against Rails sites                                                                                                                                                                                              
5-Check for dependency confusion (if the company has some public code)
