import requests
from bs4 import BeautifulSoup


def getPokemonImageURL(name: str):
    pokemon_base = 'https://bulbapedia.bulbagarden.net/wiki/'
    pokemon_suffix = '_(Pokemon)'

    pokemon_url = pokemon_base + name + pokemon_suffix

    page = requests.get(pokemon_url)

    if page.status_code != 200:
        print("error: no pokemon of that name")
        return False

    parsed_page = BeautifulSoup(page.content, 'html.parser')

    links = parsed_page.find_all('a')

    for link in links:
        title = link.get('title')
        if title:
            if title.lower() == name.lower():
                image_link = link.findChildren('img')
                print('http:' + image_link[0]['src'])
                break


getPokemonImageURL('charmander')
getPokemonImageURL('pikachu')
getPokemonImageURL('bulbasaur')
