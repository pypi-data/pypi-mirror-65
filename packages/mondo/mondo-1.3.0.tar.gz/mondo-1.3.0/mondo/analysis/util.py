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

import binascii
import bisect
import datetime
import json
import logging
import lzma
import operator
import os.path
import struct

import numpy
from PySide2 import QtCore, QtWidgets

import asphodel
import hyperborea.unit_preferences

from ..datetime_subset import DateTimeSubsetDialog
from ..psd_options import PSDOptionsDialog, MultiplePSDOptionsDialog
from ..select_subchannels import SelectSubchannelsDialog
from ..select_synchronous import SelectSynchronousDialog

logger = logging.getLogger(__name__)


def get_packdata_file(parent=None):
    settings = QtCore.QSettings()

    # find the directory from settings
    directory = settings.value("fileOpenDirectory")
    if directory and type(directory) == str:
        if not os.path.isdir(directory):
            directory = None

    if not directory:
        directory = ""

    # ask the user for the file name
    caption = "Open File"
    file_filter = "Packed Data Files (*.apd);;All Files (*.*)"
    val = QtWidgets.QFileDialog.getOpenFileName(parent, caption, directory,
                                                file_filter)
    output_path = val[0]

    if output_path:
        # save the directory
        output_dir = os.path.dirname(output_path)
        settings.setValue("fileOpenDirectory", output_dir)
        return output_path
    else:
        return None


def get_packdata_files(parent=None):
    settings = QtCore.QSettings()

    # find the directory from settings
    directory = settings.value("fileOpenDirectory")
    if directory and type(directory) == str:
        if not os.path.isdir(directory):
            directory = None

    if not directory:
        directory = ""

    # ask the user for the file name
    caption = "Open Files"
    file_filter = "Packed Data Files (*.apd);;All Files (*.*)"
    val = QtWidgets.QFileDialog.getOpenFileNames(parent, caption, directory,
                                                 file_filter)
    files = val[0]

    if len(files) > 0:
        # save the directory (use 1st file for simplicity)
        output_dir = os.path.dirname(files[0])
        settings.setValue("fileOpenDirectory", output_dir)
        return sorted(files)
    else:
        return None


