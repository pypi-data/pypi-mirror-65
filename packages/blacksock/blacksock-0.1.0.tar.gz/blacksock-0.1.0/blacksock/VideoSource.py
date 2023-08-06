"""Module controlling cameras and supplying frames.
"""
import subprocess
import platform

import cv2

class VideoSource:
    """Class for supplying video input"""

    def __init__(self):
        self._input_id = -1
        self._input = None
        self.select_next_input()

    def get_frame(self, flip=True):
        """Return the current frame as numpy array"""
        ret, frame = self._input.read()
        if flip:
            frame = cv2.flip(frame, 1)
        return frame

    def select_next_input(self):
        """Select the next input.

        Raise IO Error if no input is found."""
        MAX_NR_DEVICES_ARBITRARILY_SET = 100
        for _ in range(MAX_NR_DEVICES_ARBITRARILY_SET):
            self._input_id = (self._input_id+1)%MAX_NR_DEVICES_ARBITRARILY_SET
            print(self._input_id)
            self._input = cv2.VideoCapture(self._input_id)
            if self._input.isOpened():
                break
        else:
            raise IOError("Cannot open any webcam")

    def release_input(self):
        self._input.release()
