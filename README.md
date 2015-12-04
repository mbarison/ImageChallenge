# ImageChallenge

We would like you to implement a program that downloads a list of images off the internet, and applies a given set of filters to each of the images. The choice of programming language and libraries is yours (but I think Python might make all our lives easier).

The program should be able to apply the following filters to an image, in arbitrary sequence and combination: blur, sharpen, smooth, edge enhancement, and conversion to grayscale. The implementation should be efficient with respect to overall running time.

We have posted 3 sets of images on the internet (taken from the ImageNet, the actual content of the images is without any relevance):

    https://www.dropbox.com/s/jcdd5uvpv5aw0dl/challenge1.html?dl=0 (smooth, blur, grayscale)
    https://www.dropbox.com/s/aplr60xqdxgo6qb/challenge2.html?dl=0 (grayscale, sharpen, edge enhancement)
    https://www.dropbox.com/s/05md6kg8d4z7rh3/challenge3.html?dl=0 (edge enhancement, grayscale)


For each of the set set, all images listed should be downloaded and individually processed with the sequence of filters named in parenthesis after the URL.

Our idea was to isolate the image filtering and processing into a separate library/module with a clear API, maybe the downloading as well, and a main part that actually calls the functionalities provided by the libs.
