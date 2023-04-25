from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 
from bs4 import BeautifulSoup
import time 
import random
import json


def gather_links():

    #driver setup 
    driver = uc.Chrome()
    thy_help_url = 'https://www.turkishairlines.com/en-int/any-questions/'
    driver.get(thy_help_url)
    driver.save_screenshot("/Users/denizdemirtas/Desktop/THY_Scraper/SS.png")
    # wait setup 
    wait = WebDriverWait(driver=driver, timeout=30)
    get_url = driver.current_url
    wait.until(EC.url_to_be(thy_help_url))
    if get_url == thy_help_url:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features="html.parser")
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="cookieWarningAcceptId"]')))
        #enable cookies
        #driver.find_element(By.XPATH, '//*[@id="cookieWarningAcceptId"]').click()
        #wait.until(EC.invisibility_of_element((By.XPATH, '//*[@id="cookieWarningAcceptId"]')))
        help_col = soup.find_all("ul", {"id" : "navBarItems"})
        links = []
        for header in help_col:
            topic = header.findChildren("li")
            for section in topic:
                children = section.findChildren("a")
                for link in children:
                    links.append(link.get("href"))
                    
    f = open("/Users/denizdemirtas/Desktop/THY_Scraper/infolinks.txt", "x")
    for link in links:
         f.write(f"{link}\n")
    print("links gathered")
    



def get_content():
    driver = uc.Chrome()
    wait = WebDriverWait(driver=driver, timeout=30)
    base_url = 'https://www.turkishairlines.com'
    f = open("/Users/denizdemirtas/Desktop/THY_Scraper/infolinks.txt", "r")
    links = f.readlines()
    result = []
    question_statement_lst = []
    answer_statement_lst = []
    

    for link in links:
        time.sleep(random.uniform(1,5))
        link = link.replace("\n", "")
        curr_url = base_url+link
        driver.get(curr_url)
        get_url = driver.current_url
        wait.until(EC.url_to_be(curr_url))
        get_url = driver.current_url
    
        if get_url == curr_url:

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, features="html.parser")
            #driver.save_screenshot("/Users/denizdemirtas/Desktop/THY_Scraper/SS.png")
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cookieWarningAcceptId"]')))
            info = soup.find_all("div", {"class" : "grid"})
            #driver.save_screenshot("/Users/denizdemirtas/Desktop/THY_Scraper/SS.png")
            print("URL: ", get_url)
            
            for i in info:
                question_children = i.findChildren("h4")
                for q in question_children:
                    question_statement = q.getText()
                    print("Elem: ", q.get("href"))
                    question_statement = question_statement.replace("\n", "")
                    question_statement_lst.append(question_statement)
                
                answer = i.find_all("div", {"class" : "charlimit"})

                for a in answer:

                    answer_statement = a.getText()
                    answer_statement = answer_statement.replace("\n", "")
                    answer_statement_lst.append(answer_statement)

    
    for q, a in zip(question_statement_lst, answer_statement_lst):
        result.append({"prompt" : q, "completion" : a})


    with open("/Users/denizdemirtas/Desktop/THY_Scraper/info2.json", "w") as outfile:
        json.dump(result, outfile)
    print("done")

get_content()