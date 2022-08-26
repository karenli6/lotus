# scrape google journeys
# chrome://history/journeys

import sqlite3
import os.path
import csv

data_path = os.path.expanduser('~')+"/Library/Application Support/Google/Chrome/Default"
print(data_path)
files = os.listdir(data_path)
# print(files)
history_db = os.path.join(data_path, 'History')

# all tables sql
sql_query = """SELECT name FROM sqlite_master  
  WHERE type='table';"""

# tables: 
# [('meta',), ('downloads',), ('downloads_url_chains',), ('downloads_slices',), 
# ('typed_url_sync_metadata',), ('downloads_reroute_info',), ('urls',), 
# ('sqlite_sequence',), ('visit_source',), ('keyword_search_terms',), ('segments',), 
# ('segment_usage',), ('content_annotations',), ('context_annotations',), ('clusters',), 
# ('clusters_and_visits',), ('visits',)]

c = sqlite3.connect(history_db)
cursor = c.cursor()

select_statement = "SELECT * from keyword_search_terms;"
cursor.execute(select_statement)

# write to csv
with open("key_search_terms_cynthia.csv", 'w',newline='') as csv_file: 
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description]) 
    csv_writer.writerows(cursor)
c.close()
##