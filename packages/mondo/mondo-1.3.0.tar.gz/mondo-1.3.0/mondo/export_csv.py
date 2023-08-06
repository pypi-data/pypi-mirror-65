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

import os.path

from PySide2 import QtGui, QtWidgets

from . import mondo_rc  # needed for the icon
from .analysis.csv import get_csv_file


def _do_export(filename, labels, xdata, ydata):
    with open(filename, "w") as f:
        f.write(", ".join(labels))
        f.write("\n")

        for x, y in zip(xdata, ydata):
            f.write("{}, {}\n".format(x, y))


def add_export_csv_action(figure, labels, data):
    toolbar = figure.canvas.toolbar
    actionText = QtWidgets.QApplication.translate("ExportCSVAction",
                                                  "Export CSV")
    action = QtWidgets.QAction(actionText, toolbar)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/icon/icons/export-csv.png"))
    action.setIcon(icon)

    def handle_export():
        base_file = get_csv_file("export", parent=toolbar)
        if not base_file:
            return

        root, ext = os.path.splitext(base_file)

        for xdata, ydata, name in data:
            if len(data) == 1:
                filename = base_file
            else:
                filename = root + "_" + name + ext

            _do_export(filename, labels, xdata, ydata)

    action.triggered.connect(handle_export)

    toolbar.addAction(action)
