# What
A python script accessing Github's REST API and exporting relevant data to a YML for JS to process on my own personal website.

# Exported Result
```YML
repos:

- name: aNc_pyRequest
  private: False
  permalink: https://github.com/codyduong/aNc_pyRequest
  description: A personal tool used to access GitHub's REST API and use it to create YML for the artNcode repository.
  languages:
    - name: Python
      color: '#3572A5'
      percent: 100.0%
    - name: 
      color: 
      percent: 0%
    - name: 
      color: 
      percent: 0%
    - name: other
      color: white
      percent: 0%
  created: Jan 03, 2021
  updated: Jan 06, 2021

- name: artNcode
  private: False
  permalink: https://github.com/codyduong/artNcode
  description: My website.
  languages:
    - name: SCSS
      color: '#c6538c'
      percent: 58.21%
    - name: HTML
      color: '#e34c26'
      percent: 32.81%
    - name: Ruby
      color: '#701516'
      percent: 8.13%
    - name: other
      color: white
      percent: 0.85%
  created: Sep 04, 2020
  updated: Jan 06, 2021
```

# Utilizing for yourself
Unfortunately poetry wasn't complying so there aren't any dependencies in this repo. If you need to know, any versions of requests should work, and python 3.9+. But I reckon since it's so simple, that any combination of the versions should work... But don't quote me on that.

Simply change the relevant information:
```python
6 | USERNAME = 'codyduong'
7 | REPOS_LINK = 'https://api.github.com/users/codyduong/repos'
```
For using a personal token, create a token.txt in the same directory as request.py, this step is optional and is not necessary for it to function. It is recommended if you want to access private repos.

The first time you run request.py it will export a whitelist.txt, where you have to set the true/false values for repos you want to export to YML
```
aNc_pyRequest true
artNcode false
...so on and so forth
```

Everytime afterwards it should export any repos marked with true to the YML. If your repos changed, it'll automatically add it to the list and default it to false.
