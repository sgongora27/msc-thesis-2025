# Santiago Góngora - Master's Thesis resources

This repository compiles the resources developed as part of my Master’s thesis.
The resources are as follows:
- Three tests to evaluate open-world gamemastering models. They are available in the [GitHub repository](https://github.com/sgongora27/skill-check-GM-tests) associated with the “[Skill check: Some considerations on the evaluation of gamemastering models for role-playing games](https://link.springer.com/chapter/10.1007/978-3-031-49065-1_27)” paper.
- The latest version of the PAYADOR system, originally introduced in the ICCC24 paper “[PAYADOR: A Minimalist Approach to Grounding Language Models on Structured Data for Interactive Storytelling and Role-playing Games](https://computationalcreativity.net/iccc24/papers/ICCC24_paper_152.pdf)”. It is available in the root of this repository.
- Playthroughs from the evaluation process. They are available in the “playthroughs” directory.


## 🗂️ Project structure

This folder contains all the files needed to run the latest version of PAYADOR, introduced and used in this thesis.

- `playthroughs_processing.py` implements an algorithm to convert the gamelogs stored in .json files (under `playthroughs/raw`) to human-readable .txt files.
- `app.py` implements the main loop of PAYADOR, according to the [Gradio](https://www.gradio.app/) specifications. 
- `world.py` implements the four components of the world model (Items, Characters, Locations and Puzzles) as well as the world itself. This module also implements the world state rendering in natural language and the update of the world state according to three transformations: "Moved Items", "Unblocked Locations" and "Player movement".
    - ❗ If you are working for a different language than English of Spanish, you will need to adapt the *render_world* and *update* methods.
    - ❗ If you want to include other transformations (e.g. mood during a conversation, like in the [Emolift paper](https://computationalcreativity.net/iccc2019/papers/iccc19-paper-44.pdf)) you will need to call additional functions in the *update* method.
- `example_worlds.py` includes some ready-to-play worlds. Worlds 1 and 2 were used in the experiments.
- `models.py` loads and prompts LLMs.
    - ❗ If you want to use a different model, you can add another class for it.
- `prompts.py`
    - ❗ If you are working for a different language than English or Spanish, you will need to adapt these prompts.
    - ❗ If you are working for other transformations, you will need to include additional instructions in the *prompt_world_update* function.

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
