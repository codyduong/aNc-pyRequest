import requests
import json
import os.path


USERNAME = 'codyduong'
MIN_PERCENTAGE_THRESHOLD = 0 #Percentage threshold before the lang is tossed into the other pile


def runRequest(u):
    token = ''
    with open('token.txt', "r") as f:
        token = f.read()
    if token: 
        #print("runRequest with Token: %s"  % (token))
        "Private repo access is broken, even with the token. wontfix (until i have to anyway)"
        return(requests.get(u, headers=('Authorization: token %s' % (token))))
    else: 
        #print("runRequest w/out Token")
        return(requests.get(u))


#ISO8601 to Month Day, Year (Jan 1, 2000)
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
def ISO8601toString(i):
    split = (i.split('T'))[0].split('-')
    year = str(split[0])
    month = str(MONTHS[int(split[1])-1])
    day = str(split[2])
    return('%s %s, %s' % (month, day, year))


def colorFromLang(lang): #reads from colors.json which was taken from here: https://github.com/ozh/github-colors
    with open('colors.json', "r") as f:
        cjson = f.read()
        cdata = json.loads(cjson)
        try:
            return("'%s'" % cdata[lang]['color'])
        except:
            print("No color detected for this language: %s, defaulting: White" % (lang))
            return("white")


def handleLangAPI(langs):
    otherPercent = 0
    string = '  languages:\n'
    string_other = ''
    total = 0
    for lang in langs: total+= langs[lang]
    for lang in langs:
        percent = ((langs[lang]/total)) * 100
        if percent > MIN_PERCENTAGE_THRESHOLD:
            string += ('    - name: %s\n      color: %s\n      percent: %s\n' % (lang, colorFromLang(lang), round(percent,2)))
        else:
            string_other += ('    - name: %s\n      color: %s\n      percent: %s\n' % (lang, colorFromLang(lang), round(percent,2)))
            otherPercent += percent
    string += ('  languages_other_percent: %s\n  languages_other:\n' % (round(otherPercent, 2))) + string_other
    return string


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
    r = runRequest('https://api.github.com/users/%s/repos' % (USERNAME))
    if r.status_code == 200: 
        print('200 OK')
        convertRequest(r.json())
        print('Completed creating repos.yml')
    else: 
        print(r.status_code + ': Something went wrong')