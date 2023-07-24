@echo off
docker build -t py-placebot .
docker tag py-placebot zeepheru/rplace-2023-bot:py-placebot
docker push zeepheru/rplace-2023-bot:py-placebot