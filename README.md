# 🤖 UNO Bot – Unstop Coding Challenge Submission

This repository contains a Python-based UNO-playing bot built for the **Unstop Submission Round – April 2025**. The bot's logic is implemented by editing the `choose_card()` function inside the provided starter kit (`playerBot.py`), as per the challenge instructions.

## 📦 Starter Kit

This project uses the official starter kit provided by Unstop.  
🔗 [Download Starter Kit](https://bit.ly/UNOCODESTARTERKIT)

## 🧠 Bot Logic

The core logic is written in the `choose_card()` function located in `playerBot.py`. The bot evaluates the top card on the pile and chooses a card from its hand based on UNO rules. If no valid move exists, it returns `None` to indicate a draw.

## 🚀 How to Run

You can test the bot in **two different ways**:

### 1. Manual Input (Single Turn Test)
```bash
python playerBot.py

### 📄  Output Log
A .txt file is generated as part of the submission. This output log includes:
Top card on the pile
Bot's current hand
Chosen move
Declared colour (for Wild cards)
📁 Example log file: output_log.txt

### 🛠️ Files
File	Description
main.py	Runs a full simulation of a 4-player UNO game
playerBot.py	Contains your custom bot logic inside choose_card()
output_log.txt	Captures the bot's decision-making steps for submission
