docker build -t teste-final-rpa .

CMD
docker run --rm -v "%cd%\data:/app/data" -v "%cd%\image-graphic:/app/image-graphic" teste-final-rpa

POWERSHELL
docker run --rm -v "${PWD}\data:/app/data" -v "${PWD}\image-graphic:/app/image-graphic" teste-final-rpa

WSL/LINUX ( se estiver usando git bash no windows, entre dentro do wsl para executar esse comando )
docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/image-graphic:/app/image-graphic" teste-final-rpa
