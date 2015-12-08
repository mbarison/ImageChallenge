##################################################################
# ImageManipulator.py
# 2015/12/06 Marcello Barisonzi
#
##################################################################

import os, time, glob, codecs
from PIL import Image
from PIL import ImageFilter

class ImageManipulator(object):
    """ImageManipulator class. Apply filters to a whole directory of images."""
    def __init__(self):
        self.__output_dir  = None
        self.__input_dir   = None
        self.__no_clobber  = True
        self.__collection   = None
        self.__filters      = []
        self.__pipeline     = []
        return

    # additional filters can be added in this dictionary
    # "fun" needs to be an Image function, and "par" the parameter
    __filterDict = {"smooth"           : {"fun" : Image.Image.filter,  "par" : ImageFilter.SMOOTH},
                    "edge_enhancement" : {"fun" : Image.Image.filter,  "par" : ImageFilter.EDGE_ENHANCE},
                    "sharpen"          : {"fun" : Image.Image.filter,  "par" : ImageFilter.SHARPEN},
                    "blur"             : {"fun" : Image.Image.filter,  "par" : ImageFilter.BLUR},
                    "grayscale"        : {"fun" : Image.Image.convert, "par" : 'LA'},
                    }

    def set_input_dir(self, value):
        """Set the directory containing the images."""
        self.__input_dir = value

    def set_output_dir(self, value):
        """Set the output directory for the processed images."""
        self.__output_dir = value
        
    def set_filters(self, f):
        """Set list of filters (need to be a list as input)."""
        if f.__class__ == [].__class__:
            self.__filters = f
        else:
            print("ImageManipulator.set_filters() : Invalid filters class", f.__class__)
        
    def add_filter(self, f):
        """Add single filter (need to be a string as input)."""
        if f.__class__ == "".__class__:
            self.__filters.append(f)
        else:
            print("ImageManipulator.add_filter() : Invalid filters class", f.__class__)        
        
        
    def get_filters(self):
        """Returns list of filters."""
        return self.__filters
    
    def clear_filters(self):
        """Reset list of filters if necessary."""
        self.__filters = []
        return
        
    def __get_collection(self):
        """Extract filenames from directory. I am assuming *.jpg for simplicity."""
        self.__collection = glob.glob(os.path.join(self.__input_dir,"*.jpg"))
        #print(self.__collection)
        return
                
    def __build_pipeline(self):
        """ImageManipulator.build_pipeline(): Build a list of filters to be applied sequentially.
            The list contains dictionaries in the form (function pointer, argument)"""
        self.__pipeline = []
                
        for i in self.__filters:
            if i in self.__filterDict.keys():
                print("ImageManipulator.build_pipeline() : Adding %s filter" % i)
                self.__pipeline.append(self.__filterDict[i]) 
            else:
                print("ImageManipulator.build_pipeline() : Unknown filter", i)
        return
        
    def __process_img(self, img):
        """Apply single filter to image"""
        for dct in self.__pipeline:
            img = dct["fun"](img, dct["par"])
        return img   
    
    def process_images(self):
        """Process directory of images."""
        
        # check that the directories exist
        if not (os.path.isdir(self.__input_dir) and os.path.isdir(self.__output_dir)):
            print("ImageManipulator.process_images(): Output/Input directories do not exist.")
            return
        
        # get list of files
        self.__get_collection()
        
        # build pipeline of filters
        self.__build_pipeline()
        
        # some bookkeeping
        fCnt = 0
        fTot = len(self.__collection)
        missed_files = []
        t0 = time.time()
        
        # start processing
        for fname in self.__collection:
            _filename = os.path.basename(fname)
            #print(_filename)
            fCnt += 1
            try:
                img = Image.open(fname)
            except:
                missed_files.append(_filename)
                print("ImageManipulator.process_images() : Could not open file", _filename)
                continue
            
            try:
                new_img = self.__process_img(img)
            except:
                missed_files.append(_filename)
                print("ImageManipulator.process_images() : Could not process file", _filename)
                continue
            
            try:
                _filename = _filename.replace(".jpg",".png")
                new_img.save(os.path.join(self.__output_dir, _filename))
            except:
                missed_files.append(_filename)
                print("ImageManipulator.process_images() : Could not save file", os.path.join(self.__output_dir, _filename))
                continue
            
            t1 = time.time()
            print("Image %d/%d\tElapsed time (sec): %d\tETA (sec): %d" % (fCnt,fTot,t1-t0,1.*(t1-t0)/fCnt*(fTot-fCnt)))
    
        # write logfile for checks
        logF = codecs.open(os.path.join(self.__output_dir, "log.txt"),"w","utf-8")
        logF.write("== Log ==\n")
        logF.write("Processed %d images out of %d in %d seconds.\n" % (fTot-len(missed_files), fTot,(t1-t0)))
        logF.write("Missing Images:\n")
        for i in sorted(missed_files):
            logF.write("%s\n" % i)
        logF.close()
        
        return