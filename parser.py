import glob
import re
import json

imports_json = {
	"scope": "source.js - variable.other.js",
	"comment": "React Native Imports",
	"completions": []
}

componenets = []
# componenets = glob.glob("react-native/Libraries/Components/*.js")

imports = [
	glob.glob("react-native/Libraries/*/*.js"),
	glob.glob("react-native/Libraries/*/*/*.js"),
]

for each in imports:
	componenets += each
componenets = list(set(componenets))
	

classfinder = re.compile(r"^class \w+ = createReact", re.MULTILINE)
constfinder = re.compile(r"const \w+ = createReact", re.MULTILINE)
varfinder = re.compile(r"var \w+ = createReact", re.MULTILINE)
providemodulefind = re.compile(r"providesModule (\w+)", re.MULTILINE)


res = []


for c in componenets:
	fndd = False
	cont = open(c).read()
	# for each in classfinder.findall(cont):
	# 	fndd = True
	# 	res.append( each.split(' ')[0] )

	# for each in constfinder.findall(cont):
	# 	fndd = True
	# 	res.append( each.split(" = ")[0].split(' ')[1] )

	# for each in varfinder.findall(cont):
	# 	fndd = True
	# 	res.append( each.split(" = ")[0].split(' ')[1] )

	try:
		res += providemodulefind.findall(cont)
	except:
		pass

	# if not fndd:
		# print c

print res
res = list(set(res))
imports_json["completions"] = sorted(res)

json.dump(imports_json, open("RNImport.sublime-completions", "w"), indent=4)
# print len(res)
# print len(list(set(res)))