def decode_header(header_bytes, parent=None):
    try:
        header_str = header_bytes.decode("UTF-8")
        header = json.loads(header_str)
    except:
        message = "Could not parse file header!"
        logger.exception(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return

    try:
        # convert the JSON info back into an actual Asphodel structure
        all_streams = [asphodel.AsphodelStreamInfo.from_json_obj(s)
                       for s in header['streams']]
        all_channels = [asphodel.AsphodelChannelInfo.from_json_obj(c)
                        for c in header['channels']]

        header['streams'] = all_streams
        header['channels'] = all_channels

        # stream rate info
        stream_rate_info = []
        for values in header.get('stream_rate_info', []):
            # fix floats getting converted to strings in older files
            values = [float(v) if isinstance(v, str) else v for v in values]

            if values is not None:
                stream_rate_info.append(asphodel.StreamRateInfo(*values))
            else:
                stream_rate_info.append(None)
        header['stream_rate_info'] = stream_rate_info

        # supplies
        supplies = []
        for name, values in header.get('supplies', []):
            # fix floats getting converted to strings in older files
            values = [float(v) if isinstance(v, str) else v for v in values]

            supplies.append((name, asphodel.SupplyInfo(*values)))
        header['supplies'] = supplies

        # control variables
        ctrl_vars = []
        for name, values, setting in header.get('ctrl_vars', []):
            # fix floats getting converted to strings in older files
            values = [float(v) if isinstance(v, str) else v for v in values]

            ctrl_vars.append((name, asphodel.CtrlVarInfo(*values), setting))
        header['ctrl_vars'] = ctrl_vars

        # nvm
        header['nvm'] = binascii.a2b_hex(header['nvm'])

        # custom enums: need to convert keys back from strings to ints
        custom_enums = {int(k): v for k, v in header['custom_enums'].items()}
        header['custom_enums'] = custom_enums

        # settings
        settings = []
        for setting_str in header['settings']:
            try:
                setting = asphodel.AsphodelSettingInfo.from_str(setting_str)
            except:
                setting = None
            settings.append(setting)
        header['settings'] = settings

    except:
        message = "Unknown error in file header!"
        logger.exception(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return

    return header


def load_single_file(parent=None):
    """
    returns (file_infos, header) where file_infos is a sequence of tuples
    containing (filename, dt).
    * header is the dictionary loaded from the file's JSON data, with
      appropriate conversions applied to Asphodel struct data.
    * filename is the absolute path to the file location.
    * dt is the UTC datetime of the first packet in the file.
    """

    filename = get_packdata_file(parent)
    if filename is None:
        return None  # user cancelled

    try:
        with lzma.LZMAFile(filename, "rb") as f:
            # read the header
            header_leader = struct.unpack(">dI", f.read(12))
            _header_dt = datetime.datetime.fromtimestamp(
                header_leader[0], datetime.timezone.utc)
            header_bytes = f.read(header_leader[1])

            if len(header_bytes) == 0:
                message = "Empty header in {}!".format(filename)
                logger.error(message)
                QtWidgets.QMessageBox.critical(parent, "Error", message)
                return None  # error

            # read the first packet's datetime
            first_packet_timestamp = struct.unpack(">d", f.read(8))[0]
            first_packet_dt = datetime.datetime.fromtimestamp(
                first_packet_timestamp, datetime.timezone.utc)

            header = decode_header(header_bytes, parent=parent)

            return ([(filename, first_packet_dt)], header)

    except:
        message = "Could not read header on {}!".format(filename)
        logger.exception(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return None  # error


def load_batch(parent=None):
    """
    returns (file_infos, header) where file_infos is a sequence of tuples
    containing (filename, dt).
    * header is the dictionary loaded from the file's JSON data, with
      appropriate conversions applied to Asphodel struct data.
    * filename is the absolute path to the file location.
    * dt is the UTC datetime of the first packet in the file.
    """

    first_file = True

    loaded_files = []

    file_infos = []

    while True:
        files = get_packdata_files(parent)
        if files is None or len(files) == 0:
            # user cancelled
            if first_file:
                return None
            else:
                files = []

        for filename in files:
            if filename in loaded_files:
                message = "File {} already loaded! Skipping.".format(filename)
                logger.info(message)
                QtWidgets.QMessageBox.information(parent, "Already Loaded",
                                                  message)
                continue

            try:
                with lzma.LZMAFile(filename, "rb") as f:
                    # read the header
                    header_leader = struct.unpack(">dI", f.read(12))
                    header_dt = datetime.datetime.fromtimestamp(
                        header_leader[0], datetime.timezone.utc)
                    header_bytes = f.read(header_leader[1])

                    if len(header_bytes) == 0:
                        message = "Empty header in {}!".format(filename)
                        logger.error(message)
                        QtWidgets.QMessageBox.critical(
                            parent, "Error", message)
                        return None  # error

                    # read the first packet's datetime
                    first_packet_timestamp = struct.unpack(">d", f.read(8))[0]
                    first_packet_dt = datetime.datetime.fromtimestamp(
                        first_packet_timestamp, datetime.timezone.utc)

                    if first_file:
                        first_file = False
                        first_header_bytes = header_bytes
                        first_header_dt = header_dt

                        header = decode_header(header_bytes, parent=parent)
                        if not header:
                            return  # error message already displayed
                    else:
                        if (first_header_bytes != header_bytes or
                                first_header_dt != header_dt):
                            # error
                            s = ("Headers do not match on {}!\n"
                                 "\n"
                                 "Files must come from the same session.")
                            message = s.format(filename)
                            logger.error(message)
                            QtWidgets.QMessageBox.critical(parent, "Error",
                                                           message)
                            return None  # error

                    file_infos.append((filename, first_packet_dt))
                    loaded_files.append(filename)

            except:
                message = "Could not read header on {}!".format(filename)
                logger.exception(message)
                QtWidgets.QMessageBox.critical(parent, "Error", message)
                return None  # error

        # ask the user if they want to load more files
        ret = QtWidgets.QMessageBox.question(
            parent, "More Files?", "Load more files for this batch?",
            buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
            default=QtWidgets.QMessageBox.No)

        if ret != QtWidgets.QMessageBox.Yes:
            break

    return (file_infos, header)


def choose_channel(header, parent=None):
    """
    returns a channel index selected by the user.
    """
    channel_indexes = set()
    for stream_id in header['streams_to_activate']:
        stream = header['streams'][stream_id]
        for index in stream.channel_index_list[0:stream.channel_count]:
            channel_indexes.add(index)

    channel_names = []
    name_dict = {}
    for channel_index in sorted(channel_indexes):
        channel = header['channels'][channel_index]
        channel_name = channel.name[0:channel.name_length].decode("UTF-8")
        channel_names.append(channel_name)
        name_dict[channel_name] = channel_index

    value, ok = QtWidgets.QInputDialog.getItem(parent, "Select Channel",
                                               "Select Channel", channel_names,
                                               0, editable=False)
    if not ok:
        return  # user cancelled

    return name_dict[value]


def choose_synchronous_channels(header, parent=None):
    """
    returns a sequence of channel indexes selected by the user, from a single
    stream.
    """

    dialog = SelectSynchronousDialog(header['streams'], header['channels'],
                                     parent=parent)
    ret = dialog.exec_()
    if ret == 0:
        return  # user cancelled

    channel_list = dialog.get_channel_list()

    if len(channel_list) == 0:
        return None  # user didn't select any channels; treat like a cancel
    else:
        return channel_list


class ChannelData:
    def __init__(self, stream, channel, channel_decoder):
        self.stream = stream
        self.channel = channel
        self.channel_decoder = channel_decoder

        self.samples = self.channel.samples
        self.subchannels = self.channel_decoder.subchannels

        if self.samples == 0 or self.subchannels == 0 or stream.rate == 0:
            raise ValueError("Invalid channel configuration")

        self.last_counter = -1

        self.lost_packet_list = []
        self.lost_packet_file_boundary_list = []

        self.file_boundary = False
        self.next_timestamp = None

        self.allocated = 1000
        self.length = 0
        self.data = numpy.empty((self.allocated * self.samples,
                                 self.subchannels), dtype=numpy.double)
        self.indexes = numpy.empty((self.allocated,), dtype=numpy.uint64)
        self.timestamps = numpy.empty((self.allocated,), dtype=numpy.double)

    def set_file_boundary(self):
        self.file_boundary = True

    def set_next_timestamp(self, timestamp):
        self.next_timestamp = timestamp

    def trim(self):
        self.allocated = self.length
        self.data = self.data[0:self.length * self.samples]
        self.indexes = self.indexes[0:self.length]
        self.timestamps = self.timestamps[0:self.length]

    def decode_callback(self, counter, data, samples, subchannels):
        if self.samples != samples:
            raise ValueError("Bad sample count in callback!")

        if self.subchannels != subchannels:
            raise ValueError("Bad subchannel count in callback!")

        if self.last_counter + 1 != counter and self.length != 0:
            # NOTE: first data point being non-zero doesn't count as a loss
            lost_tuple = (self.last_counter, counter, self.length)
            self.lost_packet_list.append(lost_tuple)
            if self.file_boundary:
                self.lost_packet_file_boundary_list.append(lost_tuple)

        self.last_counter = counter

        if self.length == self.allocated:
            # increase the size of the arrays

            self.allocated = self.allocated * 2

            new_data = numpy.empty((self.allocated * self.samples,
                                    self.subchannels), dtype=numpy.double)
            new_data[0:self.length * self.samples] = self.data
            self.data = new_data

            new_indexes = numpy.empty((self.allocated,), dtype=numpy.uint64)
            new_indexes[0:self.length] = self.indexes
            self.indexes = new_indexes

            new_timestamps = numpy.empty((self.allocated,), dtype=numpy.double)
            new_timestamps[0:self.length] = self.timestamps
            self.timestamps = new_timestamps

        d = numpy.array(data).reshape(samples, subchannels)

        self.indexes[self.length] = counter
        self.timestamps[self.length] = self.next_timestamp
        self.data[self.length * samples:(self.length + 1) * samples] = d

        self.length += 1

        if self.file_boundary:
            self.file_boundary = False


def decode_batch(file_infos, header, channel_indexes, parent=None):
    """
    returns a map with keys of channel indexes, values of ChannelData
    """
    info_list = []
    remaining_channels = set(channel_indexes)
    for stream_id in header['streams_to_activate']:
        stream = header['streams'][stream_id]
        indexes = stream.channel_index_list[0:stream.channel_count]
        use_stream = False

        for index in indexes:
            if index in remaining_channels:
                use_stream = True
                remaining_channels.discard(index)

        if use_stream:
            channel_list = [header['channels'][ch_id] for ch_id in indexes]
            info_list.append((stream_id, stream, channel_list))

    # create the device decoder
    decoder = asphodel.nativelib.create_device_decoder(
        info_list, header['stream_filler_bits'], header['stream_id_bits'])

    # create and register callbacks
    batch_info = {}
    remaining_channels = set(channel_indexes)
    try:
        for i, stream_decoder in enumerate(decoder.decoders):
            stream = header['streams'][decoder.stream_ids[i]]
            for j, channel_decoder in enumerate(stream_decoder.decoders):
                channel_id = stream_decoder.stream_info.channel_index_list[j]
                if channel_id in remaining_channels:
                    remaining_channels.discard(channel_id)
                else:
                    continue
                channel = header['channels'][channel_id]

                channel_data = ChannelData(stream, channel, channel_decoder)
                batch_info[channel_id] = channel_data
                channel_decoder.set_callback(channel_data.decode_callback)
    except:
        message = "Could not create device decoder!"
        logger.exception(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return None  # error

    # sort by first packet datetime, so earlier files get decoded first
    sorted_file_infos = sorted(file_infos, key=operator.itemgetter(1))

    opened_files = []  # list of (filename, rawfile, rawlen, lzmafile)
    total_length = 0

    # open input files and find their lengths
    for filename, _first_packet_dt in sorted_file_infos:
        try:
            # open the compressed file, and figure out how many bytes it has
            rawfile = open(filename, 'rb')
            rawfile.seek(0, os.SEEK_END)
            rawlen = rawfile.tell()
            total_length += rawlen
            rawfile.seek(0, os.SEEK_SET)

            # open the LZMA wrapper object
            lzmafile = lzma.LZMAFile(rawfile, "rb")

            # skip over the header (since it's already been processed)
            header_leader = struct.unpack(">dI", lzmafile.read(12))
            _header_bytes = lzmafile.read(header_leader[1])

            opened_files.append((filename, rawfile, rawlen, lzmafile))
        except:
            message = "Could not open file {}!".format(filename)
            logger.exception(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return None  # error

    packet_leader = struct.Struct(">dI")
    stream_packet_length = header['stream_packet_length']

    # create a progress dialog box
    window_flags = (QtCore.Qt.MSWindowsFixedSizeDialogHint)
    progress = QtWidgets.QProgressDialog("Loading Data...", "Abort", 0,
                                         total_length, parent, window_flags)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.forceShow()

    # make sure it gets at least one value different than total_length
    progress.setValue(0)

    process_countdown = 0
    total_position = 0

    # start processing the files
    for filename, rawfile, rawlen, lzmafile in opened_files:
        # notify channel data about a file boundary
        for channel_data in batch_info.values():
            channel_data.set_file_boundary()

        try:
            while True:
                leader_bytes = lzmafile.read(packet_leader.size)

                if not leader_bytes:
                    break  # file is finished

                leader = packet_leader.unpack(leader_bytes)
                packet_timestamp = leader[0]
                packet_bytes = lzmafile.read(leader[1])

                for channel_data in batch_info.values():
                    channel_data.set_next_timestamp(packet_timestamp)

                for i in range(len(packet_bytes) // stream_packet_length):
                    start = i * stream_packet_length
                    packet = packet_bytes[start:start + stream_packet_length]
                    decoder.decode(packet)

                file_position = rawfile.tell()
                progress.setValue(total_position + file_position)

                # update the window periodically
                if process_countdown == 0:
                    process_countdown = 100
                    QtCore.QCoreApplication.processEvents()
                else:
                    process_countdown -= 1

                # abort if required
                if progress.wasCanceled():
                    return  # user cancelled
        except:
            progress.cancel()
            m = "Error while processing data in file {}!".format(filename)
            logger.exception(m)

            # ask the user if they want to ignore the error
            ret = QtWidgets.QMessageBox.critical(
                parent, "Error", m, buttons=(QtWidgets.QMessageBox.Abort |
                                             QtWidgets.QMessageBox.Ignore),
                default=QtWidgets.QMessageBox.Abort)
            if ret != QtWidgets.QMessageBox.Ignore:
                return  # user aborted
            else:
                break

        total_position += rawlen
        logger.debug("Finished reading {}.".format(filename))

    for channel_data in batch_info.values():
        channel_data.trim()

    return batch_info


def get_datetime_subset(batch_info, parent=None):
    """
    filters data by datetime, provided by the user.
    """
    for _channel_index, channel_data in sorted(batch_info.items()):
        channel_name = channel_data.channel_decoder.channel_name

        d = numpy.diff(channel_data.timestamps)
        if numpy.min(d) < 0.0:
            # timestamps aren't monotonic!
            s = "Timestamps are not monotonic on channel {}! Continue?"
            message = s.format(channel_name)
            logger.warning(message)
            ret = QtWidgets.QMessageBox.warning(
                parent, "Warning", message,
                buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                default=QtWidgets.QMessageBox.Yes)

            if ret == QtWidgets.QMessageBox.No:
                return None  # user aborted

    starts = [d.timestamps[0] for d in batch_info.values()]
    ends = [d.timestamps[-1] for d in batch_info.values()]

    # NOTE: floor and ceil allow seconds to be rounded neatly
    start = datetime.datetime.fromtimestamp(numpy.floor(min(starts)),
                                            datetime.timezone.utc)
    end = datetime.datetime.fromtimestamp(numpy.ceil(max(ends)),
                                          datetime.timezone.utc)

    start_qdt = QtCore.QDateTime(start)
    end_qdt = QtCore.QDateTime(end)

    dialog = DateTimeSubsetDialog(start_qdt, end_qdt, parent=parent)

    while True:  # allow opening the dialog multiple times
        ret = dialog.exec_()
        if ret == 0:
            return  # user cancelled

        if dialog.should_use_all():
            return batch_info
        else:
            start_qdt, end_qdt = dialog.get_subset()
            utc = datetime.timezone.utc
            start = start_qdt.toPython().replace(tzinfo=utc).timestamp()
            end = end_qdt.toPython().replace(tzinfo=utc).timestamp()

            new_indexes = {}
            some_empty = False

            for channel_index, channel_data in batch_info.items():
                start_index = bisect.bisect_left(channel_data.timestamps,
                                                 start)
                end_index = bisect.bisect_right(channel_data.timestamps, end)

                if start_index >= end_index:
                    some_empty = True

                new_indexes[channel_index] = (start_index, end_index)

            if some_empty:
                message = ("No data is present within this interval on one or "
                           "more channels.")
                logger.warning(message)
                QtWidgets.QMessageBox.warning(parent, "Warning", message)
                continue  # bring the dialog back up

            for channel_index, channel_data in batch_info.items():
                # trim the data
                start_index, end_index = new_indexes[channel_index]
                if start_index >= end_index:
                    # remove possibility of negative lengths
                    start_index = 0
                    end_index = 0

                data_start = start_index * channel_data.samples
                data_end = end_index * channel_data.samples
                channel_data.data = channel_data.data[data_start:data_end]
                channel_data.indexes = channel_data.indexes[start_index:
                                                            end_index]
                channel_data.timestamps = channel_data.timestamps[start_index:
                                                                  end_index]

                def trim_list(lost_packet_list, start_index, end_index):
                    new_lost_packet_list = []
                    for last, current, index in lost_packet_list:
                        # NOTE: bounds are not inclusive, since we can't have
                        # lost data before the start or after the end.
                        if index > start_index and index < end_index:
                            new_lost_packet_list.append((last, current,
                                                         index - start_index))
                    return new_lost_packet_list

                channel_data.lost_packet_list = trim_list(
                    channel_data.lost_packet_list, start_index, end_index)
                channel_data.lost_packet_file_boundary_list = trim_list(
                    channel_data.lost_packet_file_boundary_list, start_index,
                    end_index)

                channel_data.length = end_index - start_index
                channel_data.allocated = channel_data.length

            return batch_info


def warn_about_lost_packets(batch_info, once=False, parent=None):
    """
    Warns the user about problems with the decoded data, such as lost packets
    or gaps between files. Returns True to continue, False if the user aborts.
    """
    for _channel_index, channel_data in sorted(batch_info.items()):
        channel_name = channel_data.channel_decoder.channel_name

        if len(channel_data.timestamps) < 2:
            continue  # not enough data to have lost anything

        lost_packets = 0
        lost_sections = 0
        for last, current, _i in channel_data.lost_packet_list:
            packets_lost = current - last - 1
            lost_packets += packets_lost
            lost_sections += 1

        lost_packets_file_boundaries = 0
        lost_sections_file_boundaries = 0
        for last, current, _i in channel_data.lost_packet_file_boundary_list:
            packets_lost = current - last - 1
            lost_packets_file_boundaries += packets_lost
            lost_sections_file_boundaries += 1

        if lost_packets != 0:
            m1 = "{}: Lost {} packet{} in {} place{}".format(
                channel_name,
                lost_packets, "s" if lost_packets != 1 else "",
                lost_sections, "s" if lost_sections != 1 else "")
            if lost_packets_file_boundaries != 0:
                m2 = "Lost {} packet{} in {} place{} between files".format(
                    lost_packets_file_boundaries,
                    "s" if lost_packets_file_boundaries != 1 else "",
                    lost_sections_file_boundaries,
                    "s" if lost_sections_file_boundaries != 1 else "")
                message = "\n".join([m1, m2, "Continue?"])
            else:
                message = "\n".join([m1, "Continue?"])
            logger.info(message)
            ret = QtWidgets.QMessageBox.warning(
                parent, "Warning", message,
                buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                default=QtWidgets.QMessageBox.Yes)

            if ret == QtWidgets.QMessageBox.No:
                return False  # user aborted

            if once:
                return True

    return True


def sequence_data(batch_info, chunk=False, raw_units=False, parent=None):
    """
    returns a tuple, first element is a map keyed by channel index with a
    value of a list of tuples with (time, data, start_time, end_time) where
    time and data are numpy arrays of the same length. The second tuple element
    is a map keyed by channel index with a value of of map of unit strings in
    various formats, supporting keys of at least 'ascii', 'html', 'utf8'

    If chunk is False then a single NaNs will be inserted at any location where
    packets have been lost. This means that the tuple list will be length 1.

    If chunk is True, then each tuple will be broken up along lost packet
    boundaries.

    The first entry in the first time array will start at zero, regardless of
    its actual index value.

    The start_time value will be the UTC timestamp of the first decoded packet
    in the chunk. Likewise, end_time will be the UTC timestamp of the last
    decoded packet in the chunk
    """
    sequence_info = {}
    unit_info = {}
    for channel_index, channel_data in sorted(batch_info.items()):
        # create a time array with length of the original data array
        indexes = channel_data.indexes - channel_data.indexes[0]
        repeated_indexes = numpy.repeat(indexes.astype(numpy.double),
                                        channel_data.samples)
        fractional_section = (numpy.array(range(channel_data.samples),
                                          dtype=numpy.double) /
                              channel_data.samples)
        fractional_indexes = numpy.tile(fractional_section,
                                        channel_data.length)
        orig_time = ((repeated_indexes + fractional_indexes) /
                     channel_data.stream.rate)

        orig_data = channel_data.data

        # get the unit info now
        if raw_units:
            unit_formatter = asphodel.nativelib.create_unit_formatter(
                channel_data.channel.unit_type, 0.0, 0.0,
                channel_data.channel.resolution, use_metric=True)
        else:
            settings = QtCore.QSettings()
            unit_formatter = hyperborea.unit_preferences.create_unit_formatter(
                settings, channel_data.channel.unit_type,
                numpy.nanmin(orig_data), numpy.nanmax(orig_data),
                channel_data.channel.resolution)

        # save the units
        unit_info[channel_index] = {'ascii': unit_formatter.unit_ascii,
                                    'html': unit_formatter.unit_html,
                                    'utf8': unit_formatter.unit_utf8}

        # apply the scaling and offset
        orig_data = (orig_data * unit_formatter.conversion_scale +
                     unit_formatter.conversion_offset)

        if chunk:
            chunk_list = []

            last_data_index = 0
            last_timestamp_index = 0
            for i, (_x, _y, index) in enumerate(channel_data.lost_packet_list):
                data_index = index * channel_data.samples
                new_data = orig_data[last_data_index:data_index]
                new_time = orig_time[last_data_index:data_index]

                start = channel_data.timestamps[last_timestamp_index]
                end = channel_data.timestamps[index - 1]

                last_data_index = data_index
                last_timestamp_index = index

                chunk_list.append((new_time, new_data, start, end))

            # create a chunk for the last section
            new_data = orig_data[last_data_index:]
            new_time = orig_time[last_data_index:]

            start = channel_data.timestamps[last_timestamp_index]
            end = channel_data.timestamps[-1]

            chunk_list.append((new_time, new_data, start, end))

            sequence_info[channel_index] = chunk_list
        else:
            # create a new data array with space for the NaNs
            nan_count = len(channel_data.lost_packet_list)
            new_shape = (orig_data.shape[0] + nan_count, orig_data.shape[1])
            new_data = numpy.empty(new_shape)

            nan_slice = numpy.full((), numpy.nan, dtype=numpy.double)

            # create the new time array with spaces for NaNs
            new_time = numpy.empty((new_shape[0],))

            last = 0
            for i, (_x, _y, index) in enumerate(channel_data.lost_packet_list):
                index *= channel_data.samples
                new_data[last + i:index + i] = orig_data[last:index]
                new_data[index + i] = nan_slice
                new_time[last + i:index + i] = orig_time[last:index]
                new_time[index + i] = (orig_time[index - 1] +
                                       1 / (channel_data.stream.rate *
                                            channel_data.samples))
                last = index

            # copy in the last section
            new_data[last + nan_count:] = orig_data[last:]
            new_time[last + nan_count:] = orig_time[last:]

            # pull out start_time and end_time
            start_time = channel_data.timestamps[0]
            end_time = channel_data.timestamps[-1]

            sequence_info[channel_index] = [(new_time, new_data, start_time,
                                             end_time)]

    return sequence_info, unit_info


def choose_subchannel(channel_data, allow_all=False, parent=None):
    """
    returns a subchannel index selected by the user.

    If allow_all is set, it will present the user with a default "All
    Subchannels" option, which will return a value of -1 when selected.
    """

    options = list(channel_data.channel_decoder.subchannel_names)

    if len(options) == 1:
        return 0

    if allow_all:
        options.insert(0, "All Subchannels")

    value, ok = QtWidgets.QInputDialog.getItem(parent, "Select Subchannel",
                                               "Select Subchannel", options, 0,
                                               editable=False)
    if not ok:
        return  # user cancelled

    try:
        return channel_data.channel_decoder.subchannel_names.index(value)
    except ValueError:
        # must have been the "all subchannels" option
        return -1


def choose_subchannels(header, parent=None):
    """
    returns a sequence of tuples of the form (channel_index, subchannel_index)
    selected by the user.
    """

    info_list = []
    channel_indexes = set()
    for stream_id in header['streams_to_activate']:
        stream = header['streams'][stream_id]
        indexes = stream.channel_index_list[0:stream.channel_count]
        for index in indexes:
            channel_indexes.add(index)

        channel_list = [header['channels'][ch_id] for ch_id in indexes]
        info_list.append((stream_id, stream, channel_list))

    # create the device decoder
    decoder = asphodel.nativelib.create_device_decoder(
        info_list, header['stream_filler_bits'], header['stream_id_bits'])

    remaining_channels = set(channel_indexes)
    names = []  # list of (channel_id, channel_name, subchannel_names)
    try:
        for stream_decoder in decoder.decoders:
            for j, channel_decoder in enumerate(stream_decoder.decoders):
                channel_id = stream_decoder.stream_info.channel_index_list[j]
                if channel_id in remaining_channels:
                    remaining_channels.discard(channel_id)
                else:
                    continue

                names.append((channel_id, channel_decoder.channel_name,
                              channel_decoder.subchannel_names))
    except:
        message = "Could not create device decoder!"
        logger.exception(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return None  # error

    dialog = SelectSubchannelsDialog(names, parent=parent)
    ret = dialog.exec_()
    if ret == 0:
        return  # user cancelled

    subchannels_list = dialog.get_subchannels_list()

    if len(subchannels_list) == 0:
        return None  # user didn't select any channels; treat like a cancel
    else:
        return subchannels_list


def get_contiguous_chunk(sequence, parent=None):
    if len(sequence) == 1:
        return sequence[0]  # nothing to do

    str_list = []
    str_indexes = {}

    max_points = 0
    max_index = 0

    for i, (time, _data, start_time, _end_time) in enumerate(sequence):
        points = len(time)

        if max_points < points:
            max_points = points
            max_index = i

        duration = time[-1] - time[0]  # close enough
        start_dt = datetime.datetime.fromtimestamp(start_time,
                                                   datetime.timezone.utc)
        start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S (UTC)")
        s = "{} points ({} s), starting {}".format(points, duration, start_str)
        if s not in str_list:
            # NOTE: this prevents selection of duplicate chunks small enough
            # to have the same start time, but in reality, this isn't a
            # realistic use case
            str_list.append(s)
            str_indexes[s] = i

    value, ok = QtWidgets.QInputDialog.getItem(
        parent, "Select Contiguous Section", "Select Section", str_list,
        max_index, editable=False)
    if not ok:
        return  # user cancelled

    return sequence[str_indexes[value]]


def get_psd_options(chunks_list, sampling_rate, parent=None):
    dialog = PSDOptionsDialog(chunks_list, sampling_rate)

    ret = dialog.exec_()
    if ret == 0:
        return  # user cancelled

    return dialog.get_options()


def get_multiple_psd_options(sections, parent=None):
    dialog = MultiplePSDOptionsDialog(sections)

    ret = dialog.exec_()
    if ret == 0:
        return  # user cancelled

    return dialog.get_options()
