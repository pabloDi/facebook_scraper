from scraper import *



##Get aktører from .txt file, returns a list
aktor = getAktorer("aktor.txt")
print("finished getAktorer()")
##Gets the href path for an aktors event page, the page contains all the events
eventPage = getEventPage(aktor)
print("finished getEventPage()")
##Gets the event paths for all events, returns a dictionary with group id as key, and event paths as elements in a list
dictWithEventPaths = getEvents(eventPage)
print("finished getEvents()")
##
getIndividualEvents(dictWithEventPaths)
print("finished GetIndividualEvents")