from bs4 import BeautifulSoup
import urllib.request as urllib2
import os


class GoogleeImageDownloader(object):
    _URL = "https://www.google.co.in/search?q={}&source=lnms&tbm=isch"
    _BASE_DIR = 'GoogleImages'
    _HEADERS = {
        'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    def __init__(self):
        query = input("Enter keyword to search images\n")
        self.dir_name = os.path.join(self._BASE_DIR, query.split()[0])
        self.url = self._URL.format(urllib2.quote(query)) 
        self.make_dir_for_downloads()
        self.initiate_downloads()

    def make_dir_for_downloads(self):
        print("Creating necessary directories")
        if not os.path.exists(self._BASE_DIR):
            os.mkdir(self._BASE_DIR)

        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)

    def initiate_downloads(self):
        src_list = []
        soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(self.url,headers=self._HEADERS)),'html.parser')
        for img in soup.find_all('img'):
            if img.has_attr("data-src"):
                src_list.append(img['data-src'])
        print("{} of images collected for downloads".format(len(src_list)))
        self.save_images(src_list)

    def save_images(self, src_list):
        print ("Saving Images...")
        for i , src in enumerate(src_list):
            try:
                req = urllib2.Request(src, headers=self._HEADERS)
                raw_img = urllib2.urlopen(req).read()
                with open(os.path.join(self.dir_name , str(i)+".jpg"), 'wb') as f:
                    f.write(raw_img)
            except Exception as e:
                print ("could not save image")
                raise e


if __name__ == "__main__":
    GoogleeImageDownloader()