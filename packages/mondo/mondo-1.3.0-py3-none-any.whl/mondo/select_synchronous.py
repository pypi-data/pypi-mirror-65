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

from PySide2 import QtWidgets

from .ui_select_synchronous import Ui_SelectSynchronousDialog

logger = logging.getLogger(__name__)


class SelectSynchronousDialog(QtWidgets.QDialog, Ui_SelectSynchronousDialog):
    def __init__(self, streams, channels, parent=None):
        super().__init__(parent)

        self.streams = streams
        self.channels = channels

        # these are ordered by display order
        self.stream_buttons = []  # radio buttons
        self.channel_groups = []  # {ch_index: check box}

        self.widgets = []  # to prevent premature garbage collection

        self.setupUi(self)

        self.add_buttons()

    def add_buttons(self):
        d = {}  # key: min(channel index), value: stream index

        # sort the streams by lowest channel index
        for stream_index, stream in enumerate(self.streams):
            stream_channels = stream.channel_index_list[:stream.channel_count]
            d[min(stream_channels)] = stream_index

        for _sort_key, stream_index in sorted(d.items()):
            stream = self.streams[stream_index]
            stream_channels = stream.channel_index_list[:stream.channel_count]

            if not stream_channels:
                continue

            # create the radio button
            radio_button = QtWidgets.QRadioButton(
                "Stream {}".format(stream_index), parent=self)
            self.stream_buttons.append(radio_button)
            self.verticalLayout.addWidget(radio_button)

            group_widget = QtWidgets.QWidget(parent=self)
            self.widgets.append(group_widget)
            layout = QtWidgets.QVBoxLayout(group_widget)

            channel_group = {}
            self.channel_groups.append(channel_group)

            # create the channel check box group
            for channel_index in sorted(stream_channels):
                channel = self.channels[channel_index]
                channel_name = channel.name.decode("utf-8")
                check_box = QtWidgets.QCheckBox(channel_name,
                                                parent=group_widget)
                channel_group[channel_index] = check_box
                check_box.setChecked(False)
                layout.addWidget(check_box)

            self.verticalLayout.addWidget(group_widget)
            group_widget.setEnabled(False)

            # connect the triggered signal to the enabled slot
            radio_button.toggled.connect(group_widget.setEnabled)

        self.stream_buttons[0].setChecked(True)

    def get_channel_list(self):
        for i, stream_button in enumerate(self.stream_buttons):
            if stream_button.isChecked():
                indexes = set()
                for ch_index, check_box in self.channel_groups[i].items():
                    if check_box.isChecked():
                        indexes.add(ch_index)
                return sorted(indexes)

        return []  # error condition, shouldn't happen
