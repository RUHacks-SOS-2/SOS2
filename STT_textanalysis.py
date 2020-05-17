# -*- coding: utf-8 -*-
"""
Created on Sat May 16 21:03:47 2020

@author: azizu
"""

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import s2t_stream as s2t
# Instantiates a client
client = language.LanguageServiceClient()
def main():
    #open all speech to text files, these files would have been created by the speech to text program 
    with open ('fname.txt','r+') as fname:
        First_name = fname.readline()
        
    with open ('lname.txt','r+') as lname:
        Last_name = lname.readline()
        
    with open ('age.txt','r+') as age:
        aged = age.readline()
        
    with open ('address.txt','r+') as address:
        addresss = address.readline()
        
    with open ('postal.txt','r+') as postal:
        postal_code = postal.readline()
        
    with open ('need.txt','r+') as need:
        needs = need.readline()
    
    #store all speech to text files in a list
    senior_info = [First_name,Last_name,aged,addresss,postal_code,needs]
    
    #use a loop to refer to each instance and analyze the entities for keywords in senior_info
    
    count = 0
    while count < len(senior_info):
        document = types.Document(
        content=senior_info[count],
        type=enums.Document.Type.PLAIN_TEXT)
        
    # Detects the entities of the text
        response_entities = client.analyze_entities(document=document,encoding_type='UTF32')
        
        with open ('fireDB.txt','a+') as f: 
            for entity in response_entities.entities:       
                f.writelines("{0}\n".format(entity.name))
        f.close()
        count += 1
        
    #View what the text analysis will spit out
    Firebase_input = open('fireDB.txt','r')
    print(Firebase_input.read())

if __name__ == '__main__':
    print("Speech to text")
    s2t.main()
    print("Text analysis")
    main()
    
