# -*- coding: utf-8 -*-
import fileinput
import subprocess
import datetime
import sys
from HTMLParser import HTMLParser

class RozkladParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.data = []
    self.level = 0
    self.current = None
  def handle_starttag(self, tag, attrs):
    if tag == 'tr':
      self.level = 1
      self.col = -1
    if self.level == 1 and tag == 'td':
      self.level = 2
      self.col +=1
      self.value2 = ""
    if self.level == 2 and tag == 'a':
      self.level = 3
      self.value3 = ""
    #if self.level > 0:
    #  print "Entered level", self.level
  def handle_endtag(self, tag):
    if self.level == 3 and tag == 'a':
      self.current = {'name': self.value3}
      self.level = 2
    if self.level == 2 and tag == 'td':
      if self.current is not None:
        if self.col == 2:
          self.current['arrival'] = parsetime(self.value2)
        if self.col == 3:
          self.current['departure'] = parsetime(self.value2)
      self.level = 1
    if self.level == 1 and tag == 'tr':
      if self.current is not None:
        self.data.append(self.current)
        self.current = None
      self.level = 0

  def handle_data(self, data):
    if self.level == 3:
      self.value3 += data
    if self.level == 2:
      self.value2 += data
      #print "Encountered some data  :", data
  def handle_charref(self, name):
    if self.level == 3:
      #print "Encountered some char  :", name, unichr(int(name))
      self.value3 += unichr(int(name))

class InfopasazerStationSearchParser(HTMLParser):
  def __init__(self, station):
    HTMLParser.__init__(self)
    self.inatag = False
    self.station = station
    self.url = None
    self.attrs = None
  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      self.inatag = True
      self.attrs = attrs
  def handle_endtag(self, tag):
    if tag == 'a':
      self.inatag = False
  def handle_data(self, data):
    udata = data.decode('utf-8')
    if self.inatag:
     if udata.strip() == station['name'] or (udata.strip().startswith(station['name']) and self.url is None):
        self.url = self.attrs[0][1]

class InfopasazerStationParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.inatag = False
    self.odjazdy = []
    self.przyjazdy = []
    self.current = self.przyjazdy
  def handle_starttag(self, tag, attrs):
    if tag == 'td':
      self.inatag = True
  def handle_endtag(self, tag):
    if tag == 'td':
      self.inatag = False
  def handle_data(self, data):
    udata = data.decode('utf-8')
    if self.inatag and ':' in data:
      train = parsetime(udata.strip())
      if train is not None:
        if len(self.current) > 0 and train < self.current[-1]:
          self.current = self.odjazdy
        self.current.append(train)

def parsetime(data):
  splitted = data.strip().split(':')
  if len(splitted) != 2:
    return None
  try:
    return datetime.time(int(splitted[0]),int(splitted[1]))
  except ValueError:
    return None

parser = RozkladParser()
url = sys.argv[1]
rozklad_html = subprocess.check_output(['curl', url])
parser.feed(rozklad_html)

data = parser.data

for station in data:
  parser = InfopasazerStationSearchParser(station)
  url = 'http://infopasazer.intercity.pl/index_set.php?stacja='+station['name'].replace(' ', '%20')
  station_search_html = subprocess.check_output(['curl', url])
  parser.feed(station_search_html)
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
