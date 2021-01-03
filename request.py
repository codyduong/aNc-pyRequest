import requests
import json
import os.path

def runRequest(u):
    token = ''
    with open('token.txt', "r") as f:
        token = f.read()
    if token: 
        print("runRequest with Token: %s"  % (token))
        return(requests.get(u, auth=('codyduong', token)))
    else: 
        print("runRequest with noToken")
        return(requests.get(u))


"""
Relevant dictionary values I want to store in YAML
name 
private -> have to switch the token for utilization of this, otherwise this will always be false
html_url -> Used for permalinking (not the API Url for the Repo)
description -> Quick thumbnail Description
languages_url -> Gives the GitHub API Url again, have to input back into requests.get ... An example of json given after request below. (Lang && Lines of Code)
    |   {
    |     "SCSS": 26226,
    |     "HTML": 13103,
    |     "Ruby": 3664,
    |     "Shell": 384
    |   }
    --> Calculate relevant percentages, give to YAML which then is used by Liquid and JS to create a cool visual. Or something...
created_at -> YAML
updated_at -> YAML

---YAML---
repos:

- name:
  private:
  html_url:
  descrption:
  languages: <-- supports only 3 languages (maybe I'll change this)
    - language: SCSS
      LoC: 26226
    - language2: HTML
      LoC: 13103
    - language3: Ruby
      LoC: 3664
    - other: Other
      LoC: 384
  created:
  updated:
"""
def requestsToMarkdown(l): #takes the request and parses it into a table only of the info i need.
    #reads the whitelist. if there isn't one it regenerates one, but doesn't export YAML
    if os.path.exists('whitelist.txt'):
        with open('whitelist.txt', "r+") as f:
            pref = []
            for line in f:
                pref.append(line.strip().split(' '))
            whitelist = dict(pref)
            for repo in l: 
                repoName = repo["name"]
                try:
                    if whitelist[repoName] == 'true':
                        print("Whitelisted, converting %s..." % (repoName))
                        #complete YAML
                    else:
                        print("Blacklisted, ignoring %s..." % (repoName))
                except:
                    print("Missing, creating %s..." % (repoName))
                    f.writelines("%s false\n" % (repoName))
    else:
        print("Creating new whitelist.txt, YAML not exported.")
        with open("whitelist.txt", "w") as f:
            repoList = []
            for repo in l:
                repoList.append("%s false\n" % (repo["name"]))
            f.writelines(repoList)


if __name__ == "__main__":
    r = runRequest('https://api.github.com/users/codyduong/repos')
    if r.status_code == 200: 
        print('200 OK')
        requestsToMarkdown(r.json())
    else: 
        print(r.status_code + ': Something went wrong')