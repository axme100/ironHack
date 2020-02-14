import scrape
import jornada_scraper
import la_prensa_scraper
import excelsior

#myJornadaScraper = jornada_scraper.jornada()
#myJornadaScraper.scrape_la_jornada()
#myJornadaScraper.get_daily_stats()
#
#
#myPrensaScraper = la_prensa_scraper.la_prensa_scraper()
#myPrensaScraper.scrape_la_prensa()
#myPrensaScraper.get_daily_stats()

myExcelsiorScrapper = excelsior.excelsior_scraper()
myExcelsiorScrapper.scrape_excelsior()
myExcelsiorScrapper.get_daily_stats()
