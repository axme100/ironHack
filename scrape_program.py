import rss_feeds
import scrape

if __name__ == "__main__":
    for site in rss_feeds.sites_to_scrape:
        scraper = scrape.daily_scraper(site['link'], site['name'], site['soup_info'])
        scraper.get_target_articles_to_scrape()
        scraper.scrape_articles(site['custom_regex_trimming'])
        scraper.get_daily_stats()
