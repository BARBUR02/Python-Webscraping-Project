import os
from selenium import webdriver
import time
from dataclasses import dataclass
import web_scraper.constants as const
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By

"""
    dataclass for storing offer objects
    basic data fields + link from offer HTML anchor tag
"""


@dataclass
class TutoringOffer:
    subject: str
    name: str
    price: int
    city: str
    description: str
    link: str


"""
    Class performing scraping
"""


class TutoringScraper(webdriver.Chrome, ABC):
    # indirect path in my system to chrome driver
    def __init__(self):
        self.curr_page = 0
        self.curr_page_url = None
        self.offers = []
        self.driver_path = const.url_path  # located in constants.py module
        os.environ['PATH'] += self.driver_path
        super(TutoringScraper, self).__init__()
        self.implicitly_wait(10)
        self.maximize_window()

    """
        scrapes given subjects ->  maps subject strings to links given mapping functions
        specified in constants.py file ( different for each site )
    """
    @abstractmethod
    def scrape_subjects(self, subjects, page_num):
        pass

    """
        scrapes given amount of pages -> scrapes given amount of pages for specified subject ( called from scrape_subjects )
    """
    @abstractmethod
    def scrape_pages(self, page_num):
        pass

    """
        scrapes offer from more general HTML element (ex. div containing all interesting information )
    """
    @abstractmethod
    def scrape_offer(self, offer_element):
        pass

    """
        Loads next page inside given subject ( used by scrape pages )
    """
    @abstractmethod
    def load_next_page(self):
        pass

    """
        web popup destructor -> kills web pop up process after scraping
    """

    def __exit__(self, *args):
        self.quit()
        return super().__exit__(*args)


class E_KORKI(TutoringScraper):
    def __init__(self):
        super().__init__()

    def scrape_subjects(self, subjects, page_num):
        func = const.e_korki_mapper
        urls = list(map(func, subjects))
        for url in urls:
            self.get(url)
            self.curr_page_url = url
            self.curr_page = 0
            self.scrape_pages(page_num)

    def scrape_pages(self, page_num):
        for _ in range(page_num):
            # offers_elements = self.find_elements_by_class_name('certificate_trow')
            offers_elements = self.find_elements(By.CLASS_NAME,'certificate_trow')
            for offer_el in offers_elements:
                self.offers.append(self.scrape_offer(offer_el))
            self.load_next_page()

    def scrape_offer(self, offer_element):
        # subject = offer_element.find_element_by_tag_name("strong").text.strip()
        subject = offer_element.find_element(By.TAG_NAME,"strong").text.strip()
        # name = offer_element.find_element_by_class_name("offermainlisting_item-subject").text.strip()
        name = offer_element.find_element(By.CLASS_NAME,"offermainlisting_item-subject").text.strip()
        # price = offer_element.find_element_by_class_name("pr0").text
        price = offer_element.find_element(By.CLASS_NAME,"pr0").text
        price = price.split()[0]
        price = int(price.strip().split(',')[0])
        # place = offer_element.find_element_by_class_name("offermainlisting_item-place").text.split(',')
        place = offer_element.find_element(By.CLASS_NAME,"offermainlisting_item-place").text.split(',')
        place = place[1:] if place[0].lower() == 'online' else place[0].strip()
        if isinstance(place, list):
            place = ' '.join(place).strip()
        # description = offer_element.find_element_by_class_name("offermainlisting_item-desc").text.strip()
        description = offer_element.find_element(By.CLASS_NAME,"offermainlisting_item-desc").text.strip()
        # link = offer_element.find_element_by_class_name("offermainlisting_item-desc").find_element_by_tag_name('a').get_attribute("href").strip()
        link = offer_element.find_element(By.CLASS_NAME,"offermainlisting_item-desc").find_element(By.TAG_NAME,'a').get_attribute("href").strip()
        return TutoringOffer(subject, name, price, place, description, link)

    def increment_page(self):
        self.curr_page += 1

    def load_next_page(self):
        self.increment_page()
        path = self.curr_page_url[:-1] + str(self.curr_page)
        self.get(path)
