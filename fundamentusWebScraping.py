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

with open('C:/Users/Yuri Oliveira/Desktop/BolsaDeValoresB3/codigos_b3.txt') as f:
    codes = f.read().splitlines()
    f.close()

#removing \n from codes
#for codes in

#options of web driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#actions = ActionChains(driver)
driver = webdriver.Chrome("C:/chromedriver.exe", chrome_options = options)

code = codes
for code in codes:

    url = "'https://www.fundamentus.com.br/detalhes.php?papel=" + code + "'"
    driver.execute_script("window.open("+ url + ");")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    window_name = driver.window_handles[0]
    
    try:
        #pega o html da pagina atual
        page_source = driver.page_source                                                              
        #utiliza o pandas para encontrar as tabelas do html
        df = pd.read_html(page_source)
        
        #Pega só a tabela dos indicadores fundamenalista
        dfIndicFund = df[2]
        dfIndicFund = dfIndicFund.loc[:, 2:]
        
        dfIndicFund2 = dfIndicFund.loc[:, 2:3]
        dfIndicFund = dfIndicFund.loc[:, 4:5]
        dfIndicFund = dfIndicFund.T
        
        
    except:
        print("A pagina com codigo " + code +" nao possui tabelas!")
                                                       


