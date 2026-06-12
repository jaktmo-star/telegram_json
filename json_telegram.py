# autor: Elcio Mello
# Projeto: Envio de mensagem com preço pelo telegram

# Importação da biblioteca
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import json #adicionando a biblioteca json

#abra o arquivo leia ele e arquive o conteudo no arquivo
with open("telegram.json","r") as arquivo:
    dados = json.load(arquivo) 

# Acesso a os dados de token e chat_id do telegram
TOKEN = dados ["token"] 
CHAT_ID = dados ["chat_id"] 

#abrir o navegador
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)
# URLs dos produtos
url = "https://www.amazon.com.br/Insta360-desempenho-aprimorado-atualizadas-substitu%C3%ADveis/dp/B0F3P4G8SY"
    
driver.get(url)
    
# Aguarda carregamento da página
time.sleep(5)

inteiro = driver.find_element(By.CLASS_NAME, "a-price-whole").text
decimal = driver.find_element(By.CLASS_NAME, "a-price-fraction").text

# retirar caracteres
inteiro = inteiro.replace(".","").replace(",","")

# concatenar as variáveis
preco = float(f"{inteiro}.{decimal}")

# Análise da condição do preço
if preco <= 3200:
    mensagem = (
         f"Pode comprar, o preço está bom!!!\n"
         f"O preço do produto é: {preco:.2f}\n"
         f"{url}"
    )

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
               "chat_id" : CHAT_ID,
               "text" : mensagem
            }
        )
    print('Pesquisa realizada e Mensagem enviada!')

driver.quit()



