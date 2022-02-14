# With expression

#for simple file with few words,or lines

with open("text.txt") as f:
  print(f.read())
  
#readlines - for few lines

with open("text.txt") as f:
  print(f.readlines())
  
#overwrite original text

with open("text.txt", "w") as f:
  print(f.write("new input"))

with open("text.txt") as f:
  print(f.read()) #output new input
  
  
# use pathlib - reading and writing files- pathlb handles file object 

#reading

```
import pathlib

path = pathlib.Path("/Users/tndlebe/downloads/index.py")

path.read_text()

#writing

```
import pathlib

path = pathlib.Path("/Users/tndlebe/downloads/index.html")

path.write_text("Hello World")
  
