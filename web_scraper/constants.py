url_dict = {
    'E_KORKI_MATH_URL': "https://ekorki.pl/korepetycje/matematyka.html?page=0",
    'E_KORKI_ENGLISH_URL': "https://ekorki.pl/korepetycje/jezyk-angielski.html?page=0",
    'E_KORKI_PHYSICS_URL': "https://ekorki.pl/korepetycje/fizyka.html?page=0",
    'E_KORKI_CHEMISTRY_URL': "https://ekorki.pl/korepetycje/chemia.html?page=0",
    'E_KORKI_POLISH_URL': "https://ekorki.pl/korepetycje/jezyk-polski.html?page=0",
}

# system Chrome driver path
url_path = 'C:/SeleniumDrivers'

"""
  e_korki platform url mathcer (works only for correctly specified fields) ->
  we assume that they are correctly given
"""


def e_korki_mapper(subject):
    return url_dict[f'E_KORKI_{subject.upper()}_URL']


# indirect path to resource folder where temporarily csv and excel files are stored
RESOURCES = "./resources/"
