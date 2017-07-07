from bs4 import BeautifulSoup
import requests
import json


imports_json = {
	"scope": "source.js - variable.other.js",
	"comment": "React Native Imports",
	"completions": []
}


url = "https://facebook.github.io/react-native/docs/getting-started.html"
soup = BeautifulSoup(requests.get(url).content, "html.parser")
sections = soup.find_all("div", {"class": "nav-docs-section"})[-2:]
sections = sections[0].find_all("a") + sections[1].find_all("a")
sections = [{
	"title": s.text,
	"url": s["href"]
} for s in sections]

imports_json["completions"] = sorted([s["title"] for s in sections])

json.dump(imports_json, open("RNImport.sublime-completions", "w"), indent=4)
# print len(list(set(res)))