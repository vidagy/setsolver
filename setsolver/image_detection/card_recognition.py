import math
from typing import Any, List

import cv2
import numpy as np
from scipy.spatial import distance

from setsolver.card import Card
from setsolver.properties import Color, Count, Fill, Shape


class CardRecognition:
    def __init__(self, img=None):
        self._img = img
        self._processed_image = None
        self._processed_threshold = None
        self.shape_contours = None
        self.shape_contours = []
        self.processed_for_shade = None
        self.card_info = dict()
        self.abstract_card = None

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value: np.ndarray):
        if value != self._img:
            self._img = value

    @staticmethod
    def adjust_gamma(image, gamma=1.0) -> np.ndarray:
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        inverse_gamma = 1.0 / gamma
        table = np.array(
            [((i / 255.0) ** inverse_gamma) * 255 for i in np.arange(0, 256)]
        ).astype("uint8")
        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def get_color(self) -> str:
        img = self._img
        colors = dict()
        boundaries = {
            "red": ([58, 37, 120], [100, 100, 230]),
            "green": ([0, 60, 0], [90, 200, 90]),
            "purple": ([35, 0, 35], [200, 90, 150]),
        }
        map_to_card = {
            "red": Color.RED,
            "green": Color.GREEN,
            "purple": Color.PURPLE,
        }
        for key, value in boundaries.items():
            # create NumPy arrays from the boundaries
            lower = np.array(value[0], dtype="uint8")
            upper = np.array(value[1], dtype="uint8")
            mask = cv2.inRange(img, lower, upper)
            output = cv2.bitwise_and(img, self._img, mask=mask)
            colors[key] = np.count_nonzero(output)
        most_intense_color = max(colors.items(), key=lambda x: x[1])
        color = most_intense_color[0]
        # print(colors)
        self.card_info["color"] = map_to_card.get(color)
        return color

    def preprocess_card(self) -> np.ndarray:
        image = self._img
        img = image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result_planes = []
        result_norm_planes = []
        clache = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
        img = clache.apply(img)
        self.processed_for_shade = img
        rgb_planes = cv2.split(img)
        # this removes the shading
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(
                diff_img,
                None,
                alpha=0,
                beta=255,
                norm_type=cv2.NORM_MINMAX,
                dtype=cv2.CV_8UC1,
            )
            result_planes.append(diff_img)
            result_norm_planes.append(norm_img)
        result_norm = cv2.merge(result_norm_planes)
        img = cv2.GaussianBlur(result_norm, (5, 5), 1)
        kernel = np.ones((5, 5))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        # cv2.imshow("given to thresh", img)
        return img

    def get_fill(self) -> str:
        if len(self.shape_contours) > 0:
            # preprocess image
            img = self.processed_for_shade
            sharpen_kernel = np.array(
                [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
            )
            img = cv2.filter2D(img, -1, sharpen_kernel)
            # caclulate diff for every found shape take the maximum one
            current_avg: int = 255
            for contour in self.shape_contours:
                moments = cv2.moments(contour)
                center_of_shape_x = int(moments["m10"] / moments["m00"])
                center_of_shape_y = int(moments["m01"] / moments["m00"])
                left_corner_x = center_of_shape_x - 20
                left_corner_y = center_of_shape_y - 20
                right_corner_x = center_of_shape_x + 20
                right_corner_y = center_of_shape_y + 20
                within_cnt = img[
                    left_corner_y:right_corner_y, left_corner_x:right_corner_x
                ]
                avg_color_per_row_cnt = np.average(within_cnt, axis=0)
                avg_colors_cnt = np.average(avg_color_per_row_cnt, axis=0)
                int_averages_cnt = np.array(avg_colors_cnt, dtype=np.uint8)
                if int(int_averages_cnt) < current_avg:
                    current_avg = int(int_averages_cnt)

            edge_x = 30
            edge_y = 30
            top_edge_x = edge_x - 20
            top_edge_y = edge_y - 20
            bottom_edge_x = edge_x + 20
            bottom_edge_y = edge_y + 20

            edge = img[top_edge_y:bottom_edge_y, top_edge_x:bottom_edge_x]
            # cv2.imshow("proc", img)
            # cv2.waitKey()
            avg_color_per_row = np.average(edge, axis=0)
            # calculate the averages of our rows
            avg_colors_edge = np.average(avg_color_per_row, axis=0)
            int_averages_edge = np.array(avg_colors_edge, dtype=np.uint8)

            diff = abs(int(int_averages_edge) - current_avg)
            print(f"diff: {diff}")
            if diff <= 15:
                self.card_info["fill"] = Fill.EMPTY
                return "empty"
            elif diff > 80:
                self.card_info["fill"] = Fill.FULL
                return "full"
            else:
                self.card_info["fill"] = Fill.STRIPED
                return "striped"
        raise RuntimeError("No shapes detected")

    def get_number_of_shapes(self) -> int:
        """
        Returns the number of cards on an image and sets the main contour
        """
        card_map = {1: Count.ONE, 2: Count.TWO, 3: Count.THREE}
        img = self.preprocess_card()
        min_area = img.size * 0.06
        max_area = img.size * 0.9
        threshold = cv2.threshold(
            img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY
        )[1]
        cnt, hier = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        new_cnt: List[Any] = []
        central_coordinates: List[List[int]] = []
        for i, c in enumerate(cnt):
            if max_area > cv2.contourArea(c) > min_area:
                moments = cv2.moments(c)
                center_of_shape_x = int(moments["m10"] / moments["m00"])
                center_of_shape_y = int(moments["m01"] / moments["m00"])
                # if there are recorded found shapes
                all_far = True
                for coord in central_coordinates:
                    dist = distance.euclidean(
                        (coord[0], coord[1]),
                        (center_of_shape_x, center_of_shape_y),
                    )
                    if dist < 50:
                        all_far = False
                        break
                if all_far:
                    new_cnt.append(c)
                central_coordinates.append(
                    [center_of_shape_x, center_of_shape_y]
                )
        # cv2.drawContours(threshold, new_cnt, -1, (255, 255, 255), 3)
        self.shape_contours = new_cnt
        self.card_info["count"] = card_map.get(len(new_cnt))
        return len(new_cnt)

    def get_shape(self) -> str:
        if len(self.shape_contours) > 0:
            contour = self.shape_contours[0]
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon=epsilon, closed=True)
            moments = cv2.moments(contour)
            # Calculate Hu Moments
            hu_moments = cv2.HuMoments(moments)
            new_moments = []
            for i in range(7):
                new_moments.append(
                    -1
                    * math.copysign(1.0, hu_moments[i])
                    * math.log10(abs(hu_moments[i]))
                )
            hu1 = new_moments[0]
            print(new_moments)
            if len(approx) == 4:
                self.card_info["shape"] = Shape.DIAMOND
                return "diamond"
            if hu1 < 0.62:
                self.card_info["shape"] = Shape.WAVE
                return "wave"
            elif 0.62 <= hu1 < 0.669:
                self.card_info["shape"] = Shape.DIAMOND
                return "diamond"
            elif hu1 >= 0.669:
                self.card_info["shape"] = Shape.OVAL
                return "oval"
        raise RuntimeError("No shapes detected")

    def create_card(self) -> None:
        fill = self.card_info.get("fill")
        count = self.card_info.get("count")
        color = self.card_info.get("color")
        shape = self.card_info.get("shape")
        if all([fill, count, color, shape]):
            card = Card(fill, count, color, shape)
        else:
            card = None
        self.abstract_card = card
        return card

    def process_all_properties(self):
        self.get_number_of_shapes()
        self.get_color()
        self.get_shape()
        self.get_fill()
        self.create_card()
