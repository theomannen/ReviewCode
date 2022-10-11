import requesting_urls
import re


def month(string):
    """
    Description: converts months from string to digits
    Args:
        string: String, the month in chars

    Returns:
        String: the month in digits
    """
    if string == 'Jan' or string == 'January':
        return '01'
    elif string == 'Feb' or string == 'February':
        return '02'
    elif string == 'Mar' or string == 'March':
        return '03'
    elif string == 'Apr' or string == 'April':
        return '04'
    elif string == 'May':
        return '05'
    elif string == 'Jun' or string == 'June':
        return '06'
    elif string == 'Jul' or string == 'July':
        return '07'
    elif string == 'Aug' or string == 'August':
        return '08'
    elif string == 'Sep' or string == 'September':
        return '09'
    elif string == 'Oct' or string == 'October':
        return '10'
    elif string == 'Nov' or string == 'November':
        return '11'
    elif string == 'Dec' or string == 'December':
        return '12'
    else:
        print('invalid month')


def find_dates(html, output=None):
    """
    Description: This method searches through the given HTML file using regular expressions.
                The expresseions filters all types of dates that can be cound in the file.
    Args:
        html: The entire file of the given url in HTML format
        output: The name of the filename, which is to be saved

    Returns:
        List: Returns all dates found
    """
    regexISO = r'\d{4}-[0-1]\d-[0-3]\d'
    # This regex finds 4 consecutive digits, followed by a '-' followed
    # by 0 or 1, followed by a digit, followed by a digit between 0 and 3, followed by a digit.
    # This results in the format YYYY-MM-DD
    ISO_dates = re.findall(regexISO, html)
    regexDMY = r'([0-3]\d (January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug' \
               r'|September|Sept|October|Oct|November|Nov|December|Dec) \d{4})'
    # This regex finds a digit between 0 and 3, followed by a digit, followed by a month in
    # String format, followed by 4 consecutive digits.
    # This results in the format DD-MONTH-YYYY
    DMY_dates = re.findall(regexDMY, html)
    regexMDY = r'((January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug' \
               r'|September|Sept|October|Oct|November|Nov|December|Dec) [0-3]\d, \d{4})'
    # This regex finds a month in String format, followed by a digit between 0 and 3, followed by a comma,
    # followed by a digit, followed by 4 consecutive digits.
    # This results in the format MONTH-DD-YYYY
    MDY_dates = re.findall(regexMDY, html)
    regexYMD = r'(\d{4} (January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug' \
               r'|September|Sept|October|Oct|November|Nov|December|Dec) [0-3]\d)'
    # This regex finds 4 consecutive digits, followed by a month in String format,
    # followed by a digit between 0 and 3, followed by a digit.
    # This results in the format YYYY-MONTH-DD
    YMD_dates = re.findall(regexYMD, html)
    regexMY = r'[^\d][^\d] ?((January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug' \
              r'|September|Sept|October|Oct|November|Nov|December|Dec) \d{4})'
    # This regex finds a month in String format, followed by 4 consecutive digits.
    # This results in the format MONTH-YYYY
    MY_dates = re.findall(regexMY, html)
    print(len(MY_dates))
    list_of_dates = []

    for date in ISO_dates:
        inn_date = date[:4] + '/' + date[5:7] + '/' + date[8:]
        list_of_dates.append(inn_date)
    for date in DMY_dates:
        frag = date[0].split(' ')
        inn_date = frag[2] + '/' + month(frag[1]) + '/' + frag[0]
        list_of_dates.append(inn_date)
    for date in MDY_dates:
        frag = date[0].split(' ')
        inn_date = frag[2] + '/' + month(frag[0]) + '/' + frag[1][:2]
        list_of_dates.append(inn_date)
    for date in YMD_dates:
        frag = date[0].split(' ')
        inn_date = frag[0] + '/' + month(frag[1]) + '/' + frag[2]
        list_of_dates.append(inn_date)
    for date in MY_dates:
        frag = date[0].split(' ')
        inn_date = frag[1] + '/' + month(frag[0])
        list_of_dates.append(inn_date)

    if output is not None:
        list_of_dates.sort()
        with open('filter_dates_regex/' + output, 'w') as file:
            for date in list_of_dates:
                file.write(date + '\n')

    return list_of_dates


text = requesting_urls.get_html('https://en.wikipedia.org/wiki/Linus_Pauling')
find_dates(text, 'Linus_Pauling_dates.txt')
text = requesting_urls.get_html('https://en.wikipedia.org/wiki/Rafael_Nadal')
find_dates(text, 'Rafael_Nadal_dates.txt')
text = requesting_urls.get_html('https://en.wikipedia.org/wiki/J._K._Rowling')
find_dates(text, 'J_K_Rowling.txt')
text = requesting_urls.get_html('https://en.wikipedia.org/wiki/Richard_Feynman')
find_dates(text, 'Richard_Feynman_dates.txt')
text = requesting_urls.get_html('https://en.wikipedia.org/wiki/Hans_Rosling')
find_dates(text, 'Hans_Rosling_dates.txt')
