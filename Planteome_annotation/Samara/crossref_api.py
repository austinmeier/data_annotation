import requests
import json

url3 = "https://api.crossref.org/works"

url2= "https://doi.crossref.org/search/doi"
url = 'https://doi.crossref.org/servlet/query'
query = "R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795."
pid = 'meiera@science.oregonstate.edu'
q2 = "|%20Natl%20Acad.%20Sci.%20USA|Zhou|94|24|13215|1997|||%0A|J.%20Mol.%20Biol.|Hagerman|260|||1996|||"
q3 = "10.1021/jf010280h"

data = {'query': query}

r = requests.get(url3, params=data)
# print r.headers
# print r.url
results = r.text
# print r.json

pretty_results = json.loads(results)

print pretty_results.keys()

print pretty_results['message']['items'][0]['DOI']

#print json.dumps(pretty_results, sort_keys=True,indent=4, separators=(',', ': '))