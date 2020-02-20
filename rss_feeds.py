sites_to_scrape = [  # Excelsior
                    {"name": "Excelsior",
                     "link": "https://www.excelsior.com.mx/rss.xml",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "node-article-body"},
                     "custom_regex_trimming": [r"^[A-ZÁÍÚÉÓÑ\s]+(?=[A-ZÁÍÚÉÓ][a-z])|(^[A-ZÁÍÚÉÓ\s]+\.)", r"La ley de derechos de autor prohíbe estrictamente.*"]},
                    # La jornada
                    {"name": "La Jornada",
                     "link": "https://www.jornada.com.mx/rss/edicion.xml?v=1",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "article-text"},
                     "custom_regex_trimming": []},
                    # El País (España)
                    {"name": "El país (España)",
                     "link": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "articulo_contenedor"},
                     "custom_regex_trimming": [r'Se adhiere a los criterios deM.*']},
                    # El país (América)
                    {"name": "El país (América)",
                     "link": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "articulo_contenedor"},
                     "custom_regex_trimming": [r'Se adhiere a los criterios deM.*']},
                    # Expansión - Economía
                    {"name": "Expansión - Nacional",
                     "link": "https://expansion.mx/rss/nacional",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "class",
                      "target_tag_att_value": "ArticlePage-articleBody"},
                     "custom_regex_trimming": []},
                    # Expansión Portada
                    {"name": "Expansión - Portada",
                     "link": "https://expansion.mx/rss",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"},
                     "custom_regex_trimming": []},
                    # Expansión empresas
                    {"name": "Expansión - Empresas",
                     "link": "https://expansion.mx/rss/empresas",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"},
                     "custom_regex_trimming": []},
                    # Expansión nacional
                    {"name": "Expansión - Nacional",
                     "link": "https://expansion.mx/rss/nacional",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"},
                     "custom_regex_trimming": []},
                    # Expansión technología
                    {"name": "Expansión - Tecnología",
                     "link": "https://expansion.mx/rss/tecnologia",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"},
                     "custom_regex_trimming": []},
                    # Expansión carrera
                    {"name": "Expansión - Carrera",
                     "link": "https://expansion.mx/rss/carrera",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"},
                     "custom_regex_trimming": []},
                    # Expansión dinero
                    {"name": "Expansión - Dinero",
                     "link": "https://expansion.mx/rss/dinero",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"},
                     "custom_regex_trimming": []},
                    # Expansión Emprendedores
                    {"name": "Expansión - Emprendedores",
                     "link": "https://expansion.mx/rss/emprendedores",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"},
                     "custom_regex_trimming": []},
                    # Expansión Opinión
                    {"name": "Expansión - Opinión",
                     "link": "https://expansion.mx/rss/opinion",
                     "soup_info":
                     {"target_tag": "article",
                      "target_tag_att": "itemprop",
                      "target_tag_att_value": "articleBody"},
                     "custom_regex_trimming": []},
                    # EFE SPAIN
                    {"name": "EFE (España)",
                     "link": "https://www.efe.com/efe/espana/1/rss",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "div_texto"},
                     "custom_regex_trimming": []},
                    # EFE AMÉRICA
                    {"name": "EFE (América)",
                     "link": "https://www.efe.com/efe/america/2/rss",
                     "soup_info":
                     {"target_tag": "div",
                      "target_tag_att": "id",
                      "target_tag_att_value": "div_texto"},
                     "custom_regex_trimming": []}
                     ]
