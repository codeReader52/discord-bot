#!/bin/bash

docker build -t discord_bot .

docker run -e "BOT_TOKEN=$1" -d discord_bot