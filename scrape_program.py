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
                    # El País (España)
                    {"name": "El país (España)",
                     "link": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "articulo_contenedor"}},
                    # El país (América)
                    {"name": "El país (América)",
                     "link": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "articulo_contenedor"}},
                    # Expansión - Economía
                    {"name": "Expansión - Nacional",
                     "link": "https://expansion.mx/rss/nacional",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "class",
                      "target_tag_att_value": "ArticlePage-articleBody"}},
                    # Expansión Portada
                    {"name": "Expansión - Portada",
                     "link": "https://expansion.mx/rss",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"}},
                    # Expansión empresas
                    {"name": "Expansión - Empresas",
                     "link": "https://expansion.mx/rss/empresas",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"}},
                    # Expansión nacional
                    {"name": "Expansión - Nacional",
                     "link": "https://expansion.mx/rss/nacional",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"}},
                    # Expansión technología
                    {"name": "Expansión - Tecnología",
                     "link": "https://expansion.mx/rss/tecnologia",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"}},
                    # Expansión carrera
                    {"name": "Expansión - Carrera",
                     "link": "https://expansion.mx/rss/carrera",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"}},
                    # Expansión dinero
                    {"name": "Expansión - Dinero",
                     "link": "https://expansion.mx/rss/dinero",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"}},
                    # Expansión Emprendedores
                    {"name": "Expansión - Emprendedores",
                     "link": "https://expansion.mx/rss/emprendedores",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"}},
                    # Expansión Opinión
                    {"name": "Expansión - Opinión",
                     "link": "https://expansion.mx/rss/opinion",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"}},
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


if __name__ == "__main__":
  for site in sites_to_scrape:
    scraper = scrape.daily_scraper(site['link'],
                                   site['name'],
                                   site['soup_info'])

    scraper.get_target_articles_to_scrape()
    scraper.scrape_articles()
    scraper.get_daily_stats()