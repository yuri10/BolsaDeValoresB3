# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:51:35 2020

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

def login(email, password):
    
    #espera o botao de login carregar
    botaoLogin_path = '#__next > div > div > header > nav > div > a'
    try:
        botaoLogin = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, botaoLogin_path)))
        print ("botao de login está pronto!")
    except TimeoutException:
        print ("botao de login demorou muito para carregar!")
    
    #clicka no botao de login
    botaoLogin.click()
    
    #espera botao de continuar carregar
    botaoContinuar_path = '#__next > div > div > div > div.css-xcgtpu > div.css-1i6q64e > form > button'
    try:
        botaoContinuar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, botaoContinuar_path)))
        print ("botao de continuar está pronto!")
    except TimeoutException:
        print ("botao de continuar demorou muito para carregar!")

    #coloca as credenciais para logar no site
    email_path = '#__next > div > div > div > div.css-xcgtpu > div.css-1i6q64e > form > input:nth-child(1)'
    password_path = '#__next > div > div > div > div.css-xcgtpu > div.css-1i6q64e > form > input:nth-child(2)'
    
    #elemento usuario para se logar na plataforma da skyteam
    email_element = driver.find_element_by_css_selector(email_path)
    email_element.send_keys(email)
    
    #elemento password para se logar na plataforma da skyteam
    pwd_element = driver.find_element_by_css_selector(password_path)
    pwd_element.send_keys(password)
    
    #clicka no botao de continuar
    botaoContinuar.click()
    
#Armazena os codigos das empresas numa lista que sera usada para acessar o site
# e obter mais dados sobre a empresa
empresas = pd.read_csv('C:/Users/Yuri Oliveira/Desktop/BolsaDeValoresB3/fundamentei.csv')

#pega apenas a coluna com os codigos das empresas
codigos = empresas['Ticker']

#options of web driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#actions = ActionChains(driver)
driver = webdriver.Chrome("C:/chromedriver.exe", chrome_options = options)

driver.get('https://fundamentei.com')


#para que os dados das empresas possam ser vistos por um usuario, é necessario
# fazer o login no site. Substitua as variaveis abaixo com suas credenciais
email = 'oliveirayuri10@hotmail.com'
password = input("Digite sua senha do fundamentei.com: ")
login(email, password)

#espera a pagina carregar depois de fazer o login
ativos_path = '#__next > div.css-1gmso8b > nav > div.css-fmng4b > ul > li.css-1h66nt4 > a'
try:
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ativos_path)))
    print ("site carregou com sucesso!")
except TimeoutException:
    print ("o site demorou muito para carregar, rode o programa novamente!")
    
#variaveis de teste
codigo = codigos[0]
codigos = codigos[0:5]

dataframes = [] 

#raspa cada site para cada codigo
for codigo in codigos:
    
    url =  'https://fundamentei.com/br/' + codigo
    
    #abre uma nova aba com a url acima
    driver.execute_script("window.open('"+ url + "');")
    #fecha a ultima pagina que foi utilizada
    driver.close()
    #volta o foco do driver pra pagina que será raspada
    driver.switch_to.window(driver.window_handles[0])
    
    try:
        #Da um mata leão no processo, deixa a pagina carregar meu filho
        time.sleep(1)
        #pega o html da pagina atual
        page_source = driver.page_source                                                              
        #utiliza o pandas para encontrar as tabelas do html
        #pega só a tabela com os indicadores fundamentalistas
        df = pd.read_html(page_source)[0]
        
        #coloca uma nova coluna com o codigo da empresa para identificação
        df['codigo'] = codigo
        
        dataframes.append(df)
        
        
        
    except:
        print("A pagina com codigo " + codigo +" nao possui tabelas!")
        
#pega apenas os dataframes com o numero de colunas igual a 18 (senão da ruim na hora de unir os dfs)
#list comprehension é uma delicinha
dfs = [df for df in dataframes if len(df.columns) == 18]    

#une os dataframes das diversas empresas em um unico
df_result = dfs[0] 
for i in range(1, len(dfs)):    
    df_result = dfs[i].append(df_result, ignore_index=True)

#tratamento dos dados
#numeros no padrão brasileiro, vamos trocar para o americano/internacional
df_teste=df_result.astype(int)
df_teste = df_teste.replace('.','',regex=False)    

#salva o dataframe final em um arquivo .csv que será lido pelo Tableau
df_result.to_csv('C:/Users/Yuri Oliveira/Desktop/BolsaDeValoresB3/resultado.csv')


