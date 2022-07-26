import os
path = '/Users/jgarzon/js_api/download/bigtimeempire.com_js_jquery.nice-select.min.js'
for root, dirs, files in os.walk(path, topdown=False):
   if ('inline' in root) or ('links' in root):
      for name in files:
         print(os.path.join(root, name))
