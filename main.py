import requests
import pandas as pd
from datetime import datetime


years = datetime.now().year - 100
dob_cutoff = f"{years}-01-01T00:00:00Z"


query = f"""
SELECT ?person ?personLabel ?dob WHERE {{
  ?person wdt:P31 wd:Q5;  # instance of human
          wdt:P106 wd:Q2526255;  # occupation: film director
          wdt:P19 wd:Q65;  # place of birth: Los Angeles
          wdt:P569 ?dob.  # date of birth

  FILTER(?dob >= "{dob_cutoff}"^^xsd:dateTime)
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
ORDER BY ?dob
LIMIT 200
"""


url = "https://query.wikidata.org/sparql"
headers = {
    "Accept": "application/sparql-results+json"
}


response = requests.get(url, params={'query': query}, headers=headers)
data = response.json()


results = data["results"]["bindings"]
rows = []

for result in results:
    name = result["personLabel"]["value"]
    dob = result["dob"]["value"]
    rows.append({"Name": name, "Date of Birth": dob})


df = pd.DataFrame(rows)
print(df)
