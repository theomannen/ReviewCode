import requesting_urls
import re

baseURL = 'https://en.wikipedia.org'


def find_urls(html):
    """
    Description, the method parses through the html, and uses the regex to find urls
    Args:
        html: HTML file of the given url

    Returns:
        urls: list, list of all urls in the html
    """

    regex = r'<a href ?=\"([^#:].*?[^#:])[?|\"|(|#]'
    # This regex finds all urls using the "<a href" keyword. The following regex commands attempts to
    # end the line at all possible endings, while including the entire urls

    urls = re.findall(regex, html)
    for x in range(len(urls)):
        if urls[x][1] == '/':
            urls[x] = 'https:' + urls[x]
        elif urls[x][0] == '/':
            urls[x] = baseURL + '/' + urls[x]

        frag = urls[x].split(':')
        urls[x] = frag[0] + ':' + frag[1]

        if urls[x][0] != 'h' and urls[x][0] != 'H':
            urls[x] = 'https://' + urls[x]

    print(urls)
    return urls


def find_articles(url, output=None):
    """
    Description, finds all urls in the website using the method above,
    then filters out all websites that do not contain wikipedia.
    Args:
        url: url of a website
        output: Name of the file to be saved

    Returns:
        list of all urls in the website that lead to wikipedia
    """
    text = requesting_urls.get_html(url)
    urls = find_urls(text)
    regex = r'https://.*?.?wikipedia.org.*'
    # This regex finds wikipedia urls
    matches = [re.findall(regex, url) for url in urls]
    matches = [x for x in matches if x]
    if output is None:
        output = 'no_name.txt'
    with open('filter_urls/' + output, 'w') as file:
        file.write('All urls\n')
        for url in urls:
            file.write(url + "\n")
        file.write('\nAll matches\n')
        for url_match in matches:
            for wiki in url_match:
                file.write(wiki + "\n")
    print(matches)
    return matches


find_articles('https://en.wikipedia.org/wiki/Nobel_Prize', 'Nobel_Prize_Urls.txt')
find_articles('https://en.wikipedia.org/wiki/Bundesliga', 'Bundesliga_Urls.txt')
find_articles('https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup', 'Alpine_Urls.txt')
