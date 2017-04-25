# Automatic_licence_plate_recognition

INTRODUCTION:

OpenCV-Python is the Python API of OpenCV. It combines the best qualities of OpenCV C++ API and Python language.



OPENCV-PYTHON:

Python is a general purpose programming language started byGuido van Rossum, which became very popular in short time mainly because of its simplicity and code readability. It enables the programmer to express his ideas in fewer lines of code without reducing any readability.



Compared to other languages like C/C++, Python is slower. But another important feature of Python is that it can be easily extended with C/C++. This feature helps us to write computationally intensive codes in C/C++ and create a Python wrapper for it so that we can use these wrappers as Python modules. This gives us two advantages: first, our code is as fast as original C/C++ code (since it is the actual C++ code working in background) and second, it is very easy to code in Python. This is how OpenCV-Python works, it is a Python wrapper around original C++ implementation.





And the support of Num py makes the task more easier. Numpy is a highly optimized library for numerical operations. It gives a MATLAB-style syntax. All t he OpenCV array structures are converted to-and-from Numpy arrays. So whatever operations you can do in Numpy, you can com bine it with OpenCV, which increases numb r of weapons in your arsenal. Besides th at, several other libraries like SciPy, Matplotli b which supports Numpy can be used with this.



So OpenCV-Python is an appropriate tool for fast prototyping of computer vision problems.
 FUNCTIONS USED


1	cv2.imread(filen ame[, flags])

x	The functiion imread loads an image from the specified f ile and returns it. If the i mage cannot be read (because of missing file, improper permissio ns, unsupported or invalid format), the function returns an empty matrix




2	cv2.findContours (image, mode, method[, contours[, hierarchy[, offset]]])




x  The  function  retrieves  contours  from
the  binary  i mage
using  the
algorithm [Suzuki85]. The contours are a useful tool fo r shape analysis
and object detection and recognition. See squares.cin the OpenCV sample
directory.


3  cv2.drawContours(image,  contours,  contourIdx,
color[,  thick ness[,
lineType[,
hierarchy[, maxLevel[, o ffset]]]]])




x	The funct ion draws contour outlines in the image if  or

fills the area bounded by the contours if  . The example below shows how to retrieve connected comp onents from the binary im age and label them










4	cv2.adaptiveThreshold()


x  In this, the algorithm calculate the threshold for a small regions of the

image. So we get different thresholds for different regions of the same image and it gives us better results for images with varying illumination.

x	It has three ‘special’ input params and only one output argument.

x	Adaptive Method - It decides how thresholding value is calculated.

x	cv2.ADAPTIVE_THRESH_MEAN_C : threshold value is the mean of neighbourhood area.
x	cv2.ADAPTIVE_THRESH_GAUSSIAN_C : threshold value is the weighted sum of neighbourhood values where weights are a gaussian window.
x  Block Size - It decides the size of neighbourhood area.

x	C - It is just a constant which is subtracted from the mean or weighted mean calculated.

5	cv2.gaussianBlurr()

x	Image blurring is achieved by convolving the image with a low-pass filter kernel. It is useful for removing noises. It actually removes high frequency content (eg: noise, edges) from the image. So edges are blurred a little bit in this operation

x	We should specify the width and height of kernel which should be positive and odd. We also should specify the standard deviation in X and Y direction, sigmaX and sigmaY respectively. If only sigmaX is specified, sigmaY is taken as same as sigmaX. If both are given as zeros, they are calculated from kernel size. Gaussian blurring is highly effective in removing gaussian noise from the image.

6	cv2.cvtColor(input_image, flag)
x	For color conversion, we use the function cv2.cvtColor(input_image, flag) where flag determines the type of conversion.

7	findPossibleContoursInScene(imgThresh)

x	used to find all the contours in the image.

x	Input is the thresholded image
x	Output is the image with contours drawn on it.

8	checkIfPossibleContour(possibleContour)

x	used to verify whether a contour matches with the approximate plate parameters.
x	If contour matches the plate parameters function returns true.

x	Input is a contour with bounded rectangle

9	findListOflistof MatchingContours(possibleContour, listOfContours)

x	finds list of list of matching contours.

x	Input is a contour and list of possible contours.

x	Output is a list of list of matching contours.

10	extractPlate(imgOriginal, listOfMatchingContours)

x	used to detect possible plate dimensions from the list of matching contours.
x	Input is an image and list of matching contours.

x	Output is a possible plate with known dimensions.

FLOW CHART OF THE PROCESS

Start --->
Img Original Scene--->

Preprocess( )
{
imgGrayscale,imgThreshscene
}--->

findPossibleContoursinScene()
{
listOfPossibleContoursInScene
}-->

findListOfListOfMactchingContours() 
{
listOfListsOfMatchingContours
}---->

extractPlate( )
{
listOfPossiblePlates
}

Suppose the plate with the most recognized contours is the actual plate

Image with license plate localized ---->

Stop

