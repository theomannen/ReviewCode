from bs4 import BeautifulSoup as bs
import requesting_urls as req
import re
import matplotlib.pyplot as plt

base_url = 'https://en.wikipedia.org'
html = req.get_html('https://en.wikipedia.org/wiki/2020_NBA_playoffs')
soup = bs(html, "html.parser")

soup_table = soup.find('table', {"style": 'font-size: 90%; margin:1em 2em 1em 1em;'})
rows = soup_table.find_all('tr')
regex = r'[A-Z]\d'
list_of_semi = []
for row in rows:
    data = row.find_all('td')
    if not len(data) < 4:
        ting = re.findall(regex, data[2].text)
        if len(ting) == 1:
            add = re.findall(r'(.*?)[*|\n]', data[3].text)[0]
            if add not in list_of_semi:
                list_of_semi.append(add)


def check_float(potential_float):
    """

    Args:
        potential_float: Float, value that could be float

    Returns:
        Boolean, whether potential_float is a float or not
    """
    try:
        float(potential_float)
        return True
    except ValueError:
        return False


def extract_url(table, teams):
    """

    Args:
        table: soup table of the html
        teams: list of teams that made it to Conference Semifinals

    Returns:
        List: list of urls to the teams that made it to the Conference Semifinals
    """
    return_list = []

    team_rows = table.find_all('tr')
    for team_row in team_rows:
        team_data = team_row.find_all('td')
        for cell in team_data:
            link = cell.find('a')
            if link and re.findall(r'(.*?)[*|\n]', cell.text)[0] in teams:
                full_link = base_url + cell.find('a').attrs['href']
                if full_link not in return_list:
                    return_list.append(full_link)

    return return_list


team_urls = extract_url(soup_table, list_of_semi)
print('\n\n\n')
print(len(team_urls))
print(team_urls)
print(len(list_of_semi))
print(list_of_semi)

ppg = {}
bpg = {}
rpg = {}


def fill_lists(url):
    """
    Description: This method crawls through a teams url to find the player roster table.
    We then find all links in a given column position, which we then add to a list.
    Args:
        url: String, url of a team

    Returns:
        List: list of player urls for a given team
    """
    player_list = []
    team_html = req.get_html(url)
    full = bs(team_html, "html.parser")
    var1 = full.find('table', {'class': 'toccolours'})
    body = var1.find('tbody')
    body_tr = body.find_all('tr')
    for tr in body_tr:
        table_data = tr.find_all('td')
        if len(table_data) > 2:
            link = table_data[2].find('a')
            if link:
                player_list.append((base_url + table_data[2].find('a').attrs['href']))
    return player_list


player_urls = []
for url in team_urls:

    print(list_of_semi[team_urls.index(url)])
    player_urls.append(fill_lists(url))


def swap(list, point, player, re, bl):
    """
    Description, this method swaps out players in the list if their score is higher than another players
    score. The method also makes sure they are in order

    Args:
        list: list of players, and their points
        point: Float, ppg for given player
        player: String, name of given player
        re: Float, rpg for given player
        bl: Float, bpg for given player

    Returns:
        List, new adjusted list
    """
    for x in list:
        if x[1][0] < point:
            print('swap')
            print(x[0])

            for y in range(len(list)-1, list.index(x), -1):
                print(list)
                if y >= 0:
                    list[y] = list[y-1]
            print(list)
            print('swapping ' + str(list[list.index(x)]) + ' and ' + player + str(point))

            list[list.index(x)] = (player, [point, re, bl])
            print(list)

            return list
    return list

"""

The following for-loop is the essential part of this script:
This for-loop parses through all teams, then all players.
We then find the first table after finding the headline "NBA", so that we are sure it is the NBA 
point table we are looking at. The program also has to take into account that the 19/20 row could be a 
link or not, meaning we have to check for an 'a' in the html.

"""
for team in player_urls:
    print(list_of_semi[player_urls.index(team)])
    go = True
    top_p = []
    for x in range(3):
        top_p.append(('', [0, 0, 0]))
    top_b = []
    for x in range(3):
        top_b.append(('', [0, 0, 0]))
    top_r = []
    for x in range(3):
        top_r.append(('', [0, 0, 0]))
    print(top_p)
    for player in team:
        print(player)
        player_name = player.split('/')[len(player.split('/'))-1]
        player_name = re.findall(r'([\w.-]*?)([^\w.-]|$)', player_name)
        if len(player_name) > 1:
            player_name = player_name[0][0]
        player_html = req.get_html(player)
        soup = bs(player_html, "html.parser")
        headlines = soup.find_all('h3')
        for headline in headlines:
            spans = headline.find_all('span')
            for span in spans:
                if span.text == 'NBA':
                    print('NBA found')
                    go = True
        if go:
            split_html = player_html.split('>NBA<')[1]
            split_soup = bs(split_html, 'html.parser')
            point_tables = soup.find_all('table', {'class': 'wikitable sortable'})
            if len(point_tables) > 0:
                table_rows = point_tables[0].find_all('tr')
                for season in table_rows:
                    cells = season.find_all('td')
                    if len(cells) > 0:

                        link = cells[0].find_all('a')
                        if len(link) > 0:
                            print(link[0].text)
                            check_year = re.findall(r'.*?19.20', link[0].text)
                        else:
                            check_year = re.findall(r'.*?19.20', cells[0].text)
                        print(check_year)
                        if len(check_year) > 0:

                            print('ferferferferferffr')
                            print(cells[12].text)
                            rebound = 0
                            block = 0
                            if check_float(cells[8].text):
                                rebound = cells[8].text
                            if check_float(cells[11].text):
                                block = cells[11].text
                            if check_float(cells[12].text):
                                points = float(cells[12].text)
                                top_p = swap(top_p, points, player_name, rebound, block)

    ppg[list_of_semi[player_urls.index(team)]] = top_p

print(ppg)

p_table = []
b_table = []
r_table = []

"""

Fills list with 0 before commas that are missing them

"""
for team in list_of_semi:
    for player in ppg[team]:
        in1 = str(player[1][0])
        if in1[0] == '.':
            in1 = '0' + in1
        in2 = str(player[1][1])
        if in2[0] == '.':
            in2 = '0' + in2
        in3 = str(player[1][2])
        if in3[0] == '.':
            in3 = '0' + in3

        p_table.append([team, player[0], in1])
        b_table.append([team, player[0], in2])
        r_table.append([team, player[0], in3])


def save(col, bord, name):
    """
    Description, this method creates and saves a matplotlib pyplot as a png
    Args:
        col: List, names of the columns
        bord: List, table of players, teams, and points
        name: String, name of file

    Returns:
        nothing
    """
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=bord, colLabels=col, loc='center')
    plt.savefig('NBA_player_statistics/' + name)


save(('TEAM', 'NAME', 'PPG'), p_table, 'players_over_ppg.png')
save(('TEAM', 'NAME', 'BPG'), b_table, 'players_over_bpg.png')
save(('TEAM', 'NAME', 'RPG'), r_table, 'players_over_rpg.png')
