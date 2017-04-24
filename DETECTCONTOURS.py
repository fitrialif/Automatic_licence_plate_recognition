import cv2
import numpy as np
import math
import random

MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0
MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2
MAX_ANGLE_BETWEEN_CHARS = 12.0
MIN_NUMBER_OF_MATCHING_CHARS = 3
RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30
MIN_CONTOUR_AREA = 100

def checkIfPossibleContour(possibleContour):
    if (possibleContour.intBoundingRectArea > MIN_PIXEL_AREA and possibleContour.intBoundingRectWidth > MIN_PIXEL_WIDTH and possibleContour.intBoundingRectHeight > MIN_PIXEL_HEIGHT and MIN_ASPECT_RATIO < possibleContour.fltAspectRatio and possibleContour.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False


def findListOfListsOfMatchingContours(listOfPossibleContours):
    listOfListsOfMatchingContours = []
    for possibleContour in listOfPossibleContours:
        listOfMatchingContours = findListOfMatchingContours(possibleContour, listOfPossibleContours)
        listOfMatchingContours.append(possibleContour)
        if len(listOfMatchingContours) < MIN_NUMBER_OF_MATCHING_CHARS:
            continue
        listOfListsOfMatchingContours.append(listOfMatchingContours)
        listOfPossibleContoursWithCurrentMatchesRemoved = []
        listOfPossibleContoursWithCurrentMatchesRemoved = list(set(listOfPossibleContours) - set(listOfMatchingContours))
        recursiveListOfListsOfMatchingContours = findListOfListsOfMatchingContours(listOfPossibleContoursWithCurrentMatchesRemoved)
        for recursiveListOfMatchingContours in recursiveListOfListsOfMatchingContours:
            listOfListsOfMatchingContours.append(recursiveListOfMatchingContours)
            break
    return listOfListsOfMatchingContours


######################################################################## ###########################
def findListOfMatchingContours(possibleContour, listOfContours):
    listOfMatchingContours = []
    for possibleMatchingContour in listOfContours:
        if possibleMatchingContour == possibleContour:
            continue
        DistanceBetweenContours = distanceBetweenContours(possibleContour, possibleMatchingContour)
        AngleBetweenContours = angleBetweenContours(possibleContour, possibleMatchingContour)
        ChangeInArea = float(abs(possibleMatchingContour.intBoundingRectArea - possibleContour.intBoundingRectArea)) / float(possibleContour.intBoundingRectArea)
        ChangeInWidth = float(abs(possibleMatchingContour.intBoundingRectWidth - possibleContour.intBoundingRectWidth)) / float(possibleContour.intBoundingRectWidth)
        ChangeInHeight = float(abs(possibleMatchingContour.intBoundingRectHeight - possibleContour.intBoundingRectHeight)) / float(possibleContour.intBoundingRectHeight)
    if (DistanceBetweenContours < (possibleContour.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and AngleBetweenContours < MAX_ANGLE_BETWEEN_CHARS and ChangeInArea < MAX_CHANGE_IN_AREA and ChangeInWidth < MAX_CHANGE_IN_WIDTH and ChangeInHeight < MAX_CHANGE_IN_HEIGHT):
        listOfMatchingContours.append(possibleMatchingContour)
    return listOfMatchingContours

###########################
def distanceBetweenContours(firstChar, secondChar):
   intX = abs(firstChar.intCenterX - secondChar.intCenterX) intY = abs(firstChar.intCenterY - secondChar.intCenterY)
   return math.sqrt((intX ** 2) + (intY ** 2))
######################################################################## ###########################
def angleBetweenContours(firstChar, secondChar):
    fltAj=float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))
    if fltAdj != 0.0:
        fltAngleInRad = math.atan(fltOpp / fltAdj)
    else:
        fltAngleInRad = 1.5708
        fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)
    return fltAngleInDeg


