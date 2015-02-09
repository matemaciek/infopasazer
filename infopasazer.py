# -*- coding: utf-8 -*-
import fileinput
import subprocess
import datetime
import os
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
    self.train = None
  def handle_starttag(self, tag, attrs):
    if tag == 'td':
      self.inatag = True
  def handle_endtag(self, tag):
    if tag == 'td':
      self.inatag = False
  def handle_data(self, data):
    udata = data.decode('utf-8')
    if self.inatag and 'min' in data:
      if self.train is not None:
        if len(self.current) > 0 and self.train < self.current[-1][0]:
          self.current = self.odjazdy
        self.current.append((self.train,udata))
    if self.inatag and ':' in data:
      self.train = parsetime(udata.strip())

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

FNULL = open(os.devnull, 'w')

for station in data:
  parser = InfopasazerStationSearchParser(station)
  url = 'http://infopasazer.intercity.pl/index_set.php?stacja='+station['name'].replace(' ', '%20')
  station_search_html = subprocess.check_output(['curl', url], stderr=FNULL)
  parser.feed(station_search_html)
  station_id = u"{0}/{1}, {2}".format(station['arrival'], station['departure'], station['name'])
  if parser.url is not None:
    station['url'] = 'http://infopasazer.intercity.pl/'+parser.url
    station_html = subprocess.check_output(['curl', station['url']], stderr=FNULL)
    parser = InfopasazerStationParser()
    parser.feed(station_html)
    przyjazd = [b for (a, b) in parser.przyjazdy if a == station['arrival']]
    odjazd = [b for (a, b) in parser.odjazdy if a == station['departure']]
    op_przyj = przyjazd[0] if len(przyjazd) > 0 else None
    op_odj = odjazd[0] if len(odjazd) > 0 else None
    if (op_przyj is None) and (op_odj is None):
      print u"{0}: Pociągu nie ma na tablicy.".format(station_id)
    else:
      print u"{0} ({2}/{3}): Pociąg jest na tablicy: {1}".format(station_id, station['url'], op_przyj, op_odj)
  else:
    print u"{0}: Nie znaleziono tablicy.".format(station_id)
