from bs4 import BeautifulSoup
import requests
import json
import re

sections = []
domain = "https://facebook.github.io/react-native/"

def main():
	imports_json = {
		"scope": "source.js, source.jsx",
		"comment": "React Native Imports",
		"completions": []
	}
	url = "https://facebook.github.io/react-native/docs/getting-started.html"
	soup = BeautifulSoup(requests.get(url).content, "html.parser")
	sections = soup.find_all("div", {"class": "nav-docs-section"})[-2:]
	sections = sections[0].find_all("a") + sections[1].find_all("a")
	sections = [{
		"title": s.text,
		"url": domain + s["href"]
	} for s in sections]
	imports_json["completions"] = sorted([s["title"] for s in sections])
	json.dump(imports_json, open("../RNImport.sublime-completions", "w"), indent=4)
	return sections


def subParams(a):
	g = a.group(1)
	print g
	if g == "()": return ""
	ar = []
	res = ""
	i = 1
	for p in g.split(", "):
		print p
		ar.append( "${" + str(i) + ":" + p + "}" )
		i += 1

	# print ar
	return "(" + ", ".join(ar) + ")"

def save_section_methods(section):
	soup = BeautifulSoup(requests.get(section["url"]).content, "html.parser")
	props = soup.find_all("div", {"class": "props"})

	# print len(props)
	methods = None
	for prop in props:
		h3 = prop.previousSibling
		h3.a.extract()
		h3.a.extract()
		if h3.text.strip() == "Methods":
			methods = prop
			break

	methods = methods.find_all("h4", {"class": "methodTitle"})
	autocomps = []
	for method in methods:
		method.a.extract()
		method.a.extract()
		# method.span.extract()
		mt = section["title"] + "." + method.text.strip()
		short = re.sub(r"\(([\w, ?]+)\)", "", mt)
		print "SHORT:", short
		print "MTO:", mt
		# mt = re.sub(r"\(([\w\W]*?)\)", subParams, mt)

		a = "(".join(mt.split("(")[1:])
		a = ")".join(a.split(")")[:-1])
		ar = []
		i = 1
		for p in a.split(", "):
			# print p
			ar.append( "${" + str(i) + ":" + p + "}" )
			i += 1
		mt = "(" + ", ".join(ar) + ")"

		print "MT:", mt
		print "\n\n"
		# print "ST:", short
		# print mt, short, "\n"
		autocomps.append({
	        "trigger": short, 
	        "contents": mt
	    })

	json.dump({
		"scope": "source.js, source.jsx",
		"comment": "React Native " + section["title"],
		"completions": autocomps
	}, open("../completions/" + section["title"] + ".sublime-completions", "w"), indent=4)


for section in main():
	try:
		save_section_methods(section)
	except:
		print section