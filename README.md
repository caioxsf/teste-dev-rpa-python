# 🐍 Teste RPA com Docker

📌 Este projeto executa um processo de RPA utilizando Python dentro de um container Docker. O código realiza tarefas automatizadas e armazena dados e imagens geradas em diretórios locais. O projeto acessa dois portais públicos utilizando `Selenium` e `concurrent.futures` para rodar em paralelo, baixa os dados (CSV e XLSX), realiza o cruzamento de dados extraindo apenas os registros de obitos e casos confirmados por mês e gera um gráfico comparativo.

## 📦 Alguns dos recursos utilizados foram: 
- Selenium → Automação do navegador
- Concurrent.futures → Realizar downloads de arquivos em paralelo
- Tenacity → Tentativas automáticas em falhas
- Pandas → Leitura, manipulação e análise e dados, permitindo cruzar informações relevantes
- Matplotlib → Geração de gráficos
- Docker → Empacotar o projeto para rodar em qualquer sistema operacional

## 🐳 Requisitos

- [Docker](https://www.docker.com/) instalado na sua máquina.

## 🚧 Build da Imagem

Para construir a imagem Docker do projeto, execute o seguinte comando no terminal dentro da pasta do projeto:

```
docker build -t teste-rpa .
```
## 🚀 Executando o Container
A execução do container varia conforme o terminal que você estiver utilizando:

## 🔹 CMD (Prompt de Comando do Windows)
```
docker run --rm -v "%cd%\data:/app/data" -v "%cd%\image-graphic:/app/image-graphic" teste-rpa
```
## 🔹 PowerShell
```
docker run --rm -v "${PWD}\data:/app/data" -v "${PWD}\image-graphic:/app/image-graphic" teste-rpa
```
## 🔹 WSL, Linux e MacOS
💡 Se estiver usando Git Bash no Windows, entre no WSL antes de executar este comando.
```
docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/image-graphic:/app/image-graphic" teste-rpa
```
