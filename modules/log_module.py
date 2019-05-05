import os

#this is going to create a directory and create a file

def log(module_name, body):
    file = open('{}.txt'.format(module_name), 'a')
    file.write(body + '\n' + '\n')
    file.close()