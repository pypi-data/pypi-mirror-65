#!/usr/bin/env python3

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

import logging.handlers
import multiprocessing
import os
import sys
import time

from PySide2 import QtCore, QtGui, QtWidgets

import mondo

# wrapper around "import matplotlib" that captures any commands for later use
from mondo.export_script import matplotlib_wrapper as matplotlib

from .main import MondoMainWindow
from . import mondo_rc  # needed for the icon

logger = logging.getLogger(__name__)


def main_is_frozen():
    """Return True if the script is frozen, False otherwise."""
    return getattr(sys, 'frozen', False)


def get_main_dir():
    """Return the path of the main script's directory, even when frozen."""
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def setup_logging():
    """Configure logging for the whole program."""

    def my_excepthook(exctype, value, traceback):
        """Log the caught exception using the logging module."""
        exc_info = (exctype, value, traceback)
        logger.error("Uncaught Exception", exc_info=exc_info)

    sys.excepthook = my_excepthook

    # get an appropriate location for the log file
    logdir = QtCore.QStandardPaths.writableLocation(
        QtCore.QStandardPaths.DataLocation)
    logfile = os.path.join(logdir, "main.log")

    # make sure the directory exists
    os.makedirs(logdir, exist_ok=True)

    # create a log file handler
    file_log_handler = logging.handlers.RotatingFileHandler(logfile,
                                                            maxBytes=10e6,
                                                            backupCount=9)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_formatter.default_time_format = '%Y-%m-%dT%H:%M:%S'
    file_formatter.default_msec_format = '%s,%03dZ'
    file_formatter.converter = time.gmtime
    file_log_handler.setFormatter(file_formatter)
    file_log_handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_log_handler)
    root_logger.setLevel(logging.DEBUG)

    # remove pyusb's logging info
    pyusb_logger = logging.getLogger("usb")
    pyusb_logger.propagate = False

    # remove matplotlib debug level
    matplotlib_logger = logging.getLogger("matplotlib")
    matplotlib_logger.setLevel(logging.INFO)


def main():
    """Run the program."""

    # freeze_support() MUST be first. Anything before this will cease to exist
    multiprocessing.freeze_support()

    # work around for requests library to find root certificates
    if main_is_frozen():
        cacert = os.path.join(os.path.dirname(sys.executable), 'cacert.pem')
        os.environ["REQUESTS_CA_BUNDLE"] = cacert

    if not sys.stdout or not sys.stderr:
        sys.stdout = open(os.devnull)
        sys.stderr = open(os.devnull)

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Mondo")
    app.setOrganizationDomain("suprocktech.com")
    app.setOrganizationName("Suprock Tech")

    # load the application icon
    icon = QtGui.QIcon()
    icon_reader = QtGui.QImageReader(":/mondo.ico")
    while True:
        pixmap = QtGui.QPixmap.fromImage(icon_reader.read())
        icon.addPixmap(pixmap)
        if not icon_reader.jumpToNextImage():
            break
    app.setWindowIcon(icon)

    # force the settings to use an INI file instead of the registry
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)

    # remove "What's This" button across the whole application
    app.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)

    app.setApplicationVersion(mondo.__version__)

    setup_logging()

    logger.info("Mondo started (Version {})".format(mondo.__version__))

    # fix for matplotlib unicode characters like Omega
    matplotlib.rc('font', size=17)

    mainwin = MondoMainWindow()
    mainwin.show()
    app.exec_()

    logger.info("Mondo finished")


if __name__ == '__main__':
    main()
