# Arduino Interaction Guide in Python

## Portuguese

### Objetivo Principal
O objetivo principal deste trabalho é conseguir interagir com o Arduino sem usar o Arduino IDE. No fundo, é usar o Arduino como placa de aquisição de dados, sendo que o processamento será feito no computador.

### Formas de Programar

#### Modo Texto
- Usando a consola do Python e enviando mensagens de texto através da porta série. Requer alguma programação em C++ no Arduino.

#### Modo Gráfico (por blocos)
- Usando o IDE Makeblock 5 online ou a versão instalável ([Makeblock 5 Download](https://mblock.makeblock.com/en/download/))
  - A programação é feita por blocos como o Scratch.
- Usando o Pictoblox da SteamPedia ([Download Pictoblox](https://thestempedia.com/product/pictoblox/download-pictoblox/?srsltid=AfmBOooYXyUIbJEarqKEskAzFW4EOpinY3Kp4YHRrTF6BX2xIY14gcP9))
  - Pode usar blocos ou Python.
- Usando o Scratch3 for IoT ([Scratch3 for Arduino ESP8266](https://github.com/labF212/Scratch3-for-Arduino-ESP8266))
  - Utiliza blocos como o Scratch.

#### Modo Gráfico em Python
Usando Telemetrix ou Pyfirmata como forma de comunicação via porta série:
- Tkinter
- PySimpleGUI
- Flet

---

## Tkinter
Para instalar o Tkinter no Linux:

```bash
sudo apt install python3-tk
```

---

## PySimpleGUI
**PySimpleGUI** - Interface gráfica para Python (não é gratuito para uso profissional ou educacional).

### Instalação e Dependências

```bash
pip3 install PySimpleGui           # Instalação da interface gráfica
sudo apt-get install sqlite3       # Instalação de base de dados
sudo apt-get install sqlitebrowser # Visualizador de base de dados
pip3 install pillow                # Suporte para mais tipos de imagens no PySimpleGui
```

---

## Telemetrix
O **Projeto Telemetrix** é uma substituição moderna para o Arduino StandardFirmata, equipado com muitos mais recursos integrados do que o StandardFirmata. O projeto consiste em APIs Python para criar aplicações cliente em Python e servidores C++ que comunicam com o cliente Python via porta série ou Wi-Fi.

### Instalação do Telemetrix

Para instalar o Telemetrix no Linux (incluindo Raspberry Pi) e macOS:

```bash
sudo pip3 install telemetrix
```

Para usuários de Windows:

```bash
pip install telemetrix
```

Para comunicar o Python com o Arduino, será necessário transferir um programa para o Arduino seguindo as instruções em:  
[Telemetrix Instructions for Arduino](https://mryslab.github.io/telemetrix/telemetrix4arduino/)

---

## English

### Main Objective
The main goal of this project is to interact with Arduino without using the Arduino IDE. Essentially, the Arduino will be used as a data acquisition board, while the processing will be handled by the computer.

### Programming Methods

#### Text Mode
- Using the Python console and sending text messages via the serial port. Requires some C++ programming on the Arduino.

#### Graphical Mode (Block-based)
- Using the Makeblock 5 IDE, either online or the installable version ([Makeblock 5 Download](https://mblock.makeblock.com/en/download/))
  - Programming is done using Scratch-like blocks.
- Using Pictoblox from SteamPedia ([Download Pictoblox](https://thestempedia.com/product/pictoblox/download-pictoblox/?srsltid=AfmBOooYXyUIbJEarqKEskAzFW4EOpinY3Kp4YHRrTF6BX2xIY14gcP9))
  - Allows the use of blocks or Python.
- Using Scratch3 for IoT ([Scratch3 for Arduino ESP8266](https://github.com/labF212/Scratch3-for-Arduino-ESP8266))
  - Programming is done using Scratch-like blocks.

#### Graphical Mode in Python
Using Telemetrix or Pyfirmata for serial communication, along with:
- Tkinter
- PySimpleGUI
- Flet

---

## Tkinter
To install Tkinter on Linux:

```bash
sudo apt install python3-tk
```

---

## PySimpleGUI
**PySimpleGUI** - Graphical interface for Python (not free for professional or educational use).

### Installation Steps

```bash
pip3 install PySimpleGui           # Installs the graphical interface
sudo apt-get install sqlite3       # Installs the database
sudo apt-get install sqlitebrowser # Database viewer
pip3 install pillow                # Adds support for more image formats to PySimpleGui
```

---

## Telemetrix
The **Telemetrix Project** is a modern-day replacement for Arduino StandardFirmata, equipped with many more built-in features than StandardFirmata. The project consists of Python APIs used to create Python client applications and C++ servers that communicate with the Python client over a serial or Wi-Fi link.

### Installing Telemetrix

To install Telemetrix on Linux (including Raspberry Pi) and macOS:

```bash
sudo pip3 install telemetrix
```

For Windows users:

```bash
pip install telemetrix
```

To communicate Python with Arduino, you must upload a program to the Arduino following the instructions at:  
[Telemetrix Instructions for Arduino](https://mryslab.github.io/telemetrix/telemetrix4arduino/)
















