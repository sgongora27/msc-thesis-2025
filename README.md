# ⚠️UNDER CONSTRUCTION ⚠️ (Santiago Góngora - Master's Thesis)

This repository contains the code for the latest version of the PAYADOR approach, the same that was used to perform the experiments presented in this thesis. 

The PAYADOR approach is an approach to the world-update problem in Interactive Storytellig, and it was described in the ICCC24 paper “[PAYADOR: A Minimalist Approach to Grounding Language Models on Structured Data for Interactive Storytelling and Role-playing Games](https://computationalcreativity.net/iccc24/papers/ICCC24_paper_152.pdf)”.

## 🗂️ Project structure

This folder contains all the files needed to run the latest version of PAYADOR, used to perform the experiments presented in this thesis.

- `logs_processing.py` implements an algorithm to convert the gamelogs stored in .json files to human-readable .txt files.

## ⚙️ Usage

Please, follow these steps to get this code running.

### Dependencies

To install the dependencies using [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html), just run

```shell
conda env create -f environment.yml
```

and then activate the environment


```shell
conda activate payador
```

### Credentials

The `.env` file stores private keys to access APIs. You must edit the placeholder values and write there your private credentials.

### Scenario configuration

The `config.ini` file is used to load the configuration options for the game. 

In the current version, the system can be used both in English ('en') and Spanish ('es').

### Web application
To start the web app, just run 
```
python app.py
```
and the Gradio web app will be accessible at http://127.0.0.1:7860/.
