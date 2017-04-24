import cv2
import numpy as np import os
import math import random
import DetectContours import PossiblePlate import PossibleContour
# module level variables ######################################################################## ##
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9
PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5
showSteps = True
######################################################################## ###########################
def main():
    imgOriginal = cv2.imread("23.png")
    if imgOriginal is None:
        print "\nerror: image not read from file \n\n"
        os.system("pause")
        return
    #end if
    height, width, numChannels = imgOriginal.shape
    imgGrayscale = np.zeros((height, width, 1), np.uint8)
    imgThresh = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)
    cv2.destroyAllWindows()
    if showSteps == True:
        cv2.imshow("0", imgOriginal)
    imgGrayscale, imgThresh = preprocess(imgOriginal)
    if showSteps == True:
        cv2.imshow("1a", imgGrayscale)
        cv2.imshow("1b", imgThresh)
    listOfPossibleContours = findPossibleContoursInScene(imgThresh)
    if showSteps == True:
        print "len(listOfPossibleContoursInScene) = " + str(len(listOfPossibleContours))
        imgContours = np.zeros((height, width, 3), np.uint8)
        contours = []
        for possibleContour in listOfPossibleContours:
            contours.append(possibleContour.contour)
        # end for
    cv2.drawContours(imgContours, contours, -1, SCALAR_WHITE)
    cv2.imshow("2b", imgContours)
    listOfListsOfMatchingContours = DetectContours.findListOfListsOfMatchingContours(listOfPossibleContours)
    if showSteps == True:
        print "listOfListsOfMatchingContours = " + str(len(listOfListsOfMatchingContours))
    imgContours = np.zeros((height, width, 3), np.uint8)

    for listOfMatchingContours in listOfListsOfMatchingContours:
        intRandomBlue = random.randint(0, 255)
        intRandomGreen = random.randint(0, 255)
        intRandomRed = random.randint(0, 255)
        contours = []
    for matchingContour in listOfMatchingContours:
        contours.append(matchingContour.contour)
        cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
        cv2.imshow("3", imgContours)
    listOfPossiblePlates = []

    for listOfMatchingContours in listOfListsOfMatchingContours:
        possiblePlate = extractPlate(imgOriginal, listOfMatchingContours)
    if possiblePlate.imgPlate is not None:
        listOfPossiblePlates.append(possiblePlate)
        print "\n" + str(len(listOfPossiblePlates)) + " possible plates found"
    if showSteps == True:
    print "\n"
    cv2.imshow("4a", imgContours)
    for i in range(0, len(listOfPossiblePlates)):
        RectPoints = cv2.boxPoints(listOfPossiblePlates[i].rrLocationOfPlateInScene)
        cv2.line(imgContours, tuple(RectPoints[0]), tuple(RectPoints[1]), SCALAR_RED, 2)
        cv2.line(imgContours, tuple(RectPoints[1]), tuple(RectPoints[2]), SCALAR_RED, 2)
        cv2.line(imgContours, tuple(RectPoints[2]), tuple(RectPoints[3]), SCALAR_RED, 2)
        cv2.line(imgContours, tuple(RectPoints[3]), tuple(RectPoints[0]), SCALAR_RED, 2)
        cv2.imshow("4a", imgContours)
        print "possible plate " + str(i)
        cv2.waitKey(1)
        cv2.waitKey(1)
        cv2.imshow("Original image", imgOriginal)
        cv2.imwrite("imgOriginalScene.png", imgOriginal)

        if len(listOfPossiblePlates) == 0:
            print "\nno license plates were detected\n"
        else:
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
            licPlate = listOfPossiblePlates[0]
            drawredRectangle(imgOriginal, licPlate)
            cv2.imshow("plate localisation", imgOriginal)
            cv2.waitKey(0)
            return


