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
  
  
  
