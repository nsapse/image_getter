import requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup


# Flask Setup

app = Flask(__name__)
failure_image = 'https: // upload.wikimedia.org/wikipedia/en/thumb/1/1b/Oregon_State_Beavers_logo.svg/1200px-Oregon_State_Beavers_logo.svg.png'


# if no search string is entered return the fallback beaver logo
@app.route("/")
def no_input():
    data = {'img_url': failure_image}
    return jsonify(data)


# else, return the image from imgur
@app.route("/<search_string>")
def return_img_url(search_string):
    """Route function which takes the query string being passed as part
    of the route and calls getImageURL then returns the URL as JSON.
    :returns: A JSON object containing {img_url: [the image url]}

    """
    data = {'img_url': getGenericImageURL(search_string)}
    return jsonify(data)


@app.route("/pokemon/<pokemon_name>")
def return_pokemon_url(pokemon_name: str):
    data = {'img_url': getPokemonImageURL(pokemon_name)}
    return jsonify(data)


@app.route("/wikipedia/<search_string>")
def return_wikipedia_url(search_string):
    """Route function which takes the query string being passed as part
    of the route and calls getImageURL then returns the URL as JSON.
    :returns: A JSON object containing {img_url: [the image url]}

    """
    data = {'img_url': wikiImageURL(search_string)}
    return jsonify(data)

# primary function for getting and returning strings - called by flask


def getGenericImageURL(search_string):
    """getImageURL - given a search string returns the URL to an image
    from IMGUR related to the string

    :search_string: the string describing the subject of the image sought
    :returns: str -> imgURL

    """

    # generate the actual search query and return it

    imgur_base = 'https://www.imgur.com/search?q='
    search_return = executeQuery(imgur_base, search_string)

    # return default image in case of failure
    if search_return[1] is False:
        return search_return[0]

    img_links = search_return[0].find_all('img')

    agnostic_link = img_links[3]['src']

    return 'https:' + agnostic_link


def wikiImageURL(pokemon):
    """getPokemonImageURL- given a search string returns the URL to an image
    of a Pokemon from Wikipedia related to the string

    :search_string: the string describing the subject of the
    image sought (MUST BE A POKEMON)

    :returns: str -> imgURL

    """

    wiki_base = 'https://en.wikipedia.org/wiki/'
    search_return = executeQuery(wiki_base, pokemon)

    # return default image in case of failure
    if search_return[1] is False:
        return search_return[0]

    images = search_return[0].find_all('img')
    image_link = images[0]['src']

    print('https:' + image_link)
    return 'https:' + image_link


def executeQuery(baseURL: str, searchSTR: str):

    # build the search URL
    searchURL = baseURL + searchSTR

    # execute the actual request
    search_return = requests.get(searchURL)
    if search_return.status_code != 200:
        return (failure_image, False)

    # otherwise get all image links and return the first one
    # (actually, the third, the first two image links are logos)

    parsed_content = BeautifulSoup(search_return.content, 'html.parser')

    return (parsed_content, True)


def getPokemonImageURL(name: str):
    pokemon_base = 'https://bulbapedia.bulbagarden.net/wiki/'
    pokemon_suffix = '_(Pokemon)'

    pokemon_url = pokemon_base + name + pokemon_suffix

    page = requests.get(pokemon_url)

    if page.status_code != 200:
        print("error: no pokemon of that name")
        return(failure_image,  False)

    parsed_page = BeautifulSoup(page.content, 'html.parser')

    links = parsed_page.find_all('a')

    for link in links:
        title = link.get('title')
        if title:
            if title.lower() == name.lower():
                image_link = link.findChildren('img')
                return ('http:' + image_link[0]['src'])
