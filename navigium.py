import sys
import time
import random
import urllib.parse
import requests
import selenium.common.exceptions
import re
import datetime

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 40
VOKABEL_PATTERN = re.compile(r"^([^(,]+).*$")

nicht_gekonnte_vokabeln = []

FREQUENCY = 1000
DURATION = 500
"""
^([^(,]+).*$
- [^(,] = beliebiges Zeichen außer (,
- .* = kann mit vollkommen beliebiger Zeichenkette übereinstimmen
- () = Gruppe
- ^...$ = Anker, ^([^(,]+) Gruppe bezieht sich auf Anfang der Zeichenkette, .*$ beliebige Zeichenkette am Ende
"""


# Hilfsmethoden

def click_correct_button(buttons, loesungen):
    for i in buttons:
        button = i.get_attribute("innerText").strip()
        for j in loesungen:
            if button == j:
                i.click()
                return
    random.choice(buttons).click()


def does_exist(searchItem, key):
    if searchItem.get(key):
        return searchItem[key]
    else:
        return []


def search_vokabel(vokabel, called=False):
    vokabel_raw = ""
    try:
        vokabel_raw = vokabel
        vokabel = VOKABEL_PATTERN.match(vokabel).group(1).strip()
    except AttributeError:
        pass
    r = requests.get(
        f"https://www.navigium.de/suchfunktion/_search?q={urllib.parse.quote(vokabel)}&dkk=DKK_DREI")
    data = r.json()[0]
    loesungen = []

    for searchItem in data["searchItems"]:
        loesungen.extend(does_exist(searchItem, "bedeutungenFlach") +
                         does_exist(searchItem, "schulwortschatz"[0][0]) +
                         does_exist(searchItem, "schulwortschatzFlach")
                         )
    if len(loesungen) == 0 and not called:
        nicht_gekonnte_vokabeln.append(vokabel_raw)
        return search_vokabel(vokabel.split()[0], True)
    return loesungen


def retry(solve_, max_attempts):
    attempts = 0
    while attempts < max_attempts:
        try:
            solve_()
            break
        except selenium.common.exceptions.StaleElementReferenceException:
            attempts += 1


