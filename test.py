import os
import logic, re, stat


path_string = "C:/UnityProjects/commands.txt"


name1 = "\"filename\""
name2 = "\"fol.der\""
name3 = "filename"
name4 = "*.ext"
name5 = "\"filename.ext\""
name6 = "fol.der"

path = logic.PseudoDirEntry(path_string)

print(path.default_icon)
print(path.icon)

