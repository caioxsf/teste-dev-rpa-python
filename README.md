docker build -t teste-rpa .
docker run --rm -v "%cd%\data:/app/data" -v "%cd%\image-graphic:/app/image-graphic" teste-final-rpa

docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/image-graphic:/app/image-graphic" teste-final-rpa