class Main:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--mute-audio")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-crash-reporter")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-in-process-stack-traces")
        self.chrome_options.add_argument("--disable-logging")
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_argument("--output=/dev/null")

        self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

        self.ignore_list = [selenium.common.exceptions.ElementNotVisibleException,
                            selenium.common.exceptions.ElementNotSelectableException]

        # self.unnecessary_checkboxes = {6, 7, 8, 9, 10, 11}
        self.unnecessary_checkboxes = {}

        self.unnecessary_kapitel = {3, 4, 5}

        self.retries = 10

        self.username = "gabhab"
        self.password = "30012008"

    # Selenium

    def find_element_selenium(self, by, name, ec):
        return WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=self.ignore_list).until(
            ec((by, name)))

    def find_elements_selenium(self, by, name):
        return WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=self.ignore_list).until(
            EC.presence_of_all_elements_located((by, name)))

    def load_new_page(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "navigiumlogo")))
        time.sleep(0.5)

    def uncheck_items(self):
        checkboxes = []
        for i in range(11):
            i += 1
            if i in self.unnecessary_checkboxes:
                checkboxes.append(self.find_element_selenium(By.XPATH,
                                                             f"//*[@id=\"content\"]/div/div[2]/div[2]/div[2]/div/div[{i}]/label/input",
                                                             EC.element_to_be_clickable))
        for i in checkboxes:
            i.click()

    def exists(self, by, name):
        try:
            self.driver.find_element(by, name)
        except selenium.common.exceptions.NoSuchElementException:
            return False
        return True

    def click_checkboxes(self, by, class_name):
        for checkbox in self.find_elements_selenium(by,
                                                    class_name):
            try:
                checkbox.click()
            except:
                pass
            time.sleep(1)  # Warten, da Bestätigung aufpoppt

    # Vokabeln lernen

    def noch_zu_lernende_vokabeln(self):
        return int(self.find_element_selenium(By.CLASS_NAME, "col-md-5",
                                              EC.presence_of_element_located).get_attribute(
            "innerText").strip().replace("Noch: ", ""))

    def vokabeln(self, wiederholungen: int):
        def solve():
            if "Was bedeutet diese Vokabel?" in self.find_element_selenium(By.TAG_NAME, "h5",
                                                                           EC.presence_of_element_located).get_attribute(
                "innerText"):
                buttons = self.find_elements_selenium(By.CSS_SELECTOR, ".btn.btn-default.abstandlinks")
                vokabel = self.find_element_selenium(By.XPATH,
                                                     "/html/body/app-root/app-schriftlich/div/div/div[2]/div[1]/div/div/div/h4[1]",
                                                     EC.presence_of_element_located).get_attribute(
                    "innerText").strip()
                loesungen = search_vokabel(vokabel)
                click_correct_button(buttons, loesungen)
                if self.noch_zu_lernende_vokabeln() > 0 or self.noch_zu_lernende_vokabeln() == -1:
                    self.find_element_selenium(By.CSS_SELECTOR,
                                               ".btn.btn-primary.btn-sm.ng-star-inserted",
                                               EC.element_to_be_clickable).click()  # Nächste Vokabel
                else:
                    self.stop(wiederholungen)

        while self.noch_zu_lernende_vokabeln() > 0 or self.noch_zu_lernende_vokabeln() == -1:  # Während mehr als 0 oder -1(Initialisierungswert) Vokabeln zu lernen sind
            try:
                solve()
            except:
                retry(solve, self.retries)
        else:
            self.stop(wiederholungen)

    # Ablauf

    def login(self):
        self.driver.get("https://www.navigium.de/schule/login/mainmenu.html")
        while not WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "password"))):
            pass
        self.find_element_selenium(By.ID, "name", EC.presence_of_element_located).send_keys(self.username)
        self.find_element_selenium(By.ID, "password", EC.presence_of_element_located).send_keys(self.password)
        time.sleep(0.5)
        self.find_element_selenium(By.ID, "submitbutton", EC.element_to_be_clickable).click()
        while not WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "navigiumlogo"))):
            pass

    def start_quiz(self, wiederholungen: int):
        self.load_new_page("https://www.navigium.de/schule/karteikasten")

        self.find_element_selenium(By.ID, "rbMP", EC.element_to_be_clickable).click()

        self.find_element_selenium(By.ID, "cbNicht", EC.element_to_be_clickable).click()

        self.uncheck_items()

        self.find_element_selenium(By.ID, "btnSchr", EC.element_to_be_clickable).click()

        while not "Vokabeltrainer" in self.find_element_selenium(By.TAG_NAME, "h3",
                                                                 EC.presence_of_element_located).get_attribute(
            "innerText"):
            pass
        Thread(target=self.vokabeln, args=[wiederholungen]).start()

    def stop(self, wiederholungen, instant=False):
        wiederholungen -= 1
        self.end_quiz(wiederholungen, instant)

    def end_quiz(self, wiederholungen: int, instant):
        if instant:
            self.exit()
        elif wiederholungen == 0 and not instant:
            print("[Analyse] Nicht gekonnte Vokabeln: ", nicht_gekonnte_vokabeln)
            try:
                self.find_element_selenium(By.CSS_SELECTOR, ".btn.btn-danger-outline.btn-sm.pull-right",
                                           EC.element_to_be_clickable).click()
            except selenium.common.exceptions.NoSuchElementException:
                pass
            self.find_element_selenium(By.CSS_SELECTOR, ".btn.btn-primary.btn-sm.ng-star-inserted",
                                       EC.element_to_be_clickable).click()

            for element in self.find_elements_selenium(By.CLASS_NAME, "ng-star-inserted"):
                if "Note" in element.get_attribute("innerText"):
                    file = open('ergebnisse', 'a')
                    file.write(
                        '[' + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + element.get_attribute(
                            "innerText"))
                    file.close()

            self.find_element_selenium(By.CSS_SELECTOR,
                                       ".btn.btn-primary-outline.btn-sm.hidden-print.ng-star-inserted",
                                       EC.element_to_be_clickable).click()
            self.exit()
        elif wiederholungen > 0 and not instant:
            self.main_vokabeln(wiederholungen)

    def exit(self):
        print('\a')
        print("Wird beendet...")
        self.driver.quit()
        sys.exit(0)

    def main_vokabeln(self, wiederholungen: int, first=False):
        if first:
            self.login()
        try:
            self.start_quiz(wiederholungen)
        except selenium.common.exceptions.ElementClickInterceptedException:
            retry(lambda: self.start_quiz(wiederholungen), self.retries)
        except selenium.common.exceptions.TimeoutException:
            try:
                retry(lambda: self.start_quiz(wiederholungen), self.retries)
            except selenium.common.exceptions.TimeoutException:
                print("Keine Vokabeln zu lernen")
                self.stop(wiederholungen,
                          True)  # Einstellungen funktionieren nicht, da es keine Vokabeln zu lernen gibt

    def main_karteikasten(self, name):
        self.login()

        self.load_new_page("https://www.navigium.de/schule/karteikasten")
        self.find_element_selenium(By.CLASS_NAME, "btn.btn-primary.btn-sm.pull-right.ng-star-inserted",
                                   EC.presence_of_element_located).click()
        self.find_element_selenium(By.ID, "inputWeitererKasten", EC.presence_of_element_located).send_keys(name)
        self.find_element_selenium(By.ID, "btnDoKKanlegen", EC.element_to_be_clickable).click()
        time.sleep(0.5)
        self.find_element_selenium(By.ID, "btnAuffuellen", EC.element_to_be_clickable).click()
        for button in self.find_elements_selenium(By.CLASS_NAME,
                                                  "p-button-label.ng-star-inserted"):  # p-button-label.ng-star-inserted
            button.click()
            if button.get_attribute("innerText") == "Pontes":
                self.click_checkboxes(By.TAG_NAME,
                                      "p-checkbox")  # Alle Pontes Lektionen, ng-untouched.ng-pristine.ng-valid.ng-star-inserted
            elif button.get_attribute("innerText") == "Navigium":
                i = 0
                for kapitel in self.find_elements_selenium(By.CLASS_NAME,
                                                           "p-button.p-component.p-button-icon-only.p-button-text.p-button-rounded.p-button-plain.p-ml-3"):  # p-button p-component p-button-icon-only p-button-text p-button-rounded p-button-plain p-ml-3, p-button-text.p-button-rounded.p-button-plain.p-ml-3 p-button.p-component.p-button-icon-only
                    if i not in self.unnecessary_kapitel:
                        kapitel.click()  # Kapitel aufklappen bzw. laden
                    i += 1
                self.click_checkboxes(By.CLASS_NAME,
                                      "ng-untouched.ng-pristine.ng-valid.ng-star-inserted")  # Alle sichtbaren Checkboxen klicken


