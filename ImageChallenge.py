#!/usr/bin/env Python
##################################################################
# ImageChallenge.py
# 2015/12/06 Marcello Barisonzi
# Apply arbitrary filters to online image collections.
# Usage: ImageChallenge.py <input_file>
##################################################################

#import argparse
import sys, os, yaml
from DropboxSpider import DropboxSpider
from ImageManipulator import ImageManipulator


def main():
    if len(sys.argv) != 2:
        print("\nUsage: %s <input_file>" % __file__)
        sys.exit(666)
    
    try:
        # load YAML file into configuration dictionary
        _inFile = open(sys.argv[1])
        options_dict = yaml.safe_load(_inFile)
        _inFile.close()
    except:
        print("Could not open/parse input file", sys.argv[1])
        sys.exit(666)
    
    # create target directories if not existing
    out_dir = options_dict["global_options"]["output_dir"]
    
    if not os.path.isdir(out_dir):
        try:
            os.mkdir(out_dir)
        except:
            print("ERROR! Cannot create output directory:", out_dir)
            sys.exit(666) 
        
    ### collect images into target directory
    for imageSetDict in options_dict["image_sets"]:
        set_name = list(imageSetDict.keys())[0]
        print("Processing set: %s" % set_name)
        
        # create set directories
        try:
            sub_dir = os.path.join(out_dir, set_name)
            if not os.path.isdir(sub_dir):
                os.mkdir(os.path.join(sub_dir))
                
            orig_dir = os.path.join(sub_dir, "original")
            proc_dir = os.path.join(sub_dir, "processed")
            
            if not os.path.isdir(orig_dir):
                os.mkdir(orig_dir)
            if not os.path.isdir(proc_dir):
                os.mkdir(proc_dir)
        except:
            print("ERROR! Could not create a subdirectory in", out_dir)
            sys.exit(666)
            
        # download the directories
        spider = DropboxSpider()
        spider.set_input_url(imageSetDict[set_name]["url"])
        spider.set_output_dir(orig_dir)
        
        if not spider.get_files():
            print("No files were downloaded, skipping %s" % set_name)
            continue
        
        ### pass images to manipulator
        manipulator = ImageManipulator()
        manipulator.set_input_dir(orig_dir)
        manipulator.set_output_dir(proc_dir)      
        manipulator.set_filters(imageSetDict[set_name]["filters"])
        manipulator.process_images()
    
    return

if __name__ == "__main__":
    main()