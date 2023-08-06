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

from .ui_select_subchannels import Ui_SelectSubchannelsDialog

logger = logging.getLogger(__name__)


class SelectSubchannelsDialog(QtWidgets.QDialog, Ui_SelectSubchannelsDialog):
    def __init__(self, names, parent=None):
        super().__init__(parent)

        self.names = names  # [(channel_id, channel_name, subchannel_names)]

        # these are ordered by display order
        self.subchannel_buttons = {}  # (ch_id, subchannel_id): check box

        self.widgets = []  # to prevent premature garbage collection

        self.setupUi(self)

        self.add_buttons()

    def add_buttons(self):
        for channel_id, channel_name, subchannel_names in sorted(self.names):
            if len(subchannel_names) > 1:
                # create a label for the channel
                channel_label = QtWidgets.QLabel(channel_name)
                self.widgets.append(channel_label)
                self.verticalLayout.addWidget(channel_label)

                group_widget = QtWidgets.QWidget(parent=self)
                self.widgets.append(group_widget)
                layout = QtWidgets.QVBoxLayout(group_widget)

                for i, subchannel_name in enumerate(subchannel_names):
                    check_box = QtWidgets.QCheckBox(subchannel_name,
                                                    parent=group_widget)
                    self.subchannel_buttons[(channel_id, i)] = check_box
                    check_box.setChecked(False)
                    layout.addWidget(check_box)

                self.verticalLayout.addWidget(group_widget)
            else:
                # just a single subchannel, no need for the label
                check_box = QtWidgets.QCheckBox(subchannel_names[0])
                self.subchannel_buttons[(channel_id, 0)] = check_box
                check_box.setChecked(False)
                self.widgets.append(check_box)
                self.verticalLayout.addWidget(check_box)

    def get_subchannels_list(self):
        selected_subchannels = []
        for index_tuple in sorted(self.subchannel_buttons.keys()):
            check_box = self.subchannel_buttons[index_tuple]
            if check_box.isChecked():
                selected_subchannels.append(index_tuple)
        return selected_subchannels
