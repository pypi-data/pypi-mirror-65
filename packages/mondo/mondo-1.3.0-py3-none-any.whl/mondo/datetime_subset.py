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

from PySide2 import QtCore, QtWidgets

from .ui_datetime_subset import Ui_DateTimeSubsetDialog

logger = logging.getLogger(__name__)


class DateTimeSubsetDialog(QtWidgets.QDialog, Ui_DateTimeSubsetDialog):
    def __init__(self, start_qdt, end_qdt, parent=None):
        super().__init__(parent, QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.start_qdt = start_qdt
        self.end_qdt = end_qdt

        self.setupUi(self)

        start_py = start_qdt.toPython()
        end_py = end_qdt.toPython()
        if end_py >= start_py:
            duration = int((end_py - start_py).total_seconds())
        else:
            duration = 0
            self.useSubset.setEnabled(False)

        # write the all data labels
        self.allStart.setText(self.startDateTime.textFromDateTime(start_qdt))
        self.allEnd.setText(self.endDateTime.textFromDateTime(end_qdt))
        self.allDuration.setText("{} s".format(duration))

        self.startDateTime.setDateTime(start_qdt)
        self.startDateTime.setWrapping(True)
        self.endDateTime.setDateTime(end_qdt)
        self.endDateTime.setWrapping(True)

        self.startSeconds.setMinimum(0)
        self.startSeconds.setMaximum(duration)
        self.startSeconds.setValue(0)
        self.endSeconds.setMinimum(-duration)
        self.endSeconds.setMaximum(0)
        self.endSeconds.setValue(0)
        self.duration.setMinimum(0)
        self.duration.setMaximum(duration)
        self.duration.setValue(duration)

        self.startDateTime.setCurrentSection(
            QtWidgets.QDateTimeEdit.SecondSection)
        self.endDateTime.setCurrentSection(
            QtWidgets.QDateTimeEdit.SecondSection)

        self.startDateTime.dateTimeChanged.connect(self.start_changed)
        self.startDateTime.editingFinished.connect(self.start_editing_finished)
        self.endDateTime.dateTimeChanged.connect(self.end_changed)
        self.endDateTime.editingFinished.connect(self.end_editing_finished)

        self.startSeconds.valueChanged.connect(self.start_seconds_changed)
        self.endSeconds.valueChanged.connect(self.end_seconds_changed)
        self.duration.valueChanged.connect(self.duration_changed)

        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

    def should_use_all(self):
        return self.useAllData.isChecked()

    def trim_datetime_to_range(self, value):
        if value < self.start_qdt:
            return self.start_qdt
        elif value > self.end_qdt:
            return self.end_qdt
        else:
            return value

    def datetime_in_range(self, value):
        return ((self.start_qdt <= value) and (value <= self.end_qdt))

    def get_subset(self):
        start_qdt = self.trim_datetime_to_range(self.startDateTime.dateTime())
        end_qdt = self.trim_datetime_to_range(self.endDateTime.dateTime())
        return (start_qdt, end_qdt)

    def start_changed(self, new_date_time):
        self.update_duration(moving_start=True)

        if self.datetime_in_range(new_date_time):
            if self.endDateTime.dateTime() < new_date_time:
                # start is later than end
                self.startDateTime.setStyleSheet(
                    "* { background-color: yellow }")
            else:
                # valid
                self.startDateTime.setStyleSheet("")
        else:
            # outside the bounds
            self.startDateTime.setStyleSheet("* { background-color: red }")

    def end_changed(self, new_date_time):
        self.update_duration(moving_start=False)

        if self.datetime_in_range(new_date_time):
            if new_date_time < self.startDateTime.dateTime():
                # end is before start
                self.endDateTime.setStyleSheet(
                    "* { background-color: yellow }")
            else:
                # valid
                self.endDateTime.setStyleSheet("")
        else:
            # outside the bounds
            self.endDateTime.setStyleSheet("* { background-color: red }")

    def start_editing_finished(self):
        if self.datetime_in_range(self.startDateTime.dateTime()):
            if self.endDateTime.dateTime() <= self.startDateTime.dateTime():
                self.endDateTime.setDateTime(self.startDateTime.dateTime())

                # trigger revalidation
                self.startDateTime.setDateTime(self.startDateTime.dateTime())
        else:
            self.startDateTime.setDateTime(self.start_qdt)

    def end_editing_finished(self):
        if self.datetime_in_range(self.endDateTime.dateTime()):
            if self.endDateTime.dateTime() <= self.startDateTime.dateTime():
                self.startDateTime.setDateTime(self.endDateTime.dateTime())

                # trigger revalidation
                self.endDateTime.setDateTime(self.endDateTime.dateTime())
        else:
            self.endDateTime.setDateTime(self.end_qdt)

    def update_duration(self, moving_start=True):
        start_qdt = self.startDateTime.dateTime()
        end_qdt = self.endDateTime.dateTime()

        if start_qdt < self.start_qdt:
            # clip to beginning
            start_py = self.start_qdt.toPython()
        elif self.end_qdt < start_qdt:
            # clip to end
            start_py = self.end_qdt.toPython()
        else:
            # ok
            start_py = start_qdt.toPython()

        if end_qdt < self.start_qdt:
            # clip to beginning
            end_py = self.start_qdt.toPython()
        elif self.end_qdt < end_qdt:
            # clip to end
            end_py = self.end_qdt.toPython()
        else:
            # ok
            end_py = end_qdt.toPython()

        if end_py < start_py:
            # overlapping
            if moving_start:
                end_py = start_py
            else:
                start_py = end_py

        start_seconds = (start_py - self.start_qdt.toPython()).total_seconds()
        self.startSeconds.setValue(start_seconds)
        end_seconds = (end_py - self.end_qdt.toPython()).total_seconds()
        self.endSeconds.setValue(end_seconds)

        self.duration.setValue((end_py - start_py).total_seconds())

    def start_seconds_changed(self, junk=None):
        new_start = self.start_qdt.addSecs(self.startSeconds.value())
        if new_start > self.endDateTime.dateTime():
            self.endDateTime.setDateTime(new_start)
        self.startDateTime.setDateTime(new_start)

    def end_seconds_changed(self, junk=None):
        new_end = self.end_qdt.addSecs(self.endSeconds.value())
        if new_end < self.startDateTime.dateTime():
            self.startDateTime.setDateTime(new_end)
        self.endDateTime.setDateTime(new_end)

    def duration_changed(self, junk=None):
        duration = self.duration.value()
        current_start = self.startDateTime.dateTime().toPython()
        end_py = self.end_qdt.toPython()
        headroom = int((end_py - current_start).total_seconds())

        if duration <= headroom:
            # just move the end
            self.endSeconds.setValue(duration - headroom)
        else:
            # need to move the start too
            self.endDateTime.setDateTime(self.end_qdt)
            self.startDateTime.setDateTime(self.end_qdt.addSecs(-duration))