def start():
    option = input(r"""\
███╗   ██╗ █████╗ ██╗   ██╗██╗ ██████╗ ██╗██╗   ██╗███╗   ███╗    ███████╗ ██████╗ ██╗    ██╗   ██╗███████╗██████╗ 
████╗  ██║██╔══██╗██║   ██║██║██╔════╝ ██║██║   ██║████╗ ████║    ██╔════╝██╔═══██╗██║    ██║   ██║██╔════╝██╔══██╗
██╔██╗ ██║███████║██║   ██║██║██║  ███╗██║██║   ██║██╔████╔██║    ███████╗██║   ██║██║    ██║   ██║█████╗  ██████╔╝
██║╚██╗██║██╔══██║╚██╗ ██╔╝██║██║   ██║██║██║   ██║██║╚██╔╝██║    ╚════██║██║   ██║██║    ╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║ ╚████║██║  ██║ ╚████╔╝ ██║╚██████╔╝██║╚██████╔╝██║ ╚═╝ ██║    ███████║╚██████╔╝███████╗╚████╔╝ ███████╗██║  ██║
╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝ ╚═╝     ╚═╝    ╚══════╝ ╚═════╝ ╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝
                        =========================================================                    
                        ||         ____        __  _                           ||      
                        ||        / __ \____  / /_(_)___  ____  ___  ____      || 
                        ||       / / / / __ \/ __/ / __ \/ __ \/ _ \/ __ \     ||  
                        ||      / /_/ / /_/ / /_/ / /_/ / / / /  __/ / / /     ||  
                        ||      \____/ .___/\__/_/\____/_/ /_/\___/_/ /_/      ||  
                        ||          /_/                                        ||         
                        ||                                                     ||  
                        ||         1. Aktuellen Karteikasten lernen            ||  
                        ||         2. Neuen Karteikasten anlegen               ||  
                        ||                                                     ||
                        =========================================================
>>> """)
    if option == "1":
        wiederholungen = input(
            "Wie viele Sessions sollen gemacht werden? (Desto mehr Sessions, desto wahrscheinlicher werden Fehler!)\n")
        main = Main()
        main.main_vokabeln(int(wiederholungen), True)
    else:
        name = input("Wie soll der neue Karteikasten heißen?\n")
        main = Main()
        main.main_karteikasten(name)


if __name__ == '__main__':
    try:
        start()
    except selenium.common.exceptions.NoSuchWindowException:
        exit(0)
