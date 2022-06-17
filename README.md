# ttSchweizer
Tischtennis Turnier Software im Schweizer System

## Informationen zum Spielsystem

Das "Schweizer System" ähnelt dem System "jeder gegen jeden", wobei einerseits nicht alle Runden ausgetragen werden und andererseits im Turnierverlauf vor allem Spielerinnen/Spieler ähnlicher Spielstärke gegeneinander spielen.
Durch die feste Rundenanzahl ist der Zeitrahmen eines Turniers sehr gut planbar.
... siehe http://www.bttv.de/sport/commerzbank-sports-more-bavarian-tt-race/infos-spielsystem/

## User Interface von **ttSchweizer**

* Konsolenbasiert
* Robust, stabil
* Eingaben werden mit einfachem Texteditor gemacht
* **ttSchweizer** wird in Verzeichnis mit verschiedenen Textfiles aufgerufen
* **ttSchweizer** kann zu jedem Zeitpunkt ausgeführt werden
* Für jede Runde gibt es ein Textfile: *runde1.tts*, *runde2.tts*, ...
* Ist *rundeN.tts* vollständig erfasst, wird *rundeN+1.tts* erzeugt
* *spieler.tts* enthält Spieler mit ihren TTR Werten
* Fehlt *spieler.tts* und befindet sich im Verzeichnis ein Spieler Export aus click-tt, wird daraus *spieler.tts* erzeugt.
* *runde1.tts* wird durch Losen aus *spieler.tts* erzeugt
* *ergebnis.html* wird nach jedem Aufruf aktualisiert

## Packet Abhängigkeitet

* sudo pip3 install flask
* sudo pip3 install flask-login
* sudo pip3 install Flask-SQLAlchemy
* sudo aptitude install python3-lxml libxml2-utils

Für Begleitzettel
* sudo aptitude install libffi-dev
* sudo aptitude install libxml2-dev libxslt-dev libpango1.0-0 libcairo2
* sudo pip3 install WeasyPrint
* sudo pip3 install Flask-WeasyPrint

## Docker

* docker build -t tt-schweizer:latest .
* # Mac needs --network bridge 
* docker run -l -d --network bridge -p 6000:5000 tt-schweizer
* To persist: docker run -l -d -v Data:/app/Data -u root -p 5000:5000 tt-schweizer
* Mac:
* sudo podman run --name=tt -l -d -v /Users/thomas/Git/ttSchweizer/Data:/app/Data -u root --network bridge -p 6000:5000 tt-schweizer
* podman stop tt; podman rm tt
  

## Hints

* spieler.tts nach TTR sortieren: `sort -nr --field-separator=, --key=2 spieler.tts`
