from __future__ import print_function
import csv, sys, os

# define block objects, which hold field names and can store data
class block:
    def __init__(self, list, non_id=1):
        self.name = list[0].replace(" ", "")
        try:
            self.len = list.index('')
        except:
            self.len = len(list)
        self.fields = ['BlockIdentifier', 'UniqueID'] + list[non_id:self.len]
        self.data = [self.fields]
        self.count = 0
        self.order = 0
    def count_occurrences(self, file):
        with open(file, 'r') as inputFile:
            reader = inputFile.read()
            self.count = reader.count(self.name)
        inputFile.close()
    def get_order(self, n):
        self.order = n

# get index for last non-empty element in a list
def get_last(list):
  for i, e in enumerate(reversed(list)):
    if e is not '':
      return len(list) - i - 1
  return -1
