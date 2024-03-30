## Active Project

The idea of this project is to predict the win/loss odds of teams in a sports match. The core of the analysis is to understand and explore the why fans could be the best analyst of the sport, and augment the odds of the sport. 

Pre-requisities:<br><br>
-- MongoDB is installed, and  open to all requests at port: 27017<br>
-- Miniconda is installed <br>

Command to scrape data for any sports match 

```bash

python3 main.py PremierLeague "Liverpool vs Brighton"
python3 main.py mlb "Yankees vs Mets"
```

This exploration holds the potential to yield valuable insights that could impact betting outcomes.

Model 1 - A simple sentiment approach using Bag of Words from Fans (Automation Progression Going On..)

Model 2 - A simple sentiment model approach using Bag of Words from Critics 

Model 3 - A simple ensmeble sentiment model approach using Bag of Words from both Fans& Critics 

Model 4 - Fine tuning open LLMs (llama2 etc) for sentiment analysis

Model 5 - Using Retrieval-augmented generation (RAG) with LLMs for sentiment analysis 

A microservices approch to be followed for the prodcut implementation. 

