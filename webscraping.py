# Import modules
import requests
import pandas as pd
from bs4 import BeautifulSoup

header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/89.0.4389.128 Safari/537.36",
          "X-Amzn-Trace-Id": "Root=1-608078e5-5ab47ee82924df8667c3f0e7"}
base_url = "https://www.amazon.ca/s?k="


# Function for searching amazon products given product name
def get_amazon_search(search_products):
    url = "https://www.amazon.ca/s?k=" + search_products
    print(url)
    page = requests.get(url, cookies={}, headers=header)
    if page.status_code == 200:
        return page
    else:
        return "Error"


# Function for searching amazon products given product ID
def search_product_id(asin):
    url = "https://www.amazon.ca/dp/" + asin
    print(url)
    page = requests.get(url, cookies={}, headers=header)
    if page.status_code == 200:
        return page
    else:
        return "Error"


# Function for scraping amazon product reviews
def scrape_reviews(review_link):
    url = "https://www.amazon.ca" + review_link
    print(url)
    page = requests.get(url, cookies={}, headers=header)
    if page.status_code == 200:
        return page
    else:
        return "Error"


# Function for scraping amazon product names
def get_product_names(product):
    product_names = []
    response = get_amazon_search(product)
    soup = BeautifulSoup(response.content)
    for i in soup.findAll("span", {'class': 'a-size-base-plus a-color-base a-text-normal'}):  # the tag which is
        # common for all the names of products
        product_names.append(i.text)  # adding the product names to the list
    return product_names


# returns product ID for all products
def product_id(product):
    data_asin = []
    response = get_amazon_search(product)
    soup = BeautifulSoup(response.content, "html.parser")
    for i in soup.findAll("div", {'class': "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"}):
        data_asin.append(i['data-asin'])
    return data_asin


# creates csv file containing all amazon product reviews
def create_links(product_ids):
    links = []
    reviews = []
    product_link = []
    for i in range(len(product_ids)):
        response = search_product_id(product_ids[i])
        soup = BeautifulSoup(response.content)
        for link in soup.findAll("a", {'data-hook': "see-all-reviews-link-foot"}):
            links.append(link['href'])

    for j in range(len(links)):
        for k in range(20):
            try:
                response = scrape_reviews(links[j] + '&pageNumber=' + str(k))
                soup = BeautifulSoup(response.content)
                for i in soup.findAll("span", {'data-hook': "review-body"}):
                    reviews.append(i.text)
                    product_link.append(links[j])
            finally:
                k = 21

    review_dict = {'reviews': reviews}
    product_dict = {'products': product_link}
    all_reviews = pd.DataFrame.from_dict(review_dict)
    product_list = pd.DataFrame.from_dict(product_dict)

    columnheaders = ['reviews']
    all_reviews.columns = columnheaders
    for column in all_reviews.columns:
        all_reviews[column] = all_reviews[column].str.replace(r'\n\n', '')
    all_reviews.drop(index=0, inplace=True)
    all_reviews['products'] = product_list['products']
    all_reviews.to_csv("amazonreviews.csv")
    return all_reviews


def create_reviews_csv():
    products_to_review = input("What products would you like to search for?")
    idis = product_id(products_to_review)
    create_links(idis)


if __name__ == "__main__":
    create_reviews_csv()