import feedparser
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import article


#  Define a class of scraper
class daily_scraper:

    def __init__(self, target_xml_url, publication, div_info):
        self.publication = publication
        self.articles_scraped_no_errors = []
        self.articles_scraped_with_errors = []
        self.target_xml_url = target_xml_url
        # In this case, the  list attribute urls to scrape is
        # automatically set as soon as the object is created
        self.articles_to_scrape = []
        self.div_info = div_info
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0'}

    def trackScrapes(self, rawArticle):

        # If the raw articles does not have any errors
        if not rawArticle.errors:
            # Add the URL to the list of articles that were
            # sraped with sucsess
            self.articles_scraped_no_errors.append(rawArticle.url)

        # In case the aricles does have errors
        else:
            self.articles_scraped_with_errors.append([rawArticle.url,
                                                      rawArticle.errors])

    def get_daily_stats(self):

        print("Total Artciles Scraped: " + str(len(self.articles_scraped_no_errors) + len(self.articles_scraped_with_errors)))
        print("Articles With Errors: " + str(len(self.articles_scraped_with_errors)))

        print("Errors: ")

        for problemArticle in self.articles_scraped_with_errors:
            print("url: " + problemArticle[0])
            print("")
            for error in problemArticle[1]:
                print(error)

    def get_target_articles_to_scrape(self):

        parsed_xml = feedparser.parse(self.target_xml_url)

        for entry in parsed_xml['entries']:

            # Get the author field of the XML document
            # If there is none leave it blank
            try:
                xml_author = entry['author']
            except KeyError as keyError:
                xml_author = ''
                print(keyError)

            # Create an article object
            article_to_add = article.rawArticle(url=entry['link'],
                                                title=entry['title'],
                                                date=entry['published'],
                                                publication=self.publication,
                                                xml_author=xml_author)

            if article_to_add.check_for_url_duplicate() is False:

                # Add the target article object to the scraper obje t
                self.articles_to_scrape.append(article_to_add)

            else:
                print("Article URL already present in the database")

    def configure_transport_adapter(self, domain):

        # In order to set the max_retries we need to:
        # create a re request.Session()
        # And Mount the transport adapter to it:
        # https://realpython.com/python-requests/#ssl-certificate-verification
        # The specific implementation strategy here is more similar to:
        # https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
        session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        transport_adapter = HTTPAdapter(max_retries=retries)

        session.mount(domain, transport_adapter)

        return session

    # Go through the article objects and scrape each one
    def scrape_articles(self):

        for my_article in self.articles_to_scrape:

            # Configure session to article domain name
            session = self.configure_transport_adapter(my_article.get_domain())

            try:
                html_soup = session.get(my_article.get_url(), headers=self.headers)
                parsed_soup = BeautifulSoup(html_soup.text, 'html.parser')

            except ConnectionError as ce:
                my_article.add_error({"HTTP Connection Error": repr(ce)})

            # Get the text from the article
            try:
                # Get the article text
                articleText = parsed_soup.find(self.div_info['target_tag'],
                                               {self.div_info['target_tag_att']: self.div_info['target_tag_att_value']})

                # This will get rid of any text within javascript tags not wanted
                try:
                    for script in articleText("script"):
                        script.decompose()
                # Just do not use a bare except
                except Exception:
                    pass

                # Get text and clean it ups
                articleText = articleText.get_text().replace('\n', '').strip()

                my_article.set_article_text(articleText)
                print(articleText)

            except AttributeError as error:
                my_article.add_error({"Error getting article text: ": repr(error)})

            my_article.save_to_database()

            self.trackScrapes(my_article)
