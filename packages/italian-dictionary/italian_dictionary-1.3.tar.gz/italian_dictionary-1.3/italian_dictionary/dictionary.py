from italian_dictionary import scraper

URL = "https://www.dizionario-italiano.it/dizionario-italiano.php?parola={}"


# ------italian_dictionary-------
def get_definition(word, all_data=True,limit=None):
     if all_data:
         return scraper.get_all_data(word)
     else:
        defs = scraper.get_defs(word)
        if limit is not None and len(defs) > limit:
            del defs[limit:]
        return defs
