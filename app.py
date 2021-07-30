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


@app.route("/pokemon/<search_string>")
def return_pokemon_url(search_string):
    """Route function which takes the query string being passed as part
    of the route and calls getImageURL then returns the URL as JSON.
    :returns: A JSON object containing {img_url: [the image url]}

    """
    data = {'img_url': getPokemonImageURL(search_string)}
    return jsonify(data)

# primary function for getting and returning strings - called by flask


def getGenericImageURL(search_string):
    """getImageURL - given a search string returns the URL to an image
    from IMGUR related to the string

    :search_string: the string describing the subject of the image sought
    :returns: str -> imgURL

    """

    # # link to image of OSU beaver for failed queries
    # failure_image = 'https: // upload.wikimedia.org/wikipedia/en/thumb/1/1b/Oregon_State_Beavers_logo.svg/1200px-Oregon_State_Beavers_logo.svg.png'

    # generate the actual search query and return it

    imgur_base = 'https://www.imgur.com/search?q='
    search_return = executeQuery(imgur_base, search_string)

    # return default image in case of failure
    if search_return[1] is False:
        return search_return[0]

    img_links = search_return[0].find_all('img')

    agnostic_link = img_links[3]['src']

    return 'https:' + agnostic_link


def getPokemonImageURL(pokemon):
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