######################################################################## ###########################
def drawredRectangle(imgOriginal, licPlate):
    RectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)
    cv2.line(imgOriginal, tuple(RectPoints[0]), tuple(RectPoints[1]), SCALAR_RED, 2)
    cv2.line(imgOriginal, tuple(RectPoints[1]), tuple(RectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginal, tuple(RectPoints[2]), tuple(RectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginal, tuple(RectPoints[3]), tuple(RectPoints[0]), SCALAR_RED, 2)
######################################################################## ###########################
def preprocess(imgOriginal):
    imgGrayscale = extractvalue(imgOriginal)
    imgMaxContrastGrayscale = maximizecontrast(imgGrayscale)
    height, width = imgGrayscale.shape
    imgBlurred = np.zeros((height, width, 1), np.uint8)
    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)
    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
    return imgGrayscale, imgThresh
######################################################################## ###########################
def extractvalue(imgOriginal):
    height, width, numChannels = imgOriginal.shape
    imgHSV = np.zeros((height, width, 3), np.uint8)
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV) imgHue, imgSaturation, imgValue = cv2.split(imgHSV)
    return imgValue
######################################################################## ###########################
def maximizecontrast(imgGrayscale):
    height, width = imgGrayscale.shape
    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)
    imgGrayscaleplusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscaleplusTopHatMinusBlackHat = cv2.subtract(imgGrayscaleplusTopHat, imgBlackHat)
    return imgGrayscaleplusTopHatMinusBlackHat
######################################################################## ###########################
def findPossibleContoursInScene(imgThresh):
   listOfPossibleContours = []
   intCountOfPossibleContours = 0
   imgThreshCopy = imgThresh.copy()
   imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
   height, width = imgThresh.shape
   imgContours = np.zeros((height, width, 3), np.uint8)
   for i in range(0, len(contours)):
       if showSteps == True:
           cv2.drawContours(imgContours, contours, i, SCALAR_WHITE)
           possibleContour = PossibleContour.PossibleContour(contours[i])
           if DetectContours.checkIfPossibleContour(
               possibleContour): intCountOfPossibleContours = intCountOfPossibleContours + 1
           listOfPossibleContours.append(possibleContour)
           if showSteps == True:
               print "\nstep 2 - len(contours) = " + str(len(contours))
               print "step 2 - intCountOfPossibleContours = " + str(intCountOfPossibleContours)
               cv2.imshow("2a", imgContours)
    return listOfPossibleContours

######################################################################## ###########################

def extractPlate(imgOriginal, listOfMatchingContours):
    possiblePlate = PossiblePlate.PossiblePlate()
    listOfMatchingContours.sort(key=lambda matchingContour: matchingContour.intCenterX)
    PlateCenterX = (listOfMatchingContours[0].intCenterX + listOfMatchingContours[len(listOfMatchingContours) - 1].intCenterX) / 2.0
    PlateCenterY = (listOfMatchingContours[0].intCenterY + listOfMatchingContours[len(listOfMatchingContours) - 1].intCenterY) / 2.0
    PlateCenter = PlateCenterX, PlateCenterY
    intPlateWidth = int((listOfMatchingContours[len(listOfMatchingContours) - 1].intBoundingRectX + listOfMatchingContours[len(listOfMatchingContours) - 1].intBoundingRectWidth - listOfMatchingContours[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    int TotalOfCharHeights=0

    for matchingContour in listOfMatchingContours: intTotalOfCharHeights = intTotalOfCharHeights + matchingContour.intBoundingRectHeight
    AverageCharHeight = intTotalOfCharHeights / len(listOfMatchingContours)
    intPlateHeight = int(AverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)
    Opposite = listOfMatchingContours[len(listOfMatchingContours) - 1].intCenterY - listOfMatchingContours[0].intCenterY
    Hypotenuse = DetectContours.distanceBetweenContours(listOfMatchingContours[0],
                                                    listOfMatchingContours[len(listOfMatchingContours) - 1])
    CorrectionAngleInRad = math.asin(Opposite / Hypotenuse)
    CorrectionAngleInDeg = CorrectionAngleInRad * (180.0 / math.pi)
    possiblePlate.rrLocationOfPlateInScene = (tuple(PlateCenter), (intPlateWidth, intPlateHeight), CorrectionAngleInDeg)
    rotationMatrix = cv2.getRotationMatrix2D(tuple(PlateCenter), CorrectionAngleInDeg, 1.0)
    height, width, numChannels = imgOriginal.shape
    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))
    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(PlateCenter))
    possiblePlate.imgPlate = imgCropped
    return possiblePlate
################################################################################################################################################

if __name__ == "__main__": main()
main()
