

def extract_key_terms(array):
  new_array = []
  for link in array:
    index = link.find('search?q=') + 9
    key_terms = ''
    while (index < len(link)):

      if (link[index] == '&'):
        break
      elif (link[index] == '+'):
        key_terms += ' '
      elif (link[index].isalpha()):
        key_terms += link[index]

      index +=1
    
    new_array.append(key_terms)
  return new_array


def write_file(final_array):
  print("writing to existing csv file .. ")
  with open('../search_terms.csv','w') as fd:
    for key_search_term in final_array:
      string = 'blah,blah,term,'+key_search_term+'\r\n'
      # print(string)
      fd.write(string)