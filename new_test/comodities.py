import requests

url = 'http://atlas.media.mit.edu/hs/export/2010/usa/all/show/'

h = requests.get(url)
print h.text
