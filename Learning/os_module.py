# useful methods for os module

import os 

# os.listdir - List contents of a directory


os.listdir('.')


# os.rename - Rename a directory


os.rename('stage', 'preprod')


# os.chmod - Change permissions of file or directory


os.chmod('python.py', 0o777 )


# os.mkdir - Create directory


os.mkdir('/Documents/images')


# os.makedirs - Recursively create directory - makes intermediary directories needed 


os.makedirs('/Users/tndlebe/Downloads/scripts')


# os.remove - Delete file


os.remove('python.py')


#os.rmdir - delete single directory


os.rmdir('/Documents/images')


# os.removeddirs - delete tree of directories


os.removedirs('/Users/tndlebe/Downloads/scripts')


# os.stat - create stats for directory


os.stat('python.py')


# os.path - processing files from different places in system - join, split, basename, expanduser

os.path

# os.getcwd - get present working directory

print(os.getcwd())

#os.chdir - change current woeking directory

os.chdir('/new')
print(os.getcwd())
