# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 11:20:16 2022

@author: luisf
"""

from bs4 import BeautifulSoup
import requests
import numpy as np

typesWithStats  = ['Creature', 'Legendary Creature', 'Snow Creature', 'Artifact Creature', 'Legendary Artifact Creature', 'Enchantment Creature', 'Legendary Enchantment Creature', 'Legendary Planeswalker']
typesWithoutCMC = ['Land', 'Basic Land', 'Legendary Land', 'Snow Land', 'Basic Snow Land', 'Artifact Land']

# =============================================================================
# Function to call gather info of the cards from the set taken from the webpage
# =============================================================================
def getCardInfo(soup):
    name = ''
    efect = ''
    CMC = ''
    primarytype = ''
    subtype = ''
    stats = ''
    amorcito = ''
    name   = soup.findAll('span',class_='card-text-card-name')[0].text.strip() #name
    efect = soup.findAll('div',class_="card-text-oracle")     #effect
    if(len(efect)>0):
        efect=efect[0].text.strip()
    else:
        efect=''
    CMC = soup.findAll('span',class_='card-text-mana-cost')
    if(len(CMC)>0):
        CMC = CMC[0].text.strip() #CMC
    else:
        CMC = '0'
    stats = soup.findAll('div',class_="card-text-stats")
    if(len(stats)>0):
        stats = stats[0].text.strip()
    else:
        stats = ''
    type = soup.findAll('p',class_="card-text-type-line")[0].text.strip().split(' — ')
    primarytype = type[0]
    if((primarytype in typesWithStats) and (len(type)>1)):
        subtype = type[1]

    return name, efect, CMC, primarytype, subtype, stats
# =============================================================================
# This function runs through the set webpage and separetes the URL of each card in the set
# this URLs are stored in an array and will be used to gather info for each card.
# =============================================================================
def getCardsURL(url):
    SetPage = requests.get(url)
    SetPageHTML = SetPage.content
    SetSoup = BeautifulSoup(SetPageHTML, "html.parser")
    SetName = SetSoup.findAll('h1',class_='set-header-title-h1')[0].text.strip() 
    CardsURL = []
    
    for a in SetSoup.find_all('a',class_='card-grid-item-card', href=True):
        CardsURL.append(a['href'])
    return SetName, CardsURL
# =============================================================================
# 
# =============================================================================
def saveData(CardsURL,SetName,filepath):
    filename = ((filepath + SetName + "_Cards_Info.txt"))
    print("Criando o arquivo: ", filename)
    file = open((filename), "w", encoding="utf-8")
    file.write('name, CMC, primarytype, subtype,stats, efect\n')
    for i in range(len(CardsURL)):
        CardPage = requests.get(CardsURL[i])
        html = CardPage.content
        soup = BeautifulSoup(html, "html.parser")
        name, efect, CMC, primarytype, subtype,stats = getCardInfo(soup)
        file.write(name + ' | ' + CMC + ' | ' + primarytype + ' | ' + subtype + ' | ' + stats + ' | ' + efect + '\n')
    
    file.close()

# =============================================================================
#  Main part of the code
# =============================================================================
specialChars = ":'<>" #used to allow the creation of files in a windows OS
SiteURL = 'https://scryfall.com/sets'
filepath = r'C:\Users\luisf\Documents\python\files'
reqs = requests.get(SiteURL)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
SetsURL = []
for link in soup.find_all('a'):
    var = link.get('href')
    if(bool(var)):      
        if('https://scryfall.com/sets/' in link.get('href')):
            SetsURL.append(link.get('href'))

SetsURL=np.unique(SetsURL)
# =============================================================================
for i in range(len(SetsURL)):
    SetName, CardsURL = getCardsURL(SetsURL[i])
    for specialChar in specialChars:
        SetName = SetName.replace(specialChar, '_')
        SetName = SetName.replace(" ","_")
    saveData(CardsURL,SetName,filepath)



