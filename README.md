# Navigium Solver
Der Navigium Solver nutzt Navigiums Wörterbuch um den Karteikasten auf Navigium zu lösen. Dadurch bekommt man Punkte, welche jeder in der Schule sehen kann. Das Script ist nicht perfekt, deswegen "schreibt" es im Durchschnitt eine 2-3, jedoch macht es nach jeder "Session" ein Screenshot vom Ergebnis, damit man gucken kann was das Script erreicht hat während man AFK war. Hat man vor, länger AFK zu bleiben, kann man das Script auch mehrere "Sessions" laufen lassen. So fragt dich das Script am Anfang, wieviel "Sessions" es machen soll. Unter einer "Session" wird eine Abfrage verstanden. Der Navigium Solver nutzt Selenium für alles, bis auf das nachgucken der Wörter. Dafür hat [Anton](https://github.com/xImAnton) vorgeschlagen, einfach die Navigium Wörterbuch "API" zu nutzen. 
Nachdem man sich eingeloggt(Navigium scheint das automatische Einloggen zu erkennen, zumindest in den letzten Testdurchläufen) hat ist das Script komplett selbstständig und man kann es laufen lassen. 

### Wichtig ist außerdem noch folgende Einstellung: 

```self.unnecessary_checkboxes = {6, 7, 8, 9, 10, 11}```

Bei den *unnecessary_checkboxes* kann man angeben welche Wortarten das Script NICHT lernen soll. Dadurch bekommt man weniger Punkte (da weniger Vokabeln abgefragt werden), jedoch sinkt dann auch die Fehlerquote, da manche Vokabeln (z.B. Eigennamen) gar nicht im Wörterbuch stehen.

![image](https://user-images.githubusercontent.com/92476790/196914662-d08a1302-97a5-4d6f-a481-5113b48b8cbe.png)

Hier ein Video vom Script im Einsatz:



Wie man im Video sieht, kann man das Quiz manuell mitten bei der Abfrage abbrechen bzw. beenden. Das erkennt das Script dann, passt sich an und endet das Script wie sonst auch (Ergebnisse speichern, Screenshot, zurück zum Hauptmenü). Natürlich kann man das Script auch einfach weiter laufen lassen und wenn es dann am Ende ist beendet es sich selber ohne, dass man irgendwas drücken muss.

## Wichtig: Da dieses Script Selenium nutzt wird ein Chrome Driver benötigt der hier gedownloadet werden kann: https://chromedriver.chromium.org/downloads
