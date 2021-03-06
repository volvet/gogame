
from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import multiprocessing
import six

if sys.version_info[0] == 3:
  from urllib.request import urlopen, urlretrieve
else:
  from urllib import urlopen, urlretrieve


def worker(url_and_target):
  try:
    (url, target_path) = url_and_target
    #print('>>> Downloading ' + target_path)
    urlretrieve(url, target_path)
  except:
    print('>>> Exiting child process')
  return ">>> Downloaded " + target_path

class KGSIndex:
  def __init__(self, kgs_url='https://u-go.net/gamerecords/',
               index_page='kgs_index.html',
               data_directory='data'):
    self.kgs_url = kgs_url
    self.index_page= index_page
    self.data_directory = data_directory
    self.file_info= []
    self.urls = []
    self.load_index()
    
  def download_files(self):
    if not os.path.exists(self.data_directory):
      os.makedirs(self.data_directory)
    
    urls_to_download = []
    for info in self.file_info:
      url = info['url']
      filename = info['filename']
      if not os.path.isfile(self.data_directory + '/' + filename):
        urls_to_download.append((url, self.data_directory + '/' + filename))
        cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cores)
        try:
          it = pool.imap(worker, urls_to_download)
          for r in it:
            print(r)
          pool.close()
          pool.join()
        except KeyboardInterrupt:
          print('>>> Caught keyboardInterrupt, terminating workers')
          pool.terminate()
          pool.join()
          sys.exit(-1)
      else:
        print('>>> ' + self.data_directory + '/' + filename + ' was already downloaded')
    
  def create_index_page(self):
    if os.path.isfile(self.index_page):
      print('>>> Reading cached index page')
      index_file = open(self.index_page, 'r')
      index_contents = index_file.read()
      index_file.close()
    else:
      print('>>> Downloading index page')
      fp = urlopen(self.kgs_url)
      data = six.text_type(fp.read())
      fp.close()
      index_contents = data
      index_file = open(self.index_page, 'w')
      index_file.write(index_contents)
      index_file.close()
    return index_contents
  
  def load_index(self):
    index_contents = self.create_index_page()
    split_page = [item for item in index_contents.split('<a href="') if item.startswith('https://')]
    for item in split_page:
      download_url = item.split('">Download')[0]
      if download_url.endswith('.tar.gz'):
        #print(download_url)
        self.urls.append(download_url)
    for url in self.urls:
      filename = os.path.basename(url)
      split_file_name = filename.split('-')      
      num_games = int(split_file_name[len(split_file_name) - 2])
      print('file: ' + filename + ', num of games: ' + str(num_games))
      self.file_info.append({'url': url, 'filename':filename, 'num_games': num_games})
    pass

if __name__ == '__main__':
  print('dlgo.data.index_processor')
  index = KGSIndex()
  index.download_files()
  #print(index)
