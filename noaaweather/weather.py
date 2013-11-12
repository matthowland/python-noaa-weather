__author__ = 'matthew howland'
from bs4 import BeautifulSoup
#from datetime import datetime
import unicodedata
import urllib2
import iso8601
import datetime
import copy
from decimal import *
class noaa(object):
    unitType = 'e'
    startTime = ''
    endTime = ''
    product = 'time-series'
    latitude = ''
    longitude = ''
    zipcodeList = None
    zipcode = ''
    soup = None
    timeSeries = {}
    subWeatherElements = {}

    def __getattr__(self, item):
        return self.subWeatherElements[item]

    def getByZip(self, zipcode):
       baseurl = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?'
       self.zipcode = zipcode
       if self.zipcodeList != None:
           self.zipcode = '+'.join(self.zipcodeList)
       requestURL = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?zipCodeList={0}&product={1}&begin={2}&end={3}&Unit={4}'.format(self.zipcode,self.product, self.startTime, self.endTime, self.unitType)
       self.fetchByURL(requestURL)

    def getByLatLong(self, lat, long):
       self.latitude =lat
       self.longitude = long
       requestURL = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?lat={0}&lon={1}product={2}&begin={3}&end={4}&Unit={5}'.format(self.latitude,self.longitude,self.product, self.startTime, self.endTime, self.unitType)

       self.fetchByURL(requestURL)

    def fetchByURL(self, strURL):
       page=urllib2.urlopen(strURL)
       self.soup = BeautifulSoup(page.read())
       self.buildTimeSeries()
       #self.buildTemps()
       self.buildElements('temperature', {'temperature'})
       self.buildElements('precipitation', {'precipitation', 'probability-of-precipitation'})
       self.buildElements('wind', {'wind-speed', 'direction'})
       self.buildElements('severe-component', {'severe-component'})
       self.buildElements('cloud-amount', {'cloud-amount'})
       self.buildElements('humidity', {'humidity'})
       #w.soup.data.findAll("time-layout")

    def buildTimeSeries(self):
        ts = self.soup.data.findAll("time-layout")
        for t in ts:
            tn = t.findAll('layout-key')
            tag = tn[0].string
            self.timeSeries[tag] = []
            for ti in t.findAll('start-valid-time'):
                self.timeSeries[tag].extend([iso8601.parse_date(ti.text)])


    def buildElements(self, dataName, arrayDataNames):
        rootDataName = dataName.replace('-', '_')
        self.subWeatherElements[rootDataName] = weatherHolder()
        self.subWeatherElements[rootDataName].displayName = dataName
        for strDataName in arrayDataNames:
            rootElement = self.subWeatherElements[rootDataName]

            if rootDataName != strDataName:
                fixedDataName = strDataName.replace('-', '_')
                self.subWeatherElements[rootDataName].subWeatherElements[fixedDataName] = weatherHolder()
                self.subWeatherElements[rootDataName].subWeatherElements[fixedDataName].displayName = strDataName
                rootElement = self.subWeatherElements[rootDataName].subWeatherElements[fixedDataName]

            temps = self.soup.parameters.findAll(strDataName)
            #print 'Creating ' + rootElement.displayName
            for t in temps:
                timestring = t['time-layout'].encode('ascii','ignore')
                typestring = t['type'].encode('ascii','ignore').replace(' ', '_')
                units = t['units'].encode('ascii','ignore')
                displayname =  t.findAll('name')[0].string
                rootElement.subWeatherElements[typestring] = weatherHolder()
                rootElement.subWeatherElements[typestring].displayName = displayname
                rootElement.subWeatherElements[typestring].unit = units
                rootElement.subWeatherElements[typestring].weatherValues = []
                curTimeSeries = self.timeSeries[timestring]

                for v in t.findAll("value"):
                    timeval = timeValuePoint(curTimeSeries[len(rootElement.subWeatherElements[typestring].weatherValues)], v.string)
                    rootElement.subWeatherElements[typestring].weatherValues.insert(len(rootElement.subWeatherElements[typestring].weatherValues),timeval)





class weatherHolder(object):

    subWeatherElements = {}
    displayName = ''
    dictName = ''
    weatherValues = None
    unit = ''
    def __getattr__(self, item):

        return self.subWeatherElements[item]

    @property
    def today(self):
        returnObj = self.daysFromNow(0)
        return returnObj
    @property
    def tomorrow(self):
        returnObj = self.daysFromNow(1)
        return returnObj

    def daysFromNow(self, intDaysForward):
        returnObj = weatherHolder()
        returnObj.displayName = self.displayName
        returnObj.dictName = self.dictName
        returnObj.unit = self.unit
        returnObj.weatherValues = []
        tomorrowsDate = datetime.datetime.today() + datetime.timedelta(days=intDaysForward)

        for weatherItem in self.weatherValues:
            if weatherItem.date.date() == tomorrowsDate.date():
                returnObj.weatherValues.insert(len(returnObj.weatherValues),weatherItem)
        return returnObj


    def now(self):
        return ''
    @property
    def value(self):
        return self.weatherValues[0].value

    @property
    def max(self):
        maxvalue = -9999999
        retValue = None
        for weatherItem in self.weatherValues:
            if weatherItem.value > maxvalue:
                maxvalue = weatherItem.value
                retValue = weatherItem

        return retValue
    @property
    def min(self):
        minvalue = 9999999
        retValue = None
        for weatherItem in self.weatherValues:
            if weatherItem.value < minvalue:
                minvalue = weatherItem.value
                retValue = weatherItem

        return retValue
    @property
    def average(self):
        valueSamples = 0
        for weatherItem in self.weatherValues:
            valueSamples += weatherItem.value

        return valueSamples/len(self.weatherValues)

class timeValuePoint(object):
    date = None
    value = None
    text = None
    def __init__(self, startT, uValue):
        self.date = startT
        if uValue is None:
            self.value = 0
        else:
            try:
                self.value = Decimal(uValue)
            except:
                self.text = uValue


class timeSeries(object):
    startTime = None
    endTime = None
    def __init__(self, start, end):
        self.startTime = iso8601.parse_date(start)
        self.endTime = iso8601.parse_date(end)


