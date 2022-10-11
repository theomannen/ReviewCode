
from bs4 import BeautifulSoup as bs
import requesting_urls as req
import re


def get_discipline(type):
    """
    Description, relabels disciplines
    Args:
        type: String, the type of competition

    Returns:
        relabeled type
    """
    type = re.findall(r'[A-Z][A-Z]', type)
    if type[0] == 'GS':
        return "Giant Slalom"
    elif type[0] == 'SL':
        return "Slalom"
    elif type[0] == 'DH':
        return "Down Hill"
    elif type[0] == 'SG':
        return "Super-G"
    elif type[0] == 'PG':
        return "Parallel Giant Slalom"
    elif type[0] == 'AC':
        return "Alpine Combined"
    elif type[0] == 'PS':
        return "Parallel Slalom"
    return 'btivh'


def extract_events(soup):
    """
    Description, this method parses through the table and filters out everything which is not
    date, venue or type. The method uses regex and knowledge of the table to filter these out.
    Args:
        soup: the table of competitions

    Returns:
        List, a new table including only, venue, date, and type
    """
    table = soup.find_all('tr')
    re_table = []
    for x in range(len(table)):
        app = []
        for y in range(3):
            app.append('O')
        re_table.append(app)
    venue = ''

    date_regex = r'.*?\d?\d .*? \d{4}'
    # This regex checks if a cell contains a date
    for x in range(len(table)):
        cells = table[x].find_all('td')
        flag_nr = len(table)
        discipline_nr = len(table)
        for y in range(len(cells)):
            # Adding date
            if re.findall(date_regex, cells[y].text):
                tekst = cells[y].get_text(strip=True)
                if ']' in tekst:
                    tekst = tekst.split(']')[1]

                re_table[x][0] = tekst
                flag_nr = y + 1

            # Adding venue
            if flag_nr == y:
                find = cells[y].find('span', {'class': 'flagicon'})
                if find is not None:
                    re_table[x][1] = cells[y].get_text(strip=True)
                    venue = cells[y].get_text(strip=True)
                    discipline_nr = y + 1
                else:
                    re_table[x][1] = venue
                    re_table[x][2] = get_discipline(cells[y].get_text(strip=True))
                    discipline_nr = len(table)

            # Adding type
            if y == discipline_nr:
                re_table[x][2] = get_discipline(cells[y].get_text(strip=True)[:2])
                discipline_nr = len(table)

    return re_table[1:]


html = req.get_html('https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup')
soup = bs(html, "html.parser")

soup_table = soup.find('table', {"class": 'wikitable plainrowheaders'})

full_table = extract_events(soup_table)

with open('datetime_filter/betting_slip_empty.md', 'w') as file:
    file.write('#BETTING SLIP\n')
    file.write('##Name:\n')

    file.write('| DATE | VENUE | DISCIPLINE | Who Wins? |\n')
    file.write('|:---:|:---:|:---:|:---:|\n')
    for row in full_table:
        file.write('| ')
        for word in row:
            file.write(word + ' | ')
        file.write('    |')
        file.write('\n')

