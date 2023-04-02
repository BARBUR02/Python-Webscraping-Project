import pandas as pd
from web_scraper.web_scraper import TutoringOffer
import web_scraper.constants as const


"""
  Parser responsible for saving data to CSV and excel files to investigate
  efficiency of scraping
"""


class OfferParser:
    def __init__(self, offer_list) -> None:
        self.offers = offer_list

    """
      RESOURCES - direct path to resources folder -> By default in resources directory
    """

    def save_to_csv(self, file_name):
        df = pd.DataFrame(self.offers)
        path = const.RESOURCES+file_name
        df.to_csv(path, index=False, encoding="utf-8")

    def save_to_excel(self, file_name):
        df = pd.DataFrame(self.offers)
        path = const.RESOURCES+file_name
        df.to_excel(path, sheet_name=file_name)
    