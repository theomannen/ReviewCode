import requests


def get_html(url, params=None, output=None):
    """
    Description, the method finds the html of a url
    Args:
        url: url of a website
        params: paramaters of get call
        output: name of file to be saved

    Returns:
        String: the html text of a website
    """
    r = requests.get(url, params=params)
    if output is not None:
        with open('requesting_urls/' + output, 'w') as file:
            file.write(r.url)
            file.write(r.text)
        return r.text
    return r.text


ghibli = 'https://en.wikipedia.org/wiki/Studio_Ghibli'
star_wars = 'https://en.wikipedia.org/wiki/Star_Wars'
dnd = 'https://en.wikipedia.org/wiki/Dungeons_%26_Dragons'
php = 'https://en.wikipedia.org/w/index.php'

get_html(ghibli, None, 'ghibli.txt')
get_html(star_wars, None, 'star_wars.txt')
get_html(dnd, None, 'dnd.txt')

params_1 = {'title': 'Main Page', 'action': 'info'}
params_2 = {'title': 'Hurricane Gonzalo', 'oldid': '983056166'}

get_html(php, params_1, 'php1.txt')
get_html(php, params_2, 'php2.txt')
