# -*- coding: utf-8 -*-
"""
module for reading in stream
"""

import glob
import time

import cv2

from sail_utils.cv.base import _Streamer


class LiveStreamer(_Streamer):
    """
    class for read from a live feed
    """

    def __init__(self, source: str, rate: int, max_errors: int = 3600):
        super().__init__(source, rate)
        self._stream = cv2.VideoCapture(self.source)
        self._fps = self._stream.get(cv2.CAP_PROP_FPS)
        self._ratio = int(self._fps / rate)
        self._count = 0
        self._error_frames = 0
        self._max_errors = max_errors

    @property
    def max_errors_allowed(self) -> int:
        """
        get number of max errors allowed
        :return:
        """
        return self._max_errors

    @property
    def fps(self) -> int:
        """
        get stream fps
        :return:
        """
        return self._fps

    def __iter__(self):
        return self

    def __next__(self):
        while self._stream.isOpened():
            ret, frame = self._stream.read()
            if ret:
                self._error_frames = 0
                self._count += 1

                if self._count >= self._ratio:
                    self._count = 0
                    return frame, time.time()
            else:
                self._error_frames += 1
                if self._error_frames >= self._max_errors:
                    raise StopIteration("# of error is greater than allowed. stop stream")
        else:
            raise StopIteration("stream is closed")

    def __del__(self):
        self._stream.release()


class ImageFileStreamer(_Streamer):
    """
    class for read from a folders file
    """

    def __init__(self, source, suffix: str = 'jpg', rate: int = 1):
        super().__init__(source, rate)
        self._stream = glob.glob((self._source / ("**" + suffix)).as_posix(), recursive=True)
        self._stream = sorted(self._stream, key=lambda x: (len(x), x))
        self._rate = rate
        self._start = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._start >= len(self._stream):
            raise StopIteration()

        file_loc = self._stream[self._start]
        self._start += self._rate
        img = cv2.imread(file_loc, cv2.IMREAD_COLOR)
        return img, file_loc


class VideoFileStreamer(_Streamer):
    """
    class for read frame from a video file
    """

    def __init__(self, source, rate: int = 1):
        super().__init__(source, rate)
        self._rate = rate
        self._stream = cv2.VideoCapture(self.source)
        self._start = 0

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            ret, img = self._stream.read()
            if not ret:
                raise StopIteration

            self._start += 1
            if self._start % self._rate == 0:
                return img, None
