import requests
import json
import os.path


USERNAME = 'codyduong'
REPOS_LINK = 'https://api.github.com/users/codyduong/repos'


def runRequest(u):
    token = ''
    with open('token.txt', "r") as f:
        token = f.read()
    if token: 
        #print("runRequest with Token: %s"  % (token))
        return(requests.get(u, auth=(USERNAME, token)))
    else: 
        print("runRequest w/out Token")
        return(requests.get(u))


#ISO8601 to Month Day, Year (Jan 1, 2000)
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
def ISO8601toString(i):
    split = (i.split('T'))[0].split('-')
    year = str(split[0])
    month = str(MONTHS[int(split[1])-1])
    day = str(split[2])
    return('%s %s, %s' % (month, day, year))


def handleLangAPI(langs):
    lang1, lang2, lang3, loc1, loc2, loc3, loc4 = ('','','',0,0,0,0)
    i = 0
    for lang in langs:
        if i==0:
            lang1 = lang
            loc1 = langs[lang]
        elif i==1:
            lang2 = lang
            loc2 = langs[lang]
        elif i==2:
            lang3 = lang
            loc3 = langs[lang]
        else: 
            loc4 += langs[lang]
        i+=1
    s = ('  languages:\n    - language1: %s\n      LoC: %s\n    - language2: %s\n      LoC: %s\n    - language3: %s\n      LoC: %s\n    - other:\n      LoC: %s\n' %
        (lang1, loc1, lang2, loc2, lang3, loc3, loc4))
    return s


def toYML(repo, lines):
    final = lines
    final.append('- name: %s\n  private: %s\n  permalink: %s\n  description: %s\n' % (repo['name'], repo['private'], repo['html_url'], repo['description']))
    #language handling
    final.append(handleLangAPI(runRequest(repo['languages_url']).json()))
    final.append('  created: %s\n  updated: %s\n\n' % (ISO8601toString(repo['created_at']), ISO8601toString(repo['updated_at'])))
    return final


def convertRequest(l): 
    if os.path.exists('whitelist.txt'): #it doesn't matter whether i check this before or after requesting API, regardless of whitelist existence, I need repo list to compare
        with open('whitelist.txt', "r+") as f:
            pref = []
            lines = []
            for line in f:
                pref.append(line.strip().split(' '))
            whitelist = dict(pref)
            for repo in l: 
                repoName = repo["name"]
                try:
                    whitelist[repoName]     #a dumb way to see if it's in the whitelist
                except:
                    print("Missing, creating %s..." % repoName)
                    f.writelines("%s false\n" % repoName)
                else:
                    if whitelist[repoName] == 'true':
                        print("Whitelisted, converting %s..." % repoName)
                        lines = toYML(repo, lines)
                        with open('repos.yml', "w") as g:
                            g.writelines("repos:\n\n")
                            g.writelines(lines)                                
                    else:
                        print("Blacklisted, ignoring %s..." % repoName)
    else:
        print("Creating new whitelist.txt, YAML not exported.")
        with open("whitelist.txt", "w") as f:
            lines = []
            for repo in l:
                lines.append("%s false\n" % repo["name"])
            f.writelines(lines)


if __name__ == "__main__":
    r = runRequest(REPOS_LINK)
    if r.status_code == 200: 
        print('200 OK')
        convertRequest(r.json())
    else: 
        print(r.status_code + ': Something went wrong')