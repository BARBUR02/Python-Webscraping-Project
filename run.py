from web_scraper.web_scraper import TutoringScraper, E_KORKI
from web_scraper.offer_parser import OfferParser
import time
import pandas as pd

"""
  Scraping data from e_korki website
"""
with E_KORKI() as bot:
    bot.scrape_subjects(
        ["math", "polish", "english", "chemistry", "physics"], 4)  # valid subjects specified in web_scraper.constants.py                                                           # num of pages per subject
    parser = OfferParser(bot.offers)
    parser.save_to_csv('e_korki_offers.csv')
    parser.save_to_excel('e_korki_offers.xlsx')
    print(f"Ilosc obiektów: {len(bot.offers)}")
    print("Exiting...")
