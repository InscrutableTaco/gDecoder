import requests
import re
from bs4 import BeautifulSoup
from html.parser import HTMLParser

#DOC_URL = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
DOC_URL = "https://docs.google.com/document/d/e/2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A/pub"

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.div_attrs = dict(attrs)

# helper function to convert html table string to a dictionary
def html_table_to_dict(html_table):
    soup = BeautifulSoup(html_table, "html.parser")
    table = soup.find("table")
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    if not headers:
        # Use first row as headers if no <th>
        first_row = table.find("tr")
        headers = [td.get_text(strip=True) for td in first_row.find_all("td")]
        data_rows = table.find_all("tr")[1:]
    else:
        data_rows = table.find_all("tr")[1:]
    rows = []
    for tr in data_rows:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            row_dict = dict(zip(headers, cells))
            rows.append(row_dict)
    return rows

def decode(url):

    # request the content of the doc and decode as an html string
    req = requests.get(url)
    content = req.content.decode('utf-8')

    # extract the table portion of the string and store as a dictionary
    table = re.findall(r"(<table.*<\/table>)", content)[0]
    char_dict = html_table_to_dict(table)
    
    # convert coordinates to integers and store the grid size
    max_x = 0
    max_y = 0
    for dict in char_dict:
        dict['x-coordinate'] = int(dict['x-coordinate'])
        if dict['x-coordinate'] > max_x:
            max_x = dict['x-coordinate']
        dict['y-coordinate'] = int(dict['y-coordinate'])
        if dict['y-coordinate'] > max_y:
            max_y = dict['y-coordinate']
    
    # build the grid
    char_array = []
    for y in range(max_y+1):
        col = []
        for x in range(max_x+1):
            col.append(" ")
        char_array.append(col)

    # populate the grid
    for dict in char_dict:
        x = dict['x-coordinate']
        y = max_y - dict['y-coordinate'] # invert y-coordinate for printing top to bottom
        char_array[y][x] = dict['Character']

    # print each row as a concatenated string
    for char_list in char_array:
        row = ""
        for char in char_list:
            row += char
        print(row)

def main():

    decode(DOC_URL)
    
if __name__ == "__main__":
    main()