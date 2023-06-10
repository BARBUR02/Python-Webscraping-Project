_e_korepetycje = "https://www.e-korepetycje.net/"
_e_korki = "https://ekorki.pl/korepetycje/"
_korepetycje = "https://korepetycje.pl/"

SUBJECTS = ["chemia", "jezyk-polski",
            "matematyka", "fizyka", "jezyk-angielski"]


def parse_e_korepetycje():
    return list(map(lambda x: _e_korepetycje + x, SUBJECTS))


def parse_e_korki():
    return list(map(lambda x: _e_korki+x, SUBJECTS))


def parse_korepetycje():
    return list(map(lambda x: _korepetycje+x, SUBJECTS))


E_KOREPETYCJE_URLS = parse_e_korepetycje()
E_KORKI_URLS = parse_e_korki()
KOREPETYCJE_URLS = parse_korepetycje()
# URLS = parse_e_korepetycje() + parse_e_korki() + parse_3rd_website()
