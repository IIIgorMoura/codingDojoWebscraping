from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

import pandas as pd

import time

chrome_driver_path = r".\chromedriver.exe"
service = Service(chrome_driver_path) 

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--window_size=1920,1080')

driver = webdriver.Chrome(service=service, options=options)

url_base = 'https://www.imdb.com/chart/top/'
driver.get(url_base)

time.sleep(5)

# armazém ITENS
dic_filmes = {'titulo':[], 'ano':[]}


while True:

    # encontrar ITENS da PÁGINA
    try:
        WebDriverWait(driver,10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, 'ipc-metadata-list-summary-item'))
        )
        print('Elementos encontrados com sucesso!')
    except TimeoutException:
        print('Tempo de espera excedido!')
    
    filmes = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

    # coletar ITENS e enviar para DICIONÁRIO
    for filme in filmes:
        try:
            titulo = filme.find_element(By.CLASS_NAME, 'ipc-title__text').text.strip()
            ano = filme.find_element(By.CLASS_NAME, 'bnnHxo ').text.strip()
           

            print(f'{titulo} - {ano}')

            dic_filmes['titulo'].append(titulo)
            dic_filmes['ano'].append(ano)

        except Exception:
            print('Não foi possível coletar dados: ', Exception)
    break 

df = pd.DataFrame(dic_filmes)
df.to_excel('filmes.xlsx',index=False)
print(f"Arquivo foi salvo com sucesso {len(df)}")