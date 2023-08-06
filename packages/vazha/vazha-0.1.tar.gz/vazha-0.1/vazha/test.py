import re
import keyword

def multiwordReplace(text, wordDic):
    rc = re.compile('|'.join(map(re.escape, wordDic))) #This is to remove escape sequences
    # rc = re.compile('|'.join(wordDic))
    print(rc)
    def translate(match):
        print(match)
        return wordDic[match.group(0)]
    return rc.sub(translate, text)
str1 = \
"""
print('Hello World)
def myfun:
	print("print hello")

"""
# the dictionary has target_word : replacement_word pairs
wordDic = {
'print':'show',
'def':'make',
}
# call the function and get the changed text
str2 = multiwordReplace(str1, wordDic)
print(str2)

for e in __builtins__.__dict__:
    print(e)
s="""
__name__
__doc__
__package__
__loader__
__spec__
__build_class__
__import__
abs
all
any
ascii
bin
breakpoint
callable
chr
compile
delattr
dir
divmod
eval
exec
format
getattr
globals
hasattr
hash
hex
id
input
isinstance
issubclass
iter
len
locals
max
min
next
oct
ord
pow
print
repr
round
setattr
sorted
sum
vars
None
Ellipsis
NotImplemented
False
True
bool
memoryview
bytearray
bytes
classmethod
complex
dict
enumerate
filter
float
frozenset
property
int
list
map
object
range
reversed
set
slice
staticmethod
str
super
tuple
type
zip
open
quit
exit
copyright
credits
license
help

"""

l = s.strip().split('\n')
print(l)
l = list(set(l))
l.sort()
print(l)
# d= dict(enumerate(l))
 

# from googletrans import Translator
# translator = Translator()


# translations = translator.translate(l, dest='ml')
# for translation in translations:
#     print(translation.text,'=',translation.origin) 


import json
with open('vazha_to_manglish.json') as f:
    a = json.load(f)
    d = a["keywords"]
    for i in d:
        name = d[i].replace(" ","")
        print("const {}Completion = new vscode.CompletionItem('{}');".format(name,i))
        print("{}Completion.filterText = '{}';".format(name,d[i]))
        print("{}Completion.kind = vscode.CompletionItemKind.Keyword;".format(name))
        print("completion_items.push({}Completion)".format(name))
        print()

# from googletrans import Translator
# translator = Translator()


# keywords = []
# for k in keyword.kwlist:
#     if(k not in __builtins__.__dict__):
#         keywords.append(k)
# print(keywords)

# translations = translator.translate(keywords, dest='ml')
# for translation in translations:
#     print(translation.text,'=',translation.origin) 


import json
from vazha_to_eng import *
code="ഉറപ്പിക്കുക കാത്തിരിക്കുക"

for i in keywords:
    name = keywords[i]
    code = re.sub(i,keywords[i],code)

print(code)



