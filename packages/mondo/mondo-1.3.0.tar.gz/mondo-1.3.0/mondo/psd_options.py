# Copyright (c) 2016 Electric Power Research Institute, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the EPRI nor the names of its contributors may be used
#    to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import logging
import math

import numpy
from PySide2 import QtCore, QtWidgets
import scipy.signal.windows

from .ui_psd_options import Ui_PSDOptionsWidget

logger = logging.getLogger(__name__)


class PSDOptionsWidget(QtWidgets.QWidget, Ui_PSDOptionsWidget):
    def __init__(self, chunks_list, sampling_rate, parent=None):
        super().__init__(parent)

        self.chunks_list = chunks_list
        self.sampling_rate = sampling_rate

        self.setupUi(self)

        self.fill_combo_boxes()

        self.changing_overlap = False

        self.fftPoints.currentIndexChanged.connect(self.fft_points_changed)
        self.overlapPercent.valueChanged.connect(self.overlap_percent_changed)
        self.overlapPoints.valueChanged.connect(self.overlap_points_changed)

        self.fft_points_changed()
        self.overlapPercent.setValue(50.0)

        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

    def fill_combo_boxes(self):
        max_lengths = []
        for chunks in self.chunks_list:
            max_lengths.append(max(len(c[0]) for c in chunks))
        max_length = min(max_lengths)

        max_pow_2 = math.floor(math.log2(max_length))
        min_pow_2 = 8  # 256 points

        self.fft_points_by_index = []
        for i in range(min_pow_2, max_pow_2 + 1):
            points = 2 ** i
            s = "{} (2^{})".format(points, i)
            self.fft_points_by_index.append(points)
            self.fftPoints.addItem(s)

        default_pow_2 = max(min_pow_2, max_pow_2 - 3)
        default_index = default_pow_2 - min_pow_2
        self.fftPoints.setCurrentIndex(default_index)

        # populate window functions
        self.window_functions = [("Hann", self.hann_window),
                                 ("Hamming", self.hamming_window),
                                 ("Flat Top", self.flattop_window),
                                 ("None (Uniform)", self.uniform_window)]
        for key, _value in self.window_functions:
            self.windowFunction.addItem(key)
        self.windowFunction.setCurrentIndex(0)

        self.detrend_options = [("Linear", "linear"),
                                ("Mean", "mean"),
                                ("None", "none")]
        for key, _value in self.detrend_options:
            self.detrendMethod.addItem(key)
        self.detrendMethod.setCurrentIndex(0)

    def update_window_count(self, window_size, overlap_points):
        window_counts = []
        for chunks in self.chunks_list:
            window_count = 0
            for chunk in chunks:
                chunk_size = len(chunk[0])
                window_count += (1 + ((chunk_size - window_size) //
                                      (window_size - overlap_points)))
            window_counts.append(window_count)
        s = ", ".join(str(w) for w in window_counts)
        self.windowCount.setText(s)

    def fft_points_changed(self, junk=None):
        index = self.fftPoints.currentIndex()
        window_size = self.fft_points_by_index[index]

        original_percent = self.overlapPercent.value()

        if self.overlapPoints.value() >= window_size:
            self.overlapPoints.setValue(window_size - 1)
        self.overlapPoints.setMaximum(window_size - 1)
        self.overlapPercent.setMaximum(100 * (window_size - 1) / window_size)

        # update the percentage (use existing)
        self.changing_overlap = True
        self.overlapPercent.setValue(original_percent)
        self.changing_overlap = False
        self.overlap_percent_changed()

        window_duration = window_size / self.sampling_rate
        self.duration.setText("{:.3f} s".format(window_duration))

        frequency_resolution = self.sampling_rate / window_size
        self.resolution.setText("{:.3f} Hz".format(frequency_resolution))

    def overlap_percent_changed(self, junk=None):
        if self.changing_overlap:
            return
        try:
            self.changing_overlap = True

            index = self.fftPoints.currentIndex()
            window_size = self.fft_points_by_index[index]

            percent = self.overlapPercent.value()
            points = math.floor(window_size * percent / 100)
            if points >= window_size:
                points = window_size - 1
            self.overlapPoints.setValue(points)

            self.update_window_count(window_size, points)
        finally:
            self.changing_overlap = False

    def overlap_points_changed(self, junk=None):
        if self.changing_overlap:
            return
        try:
            self.changing_overlap = True

            index = self.fftPoints.currentIndex()
            window_size = self.fft_points_by_index[index]

            points = self.overlapPoints.value()
            percent = points / window_size * 100
            self.overlapPercent.setValue(percent)

            self.update_window_count(window_size, points)
        finally:
            self.changing_overlap = False

    def hann_window(self, x):
        return scipy.signal.windows.hann(len(x), False) * x

    def hamming_window(self, x):
        return scipy.signal.windows.hamming(len(x), False) * x

    def flattop_window(self, x):
        return scipy.signal.windows.flattop(len(x), False) * x

    def uniform_window(self, x):
        return x

    def get_options(self):
        options = {"Fs": self.sampling_rate}

        index = self.fftPoints.currentIndex()
        window_size = self.fft_points_by_index[index]
        options['NFFT'] = window_size

        options['noverlap'] = self.overlapPoints.value()

        index = self.windowFunction.currentIndex()
        window_function = self.window_functions[index][1]
        options['window'] = window_function(numpy.ones(window_size,
                                                       dtype=numpy.double))

        index = self.detrendMethod.currentIndex()
        options['detrend'] = self.detrend_options[index][1]

        return options


