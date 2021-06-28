import requests
import pandas as pd
from bs4 import BeautifulSoup
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
userinfo = config_object["BASEURL"]

header = userinfo["header"]
base_url = userinfo["base_url"]
reviews_url = userinfo["reviews_url"]
ids_url = userinfo["ids_url"]
review_limit = userinfo["review_limit"]


# Function for searching product page given the url
def get_amazon_search(url):
    page = requests.get(url, cookies={}, headers=header)
    soup = BeautifulSoup(page.content)
    return soup


# returns product ID for all products
def product_id(product):
    data_asin = []
    url = base_url + product
    soup = get_amazon_search(url)
    for i in soup.findAll("div", {'class': "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"}):
        data_asin.append(i['data-asin'])
    return data_asin


# creates the links to all product reviews page
def create_links(product_ids):
    links = []
    for i in range(len(product_ids)):
        id_url = ids_url + product_ids[i]
        soup = get_amazon_search(id_url)
        for link in soup.findAll("a", {'data-hook': "see-all-reviews-link-foot"}):
            links.append(link['href'])
    links = list(set(links))
    return links


# pulls the reviews on each page using the links from create_links
def pull_reviews(links):
    reviews = []
    product_link = []
    for link in range(len(links)):
        page_number = 0
        review_url = reviews_url + links[link] + '&pageNumber=' + str(page_number)
        soup = get_amazon_search(review_url)
        for review in soup.findAll("span", {'data-hook': "review-body"}):
            reviews.append(review.text)
            product_link.append(review_url + links[link])
        while soup.findAll("span", {'data-hook': "review-body"}) and page_number <= review_limit:
            page_number = page_number + 1
            review_url = reviews_url + links[link] + '&pageNumber=' + str(page_number)
            soup = get_amazon_search(review_url)
            for review in soup.findAll("span", {'data-hook': "review-body"}):
                reviews.append(review.text)
                product_link.append(review_url + links[link])
    return reviews, product_link


# combines all the reviews as a dataframe for each product
def combine_reviews(reviews, product_link):
    review_dict = {'reviews': reviews}
    product_dict = {'links': product_link}
    product_names = {'products': [link.split('/')[3] for link in product_link]}
    all_reviews = pd.DataFrame.from_dict(review_dict)
    product_links = pd.DataFrame.from_dict(product_dict)
    products = pd.DataFrame.from_dict(product_names)
    for column in all_reviews.columns:
        all_reviews[column] = all_reviews[column].str.replace(r'\n\n', '')
    all_reviews.drop(index=0, inplace=True)
    all_reviews['links'] = product_links['links']
    all_reviews['products'] = products['products']
    return all_reviews


# main function for running all other functions
def run_webscraping(products_to_review):
    idis = product_id(products_to_review)
    links = create_links(idis)
    reviews, product_link = pull_reviews(links)
    df = combine_reviews(reviews, product_link)
    return df
