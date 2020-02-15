import scrape
import excelsior


excelsior_scraper = scrape.daily_scraper("https://www.excelsior.com.mx/rss.xml", 
										"Excelsior",
										{"target_tag": "div",
										"target_tag_att": "id",
										"target_tag_att_value": "node-article-body"})

excelsior_scraper.get_target_articles_to_scrape()
excelsior_scraper.scrape_articles()
excelsior_scraper.get_daily_stats()



jornada_scraper = scrape.daily_scraper("https://www.jornada.com.mx/rss/edicion.xml?v=1", 
										"La Jornada",
										{"target_tag": "div",
										"target_tag_att": "id",
										"target_tag_att_value": "article-text"})

jornada_scraper.get_target_articles_to_scrape()
jornada_scraper.scrape_articles()
jornada_scraper.get_daily_stats()


el_pais_scraper = scrape.daily_scraper("https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
									  "El País",
									  {"target_tag": "div",
									  "target_tag_att": "id",
									  "target_tag_att_value": "articulo_contenedor"})

el_pais_scraper.get_target_articles_to_scrape()
el_pais_scraper.scrape_articles()
el_pais_scraper.get_daily_stats()