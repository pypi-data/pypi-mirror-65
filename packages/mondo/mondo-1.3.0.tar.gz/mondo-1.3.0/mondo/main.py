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

import importlib
import logging
import os
import subprocess
import sys
import tempfile
import threading

from PySide2 import QtCore, QtWidgets

import asphodel
import hyperborea.download

from .ui_main import Ui_MondoMainWindow
from .about import AboutDialog
from .analysis import csv, file, psd, spectrogram, time
from .preferences import PreferencesDialog

logger = logging.getLogger(__name__)


class MondoMainWindow(QtWidgets.QMainWindow, Ui_MondoMainWindow):
    find_update_finished = QtCore.Signal(object)
    update_download_finished = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.update_progress_lock = threading.Lock()

        self.setupUi(self)

        self.extra_ui_setup()
        self.setup_callbacks()
        self.setup_update_actions()

    def extra_ui_setup(self):
        self.update_progress = QtWidgets.QProgressDialog("", "", 0, 100)
        self.update_progress.setLabelText(self.tr(""))
        self.update_progress.setWindowTitle(self.tr("Check for Update"))
        self.update_progress.setCancelButton(None)
        self.update_progress.setWindowModality(QtCore.Qt.WindowModal)
        self.update_progress.setMinimumDuration(0)
        self.update_progress.setAutoReset(False)
        self.update_progress.reset()

    def setup_callbacks(self):
        self.timeButton.clicked.connect(self.time_analysis)
        self.synchronousTimeButton.clicked.connect(
            self.synchronous_time_analysis)
        self.overlaidTimeButton.clicked.connect(self.overlaid_time_analysis)
        self.spectrogramButton.clicked.connect(self.spectrogram_analysis)
        self.psdButton.clicked.connect(self.psd_analysis)
        self.singleChannelPsdButton.clicked.connect(
            self.single_channel_psd_analysis)
        self.singleSlicePsdButton.clicked.connect(
            self.single_slice_psd_analysis)
        self.overlaidPsdButton.clicked.connect(self.overlaid_psd_analysis)
        self.csvButton.clicked.connect(self.csv_export)
        self.csvDownsampledButton.clicked.connect(self.csv_downsampled_export)
        self.fileInformationButton.clicked.connect(self.file_information)
        self.viewSettingsButton.clicked.connect(self.view_settings)
        self.rawExportButton.clicked.connect(self.raw_export)
        self.splitFileButton.clicked.connect(self.split_file)

        self.actionPreferences.triggered.connect(self.show_preferences)

        self.actionAbout.triggered.connect(self.show_about)
        self.actionAboutLibraries.triggered.connect(self.show_about_libraries)

        self.actionUpdateLatestStable.triggered.connect(
            self.update_latest_stable)
        self.actionUpdateCurrentBranch.triggered.connect(
            self.update_current_branch)
        self.actionUpdateSpecificBranch.triggered.connect(
            self.update_specific_branch)
        self.actionUpdateSpecificCommit.triggered.connect(
            self.update_specific_commit)

        self.update_progress_timer = QtCore.QTimer(self)
        self.update_progress_timer.timeout.connect(self.update_progress_cb)

        self.software_finder = hyperborea.download.SoftwareFinder()
        self.software_finder.completed.connect(self.update_finder_completed)
        self.software_finder.error.connect(self.update_finder_error)
        self.software_downloader = hyperborea.download.Downloader()
        self.software_downloader.completed.connect(
            self.software_download_completed)
        self.software_downloader.error.connect(self.software_download_error)

    def setup_update_actions(self):
        is_frozen = getattr(sys, 'frozen', False)

        valid_info = False
        if is_frozen:
            # load the build_info.txt
            main_dir = os.path.dirname(sys.executable)
            build_info_filename = os.path.join(main_dir, "build_info.txt")
            try:
                with open(build_info_filename, "r") as f:
                    lines = f.readlines()
                    self.branch_name = lines[0].strip()
                    self.commit_hash = lines[1].strip()
                    self.build_key = lines[2].strip()
                    valid_info = True
            except:
                logger.exception('Could not read build_info.txt')

        if not valid_info:
            self.menuCheckForUpdates.setEnabled(False)
            self.menuCheckForUpdates.setTitle(self.tr("Not Updatable"))
            self.actionUpdateLatestStable.setEnabled(False)
            self.actionUpdateCurrentBranch.setEnabled(False)
            self.actionUpdateSpecificBranch.setEnabled(False)
            self.actionUpdateSpecificCommit.setEnabled(False)
        else:
            if self.branch_name == "master":
                # master is latest stable
                self.actionUpdateCurrentBranch.setEnabled(False)
                self.actionUpdateCurrentBranch.setVisible(False)
            else:
                action_str = self.tr("Latest {}").format(self.branch_name)
                self.actionUpdateCurrentBranch.setText(action_str)

    def find_update(self, branch=None, commit=None):
        self.update_progress.setMinimum(0)
        self.update_progress.setMaximum(0)
        self.update_progress.setValue(0)
        self.update_progress.setLabelText(self.tr("Checking for update..."))
        self.update_progress.forceShow()

        self.software_finder.find_software("mondo", self.build_key, branch,
                                           commit)

    def update_finder_error(self, error_str):
        self.update_progress.reset()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)

    def update_finder_completed(self, params):
        self.update_progress.reset()
        url, commit, ready = params

        if commit is not None and commit == self.commit_hash:
            logger.info("Up to date with commit %s", commit)
            QtWidgets.QMessageBox.information(
                self, self.tr("Up to date"),
                self.tr("Already running this version"))
            return

        if not ready:
            logger.info("Update is not ready")
            QtWidgets.QMessageBox.information(
                self, self.tr("Update not ready"),
                self.tr("Update is not ready"))
            return

        # ask if the user wants to proceed
        ret = QtWidgets.QMessageBox.question(
            self, self.tr("Update?"), self.tr("Update available. Update now?"),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if ret != QtWidgets.QMessageBox.Yes:
            return

        logger.info("Downloading update from %s", url)

        self.update_progress.setMinimum(0)
        self.update_progress.setMaximum(0)
        self.update_progress.setValue(0)
        self.update_progress.setLabelText(self.tr("Downloading update..."))
        self.update_progress.forceShow()

        self.update_progress_written = 0
        self.update_progress_total = 0

        fd, filename = tempfile.mkstemp(".exe", "setup-", text=False)
        file = os.fdopen(fd, "wb")
        file.filename = filename
        self.software_downloader.start_download(url, file,
                                                self.update_progress_func)

        self.update_progress_timer.start(20)  # 20 milliseconds

    def update_progress_func(self, written_bytes, total_length):
        with self.update_progress_lock:
            self.update_progress_total = total_length
            self.update_progress_written = written_bytes

    def update_progress_cb(self):
        with self.update_progress_lock:
            if self.update_progress_total != 0:
                self.update_progress.setMinimum(0)
                self.update_progress.setMaximum(self.update_progress_total)
                self.update_progress.setValue(self.update_progress_written)

    def software_download_error(self, file, error_str):
        self.update_progress_timer.stop()
        self.update_progress.reset()
        file.close()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)
        os.unlink(file.filename)

    def software_download_completed(self, file):
        self.update_progress_timer.stop()
        self.update_progress.reset()
        file.close()

        # run the intstaller
        subprocess.Popen([file.filename, '/silent', "/DeleteInstaller=Yes",
                          "/SP-", "/SUPPRESSMSGBOXES", "/NORESTART",
                          "/NOCANCEL"])

        # close the application (though installer will force kill regardless)
        self.close()

    def update_latest_stable(self):
        self.find_update(branch="master")

    def update_current_branch(self):
        self.find_update(branch=self.branch_name)

    def update_specific_branch(self):
        branch, ok = QtWidgets.QInputDialog.getText(
            self, self.tr("Branch"), self.tr("Branch:"),
            QtWidgets.QLineEdit.Normal, "master")
        if not ok:
            return

        branch = branch.strip()

        self.find_update(branch=branch)

    def update_specific_commit(self):
        commit, ok = QtWidgets.QInputDialog.getText(
            self, self.tr("Commit"), self.tr("Commit:"),
            QtWidgets.QLineEdit.Normal, "")
        if not ok:
            return

        commit = commit.strip()

        self.find_update(commit=commit)

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def _get_version(self, library):
        try:
            lib = importlib.import_module(library)
            return lib.__version__
        except (AttributeError, ImportError):
            return "ERROR"

    def show_about_libraries(self):
        libraries = ["numpy", "scipy", "PySide2", "matplotlib", 'hyperborea']
        vers = {}
        for lib in libraries:
            vers[lib] = self._get_version(lib)

        # special case for asphodel and asphodel_py
        vers["asphodel_py"] = self._get_version("asphodel")
        vers["asphodel"] = asphodel.build_info

        # python version (sys.version is too long)
        is_64bit = sys.maxsize > (2 ** 32)
        bit_str = "64 bit" if is_64bit else "32 bit"
        python_ver = ".".join(map(str, sys.version_info[:3]))
        python_str = "{} ({} {})".format(python_ver, sys.platform, bit_str)
        vers['python'] = python_str

        s = "\n".join(k + ": " + vers[k] for k in sorted(vers, key=str.lower))
        QtWidgets.QMessageBox.information(self, "About Libraries", s)

    def do_analysis(self, analysis, *args, **kwargs):
        try:
            analysis(self, *args, **kwargs)
        except:
            logger.exception("Uncaught exception")
            QtWidgets.QMessageBox.critical(
                self, "Error", "Uncaught exception. See log for details.")

    def time_analysis(self):
        self.do_analysis(time.time_analysis)

    def synchronous_time_analysis(self):
        self.do_analysis(time.synchronous_time_analysis)

    def overlaid_time_analysis(self):
        self.do_analysis(time.overlaid_time_analysis)

    def spectrogram_analysis(self):
        self.do_analysis(spectrogram.spectrogram_analysis)

    def psd_analysis(self):
        self.do_analysis(psd.psd_analysis)

    def single_channel_psd_analysis(self):
        self.do_analysis(psd.single_channel_psd_analysis)

    def single_slice_psd_analysis(self):
        self.do_analysis(psd.single_slice_psd_analysis)

    def overlaid_psd_analysis(self):
        self.do_analysis(psd.overlaid_psd_analysis)

    def csv_export(self):
        self.do_analysis(csv.csv_export)

    def csv_downsampled_export(self):
        self.do_analysis(csv.csv_export, downsample=True)

    def file_information(self):
        self.do_analysis(file.file_information)

    def view_settings(self):
        self.do_analysis(file.view_settings)

    def raw_export(self):
        self.do_analysis(file.raw_export)

    def split_file(self):
        self.do_analysis(file.split_file)

    def show_preferences(self):
        dialog = PreferencesDialog(self)
        dialog.exec_()
