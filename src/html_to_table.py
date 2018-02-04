import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

title = []
with open("header_synonyms.txt", "r") as f:
    title = f.readlines()
title = [x.strip() for x in title]

deadline = []
with open("deadline_synonyms.txt", "r") as f:
    deadline = f.readlines()
deadline = [x.strip() for x in deadline]

class HTMLTableParser:

 def parse_url(self, url):
     response = requests.get(url)
     soup = BeautifulSoup(response.text, 'lxml')

     tables = []
     for table in soup.find_all('table'):
         value = self.parse_html_table(table)
         if value is not None:
             tables.append(value)

     return tables

 def parse_html_table(self, table):
     n_columns = 0
     n_rows=0
     column_names = []

     # Find number of rows and columns
     # we also find the column titles if we can
     for row in table.find_all('tr'):

         # Determine the number of rows in the table
         td_tags = row.find_all('td')
         if len(td_tags) > 0:
             n_rows+=1
             if n_columns == 0:
                 # Set the number of columns for our table
                 n_columns = len(td_tags)

         # Handle column names if we find them
         th_tags = row.find_all('th')
         if len(th_tags) > 0 and len(column_names) == 0:
             for th in th_tags:
                 column_names.append(th.get_text())

     title_index, deadline_index = relevant_table(column_names)
     # print("title_index: {}, deadline_index: {}".format(title_index, deadline_index))
     if title_index == -1 or deadline_index == -1:
         return None

     events = []
     row_marker = 0
     for row in table.find_all('tr'):
         columns = row.find_all('td')
         if columns != []:
             # print(row)
             # print(columns)
             if (title_index < len(row) and deadline_index < len(row)):
                 events.append((columns[title_index].get_text(), columns[deadline_index].get_text()))
     return events

     # columns = column_names if len(column_names) > 0 else range(0,n_columns)
     # df = pd.DataFrame(np.random.randint(low=0, high=n_rows, size=(n_rows, 2)), columns = 2)

     # events = []
     #
     # row_marker = 0
     # for row in table.find_all('tr'):
     #     column_marker = 0
     #     columns = row.find_all('td')
     #     for i in range(len(columns)):
     #         if (i == title_index or i == deadline_index):
     #             df.iat[row_marker,column_marker] = column.get_text()
     #         column_marker += 1
     #     if len(columns) > 0:
     #         row_marker += 1
     #
     # # Convert to float if possible
     # for col in df:
     #     try:
     #         df[col] = df[col].astype(float)
     #     except ValueError:
     #         pass
     #
     # return df


def relevant_table(headers):
    # TODO: find weight

    title_index = -1
    deadline_index = -1

    for i in range(len(headers)):
        # found title
        for synonym in title:
            if synonym in headers[i]:
                title_index = i
                break
        if title_index != -1:
            break

    for i in range(len(headers)):
        # found due date
        for synonym in deadline:
            if synonym in headers[i] and i != title_index:
                if synonym != "Date" or synonym == headers[i]:
                    deadline_index = i
                    break
        if deadline_index != -1:
            break

    return title_index, deadline_index


if __name__ == "__main__":
    hp = HTMLTableParser()
    tables = hp.parse_url("http://www.dgp.toronto.edu/~karan/courses/418/index.html") # Grabbing the table from the tuple

    print(tables)
    # for table in tables:
    #     print(table)
    #     print(table.loc[1])

#
# import pandas as pd
# from bs4 import BeautifulSoup
# import requests
# url = "https://www.fantasypros.com/nfl/reports/leaders/qb.php?year=2015"
# response = requests.get(url)
#
# html_string = '''
#   <table>
#         <tr>
#             <td> Hello! </td>
#             <td> Table </td>
#         </tr>
#     </table>
# '''
#
# soup = BeautifulSoup(html_string, 'lxml') # Parse the HTML as a string
#
# table = soup.find_all('table')[0] # Grab the first table
#
# new_table = pd.DataFrame(columns=range(0,2), index = [0]) # I know the size
#
# row_marker = 0
# for row in table.find_all('tr'):
#     column_marker = 0
#     columns = row.find_all('td')
#     for column in columns:
#         new_table.iat[row_marker,column_marker] = column.get_text()
#         column_marker += 1
#
# print(new_table)
