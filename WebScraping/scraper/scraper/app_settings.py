_e_korepetycje = "https://www.e-korepetycje.net/"
#_e_korki = ...
#_3rd_website = ...


def parse_e_korepetycje():
    subjects = ["chemia", "jezyk-polski", "matematyka", "fizyka", "jezyk-angielski"]
    return list(map(lambda x: _e_korepetycje + x, subjects))

def parse_e_korki():
    pass

def parse_3rd_website():
    pass

E_KOREPETYCJE_URLS = parse_e_korepetycje()
# URLS = parse_e_korepetycje() + parse_e_korki() + parse_3rd_website()