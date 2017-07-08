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


def get_prop_by_type(proptype, index=0):
	index = str(index + 1)
	if proptype[0] == "{":
		return make_dict_prop(proptype)

	elif proptype == "bool":
		return "${" + index + ":true}"

	elif proptype == "color":
		return "'#${" + index + ":000000}'"

	elif proptype == "number":
		return "${" + index + ":0}"

	elif proptype == "string":
		return "'$" + index + "'"

	elif proptype[:4] == "enum":
		return "'$" + index + "'"

def make_dict_prop(dict_prop):
	res = []
	items = re.findall(r"\w+: \w+", dict_prop)
	for i, item in enumerate(items):
		key, val = item.split(': ')
		itm_string = "\t"
		itm_string += key
		itm_string += ": "
		itm_string += get_prop_by_type(val, i)
		res.append(itm_string)
	return "{\n" + ",\n".join(res) + "\n}"


def make_enum_prop(enum_prop):
	return enum_prop

# print make_enum_prop("enum('name', 'secondname')")
# print get_prop_by_type("{width: number, height: number, opacity: string}")
# print get_prop_by_type("string")
# print get_prop_by_type("bool")

def make_complete_dict(prop):
	property_name = re.findall(r"(\w+)\?", prop.text)[0]
	description = prop.span.text
	res = {
		"trigger": property_name + "\t" + description,
		"contents": "%s: %s" % (property_name, get_prop_by_type(description))
	}
	return res


def main():
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


main()