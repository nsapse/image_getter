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
    data = {'img_url': getImageURL(search_string)}
    return jsonify(data)


# primary function for getting and returning strings - called by flask


def getImageURL(search_string):
    """getImageURL - given a search string returns the URL to an image
    from IMGUR related to the string

    :search_string: the string describing the subject of the image sought
    :returns: str -> imgURL

    """

    # # link to image of OSU beaver for failed queries
    # failure_image = 'https: // upload.wikimedia.org/wikipedia/en/thumb/1/1b/Oregon_State_Beavers_logo.svg/1200px-Oregon_State_Beavers_logo.svg.png'

    # generate the actual search query
    imgur_base = 'https://www.imgur.com/search?q='
    search_query = imgur_base + search_string

    # execute the search
    search_return = requests.get(search_query)

    # if the search fails return the failure image by default
    if search_return.status_code != 200:
        return failure_image

    # otherwise get all image links and return the first one
    # (actually, the third, the first two image links are logos)

    searchable_return = BeautifulSoup(search_return.content, 'html.parser')
    img_links = searchable_return.find_all('img')

    agnostic_link = img_links[3]['src']

    return 'https:' + agnostic_link
