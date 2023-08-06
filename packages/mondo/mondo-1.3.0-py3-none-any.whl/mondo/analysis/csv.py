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

import datetime
from fractions import gcd
import functools
import logging
import os.path

import numpy
from PySide2 import QtCore, QtWidgets

from . import util

logger = logging.getLogger(__name__)


def get_csv_file(default_name, parent=None):
    settings = QtCore.QSettings()

    # find the directory from settings
    directory = settings.value("fileSaveDirectory")
    if directory and type(directory) == str:
        if not os.path.isdir(directory):
            directory = None

    if not directory:
        directory = ""

    file_and_dir = os.path.join(directory, default_name)

    # ask the user for the file name
    caption = "Save File"
    file_filter = "Comma Seperated Value Files (*.csv);;All Files (*.*)"
    val = QtWidgets.QFileDialog.getSaveFileName(parent, caption, file_and_dir,
                                                file_filter)
    output_path = val[0]

    if output_path:
        # save the directory
        output_dir = os.path.dirname(output_path)
        settings.setValue("fileSaveDirectory", output_dir)
        return output_path
    else:
        return None


def do_downsample(array, downsample_factor):
    pad_size = (downsample_factor - (array.size % downsample_factor))
    if pad_size == downsample_factor:
        pad_size = 0
    padded_array = numpy.append(array, numpy.zeros(pad_size) * numpy.nan)
    reshaped = padded_array.reshape((-1, downsample_factor))
    result = numpy.nanmean(reshaped, axis=1)
    return result


def csv_export(parent=None, downsample=False):
    ret = util.load_batch(parent=parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    file_infos, header = ret

    if downsample:
        downsample_factor, ok = QtWidgets.QInputDialog.getInt(
            parent, "Downsample Factor", "Input downsample factor",
            value=2, minValue=2, maxValue=2147483647)
        if not ok:
            return
    else:
        downsample_factor = 1

    channel_indexes = util.choose_synchronous_channels(header, parent)
    if channel_indexes is None:
        return  # error message displayed, or user cancelled

    batch_info = util.decode_batch(file_infos, header, channel_indexes,
                                   parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    batch_info = util.get_datetime_subset(batch_info, parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    ret = util.warn_about_lost_packets(batch_info, once=True, parent=parent)
    if not ret:
        return  # user cancelled

    sequence_info, unit_info = util.sequence_data(batch_info, chunk=True,
                                                  parent=parent)

    def lcm(iterable):
        return functools.reduce(lambda x, y: x * y // gcd(x, y), iterable)

    samples_lcm = lcm(header['channels'][i].samples for i in channel_indexes)

    # make sure channels all have the same number of gaps
    chunk_count = None
    for sequence in sequence_info.values():
        if chunk_count is None:
            chunk_count = len(sequence)
        else:
            if len(sequence) != chunk_count:
                message = "Channels don't share lost packets!"
                logger.error(message)
                QtWidgets.QMessageBox.critical(parent, "Error", message)
                return

    all_data = []  # holds tuples of (data, first_time)

    for chunk_index in range(chunk_count):
        data_list = []

        first_time = None
        first_data_length = None

        for channel_index in sorted(channel_indexes):
            channel = header['channels'][channel_index]
            sequence = sequence_info[channel_index]
            time, data, _start, _end = sequence[chunk_index]

            expand_factor = samples_lcm // channel.samples
            expanded_data = numpy.repeat(data, expand_factor, axis=0)

            if downsample:
                expanded_data = numpy.apply_along_axis(
                    do_downsample, 0, expanded_data, downsample_factor)

            if first_time is None:
                first_time = time[0]
                first_data_length = len(expanded_data)
            else:
                if first_time != time[0]:
                    message = "Mismatch in channel times!"
                    logger.error(message)
                    QtWidgets.QMessageBox.critical(parent, "Error", message)
                    return
                if first_data_length != len(expanded_data):
                    message = "Mismatch in channel data sizes!"
                    logger.error(message)
                    QtWidgets.QMessageBox.critical(parent, "Error", message)
                    return

            data_list.append(expanded_data)

        all_data.append((numpy.concatenate(data_list, axis=1), first_time))

    first_timestamp = sequence_info[channel_indexes[0]][0][2]
    dt = datetime.datetime.fromtimestamp(first_timestamp,
                                         datetime.timezone.utc)
    default_name = "{}_{}.csv".format(dt.strftime("%Y_%m_%d_%H.%M"),
                                      header['serial_number'])

    stream = batch_info[channel_indexes[0]].stream
    interval = downsample_factor / (stream.rate * samples_lcm)

    row_count = sum(len(data) for data, _time in all_data)
    position = 0

    filename = get_csv_file(default_name)
    if filename is None:
        return

    window_flags = (QtCore.Qt.MSWindowsFixedSizeDialogHint)
    progress = QtWidgets.QProgressDialog("Writing CSV...", "Abort", 0,
                                         row_count, parent, window_flags)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.forceShow()

    with open(filename, "w") as f:
        # write the CSV header
        f.write("Time (s)")
        for channel_index in sorted(channel_indexes):
            channel_data = batch_info[channel_index]
            unit_str = unit_info[channel_index]['ascii']
            for name in channel_data.channel_decoder.subchannel_names:
                if unit_str:
                    f.write(", {} ({})".format(name, unit_str))
                else:
                    f.write(", {}".format(name))
        f.write("\n")

        for data, first_time in all_data:
            for i, row in enumerate(data):
                # print the time
                t = first_time + i * interval
                f.write("{}".format(t))

                for value in row:
                    f.write(", {}".format(value))
                f.write("\n")

                position += 1
                progress.setValue(position)
                if position % 100 == 0:
                    QtCore.QCoreApplication.processEvents()
                    if progress.wasCanceled():
                        message = "Aborting {}!".format(
                            os.path.basename(filename))
                        logger.info(message)
                        return

    message = "Finished writing {}!".format(os.path.basename(filename))
    logger.info(message)
    QtWidgets.QMessageBox.information(parent, "Written", message)
