#GRUIDE: https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f

# import libraries
import urllib.request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import json
import pandas as pd
from bs4 import BeautifulSoup #
import requests #
import re

##GET THE GROUP ID FROM THE TEXTFILE
#@autor Paal kobbeltvedt
#@date 29.11.2019
#@param name of textfile
#Returns a list with each line read from a text file
def getAktorer(filename):
    aktorer = []
    with open(filename) as file:
        for line in file:
            line = line[:-1]
            aktorer.append(line)
    return aktorer

##USE THE GROUP ID TO GET THE EVENT PAGE FOR EACH GROUP
#@autor Paal kobbeltvedt
#@date 29.11.2019
#@param list of facebook groups path name
#Returns a dictionary with the group path name as key, and the href for their event site
##The href seems to be the id + '/events/?ref=page_internal' , so maybe don't need this function
def getEventPage(aktorer):
    samling = {}
    url = "https://www.facebook.com/"
    for aktor in aktorer:
        aktorURL = url + aktor
        webpage = requests.get(aktorURL).content
        soup = BeautifulSoup(webpage, "html.parser")
        lnk = soup.find_all('a')
        for element in lnk:
            event = element.get("href")
            # Henter ut første string med setningen event i seg, pleier å være link til arrangement page
            if "events" in event:
                    if aktor in samling.keys():
                        pass
                    else:
                        samling[aktor] = event
    return samling




##USE THE EVENT PAGE FOR A GROUP TO GET EACH INDIVIDUAL EVENT FOR A GROUP
#@author Paal Kobbeltvedt
#@date 29.11.2019
#Returns a dictionary with the group ID as key, and all event paths as elements in a list
def getEvents(samling):
    events = {}
    url = "https://facebook.com/"
    #Change to headless browser
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(firefox_options=options)
    # key er group id, samling[key] er path til event siden
    for key in samling:
        tempEvent = []
        eventURL = url + samling[key]
        driver.get(eventURL)
        ##Temp sleep because website needs to load
        time.sleep(2)
        results = driver.page_source
        results = str(results)
        ##Get the specific event link
        target = 'href="/events/'
        getEventsRecursive(results, target, tempEvent)
        events[key] = tempEvent

    driver.close()
    return events

def getEventsRecursive(results, target, lst):
    if target in results:
        startIndex = results.find(target)
        endIndex = results[startIndex:].find(">")
        lst.append(results[startIndex:startIndex + endIndex])
        getEventsRecursive(results[startIndex+endIndex:], target, lst)
    else:
        return lst



#Use the dictionary with event paths to get all event information
#@author Paal Kobbeltvedt
#@date 29.11.2019
#@param


def getIndividualEvents(dictionary):
    events = {}
    url = 'https://www.facebook.com/events/'
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(firefox_options=options)
    #DU ER NØDT TIL Å BRUKE REGEX ELNS
    #NÅ ITERERER DU DEN SAMME FILEN 30 GANGER UNDER HER
    for name in dictionary:
        for path in dictionary[name]:
            tempurl = url + path
            driver.get(tempurl)
            #Used time.sleep(2) with browser, do not need it with headless browser
            #time.sleep(2)
            results = driver.page_source
            getDate(results)
            print("******************************************")
            #Target for finding the title
            titleTarget = "<h1 "
            #Target for finding the date
            dateTarget = "<ul "
            if titleTarget in results:
                #Title
                titleIndex = results.find(titleTarget)
                h1 = results[titleIndex:titleIndex+500]
                newTitleTarget = ">"
                #Date
                dateIndex = results.find(dateTarget)
                ul = results[dateIndex:dateIndex + 2000]
                newDateTarget = "content="
                if newTitleTarget in h1:
                    #Title
                    newTitleIndex = h1.find(newTitleTarget)
                    newestTitleTarget = "</h1>"
                    newh1 = h1[newTitleIndex+1:]
                    #Date
                    newDateIndex = ul.find(newDateTarget)
                    newUl = ul[newDateIndex:]
                    newNewDateTarget = ">"
                    if newestTitleTarget in newh1:
                        #Title
                        newNewTitleIndex = newh1.find(newestTitleTarget)
                        finalTitle = newh1[:newNewTitleIndex]
                        print(finalTitle)

                        #Date
                        newNewDateIndex = newUl.find(newNewDateTarget)
                        closeTarget = "<"
                        closeIndex = newUl[newNewDateIndex:].find(closeTarget)
                        finalDate = newUl[newNewDateIndex + 1:newNewDateIndex + closeIndex]
                        print(finalDate)

                        ##GET THE LOCALTION
                        ##GET THE DESCRIPTION
                        description = getDescription(results)
                        print(description)
                        ##DO THIS WITH REGEX OR SOMETHING THAT DOESNT REQUIRE 100 ITERATIONS

    driver.close()


def getTitle(results):
    titleTarget = "<h1 "
    try:
        titleIndex = results.find(titleTarget)
        h1 = results[titleIndex:titleIndex + 500]
        newTitleTarget = "</h1>"
        if newTitleTarget in h1:
            newNewTitleIndex = h1.find(newTitleTarget)
            finalTitle = h1[:newNewTitleIndex]
            cleanTitle = tagCleaner(finalTitle)
            return
    except:
        print("Exeption error line 170")


def getDate(results):
    dateTarget = "<ul "
    try:
        dateIndex = results.find(dateTarget)
        ul = results[dateIndex:dateIndex + 2000]
        print(ul)
    except:
        print("Waring")
        #newDateTarget = "content="
        #newDateIndex = ul.find(newDateTarget)
        #        closeTarget = "<"
        #        closeIndex = newUl[newNewDateIndex:].find(closeTarget)
        #        finalDate = newUl[newNewDateIndex + 1:newNewDateIndex + closeIndex]
        #        print(finalDate)

def getDescription(results):
    desc = results.find("_63ew")
    startIndex = results[desc:].find("<span>")
    startIndex = startIndex + desc
    endIndex = results[desc:].find("</span>")
    endIndex = endIndex + desc
    dirtyDesc = results[startIndex:endIndex]
    cleanDesc = tagCleaner(dirtyDesc)
    return cleanDesc


def tagCleaner(dirtyString):
    cleanString = re.sub('<.*?>', '', dirtyString)
    return cleanString












ids = []
with open('id.txt') as file:
    #data = json.load(json_file)
    for line in file:
        line = line[:-1]
        ids.append(line)

def scraper(url, data):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox()
    for id in data:
        eventURL = url + id
        # get web page
        driver.get(eventURL)
        #sleep for 30s
        #time.sleep(5)
        # RETURNERER source kode med event informasjon!!
        ##Iterer gjennom frem til du finner <div class="_63ew">, for hver <div>, put det i et json objekt?
        results = driver.page_source
        results = str(results)
        target = 'class="_63ew"'
        closePat = "</div>"
        if target in results:
            ##QICKFIX - finner start og sluttindex på arrangement beskrivelse
            startIndex = results.find(target)
            endIndex = results[startIndex:].find(closePat)
            event = results[startIndex:startIndex + endIndex]
            print(event)
            print("YES")
        else:
            print("NOO")

    driver.close()

#def jsonify():


