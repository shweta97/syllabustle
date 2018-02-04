import requests
from bs4 import BeautifulSoup

header = []
with open("src/header_synonyms.txt", "r") as f:
    header = f.readlines()
header = [x.strip() for x in header]

deadline = []
with open("src/deadline_synonyms.txt", "r") as f:
    deadline = f.readlines()
deadline = [x.strip() for x in deadline]

names = []
with open("src/title_synonyms.txt", "r") as f:
    names = f.readlines()
names = [x.strip() for x in names]

class HTMLTableParser:

 def parse_url(self, url):
     response = requests.get(url)
     soup = BeautifulSoup(response.text, 'lxml')

     tables = []
     for table in soup.find_all('table'):
         value = self.parse_html_table(table)
         if value is not None:
             tables.append(value)

     with open('events.txt', 'a') as f:
         if tables == []:
             f.write('[]\n')
         else:
             f.writelines("%s\n" % item for item in tables)

     return tables != []

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

     print("Column names are: {}".format(column_names))
     header_index, deadline_index = relevant_table(column_names)
     if header_index == -1 or deadline_index == -1:
         print('Cannot parse url')
         return None

     events = []
     row_marker = 0
     for row in table.find_all('tr'):
         columns = row.find_all('td')
         if columns != []:
             # print(row)
             print(columns)
             if (header_index < len(row) and deadline_index < len(row)):
                 # if relevant_name(columns[header_index].get_text()):
                 events.append((columns[header_index].get_text().strip(), columns[deadline_index].get_text().strip()))
     return events

# def relevant_name(name):
#     for syn in names:
#         if syn in name:
#             return True

def relevant_table(headers):
    # TODO: find weight

    header_index = -1
    deadline_index = -1

    for i in range(len(headers)):
        # found title
        for synonym in header:
            if synonym in headers[i]:
                header_index = i
                break
        if header_index != -1:
            break

    for i in range(len(headers)):
        # found due date
        for synonym in deadline:
            if synonym in headers[i] and i != header_index:
                if synonym != "Date" or synonym == headers[i]:
                    deadline_index = i
                    break
        if deadline_index != -1:
            break

    return header_index, deadline_index


if __name__ == "__main__":
    hp = HTMLTableParser()
    tables = hp.parse_url("http://www.dgp.toronto.edu/~karan/courses/418/index.html") # Grabbing the table from the tuple
    print(tables)
