#!/usr/bin/env python
# coding: utf-8

# In[30]:


import requests
import pandas
from bs4 import BeautifulSoup

base_url="https://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/"

r=requests.get(base_url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

c=r.content

soup=BeautifulSoup(c, "html.parser")

# grab the total page number from the html page
page_num=soup.find_all("a",{"class":"Page"})[-1].text
#print(page_num)

# list to save dictionary entries of the properties
l=[]

# retrieve each page from the url; use page_num as last range 
for page in range(0,int(page_num)*10,10):
    print(base_url+"t=0&s="+str(page)+".html")
    # store page
    r=requests.get(base_url+"t=0&s="+str(page)+".html", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    # grab content of r
    c=r.content
    # parse through the content and store in BeautifulSoup object
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})
    
    for item in all:
        # create an empty dictionary
        d={}
        d["Address"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text
        try:
            d["Locality"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"]=None
        d["Price"]=item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
        try:
            d["Beds"]=item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"]=None

        try:
            d["Area"]=item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area"]=None

        try:
            d["Full Baths"]=item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"]=None

        try:
            d["Half Baths"]=item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"]=None

        for column_group in item.find_all("div",{"class":"columnGroup"}):
            #print(column_group)
            # use zip() to iterate through two lists at a time
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                #print(feature_group.text, feature_name.text)
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text
        l.append(d)

# load list into our dataframe object
df=pandas.DataFrame(l)

# save dataframe to a .csv file
df.to_csv("Output.csv")

