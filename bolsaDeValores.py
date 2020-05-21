# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:23:33 2020

@author: Yuri Oliveira
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
import time
#from selenium.webdriver.common.action_chains import ActionChains

#options of web driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#actions = ActionChains(driver)
driver = webdriver.Chrome("C:/Users/Yuri Oliveira/Desktop/assistfly_driver/chromedriver.exe", chrome_options = options)

#indicadores das empresas
#https://www.bussoladoinvestidor.com.br/guia-empresas/empresa/QVUM3B/indicadores



'''
#pega o codigo de todas as empresas da b3
driver.find_element_by_css_selector('#table > div > div.table-body > div > table > thead > tr > th.sortable.text-left').click()

#avança uma pagina
driver.find_element_by_css_selector('#table > div > div.table-footer > div > div > div > div:nth-child(2) > div > ul > li.pagination-next.ng-scope > a').click()

lista_codigos_b3 = []

#retorna o html da pagina atual
#page_source = driver.page_source 

for p in range(67):
    for i in range(1,11):
        elemento = driver.find_element_by_css_selector("#table > div > div.table-body > div > table > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(3")
        lista_codigos_b3.append(elemento.text)
        #avança uma pagina
    driver.find_element_by_css_selector('#table > div > div.table-footer > div > div > div > div:nth-child(2) > div > ul > li.pagination-next.ng-scope > a').click()
    time.sleep(2)
'''   

def transformaDataframes(df, codigo):
    dataframes = []
    dataframe = df[3]
    for dataframe in df:
        dataframe = dataframe.T
        headers = dataframe.iloc[0]
        dataframe = pd.DataFrame(dataframe.values[1:], columns=headers)
        dataframe['codigo'] = codigo
        dataframes.append(dataframe)
    return dataframes

def mergeDataframes(dataframes):
    dfMerge = dataframes[0]    
    for i in range(1,6):
        df = dataframes[i]
        dfMerge = pd.merge(dfMerge, df)
    return dfMerge
        

with open('C:/Users/Yuri Oliveira/Desktop/BolsaDeValores/codigos_b3.txt') as f:
    codigos = f.readlines()
    f.close()

todosDataFrames = []
for codigo in codigos:
    
    #URL of the website
    driver.get("https://www.bussoladoinvestidor.com.br/guia-empresas/empresa/" + codigo + "/indicadores")
    time.sleep(5)
    page_source = driver.page_source 
    df = pd.read_html(page_source)
    
    dataframes = transformaDataframes(df, codigo)
    
    dfMerge = mergeDataframes(dataframes)
    
    todosDataFrames.append(dfMerge)
    driver.close()
    time.sleep(5)







codigo = codigos[0]
driver.get("https://www.bussoladoinvestidor.com.br/guia-empresas/empresa/" + codigo + "/indicadores")
body = driver.find_element_by_tag_name("body")
body.send_keys(Keys.CONTROL + 't')







