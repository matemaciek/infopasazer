# infopasazer
Prosty skrypt do wyszukiwania pociągów na infopasazer.intercity.pl

*Disclaimer: Pisany na szybko i na kolanie, brzydki, a miejscami bardzo brzydki. Ale działa. Czasem. Przeważnie. Zazwyczaj. Zadziałał kilka razy. SOA#1*

Intercity ma taką jedną stronę: http://infopasazer.intercity.pl/ . Fajną. Pozwala śledzić na bieżaco, gdzie jest pociąg, którego szukamy. Jest tylko pewien problem: dla każdej stacji wyświetlane jest po kilkanaście najbliższych odjazdów. Albo i dwadzieścia kilka. Nie wiem, nie liczyłem. Więc gdy pociąg chcemy znaleźć odpowiednio wcześniej, to trzeba go szukać na małych stacjach. I można go się sporo naszukać. Ale po co szukać, gdy można napisać skrypt.

HOWTO:

* na http://rozklad-pkp.pl/ znajdujemy interesujący nas pociąg, kopiujemy do niego url, może wyglądać np. tak: http://rozklad-pkp.pl/pl/ti?trainlink=2151/173411/665730/332148/55 (plus trochę śmieci dalej, okazuje się, że można je uciąć, a link dalej działa. Można nie ucinać, nic nie szkodzi, ale wygląda brzydziej.)
* odpalamy skrypt: `python infopasazer.py "http://rozklad-pkp.pl/pl/ti?trainlink=2151/173411/665730/332148/55"`
* skrypt powinien wypisać coś w rodzaju:
```
None/11:36:00, Szczecin Główny: Pociągu nie ma na tablicy.
11:49:00/11:50:00, Szczecin Dąbie: Pociągu nie ma na tablicy.
12:07:00/12:08:00, Stargard Szczeciński: Pociągu nie ma na tablicy.
12:28:00/12:29:00, Choszczno: Pociągu nie ma na tablicy.
12:48:00/12:49:00, Dobiegniew: Pociągu nie ma na tablicy.
13:06:00/13:08:00, Krzyż: Pociągu nie ma na tablicy.
13:35:00/13:36:00, Wronki: Pociągu nie ma na tablicy.
13:49:00/13:50:00, Szamotuły: Pociągu nie ma na tablicy.
14:18:00/14:28:00, Poznań Główny: Pociągu nie ma na tablicy.
14:59:00/15:00:00, Września: Pociągu nie ma na tablicy.
15:14:00/15:15:00, Słupca: Pociągu nie ma na tablicy.
15:32:00/15:33:00, Konin: Pociągu nie ma na tablicy.
15:49:00/15:50:00, Koło: Pociągu nie ma na tablicy.
16:19:00/16:21:00, Kutno: Pociąg jest na tablicy: http://infopasazer.intercity.pl/index3.php?nr_sta=32201 (False, True)
16:47:00/16:48:00, Łowicz Główny: Pociąg jest na tablicy: http://infopasazer.intercity.pl/index3.php?nr_sta=32904 (True, True)
17:03:00/17:05:00, Sochaczew: Pociąg jest na tablicy: http://infopasazer.intercity.pl/index3.php?nr_sta=34603 (True, True)
17:35:00/17:41:00, Warszawa Zachodnia: Pociągu nie ma na tablicy.
17:46:00/17:50:00, Warszawa Centralna: Pociągu nie ma na tablicy.
17:57:00/17:59:00, Warszawa Wschodnia: Pociągu nie ma na tablicy.
18:41:00/18:42:00, Pilawa: Pociąg jest na tablicy: http://infopasazer.intercity.pl/index3.php?nr_sta=39206 (True, True)
19:13:00/19:14:00, Dęblin: Pociąg jest na tablicy: http://infopasazer.intercity.pl/index3.php?nr_sta=49809 (True, True)
19:29:00/19:31:00, Puławy Miasto: Pociąg jest na tablicy: http://infopasazer.intercity.pl/index3.php?nr_sta=50021 (True, True)
19:45:00/19:46:00, Nałęczów: Pociąg jest na tablicy: http://infopasazer.intercity.pl/index3.php?nr_sta=50104 (True, True)
20:04:00/None, Lublin: Pociąg jest na tablicy: http://infopasazer.intercity.pl/index3.php?nr_sta=50500 (True, False)
```

Jak coś nie działa, daj znać, może spróbuję naprawić. Nie lubię, gdy moje programy nie działają.
