from data import *
from functions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time


class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=service, options=options)
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    # ------------------------------------------------------------------------------------------------------------------
    # ATC01 - Adatkezelési tájékoztató decline, accept
    def test_cookies(self):
        self.browser.find_element(By.XPATH, "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--decline']").click()
        assert self.browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")["value"] == "decline"
        self.browser.delete_cookie("vue-cookie-accept-decline-cookie-policy-panel")
        self.browser.refresh()
        time.sleep(varj)
        self.browser.find_element(By.XPATH, "//button[@class= 'cookie__bar__buttons__button cookie__bar__buttons__button--accept']").click()
        assert self.browser.get_cookie("vue-cookie-accept-decline-cookie-policy-panel")["value"] == "accept"

    # ------------------------------------------------------------------------------------------------------------------
    # ATC02 - Regisztráció sikeresen
    def test_regRight(self):
        self.browser.find_element(By.LINK_TEXT, 'Sign up').click()
        self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]').send_keys(regUserDict["userRight"]["name"])
        self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]').send_keys(regUserDict["userRight"]["email"])
        self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys(regUserDict["userRight"]["password"])
        self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]'))).click()
        assert WebDriverWait(self.browser, varj2).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[2].text == regUserDict["userRight"]["name"]

    # ------------------------------------------------------------------------------------------------------------------
    # ATC03 - Regisztráció üres mezőkkel
    def test_regEmpty(self):
        self.browser.find_element(By.LINK_TEXT, 'Sign up').click()
        self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
        time.sleep(varj)
        assert self.browser.find_element(By.XPATH, '//div[@class="swal-text"]').text == "Username field required."

    # ------------------------------------------------------------------------------------------------------------------
    # ATC04 - Regisztráció helytelen email címmel
    def test_regBadEmail(self):
        self.browser.find_element(By.LINK_TEXT, 'Sign up').click()
        self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]').clear()
        self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]').send_keys(regUserDict["userBad"]["name"])
        self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]').clear()
        self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]').send_keys(regUserDict["userBad"]["email"])
        self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]').clear()
        self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys(regUserDict["userBad"]["password"])
        self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
        time.sleep(varj)
        assert WebDriverWait(self.browser, varj2).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]'))).text == "Email must be a valid email."

    # ------------------------------------------------------------------------------------------------------------------
    # ATC05 - Bejelentkezés helyes adatokkal
    def test_loginRight(self):
        self.browser.find_element(By.XPATH, '//a[@href="#/login"]').click()
        self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]').send_keys(regUserDict["userRight"]["email"])
        self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys(regUserDict["userRight"]["password"])
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()
        assert WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//a[@class="nav-link router-link-exact-active active"]'))).is_displayed()

    # ------------------------------------------------------------------------------------------------------------------
    # ATC06 - Kijelentkezés, ellenőrzése
    def test_logOut(self):
        login(self.browser)
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//a[@active-class="active"]'))).click()
        assert WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]'))).is_displayed()

    # ------------------------------------------------------------------------------------------------------------------
    # ATC07 - Bejelentkezési kísérlet adatok nélkül
    def test_loginEmpty(self):
        self.browser.find_element(By.XPATH, '//a[@href="#/login"]').click()
        self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
        time.sleep(varj)
        assert WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]'))).text == "Email field required."

    # ------------------------------------------------------------------------------------------------------------------
    # ATC08 - Bejelentkezési kísérlet helytelen jelszóval
    def test_loginBadPass(self):
        self.browser.find_element(By.XPATH, '//a[@href="#/login"]').click()
        self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]').send_keys(regUserDict["userRight"]["email"])
        self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys('badpassword')
        self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
        time.sleep(varj)
        assert WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]'))).text == "Invalid user credentials."

    # ------------------------------------------------------------------------------------------------------------------
    # ATC09 - Global Feed oldalainak lapozása
    def test_pageNumber(self):
        login(self.browser)
        for page in WebDriverWait(self.browser, varj).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="page-link"]'))):
            page.click()
            assert page.text == WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//li[@class="page-item active"]'))).text

    # ------------------------------------------------------------------------------------------------------------------
    # ATC10 - Listázás Tagekkel
    def test_tags(self):
        login(self.browser)
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//div[@class="sidebar"]/div[@class="tag-list"]/a[@href="#/tag/dolor"]'))).click()
        assert len(WebDriverWait(self.browser, varj).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="preview-link"]/h1')))) != 0

    # ------------------------------------------------------------------------------------------------------------------
    # ATC11 - Cikk létrehozása, ellenőrzése
    def test_articleCreate(self):
        login(self.browser)
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]'))).click()
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Article Title"]'))).send_keys(articleDict["title"])
        self.browser.find_element(By.XPATH, '//input[starts-with(@placeholder,"What")]').send_keys(articleDict["about"])
        self.browser.find_element(By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]').send_keys(articleDict["markDown"])
        self.browser.find_element(By.XPATH, '//input[@placeholder="Enter tags"]').send_keys(articleDict["tags"])
        self.browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        assert WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//h1'))).text == articleDict["title"]

    # ------------------------------------------------------------------------------------------------------------------
    # ATC12 - Saját cikk törlése, ellenőrzése
    def test_articleDelete(self):
        login(self.browser)
        create_article(self.browser)
        time.sleep(varj)
        article_url = self.browser.current_url
        self.browser.find_element(By.XPATH, '//i[@class="ion-trash-a"]').click()
        time.sleep(varj)
        assert self.browser.current_url != article_url

    # ------------------------------------------------------------------------------------------------------------------
    # ATC13 - Komment hozzáadása, ellenőrzése
    def test_commentCreate(self):
        login(self.browser)
        create_article(self.browser)
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write a comment..."]'))).send_keys(comment)
        self.browser.find_element(By.XPATH, '//button[@class="btn btn-sm btn-primary"]').click()
        assert WebDriverWait(self.browser, varj).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="card"]')))[0].is_displayed()

    # ------------------------------------------------------------------------------------------------------------------
    # ATC14 - Komment törlése, ellenőrzése
    def test_commentDelete(self):
        login(self.browser)
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//a[@class="preview-link"][1]'))).click()
        time.sleep(varj2)
        create_comment(self.browser)
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//i[@class="ion-trash-a"]'))).click()
        assert len(WebDriverWait(self.browser, varj).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="card"]')))) != 0

    # ------------------------------------------------------------------------------------------------------------------
    # ATC15 - Cikkek létrehozása adatforrásból
    def test_importCsv(self):
        login(self.browser)
        with open('vizsgaremek_test/dataImp.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                create_article_data(self.browser, row[0], row[1], row[2], row[3])
                assert WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//h1'))).text == row[0]

    # ------------------------------------------------------------------------------------------------------------------
    # ATC16 - Címkék lementése csv adatfájlba
    def test_tag2Csv(self):
        login(self.browser)
        tag_list = WebDriverWait(self.browser, varj).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="sidebar"]/div/a[@class="tag-pill tag-default"]')))
        with open('vizsgaremek_test/listTag.csv', 'w') as file:
            writer = csv.writer(file)
            for tag in tag_list:
                writer.writerow([tag.text])
        with open('vizsgaremek_test/listTag.csv', 'r') as file:
            first_row = file.readline().rstrip('\n')
            assert first_row == tag_list[0].text

    # ------------------------------------------------------------------------------------------------------------------
    # ATC17 - Felhasználó módosítása
    def test_nameModifie(self):
        login(self.browser)
        WebDriverWait(self.browser, varj).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[1].click()
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Your username"]'))).clear()
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Your username"]'))).send_keys(newName)
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()
        WebDriverWait(self.browser, varj).until(EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]'))).click()
        assert WebDriverWait(self.browser, varj).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[2].text == newName
