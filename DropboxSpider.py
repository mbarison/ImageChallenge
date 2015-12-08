##################################################################
# DropboxSpider.py
# 2015/12/06 Marcello Barisonzi
# Download file list from Dropbox and image files from anywhere.
##################################################################

import requests, os, time, codecs
from html.parser import HTMLParser

# remove SSL verification warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class MyImageListParser(HTMLParser):
    """Utility class to parse the file list."""
    def __init__(self):
        super(MyImageListParser, self).__init__()
        self._current_item = None
        self._item_list = []
                
    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            # new image, initialize
            self._current_item = None
            #print("New Image",attrs)
        elif tag == 'a':
            # get href
            #print(attrs)
            self._current_item = dict((x,y) for x,y in attrs)
    def handle_endtag(self, tag):
        if tag == 'li':
            # image data end, push into list
            self._item_list.append(self._current_item)
            # void data
            self._current_item = None
    
    def handle_data(self, data):
        # we should have already some data at this point
        if self._current_item:
            self._current_item["filename"] = "%s.jpg" % data.strip()

    def get_item_list(self):
        return self._item_list

class DropboxSpider(object):
    """DropboxSpider class. Downloads stuff from the internet."""
    def __init__(self):
        self.__output_dir  = None
        self.__input_url   = None
        self.__no_clobber  = True
        self.__filelist    = None
        self.__files       = []
        self._missing_urls = []
        return

    def set_input_url(self, value):
        """Set the location of the input list."""
        self.__input_url = value

    def set_output_dir(self, value):
        """Set the output directory for the downloaded files."""
        self.__output_dir = value

    #def set_no_clobber(self, value):
    #    self.__no_clobber = value

    def __get_filelist(self):
        """Get HTML list of images."""
        req = requests.get(self.__input_url, verify=False)
        if not req.ok:
            print("DropboxSpider.get_filelist() : cannot open %s", self.__input_url)
            return False
        
        self.__filelist = req.text
        return True
        
    def __parse_filelist(self):
        """Parse HTML to extract list of URLs."""
        try:
            p = MyImageListParser()
            p.feed(self.__filelist)
            self.__files = p.get_item_list()
        except:
            print("DropboxSpider.parse_filelist() : Could not parse input file!")
            errF = codecs.open(os.path.join(self.__output_dir,"input_list.html"),"w","utf-8")
            errF.write(self.__filelist)
            errF.close()
            return False
        
        print("DropboxSpider.parse_filelist() : Found %d files" % len(self.__files)) 
            
        return True

    def __download_file(self, dct):
        """Download single image file."""
        try:
            req = requests.get(dct['href'], verify=False)
        except:
            print("DropboxSpider.download_file() : HTTP Exception %s", dct['href'])
            self._missing_urls.append(dct['href'])
            return
    
        if not req.ok:
            print("DropboxSpider.download_file() : cannot open %s", dct['href'])
            self._missing_urls.append(dct['href'])
            return    
    
        try:
            print("DropboxSpider.download_file() : Saving %(href)s as %(filename)s" % dct)
            outF = open(os.path.join(self.__output_dir, dct['filename']),'wb')
            outF.write(req.content)
            outF.close()
        except:
            print("DropboxSpider.download_file() : I/O error while saving %s" % os.path.join(self.__output_dir, dct['filename']))
        
        return

    def get_files(self):
        """Get all files from list."""
        
        # check that the output directory exists
        if not os.path.isdir(self.__output_dir):
            print("ImageManipulator.process_images() : Output/Input directories do not exist.")
            return False
        
        isOK = True
        # download HTML list from Dropbox...
        isOK &= self.__get_filelist()
        # ...and extract the URLs
        isOK &= self.__parse_filelist()
        
        # some bookkeeping
        t0   = time.time()
        fCnt = 0
        fTot = len(self.__files)
        
        if not isOK:
            print("DropboxSpider.get_files() : Could not get list of files to download")
        else:
            for fileDict in self.__files:
                self.__download_file(fileDict)
                t1 = time.time()
                fCnt += 1
                print("File %d/%d\tElapsed time (sec): %d\tETA (sec): %d" % (fCnt,fTot,t1-t0,1.*(t1-t0)/fCnt*(fTot-fCnt)))
        
        # write log file
        logF = codecs.open(os.path.join(self.__output_dir, "log.txt"),"w","utf-8")
        logF.write("== Log ==\n")
        logF.write("Downloaded %d files out of %d in %d seconds.\n" % (fTot-len(self._missing_urls), fTot, (t0-t1)))
        logF.write("Missing URLs:\n")
        for i in sorted(self._missing_urls):
            logF.write("%s\n" % i)
        logF.close()
        
        return isOK