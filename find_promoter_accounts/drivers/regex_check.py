import re
word = 'I am batman $100 in 12 hours'
regexp = re.compile(r'^.*[0-9]+.*[a-zA-Z]+.*[0-9]+.*$')
if regexp.search(word):
  print('matched')