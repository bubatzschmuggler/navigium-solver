import sys
import time
import random
import urllib.parse
import requests

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread


def click_correct_button(buttons, loesungen):
    for i in buttons:
        button = i.get_attribute("innerText").strip()
        for j in loesungen:
            if button == j:
                i.click()
                return
    random.choice(buttons).click()


def search_vokabel(vokabel):
    r = requests.get(
        f"https://www.navigium.de/suchfunktion/_search?q={urllib.parse.quote(vokabel.split()[0])}&dkk=DKK_DREI")
    try:
        return r.json()[0]["searchItems"][0]["bedeutungenFlach"]
    except:
        return ""


class Main:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--mute-audio")

        self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

        self.page_load_delay = 6
        self.action_delay = 1

        self.unnecessary_checkboxes = {6, 7, 8, 9, 10, 11}

    def find_element_selenium(self, by, name, delay):
        time.sleep(delay)
        return self.driver.find_element(by, name)

    def load_new_page(self, url):
        self.driver.get(url)
        time.sleep(self.page_load_delay)

    def uncheck_items(self):
        checkboxes = []
        for i in range(11):
            i += 1
            if i in self.unnecessary_checkboxes:
                checkboxes.append(self.find_element_selenium(By.XPATH,
                                                             f"//*[@id=\"content\"]/div/div[2]/div[2]/div[2]/div/div[{i}]/label/input",
                                                             0))
        for i in checkboxes:
            i.click()

    def exit(self):
        time.sleep(1)
        self.driver.quit()
        sys.exit(0)

    def end_quiz(self):
        self.find_element_selenium(By.CSS_SELECTOR, ".btn.btn-danger-outline.btn-sm.pull-right", 1).click()
        self.find_element_selenium(By.CSS_SELECTOR, ".btn.btn-primary.btn-sm.ng-star-inserted", 2.5).click()
        self.driver.save_screenshot("result.png")
        self.find_element_selenium(By.CSS_SELECTOR, ".btn.btn-primary-outline.btn-sm.hidden-print.ng-star-inserted",
                                   2.5).click()
        self.exit()

    def vokabeln(self):
        time.sleep(6)
        while True:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn.btn-default.abstandlinks")
            if len(buttons) > 0:
                try:
                    vokabel = self.find_element_selenium(By.XPATH,
                                                         "/html/body/app-root/app-schriftlich/div/div/div[2]/div[1]/div/div/div/h4[1]",
                                                         1).get_attribute("innerText").strip()
                    loesungen = search_vokabel(vokabel)

                    click_correct_button(buttons, loesungen)

                    time.sleep(2.5)
                    self.find_element_selenium(By.CSS_SELECTOR, ".btn.btn-primary.btn-sm.ng-star-inserted", 2).click()
                except:
                    self.end_quiz()

    def main(self):
        self.load_new_page("https://www.navigium.de/schule/login/mainmenu.html")

        print("Bitte einloggen...")
        while True:
            try:
                self.find_element_selenium(By.CLASS_NAME, "iconblue", 0)
                self.load_new_page("https://www.navigium.de/schule/karteikasten")
                break
            except:
                pass

        self.find_element_selenium(By.ID, "rbMP", self.action_delay).click()

        self.find_element_selenium(By.ID, "cbNicht", self.action_delay).click()

        self.uncheck_items()

        self.find_element_selenium(By.ID, "btnSchr", self.action_delay).click()

        Thread(target=self.vokabeln).start()


def start():
    print("""\
███╗   ██╗ █████╗ ██╗   ██╗██╗ ██████╗ ██╗██╗   ██╗███╗   ███╗    ███████╗ ██████╗ ██╗    ██╗   ██╗███████╗██████╗ 
████╗  ██║██╔══██╗██║   ██║██║██╔════╝ ██║██║   ██║████╗ ████║    ██╔════╝██╔═══██╗██║    ██║   ██║██╔════╝██╔══██╗
██╔██╗ ██║███████║██║   ██║██║██║  ███╗██║██║   ██║██╔████╔██║    ███████╗██║   ██║██║    ██║   ██║█████╗  ██████╔╝
██║╚██╗██║██╔══██║╚██╗ ██╔╝██║██║   ██║██║██║   ██║██║╚██╔╝██║    ╚════██║██║   ██║██║    ╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║ ╚████║██║  ██║ ╚████╔╝ ██║╚██████╔╝██║╚██████╔╝██║ ╚═╝ ██║    ███████║╚██████╔╝███████╗╚████╔╝ ███████╗██║  ██║
╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝ ╚═╝     ╚═╝    ╚══════╝ ╚═════╝ ╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝                                                                                                                                                       
    """)
    main = Main()
    main.main()


if __name__ == '__main__':
    start()
