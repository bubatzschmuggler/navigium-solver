# Navigium Solver
Der Navigium Solver nutzt Navigiums Wörterbuch um den Karteikasten auf Navigium zu lösen. Dadurch bekommt man Punkte, welche jeder in der Schule sehen kann. Das Script ist nicht perfekt, deswegen "schreibt" es im Durchschnitt eine 2-3, jedoch macht es nach jeder "Session" ein Screenshot vom Ergebnis, damit man gucken kann was das Script erreicht hat während man AFK war. Hat man vor, länger AFK zu bleiben, kann man das Script auch mehrere "Sessions" laufen lassen. So fragt dich das Script am Anfang, wieviel "Sessions" es machen soll. Unter einer "Session" wird eine Abfrage verstanden. Der Navigium Solver nutzt Selenium für alles, bis auf das nachgucken der Wörter. Dafür hat [Anton](https://github.com/xImAnton) vorgeschlagen, einfach die Navigium Wörterbuch "API" zu nutzen. 
Nachdem man sich eingeloggt(Navigium scheint das automatische Einloggen zu erkennen, zumindest in den letzten Testdurchläufen) hat ist das Script komplett selbstständig und man kann es laufen lassen. Außerdem gibt es nach einem Update eine neue UI und das Programm kann automatisch einen Karteikasten erstellen. Das erstellen des Karteikastens dauert noch, jedoch werde ich auch versuchen, die Geschwindigkeit zu verbessern. Das automatische Erstellen vom Karteikasten wurde gemacht, um Karteikästen zum Farmen zu erstellen.

### Wichtig sind außerdem noch folgende Einstellungen: 

```self.unnecessary_checkboxes = {6, 7, 8, 9, 10, 11}```

```self.unnecessary_kapitel = {3, 4, 5}```

Bei den *unnecessary_checkboxes* kann man angeben welche Wortarten das Script NICHT lernen soll. Dadurch bekommt man weniger Punkte (da weniger Vokabeln abgefragt werden), jedoch sinkt dann auch die Fehlerquote, da manche Vokabeln (z.B. Eigennamen) gar nicht im Wörterbuch stehen.
Die *unnecessary_kapitel* geben an, welche Kapitel beim Auffüllen vom Karteikasten unter dem Navigium Tab weggelassen werden sollen.

![image](https://user-images.githubusercontent.com/92476790/196914662-d08a1302-97a5-4d6f-a481-5113b48b8cbe.png)

Hier ein Video vom Script im Einsatz:

https://user-images.githubusercontent.com/92476790/200125029-d70c3d6c-d98e-46e4-be4f-88e855e27683.mp4

Mit der neuen "UI" sieht das Script nun wie folgt aus:

![new_ui](https://user-images.githubusercontent.com/92476790/205127123-edc50c9b-f020-4a63-a808-fed87b280208.PNG)

Wie man im Video sieht, wird das Quiz eigenständig gelöst. Die Fehler entstehen, wenn die Vokabel im Wörterbuch nicht gefunden werden kann. Dieser Fehler kann eigentlich sehr einfach behoben werden indem man die Vokabel durch jedes Pattern jagt, welche die Vokabel auf verschiedene Weisen isolieren. Dann versucht man eine API Request mit jeder extrahierten Vokabel und eines wird eine richtige Lösung zurückgeben. Da man sich dafür jedoch mit Latein Vokabeln und Regex auskennen muss wurde hier nur ein Pattern erstellt. Falls du dich jedoch mit Regex und Latein Vokabeln auskennen solltest kannst du die "search_vokabel"-Funktion um mehrere Patterns erweitern um jedesmal eine erfolgreiche Antwort von der API zu bekommen.

## Wichtig: Da dieses Script Selenium nutzt wird ein Chrome Driver benötigt der hier gedownloadet werden kann: https://chromedriver.chromium.org/downloads
