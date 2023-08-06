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
import os
import sys

from PySide2 import QtCore, QtWidgets

from . import __version__ as version
from .ui_about import Ui_AboutDialog

logger = logging.getLogger(__name__)


class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.setupUi(self)

        is_frozen = getattr(sys, 'frozen', False)
        if is_frozen:
            # load the build_info.txt
            main_dir = os.path.dirname(sys.executable)
            build_info_filename = os.path.join(main_dir, "build_info.txt")
            try:
                with open(build_info_filename, "r") as f:
                    lines = f.readlines()
                    build_date = lines[3].strip()
            except:
                logger.exception('Could not read build_info.txt')
                build_date = "ERROR"
        else:
            build_date = "Unknown"

        label_str = self.softwareLabel.text().format(version, build_date)
        self.softwareLabel.setText(label_str)

        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
