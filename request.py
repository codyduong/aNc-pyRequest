import requests
import json

token = open("token.txt", "r")

if token: 
    r = requests.get('https://api.github.com/users/codyduong/repos', auth=('codyduong', token.read()))
else: 
    r =  requests.get('https://api.github.com/users/codyduong/repos')


def requestsToMarkdown(d): #takes the request and parses it into a table only of the info i need.
    for each in d: #each repository
        print(each["name"])
        #todo literally everything else

if __name__ == "__main__":
    if r.status_code == 200: 
        print('200 OK: The request has succeeded.')
        requestsToMarkdown(r.json())
    else: 
        print(r.status_code + ': Something went wrong')