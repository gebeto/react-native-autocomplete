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
	"http://facebook.github.io/react-native/releases/0.46/docs/imagestyleproptypes.html",
	"http://facebook.github.io/react-native/releases/0.46/docs/layout-props.html",
	"http://facebook.github.io/react-native/releases/0.46/docs/shadow-props.html",
]

def make_complete_dict(prop):
	prop_types = {
		"bool": "${1:true}",
		"color": "'#${1:000000}'",
		"number": "${1:0}",
		"string": "'$1'",
		"enum": "'$1'",
	}
	property_name = re.findall(r"(\w+)\?", prop.text)[0]
	description = prop.span.text
	prop_type = prop_types.get(description)
	res = {
		"trigger": property_name,
		"contents": "%s/%s: %s" % (property_name, description, prop_types.get(description if prop_type else 'enum'))
	}
	return res


res = []
for url in styles_links:
	soup = BeautifulSoup(requests.get(url).content, "html.parser")
	props_block = soup.find("div", {"class": "props"})
	props = props_block.find_all("h4", {"class": "propTitle"})
	for prop in props:
		res.append( make_complete_dict(prop) )


styles_json["completions"] = res

print styles_json

json.dump(styles_json, open("RNStyles.sublime-completions", "w"), indent=4)


