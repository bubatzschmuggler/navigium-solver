# Navigium Solver
Der Navigium Solver nutzt Navigiums Wörterbuch um den Karteikasten auf Navigium zu lösen. Dadurch bekommt man Punkte, welche jeder in der Schule sehen kann. Das Script ist nicht perfekt, deswegen "schreibt" es im Durchschnitt eine 2-3, jedoch macht es nach jeder "Session" ein Screenshot vom Ergebnis, damit man gucken kann was das Script erreicht hat während man AFK war. Der Navigium Solver nutzt Selenium für alles, bis auf das nachgucken der Wörter. Dafür hat [Anton](https://github.com/xImAnton) vorgeschlagen, einfach die Navigium Wörterbuch "API" zu nutzen. 
Nachdem man sich eingeloggt(Navigium scheint das automatische Einloggen zu erkennen, zumindest in den letzten Testdurchläufen) hat ist das Script komplett selbstständig und man kann es laufen lassen. 

### Wichtig sind außerdem noch folgende Einstellungen: 

```self.page_load_delay = 6```

```self.action_delay = 1```

Die 2 obrigen sollte der Nutzer je nach der Stärke seines Internets einstellen, da diese die Pause angeben, die Selenium macht nachdem es 1. eine Seite geladen hat und 2. eine Aktion ausgeführt hat.

```self.unnecessary_checkboxes = {6, 7, 8, 9, 10, 11}```

Bei den *unnecessary_checkboxes* kann man angeben welche Wortarten das Script NICHT lernen soll. Dadurch bekommt man weniger Punkte (da weniger Vokabeln abgefragt werden), jedoch sinkt dann auch die Fehlerquote, da manche Vokabeln (z.B. Eigennamen) gar nicht im Wörterbuch stehen.

![image](https://user-images.githubusercontent.com/92476790/196914662-d08a1302-97a5-4d6f-a481-5113b48b8cbe.png)

Hier ein Video vom Script im Einsatz:


https://user-images.githubusercontent.com/92476790/196923491-e90cd19c-4d5d-4a76-9843-6a20ad45e11a.mp4

Wie man im Video sieht, kann man das Quiz manuell mitten bei der Abfrage abbrechen bzw. beenden. Das erkennt das Script dann, passt sich an und endet das Script wie sonst auch (Ergebnisse speichern, Screenshot, zurück zum Hauptmenü). Natürlich kann man das Script auch einfach weiter laufen lassen und wenn es dann am Ende ist beendet es sich selber ohne, dass man irgendwas drücken muss.

## Wichtig: Da dieses Script Selenium nutzt wird ein Chrome Driver benötigt der hier gedownloadet werden kann: https://chromedriver.chromium.org/downloads
