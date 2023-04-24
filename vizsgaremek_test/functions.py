from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


def login(browser):
    browser.find_element(By.XPATH, '//a[@href="#/login"]').click()
    browser.find_element(By.XPATH, '//input[@placeholder="Email"]').send_keys("user32@hotmail.com")
    browser.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys("Userpass1")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]'))).click()
    time.sleep(5)


def create_article(browser):
    browser.find_element(By.XPATH, '//a[@href="#/editor"]').click()
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Article Title"]'))).send_keys(
        "Teszt Title")
    browser.find_element(By.XPATH, '//input[starts-with(@placeholder,"What")]').send_keys(
        "Teszt About")
    browser.find_element(By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]').send_keys(
        "Teszt Article")
    browser.find_element(By.XPATH, '//input[@placeholder="Enter tags"]').send_keys("TesztTag1, TesztTag2")
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()


def create_article_data(browser, title_input, about_input, main_input, tag_input):
    browser.find_element(By.XPATH, '//a[@href="#/editor"]').click()
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Article Title"]'))).send_keys(title_input)
    browser.find_element(By.XPATH, '//input[starts-with(@placeholder,"What")]').send_keys(about_input)
    browser.find_element(By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]').send_keys(main_input)
    browser.find_element(By.XPATH, '//input[@placeholder="Enter tags"]').send_keys(tag_input)
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)


def create_comment(browser):
    browser.find_element(By.XPATH, '//textarea[@placeholder="Write a comment..."]').send_keys("Ez egy teszt komment.")
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-sm btn-primary"]'))).click()
    time.sleep(5)
