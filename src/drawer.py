import cv2
import numpy as np


class Drawer:
    @staticmethod
    def draw_id(
        img: np,
        text1: str,
        text2: str,
        org1=(52, 22),
        org2=(0, 22),
        fontFace=cv2.FONT_HERSHEY_COMPLEX,
        fontScale=0.8,
        color1=(0, 0, 0),
        color2=(0, 0, 0),
        thickness=1,
        lineType=cv2.LINE_AA,
    ):
        id_img1 = np.full((38, 224, 3), 255, dtype=np.uint8)
        id_img2 = id_img1.copy()

        id_img1 = cv2.putText(
            id_img1, text1, org1, fontFace, fontScale, color1, thickness, lineType
        )
        id_img2 = cv2.putText(
            id_img2, text2, org2, fontFace, fontScale, color2, thickness, lineType
        )

        return cv2.vconcat([id_img2, img, id_img1])

    @staticmethod
    def draw_rectangle(
        img: np, pt1=(0, 38), pt2=(224, 300), color=(0, 0, 225), thickness=5
    ):
        return cv2.rectangle(img, pt1, pt2, color, thickness)
