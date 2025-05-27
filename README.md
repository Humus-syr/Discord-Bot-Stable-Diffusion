# Discord Bot for Stable Diffusion
A discord bot that responds to text and Image prompts with the help of different LLM models

Developing this on 2 different systems. So will have to add a few more things over the MVP version.

### How it Works

    The bot connects to Discord using the credentials provided in the env file.
    The bot currently hardcodes a specific channel on Discord (For testing).
    The bot sends a request to generate an image based on the user's prompt to a separate server.
    The bot waits for the server to send the response and shows a thinking prompt on discord.
    The bot downloads the image and sends it to the channel.

### Steps to run locally:
1. Clone the repo

- Create a .env file with the following information
```
APP_ID=<YOUR_APP_ID>
DISCORD_TOKEN=<YOUR_BOT_TOKEN>
PUBLIC_KEY=<YOUR_PUBLIC_KEY>
```

*In case you enable Chat GPT support add the below key to your .env file*
```
OPENAI_API_KEY=
```

- Install the requirements
```
poetry install
```
- Switch to the new virtual environment
```
eval $(poetry env activate)
````
- Go to ai_server folder and run the demo ai server. (Instructions in the readme of that folder)
	Optional if you have a different server. Then you need to change the server address in config.yml
- Once the other services are ready, run
```
python bot.py
```

Now your bot is connected to discord and ready to recieve messages.

### Docker steps
TBD

<!--
Use docker to launch the project.
```
docker compose up
# or run in the daemon mode
docker compose up -d
```
-->

TODO tasks:
- Add the LLM (currently it doesn't fit in the VRAM, tested on google collab, but not moved here)
- Fix logger. (Discord has its own logger?)
- Check cTransformer[cuda] vs Transformer
- Fix TODOs in the code
- Add a timeout check for bot thinking, in case the model server does not respond back, or there was an error.


<!-- - Rough things for blog aobut this project
-- Why this project. For the memes and dota support while gaming
-- What it can currently do.
-- What I've learnt doing this so far. 
-- Next things I want to try.
-- Stretch goals
-- runpod
-- gcp app
-- code cleanup
-- streamlit? or node?
-- Understanding bit more react while making the blog
- Using A111?
 -->



 ### Project Organization

```
├── AUTHORS.md              <- List of developers and maintainers.
├── CHANGELOG.md            <- Changelog to keep track of new features and fixes.
├── CONTRIBUTING.md         <- Guidelines for contributing to this project.
├── Dockerfile              <- Build a docker container with `docker build .`.
├── LICENSE.txt             <- License as chosen on the command-line.
├── README.md               <- The top-level README for developers.
├── configs                 <- Directory for configurations of model & application.
├── data
│   ├── external            <- Data from third party sources.
│   ├── interim             <- Intermediate data that has been transformed.
│   ├── processed           <- The final, canonical data sets for modeling.
│   └── raw                 <- The original, immutable data dump.
├── docs                    <- Directory for Sphinx documentation in rst or md.
├── environment.yml         <- The conda environment file for reproducibility.
├── ai_server
│   └── models              <- Support for different model classes that handle inference
├── pyproject.toml          <- Build configuration. Don't change! Use `pip install -e .`
│                              to install for development or to build `tox -e build`.
├── scripts                 <- Analysis and production scripts which import the
│                              actual PYTHON_PKG, e.g. train_model.
├── setup.cfg               <- Declarative configuration of your project.
├── discord_src
│   └── bot                 <- The main source code of the discord bot
│   └── config              <- This is where we keep the hydra config.
│   └── utils               <- Contains the miscellaneous code that does not have anywhere
│                              else to be.
├── tests                   <- Unit tests which can be run with `pytest`.
├── .coveragerc             <- Configuration for coverage reports of unit tests.
└── .pre-commit-config.yaml <- Configuration of pre-commit git hooks.
```

 ### Running Unit tests - TBD soon
 We use `pyenv` as the testing framework and the test cases are located in the `tests/` directory.
 To run the test cases, run 
 ```
pyenv -v tests/
```
