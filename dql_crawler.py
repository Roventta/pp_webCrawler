#!/usr/bin/env python
# coding: utf-8

# In[251]:


import requests
import pandas as pd
from bs4 import BeautifulSoup


URL = "https://dogsqueensland.org.au/clubs/affiliated-clubs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


# In[252]:


'''
dsl website's fields are not well constructed, for one entry, its first child is name
its following child are random information, feature of one child is titled by its content, in 
following format: 
"Email: xxxx"

if the child contains contact information, then it will have two inner fields, 
one is contact name, one is phone number, in following format:
"contact: Name Name, Phone: 0000000"

each child is seperated by a <br />
...
'''


# In[253]:


DFcolumn_index = {
    "Name": 0,
    "Email": 1,
    "Website": 2,
    "Address": 3,
    "PetTypes": 4,
    "ContactName": 5,
    "ContactPhone": 6
}

def dql_cluster_first_entry(guide_word, soup):
    if(guide_word == "A" or guide_word == "B"):
        oneEle = soup.find(id = guide_word).parent.parent.next_sibling.next_sibling
    if(guide_word != "A" and guide_word != "B"):
        oneEle = soup.find(id = guide_word).parent.next_sibling.next_sibling
        
    for a in oneEle.find_all('a'):
        a.unwrap()
    return oneEle

def dql_next_entry(ele):
    return ele.next_sibling.next_sibling

def dql_identify_insert(source_string, target):
    ## parse the first word
    identifier = ""
    content = ""
    i = 0
    for char in source_string:
        if(char == ':'):
            content = source_string[i+1:];
            break
        if(char != ':'):
            identifier += char;
            i += 1;
    ##print(identifier);
    ##print(content);
    ##which_col = DFcolumn_index[identifier]
    ##target[which_col] = content
    if(identifier == "Contact"):
        phone_index = source_string.find("Phone:")
        which_col = DFcolumn_index["ContactName"];
        target[which_col] = source_string[0: phone_index]
        if(phone_index != -1):
            ##print(source_string[phone_index+6:])
            which_col = DFcolumn_index["ContactPhone"];
            target[which_col] = source_string[phone_index+7:]
    if(identifier != "Contact"):
        which_col = DFcolumn_index[identifier]
        target[which_col] = content
    
    return 0

def dql_parse_one_ele(source_ele, target):
    ## first element is always name
    target[0] = source_ele.contents[0].contents[0];
    
    ## loop through following elements, generate source string at first
    ss_i = 0;
    source_string = "";
    for i in range(2, len(source_ele)):
        if source_ele.contents[i].name != "br":
            source_string += str(source_ele.contents[i]);
        if source_ele.contents[i].name == "br" or i == len(source_ele)-1:
            dql_identify_insert(source_string, target);
            ##print(source_string);
            source_string = "";

majorDF = pd.DataFrame(columns=list(DFcolumn_index.keys()))

test = ["NA" for i in range(7)]


# In[254]:


oneEle =dql_cluster_first_entry("E", soup)
dql_parse_one_ele(oneEle, test)
##print(list(oneEle))
##print(oneEle.contents[3])
##dql_identify_feature(oneEle.contents[2], test)

majorDF.loc[0] = test
majorDF

