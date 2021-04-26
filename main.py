from read_data import get_data
from scraper import *

if __name__ == '__main__':
    # call get_data <- this will create a list for all posts
    get_data()
    # create scraper object
    scraper = scraper()
    # call initialize_scrapper <- this will take said list and scrape ALL comments from ALL posts! #awesome! :D
    initialize_scrapper()
