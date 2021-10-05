# Amazon Product Reviews Analytics
It is not always easy to select the best product from a myriad of products on Amazon. Even though Amazon provides a recommender system, it can still be a hassle to select the product you are looking for. 

You have to go through product reviews to get insights on a product others. This is time consuming and difficult. Plus, you may be interested in a certain feature that not everyone is interested in. For example, you may care about durability of a phone case, while most others are concerned about the aesthetics or price. 

The Amazon product reviews engine we are creating can help you analyze product reviews to obtain common themes on a product. This system uses machine learning to parse out product reviews and extract themes that could be helpful to customers when choosing which item to buy.

This repo is deployed as a web app through Heroku [here](https://amazonreviewsanalytics.herokuapp.com/).

## Installation
Clone this repository. Navigate to the repository and create a python virtual environment through your method of choosing. Activate the environment and install the required libraries through
```
git clone https://github.com/Aloagbaye/amazonreviewsanalytics.git
cd amazonreviewsanalytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Architecture
app.py --> templates/index.html --> webscraping.py --> dtm.py --> ldawithgridsearch.py --> templates/results.html
- app.py opens the user interface for collecting product names from the users
- index.html is the user interface for collecting product names used in scraping reviews from amazon.ca
- webscraping.py scrapes reviews of products from amazon and organizes these reviews into a dataframe of products, links and reviews
- dtm.py collects the dataframe from webscraping.py and converts it to a document-term-matrix useful for topic modelling
- ldawithgridsearch.py applies topic modeling to the document-term-matrix and produces a dataframe containing results of the top five words discussed in the reviews for each product
- results.html displays the dataframe results in html.

## Dependencies
The backend is developed in python 3.x.x. Other libraries and packages, along with their versions, are included in [requirements.txt]('../../requirements.txt'). In short, you need the following libraries and their dependencies.
- pandas
- numpy
- scikit-learn
- flask
- Beautiful soup
- nltk

## Usage
<a href="amazonreviewsanalytics.herokuapp.com">visit web app</a>
