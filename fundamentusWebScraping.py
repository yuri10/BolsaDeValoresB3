# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:11:28 2020

@author: Yuri Oliveira
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
#from selenium.webdriver.common.action_chains import ActionChains

with open('C:/Users/Yuri Oliveira/Desktop/BolsaDeValores/codigos_b3.txt') as f:
    codigos = f.readlines()
    f.close()


#options of web driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#actions = ActionChains(driver)
driver = webdriver.Chrome("C:/Users/Yuri Oliveira/Desktop/assistfly/chromedriver.exe", chrome_options = options)


driver.get("https://www.fundamentus.com.br/detalhes.php?papel=B3SA3")

driver.execute_script("window.open('https://www.fundamentus.com.br/detalhes.php?papel=' + codigo);")

page_source = driver.page_source                                                              
#utiliza o pandas para encontrar as tabelas do html
df = pd.read_html(page_source)                                                       


