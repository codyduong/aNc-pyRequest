import requests
import json
import os.path


USERNAME = 'codyduong'
REPOS_LINK = 'https://api.github.com/users/codyduong/repos'
MIN_PERCENTAGE_THRESHOLD = 0 #Percentage threshold before the lang is tossed into the other pile


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
    total = 0
    for lang in langs: total+= langs[lang]
    for lang in langs:
        percent = ((langs[lang]/total)) * 100
        if percent > MIN_PERCENTAGE_THRESHOLD:
            string += ('    - name: %s\n      color: %s\n      percent: %s\n' % (lang, colorFromLang(lang), round(percent,2)))
        else:
            print('flushed')
            otherPercent += percent
    string += ('    - name: Other\n      color: white\n      percent: %s\n' % (round(otherPercent, 2)))
    return string
    """
    S = 0
    for lang in langs:
        S += langs[lang]
        langList.append(lang)
        colorList.append(colorFromLang(lang))
    for lang in langs:
        percent = round((langs[lang]/S) * 100, 2)
        if len(percentList) < 3:
            percentList.append(percent)
        else:
            try:
                percentList[3] = float(percentList[3]) + percent
            except:
                percentList.append('0')
                percentList[3] = float(percentList[3]) + percent         
    if len(langList) < 3:
        for i in range(3 - len(langList)):
            langList.append('')
    if len(colorList) < 3:
        for i in range(3 - len(colorList)):
            colorList.append('')
    if len(percentList) < 4:
        for i in range(4 - len(percentList)):
            percentList.append('0')
    for i in range(len(percentList)):
        percentList[i] = str(percentList[i]) + '%'
    l1 = ('  languages:\n    - name: %s\n      color: %s\n      percent: %s\n' % (langList[0], colorList[0], percentList[0]))
    l2 = ('    - name: %s\n      color: %s\n      percent: %s\n' % (langList[1], colorList[1], percentList[1]))
    l3 = ('    - name: %s\n      color: %s\n      percent: %s\n' % (langList[2], colorList[2], percentList[2]))
    l4 = ('    - name: Other\n      color: white\n      percent: %s\n' % (percentList[3]))
    return (l1+l2+l3+l4)
    """


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
        print('Completed creating repos.yml')
    else: 
        print(r.status_code + ': Something went wrong')