class PSDOptionsDialog(QtWidgets.QDialog):
    def __init__(self, chunks_list, sampling_rate, parent=None):
        super().__init__(parent, QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.psd_options = PSDOptionsWidget(chunks_list, sampling_rate, self)
        self.verticalLayout.addWidget(self.psd_options)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                          QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.setWindowTitle(self.tr("PSD Options"))

    def get_options(self):
        return self.psd_options.get_options()


class MultiplePSDOptionsDialog(QtWidgets.QDialog):
    def __init__(self, sections, parent=None):
        # NOTE: WindowTitleHint | WindowSystemMenuHint disables "What's This"
        super().__init__(parent, QtCore.Qt.WindowTitleHint |
                         QtCore.Qt.WindowSystemMenuHint)

        self.psd_options = []
        self.extra_widgets = []  # to prevent garbage collection

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.scrollAreaContents = QtWidgets.QWidget()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaContents)

        for i, (label_text, chunks_list, sampling_rate) in enumerate(sections):
            groupbox = QtWidgets.QGroupBox(self)
            self.extra_widgets.append(groupbox)

            layout = QtWidgets.QVBoxLayout(groupbox)

            label = QtWidgets.QLabel(groupbox)
            label.setText(label_text)
            label.setWordWrap(True)
            self.extra_widgets.append(label)
            layout.addWidget(label)

            spacer = QtWidgets.QSpacerItem(
                0, 20, QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.MinimumExpanding)
            layout.addItem(spacer)

            widget = PSDOptionsWidget(chunks_list, sampling_rate, groupbox)
            self.psd_options.append(widget)
            layout.addWidget(widget)

            self.horizontalLayout.addWidget(groupbox)

            if i < 3:
                # set the minimum size to 3 complete groups
                size_hint = self.scrollAreaContents.sizeHint()
                horizontal_bar = self.scrollArea.horizontalScrollBar()
                min_bar_height = horizontal_bar.sizeHint().height()
                self.scrollArea.setMinimumHeight(size_hint.height() +
                                                 min_bar_height)
                self.scrollArea.setMinimumWidth(size_hint.width())

        self.scrollArea.setWidget(self.scrollAreaContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                          QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle(self.tr("PSD Options"))

    def get_options(self):
        return [w.get_options() for w in self.psd_options]
