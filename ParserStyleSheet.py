from bs4 import BeautifulSoup
import requests
import json
import re


styles_json = {
	"scope": "source.js, source.jsx",
	"comment": "React Native StyleSheet",
	"completions": []
}

styles_links = [
	"http://facebook.github.io/react-native/releases/0.46/docs/viewstyleproptypes.html",
	"http://facebook.github.io/react-native/releases/0.46/docs/textstyleproptypes.html",
	"http://facebook.github.io/react-native/releases/0.46/docs/imagestyleproptypes.html"
]



url = styles_links[0]
soup = BeautifulSoup(requests.get(url).content, "html.parser")
props_block = soup.find("div", {"class": "props"})
props = props_block.find_all("h4", {"class": "propTitle"})
prop = props[0]
print prop
print re.findall(r"(\w+)\?", prop.text)[0]
print prop.span.text

# sections = sections[0].find_all("a") + sections[1].find_all("a")
# sections = [{
# 	"title": s.text,
# 	"url": s["href"]
# } for s in sections]

# imports_json["completions"] = sorted([s["title"] for s in sections])

# json.dump(imports_json, open("RNImport.sublime-completions", "w"), indent=4)


