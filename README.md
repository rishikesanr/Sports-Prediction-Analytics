## Active Project

The idea of this project is to predict the win/loss odds of teams in a sports match. The core of the analysis is to understand and explore the why fans could be the best analyst of the sport, and augment the information on the sport before betting.

Pre-requisities:<br><br>
-- MongoDB is installed, and  open to all requests at port: 27017<br>
-- Postgresql is installed, and open to all requests at port: 5432 (Optional, if Grafana is inactive, credentials can also be changed using util files)<br>
-- Miniconda is installed <br><br> (For mac, follow the below miniconda installation using brew)<br>

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install --cask miniconda
brew install --cask miniconda
conda init
```
Restart your terminal, and check the miniconda version 

```
conda --version
```

-- .env created for API credentials (Reddit,.etc). Check docs for more information! (It is enabled by default for initial usage, however strongly recommended to create your own Reddit credential, and store it in ./scraping/.env)<br>

Commands to setup 

```bash
git clone https://github.com/rishikesanr/Sports-Prediction-Analytics.git
cd <path-to-current-repository>
conda env create -f ./envs/environment.yml
```

Commands to do the sports prediction

```bash
conda activate sports_analytics
python3 main.py PremierLeague "Liverpool vs Brighton"
python3 main.py mlb "Yankees vs Mets"
```

This exploration holds the potential to yield valuable insights that could impact betting outcomes.

Model 1 - A simple sentiment approach using Bag of Words from Fans
(Optional. A simple sentiment model approach using Bag of Words from Critics, A simple ensmeble sentiment model approach using Bag of Words from both Fans& Critics)

Model 2 - Applying PyTorch/TextBlob frameworks for generating sentiment scores

Model 3 - Fine tuning open LLMs (Llama2, BERT) for sentiment analysis (At the present, a non-trained BERT model in implemented using a untrained classifier)

Model 4 - Ensemble of Model 1,2, and 3

A microservices will be followed for the prodcut implementation(MongoDB, PostgresSQL, Grafana(public host), and Airflow). 

