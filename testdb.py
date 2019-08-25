#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from database import DataRetriver
import glob, os
import re

database = DataRetriver.DataRetriver("localhost", "renaud", "hulan8ye", "diceparser")

print("Set prefix Json")
#with open('prefix.json') as json_file:
    #data = json.load(json_file)
    #for p in data:
    #    print(p)
        #database.setPrefix(p, data[p])



print("Set alias Json")
with open('alias.json',"rb") as json_file: #encoding="utf-8", ,  errors="surrogateescape"
    data = json.load(json_file)
    for p in data:
        if not data[p]:
            print(p+" is empty")
        else:
            dictAlias=data[p]
            for key in dictAlias:
                cmds='\n'.join(dictAlias[key])
                if len(cmds)>0 and len(key)>0:
                    pass
  #                  print(p+" "+key)
         #           database.addAlias(p, key, cmds)



print("set macro")
os.chdir("/home/renaud/application/mine/discord-python/macros")
for filepath in glob.glob("*.json"):
 #   print(filepath)
    p = re.compile("macro_(.*).json")
    m = p.search(filepath)
    id_server =  m.group(1)
    with open(filepath, "rb") as macrofile:
        data = json.load(macrofile)
        for macros in data:
            pass
#            print(macros["pattern"])
           # print(macros["pattern"]+" cmd:"+macros["cmd"]+" regex:"+str(macros["regexp"])+" comment"+macros["comment"])
            #database.addMacro(id_server, macros["pattern"],macros["cmd"],macros["regexp"],macros["comment"])
#            for macro in macros:
#               print(macro)


print('show macro')
aliases = database.showMacro(531228945560109067,0)
print(aliases)
