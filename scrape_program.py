import scrape


sites_to_scrape = [  # Excelsior
                    {"name": "Excelsior",
                     "link": "https://www.excelsior.com.mx/rss.xml",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "node-article-body"}},
                    # La jornada
                    {"name": "La Jornada",
                     "link": "https://www.jornada.com.mx/rss/edicion.xml?v=1",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "article-text"}},
                    # El País
                    {"name": "El país",
                     "link": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "articulo_contenedor"}},
                    # Expansión
                    {"name": "Expansión - Economía",
                     "link": "https://expansion.mx/rss/nacional",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "class",
                      "target_tag_att_value": "ArticlePage-articleBody"}},
                    # La razón
                    {"name": "La Razón",
                     "link": "https://www.razon.com.mx/feed/",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "class",
                      "target_tag_att_value": "td-post-content"}},
                    {"name": "El sol de México",
                     "link": "https://www.elsoldemexico.com.mx/rss.xml",
                     "soup_info":
                     {"target_tag": "section",
                      "target_tag_att": "class",
                      "target_tag_att_value": "col-sm-8"}}
                      ]

for site in sites_to_scrape:
    scraper = scrape.daily_scraper(site['link'],
                                   site['name'],
                                   site['soup_info'])

    scraper.get_target_articles_to_scrape()
    scraper.scrape_articles()
    scraper.get_daily_stats()
