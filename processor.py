# -*- coding: utf-8 -*-
import fileinput
import subprocess
import datetime
from HTMLParser import HTMLParser

class RozkladParser(HTMLParser):
  def handle_starttag(self, tag, attrs):
    self.value = ""
    #print "Encountered a start tag:", tag
  def handle_endtag(self, tag):
    #print "Encountered an end tag :", tag
    pass
  def handle_data(self, data):
    #print "Encountered some data  :", data
    self.value += data
  def handle_charref(self, name):
    #print "Encountered some char  :", name, unichr(int(name))
    self.value += unichr(int(name))

class InfopasazerStationSearchParser(HTMLParser):
  def __init__(self, station):
    HTMLParser.__init__(self)
    self.inatag = False
    self.station = station
    self.url = None
    self.attrs = None
  def handle_starttag(self, tag, attrs):
    #self.value = ""
    if tag == 'a':
      self.inatag = True
      self.attrs = attrs
      #print "Encountered a start tag:", tag
  def handle_endtag(self, tag):
    if tag == 'a':
      self.inatag = False
      #print "Encountered an end tag :", tag
  def handle_data(self, data):
    udata = data.decode('utf-8')
    if self.inatag:
     #print "Encountered some data  :", udata.strip(), '<-'
     if udata.strip() == station['name'] or (udata.strip().startswith(station['name']) and self.url is None):
        self.url = self.attrs[0][1]
      #print station['name'], self.url
    #self.value += data

class InfopasazerStationParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.inatag = False
    self.odjazdy = []
    self.przyjazdy = []
    self.current = self.przyjazdy
  def handle_starttag(self, tag, attrs):
    #self.value = ""
    if tag == 'td':
      self.inatag = True
      #print "Encountered a start tag:", tag, attrs
  def handle_endtag(self, tag):
    if tag == 'td':
      self.inatag = False
      #print "Encountered an end tag :", tag
  def handle_data(self, data):
    udata = data.decode('utf-8')
    if self.inatag and ':' in data:
      train = parsetime(udata.strip())
      if train is not None:
        if len(self.current) > 0 and train < self.current[-1]:
          self.current = self.odjazdy
        self.current.append(train)
      #print "Encountered some data  :", parsetime(udata.strip()), '<-'
    #self.value += data

def parsetime(data):
  splitted = data.split(':')
  if len(splitted) != 2:
    return None
  try:
    return datetime.time(int(splitted[0]),int(splitted[1]))
  except ValueError:
    return None


parser = RozkladParser()
data = []
index = 0
for line in fileinput.input():
  if index == 0:
    current = {}
    parser.feed(line)
    current['name'] = parser.value[:-1]
  if index == 3:
    current['arrival'] = parsetime(line[:-1])
  if index == 6:
    current['departure'] = parsetime(line[:-1])
    data.append(current)
  index += 1
  if line == '--\n':
    index = 0

for station in data:
  parser = InfopasazerStationSearchParser(station)
  #print station['name'], station['arrival'], station['departure']
  url = 'http://infopasazer.intercity.pl/index_set.php?stacja='+station['name'].replace(' ', '%20')
  station_search_html = subprocess.check_output(['curl', url])
  parser.feed(station_search_html)
  #print station, station_search_html
  station['url'] = 'http://infopasazer.intercity.pl/'+parser.url
  station_html = subprocess.check_output(['curl', station['url']])
  parser = InfopasazerStationParser()
  parser.feed(station_html)
  station['arrivals'] = parser.przyjazdy
  station['departures'] = parser.odjazdy

for station in data:
  in_a = station['arrival'] in station['arrivals']
  in_d = station['departure'] in station['departures']
  station_id = u"{0}/{1}, {2}".format(station['arrival'], station['departure'], station['name'])
  if (not in_a) and (not in_d):
    print u"{0}: Pociągu nie ma na tablicy.".format(station_id)
  else:
    print u"{0}: Pociąg jest na tablicy: {1} ({2}, {3})".format(station_id, station['url'], in_a, in_d)

#print data
