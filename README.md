# SymbolAssistant
Symbol Assistant is an standalone device built on the Raspberry Pi. Can be used to manage your wallet using voice commands.  
See short demo on [youtube](https://youtu.be/BSM1Wyielpw)  
Project created for [Symbol Hackaton 2021](https://symbolplatform.com/hackathon)

## Hardware requirements
Raspberry Pi  
Sound card  
Microphone  
Speaker  

## Software requirements
Raspbian (OS)  
Node.js 10.22.1 or later  
Python 2.7.13 or later  

## Build Setup
### Server
Before build server set /src/config.ts file 

```bash

# install ts-node globally
$ npm install ts-node -g

# install dependencies
$ npm install

# serve at localhost:3000
$ ts-node ./server.ts

```

### Client
```bash

# install required dependencies 
sudo apt-get install sox flac python-dev python-pip python-lxml mpg123
sudo pip install SpeechRecognition tendo bs4 feedparser psutil

# run
$ python client.py

```