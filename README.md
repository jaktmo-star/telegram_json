## Explicação do Código

### Importação das bibliotecas

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import json
```

Essas bibliotecas foram importadas para permitir que o programa execute tarefas específicas:

* `webdriver` é utilizado para controlar o navegador automaticamente.
* `By` permite localizar elementos dentro da página.
* `Service` configura o ChromeDriver.
* `ChromeDriverManager` faz o download e gerenciamento automático do driver do navegador.
* `requests` é utilizado para enviar mensagens para o Telegram.
* `time` adiciona pausas durante a execução.
* `json` permite ler os dados armazenados no arquivo `telegram.json`.

### Leitura do arquivo JSON

```python
with open("telegram.json", "r") as arquivo:
    dados = json.load(arquivo)
```

Foi criado um arquivo JSON para armazenar o Token e o Chat ID do Telegram separadamente do código principal.

Essa decisão foi tomada para:

* Evitar expor informações sensíveis no código.
* Facilitar futuras alterações sem modificar o programa.
* Permitir que o arquivo seja ignorado pelo GitHub através do `.gitignore`.
* Melhorar a organização do projeto.

### Recuperação das credenciais

```python
TOKEN = dados["token"]
CHAT_ID = dados["chat_id"]
```

Após a leitura do arquivo JSON, os valores são armazenados em variáveis para serem utilizados no envio da mensagem.

### Inicialização do navegador

```python
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)
```

Essa etapa abre uma instância do navegador Google Chrome e garante que o driver necessário esteja instalado automaticamente.

### Definição da URL

```python
url = "https://www.amazon.com.br/..."
```

A variável armazena o endereço do produto que será monitorado.

### Acesso à página

```python
driver.get(url)
```

Comando responsável por abrir a página do produto no navegador.

### Tempo de espera

```python
time.sleep(5)
```

Foi utilizado para aguardar o carregamento completo da página antes da captura do preço.

### Captura do preço

```python
inteiro = driver.find_element(By.CLASS_NAME, "a-price-whole").text
decimal = driver.find_element(By.CLASS_NAME, "a-price-fraction").text
```

Essas linhas localizam os elementos que contêm o valor inteiro e os centavos do preço exibido pela Amazon.

### Tratamento dos dados

```python
inteiro = inteiro.replace(".", "").replace(",", "")
```

Remove caracteres que poderiam impedir a conversão do preço para formato numérico.

### Conversão para número

```python
preco = float(f"{inteiro}.{decimal}")
```

Une a parte inteira e decimal do preço, transformando o resultado em um valor numérico que pode ser comparado.

### Verificação do valor

```python
if preco <= 3200:
```

Define a condição para envio da notificação.

A mensagem só será enviada quando o produto atingir o valor desejado.

### Criação da mensagem

```python
mensagem = (
    f"Pode comprar, o preço está bom!!!\n"
    f"O preço do produto é: {preco:.2f}\n"
    f"{url}"
)
```

Monta a mensagem contendo o preço encontrado e o link do produto.

### Envio para o Telegram

```python
requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": mensagem
    }
)
```

Realiza uma requisição para a API do Telegram utilizando os dados armazenados no arquivo JSON.

Se a condição do preço for atendida, a mensagem é enviada automaticamente para o usuário.

### Encerramento do navegador

```python
driver.quit()
```

Fecha o navegador após a execução do processo, liberando os recursos utilizados pelo sistema.

