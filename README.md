# 🐍 Teste RPA com Docker

Este projeto executa um processo de RPA utilizando Python dentro de um container Docker. O código realiza tarefas automatizadas e armazena dados e imagens geradas em diretórios locais mapeados.

## 🐳 Requisitos

- [Docker](https://www.docker.com/) instalado na sua máquina.
- Diretórios `data/` e `image-graphic/` criados na raiz do projeto (serão usados para armazenar arquivos de saída).

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
##🔹 PowerShell
```
docker run --rm -v "${PWD}\data:/app/data" -v "${PWD}\image-graphic:/app/image-graphic" teste-rpa
```
## 🔹 WSL ou Linux
💡 Se estiver usando Git Bash no Windows, entre no WSL antes de executar este comando.
```
docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/image-graphic:/app/image-graphic" teste-rpa
```
