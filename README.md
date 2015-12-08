# ImageChallenge

## Goal

We would like you to implement a program that downloads a list of images off the internet, and applies a given set of filters to each of the images. The choice of programming language and libraries is yours (but I think Python might make all our lives easier).

The program should be able to apply the following filters to an image, in arbitrary sequence and combination: blur, sharpen, smooth, edge enhancement, and conversion to grayscale. The implementation should be efficient with respect to overall running time.

We have posted 3 sets of images on the internet (taken from the ImageNet, the actual content of the images is without any relevance):

    https://www.dropbox.com/s/jcdd5uvpv5aw0dl/challenge1.html?dl=0 (smooth, blur, grayscale)
    https://www.dropbox.com/s/aplr60xqdxgo6qb/challenge2.html?dl=0 (grayscale, sharpen, edge enhancement)
    https://www.dropbox.com/s/05md6kg8d4z7rh3/challenge3.html?dl=0 (edge enhancement, grayscale)


For each of the set set, all images listed should be downloaded and individually processed with the sequence of filters named in parenthesis after the URL.

Our idea was to isolate the image filtering and processing into a separate library/module with a clear API, maybe the downloading as well, and a main part that actually calls the functionalities provided by the libs.

## Description

+ The main file is ImageChallenge.py . It needs an input YAML file to run. The YAML file input.yml is given as example. The configuration file contains the necessary parameters to run the program. The file is self-documenting.
+ The program is invoked like this: 
> python ImageChallenge.py input.yml
+ The program first creates the output directory, if it does not exist. Inside this directory, it creates three subdirectories: &lt;set_name&gt;/, &lt;set_name&gt;/original and &lt;set_name&gt;/processed.
+ For each set, the main program creates an instance of the DropboxSpider class.
+ The DropboxSpider class downloads the list of files, parses the HTML and downloads each file in the &lt;set_name&gt;/original directory. A log.txt file is also created in the same directory to keep track of missing files.
+ After the download is complete, the main program creates one instance of the ImageManipulator class.
+ The ImageManipulator looks for all the image files in the &lt;set_name&gt;/original directory, applies the filters and writes the output into &lt;set_name&gt;/processed. Filters are taken from the Python Image Library. If a filter does not match to the list of known filters it is discarded. A log.txt file is also created in the same directory to keep track of images that could not be processed.


## Caveats

+ Many links are broken, the program ignores them and writes them in the log file.
+ For brevity, all files are downloaded with the .jpg extension (even when they are not). This does not seem to be a problem for PIL, execpt in a few cases where I think the URL links to an HTML file.
+ All output files are PNG files. PIL does not write grayscale images to JPEG. I could convert back to RGB, but I don't know if this is in the scope of the exercise ;)
+ There are some URLs which use Chinese characters. So, if you want to use this program in Windows, you need to have Unicode set up in your shell using the command here below. I haven't tested it with Linux or Mac.
> CHCP 65001


## The ImageManipulator class API
  ImageManipulator() : create an instance
  
  ImageManipulator.set_input_dir(&lt;str&gt;)  : set the name of the input directory
  
  ImageManipulator.set_output_dir(&lt;str&gt;) : set the name of the output directory
  
  ImageManipulator.set_filters(&lt;list&gt;)   : set list of filters (needs to be a list as input)
  
  ImageManipulator.add_filter(&lt;str&gt;)     : add single filter (needs to be a string as input)
  
  ImageManipulator.get_filters()         : returns list of filters
  
  ImageManipulator.clear_filters()       : remove all filters from list
  
  ImageManipulator.process_images()      : start processing the images