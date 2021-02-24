from typing import Any, List

import cv2
import numpy as np


class BoardRecognition:
    def __init__(self, img=None):
        self._img = cv2.imread(img)
        self._processed_image = None
        self._processed_threshold = None

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value: str) -> None:
        if value != self._img:
            self._img = cv2.imread(value)

    @staticmethod
    def adjust_gamma(image, gamma=1.0):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array(
            [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
        ).astype("uint8")
        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def preprocess_board(self):
        """Applies preprocessing steps on the board """
        kernel = np.ones((20, 20))
        image = cv2.morphologyEx(self._img, cv2.MORPH_OPEN, kernel)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        image = self.adjust_gamma(image, gamma=0.75)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("zz", result_norm)
        # cv2.waitKey(0)
        # using median blurs to smoothen the edges
        image = cv2.medianBlur(image, 5)
        # otsu threshold finds automatically the best threshold to pick for
        # contour detection
        threshold = cv2.threshold(
            image, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_TOZERO
        )[1]
        self._processed_threshold = threshold
        self._processed_image = image

    def extract_cards_from_board(self) -> List[Any]:
        self.preprocess_board()
        """From a board of cards returns a list of cards ndarray"""
        # RETR External will help show only main objects (nothing is recognized
        # on the cards)
        # APPROX SIMPLE aims to identify the corners of the pixels of the
        # contour - more performant
        contours, hierarchy = cv2.findContours(
            self._processed_threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        max_size = self._processed_image.size * 0.9
        min_size = self._processed_image.size * 0.005
        cards = []
        for cnt in contours:
            if min_size < cv2.contourArea(cnt) < max_size:
                epsilon = 0.1 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                if len(approx) == 4 and cv2.contourArea(cnt) > 1000:
                    cv2.drawContours(
                        self._processed_image, [approx], -1, (255, 255, 0), 2
                    )
                    approx = np.int0(approx)
                    warped = self.four_point_transform(
                        self._img, approx.squeeze()
                    )
                    width = warped.shape[1]
                    height = warped.shape[0]
                    if width > height:
                        warped = cv2.resize(warped, (600, 400))
                    else:
                        warped = cv2.resize(warped, (400, 600))
                    cards.append(warped)
                    # cv2.imshow("zz", warped)
                    # cv2.waitKey()
        return cards

    @staticmethod
    def order_points_s(pts):
        # initialzie a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        rect = np.zeros((4, 2), dtype="float32")
        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        # return the ordered coordinates
        return rect

    def four_point_transform(self, image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        rect = self.order_points_s(pts)
        (tl, tr, br, bl) = rect
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array(
            [
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1],
            ],
            dtype="float32",
        )
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        # return the warped image
        return warped

    def resize_card(self, scale_percent=20):
        """Resized the original img to a given percent default is 20"""
        width = int(self._img.shape[1] * scale_percent / 100)
        height = int(self._img.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(self._img, dim, interpolation=cv2.INTER_AREA)
