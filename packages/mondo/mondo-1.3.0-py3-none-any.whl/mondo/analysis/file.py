import datetime
import json
import logging
import lzma
import os
import struct

import matplotlib.pyplot
import numpy
from PySide2 import QtCore, QtWidgets

import asphodel

from . import util
from ..info_dialog import InfoDialog
from ..setting_viewer import SettingViewerDialog

logger = logging.getLogger(__name__)


def get_save_file(default_name, parent=None):
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


def file_information(parent=None):
    ret = util.load_single_file(parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    _file_infos, header = ret

    dialog = InfoDialog(header)
    dialog.exec_()


def view_settings(parent=None):
    ret = util.load_single_file(parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    _file_infos, header = ret

    dialog = SettingViewerDialog(
        header['settings'], header['nvm'], header['custom_enums'],
        header['setting_categories'], parent=parent)
    ret = dialog.exec_()


def raw_export(parent=None):
    filename = util.get_packdata_file(parent)
    if filename is None:
        return  # user cancelled

    try:
        # open the compressed file, and figure out how many bytes it has
        rawfile = open(filename, 'rb')
        rawfile.seek(0, os.SEEK_END)
        rawlen = rawfile.tell()
        rawfile.seek(0, os.SEEK_SET)

        # open the LZMA wrapper object
        lzmafile = lzma.LZMAFile(rawfile, "rb")

        # read the header
        header_leader = struct.unpack(">dI", lzmafile.read(12))
        header_bytes = lzmafile.read(header_leader[1])

        if len(header_bytes) == 0:
            message = "Empty header in {}!".format(filename)
            logger.error(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return  # error

        try:
            header_str = header_bytes.decode("UTF-8")
            header = json.loads(header_str)
        except:
            message = "Could not parse file header!"
            logger.exception(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return
    except:
        message = "Could not open file {}!".format(filename)
        logger.exception(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return  # error

    # ask the user for the json file name
    default_json_filename = os.path.splitext(filename)[0] + ".json"
    caption = "Save JSON File"
    json_file_filter = "JSON Files (*.json);;All Files (*.*)"
    val = QtWidgets.QFileDialog.getSaveFileName(
        parent, caption, default_json_filename, json_file_filter)
    json_filename = val[0]

    if json_filename:
        with open(json_filename, 'wt') as f:
            json.dump(header, f, sort_keys=True, indent=4)

    # ask the user for the packet file name
    default_packet_filename = os.path.splitext(filename)[0] + ".packet"
    caption = "Save Packet File"
    packet_file_filter = "Packet Files (*.packet);;All Files (*.*)"
    val = QtWidgets.QFileDialog.getSaveFileName(
        parent, caption, default_packet_filename, packet_file_filter)
    packet_filename = val[0]

    if not packet_filename:
        # user didn't want to save a packet file, just exit now
        return

    packet_file = open(packet_filename, 'wt')

    packet_leader = struct.Struct(">dI")
    stream_packet_length = header['stream_packet_length']

    # create a progress dialog box
    window_flags = (QtCore.Qt.MSWindowsFixedSizeDialogHint)
    progress = QtWidgets.QProgressDialog("Loading Data...", "Abort", 0,
                                         rawlen, parent, window_flags)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.forceShow()

    # make sure it gets at least one value different than rawlen
    progress.setValue(0)

    process_countdown = 0

    try:
        while True:
            leader_bytes = lzmafile.read(packet_leader.size)

            if not leader_bytes:
                break  # file is finished

            leader = packet_leader.unpack(leader_bytes)
            packet_timestamp = leader[0]
            packet_bytes = lzmafile.read(leader[1])

            packet_dt = datetime.datetime.fromtimestamp(packet_timestamp,
                                                        datetime.timezone.utc)
            packet_time_string = "{} ".format(
                packet_dt.strftime('%Y-%m-%dT%H:%M:%S.%f'))

            for i in range(len(packet_bytes) // stream_packet_length):
                start = i * stream_packet_length
                packet = packet_bytes[start:start + stream_packet_length]
                packet_string = ", ".join(map("0x{:02x}".format, packet))

                packet_file.write(packet_time_string)
                packet_file.write('[' + packet_string + ']\n')

            progress.setValue(rawfile.tell())

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
        QtWidgets.QMessageBox.critical(parent, "Error", m)
        return

    logger.debug("Finished reading {}.".format(filename))


def split_file(parent=None):
    sequences = []
    unit_types = []
    unit_names = []

    # load the file
    ret = util.load_single_file(parent=parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    file_infos, header = ret

    subchannels_list = util.choose_subchannels(header, parent=parent)
    if subchannels_list is None:
        return  # error message displayed, or user cancelled

    # get all valid channel indexes
    channel_indexes = sorted({t[0] for t in subchannels_list})

    batch_info = util.decode_batch(file_infos, header, channel_indexes,
                                   parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    sequence_info, unit_info = util.sequence_data(batch_info, chunk=False,
                                                  parent=parent)

    for channel_index in channel_indexes:
        sequences.append(sequence_info[channel_index][0])
        unit_types.append(header['channels'][channel_index].unit_type)
        unit_names.append(unit_info[channel_index]['utf8'])

    # find the earliest start time
    min_start = min(s[2] for s in sequences)

    # group channels by unit type
    plot_groups = []
    groups_by_unit_type = {}
    for batch_index, unit_type in enumerate(unit_types):
        if unit_type == 0:
            # don't share plots between channels with unknown units
            plot_groups.append([batch_index])
        elif unit_type in groups_by_unit_type:
            # already have a group made
            plot_group = groups_by_unit_type[unit_type]
            plot_group.append(batch_index)
        else:
            # need a new group
            plot_group = [batch_index]
            plot_groups.append(plot_group)
            groups_by_unit_type[unit_type] = plot_group

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax_list = matplotlib.pyplot.subplots(len(plot_groups), squeeze=False,
                                              sharex=True)

    for i, ax in enumerate(ax_list[:, 0]):
        plot_group = plot_groups[i]

        legend_strs = []

        for batch_index in plot_group:
            time, data, start, _end = sequences[batch_index]

            delta = start - min_start

            ax.plot(time + delta, data)

            channel_index = channel_indexes[batch_index]
            channel_data = batch_info[channel_index]
            legend_strs.extend(channel_data.channel_decoder.subchannel_names)

        ax.legend()

        ax.set_xlabel("Time (s)")
        unit_str = unit_names[plot_group[0]]
        if unit_str:
            ax.set_ylabel("Magnitude ({})".format(unit_str))
        else:
            ax.set_ylabel("Magnitude")

        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)

        ax.legend(legend_strs)

    # have the user select points
    ax_list[0, 0].set_title("Select split points. Done = right click / enter\n"
                            "Undo = middle click / backspace")
    fig.show()
    points = fig.ginput(n=-1, timeout=0, mouse_add=1, mouse_stop=3,
                        mouse_pop=2)
    matplotlib.pyplot.close(fig)

    if len(points) == 0:
        return  # cancelled

    split_times = [p[0] for p in points]

    logger.debug("Selected split times: %s", split_times)

    split_timestamps = []

    for split_time in split_times:
        min_ts = None
        for channel_index, channel_data in sorted(batch_info.items()):
            delta = channel_data.timestamps[0] - min_start

            target_index = (split_time - delta) * channel_data.stream.rate
            i = numpy.searchsorted(channel_data.indexes, target_index)
            timestamps = channel_data.timestamps[i - 1:i + 1]
            if len(timestamps) == 2:
                ts = min(timestamps)
                if min_ts is None or ts < min_ts:
                    min_ts = ts
        split_timestamps.append(min_ts)

    bad_element_count = sum(ts is None for ts in split_timestamps)
    if bad_element_count == len(split_timestamps):
        message = "No valid split points"
        logger.error(message)
        QtWidgets.QMessageBox.critical(parent, "Invalid Points", message)
        return
    elif bad_element_count > 0:
        message = "Selected {} invalid split point{}".format(
            bad_element_count, "s" if bad_element_count != 1 else "")
        logger.info(message)
        QtWidgets.QMessageBox.information(parent, "Invalid Points", message)

    split_timestamps = sorted(ts for ts in split_timestamps if ts is not None)
    logger.debug("Selected split timestamps: %s", split_timestamps)

    output_file_count = len(split_timestamps) + 1

    # do the actual splitting
    filename = file_infos[0][0]
    root, ext = os.path.splitext(filename)
    if ext == ".apd" or ext == ".apdbak":
        base_filename = root
    else:
        base_filename = filename

    try:
        # open the compressed file, and figure out how many bytes it has
        rawfile = open(filename, 'rb')
        rawfile.seek(0, os.SEEK_END)
        rawlen = rawfile.tell()
        rawfile.seek(0, os.SEEK_SET)

        # open the LZMA wrapper object
        lzmafile = lzma.LZMAFile(rawfile, "rb")

        # read the header
        header_leader = struct.unpack(">dI", lzmafile.read(12))
        header_bytes = lzmafile.read(header_leader[1])
    except:
        message = "Could not open file {}!".format(filename)
        logger.exception(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return  # error

    packet_leader = struct.Struct(">dI")

    # create a progress dialog box
    window_flags = (QtCore.Qt.MSWindowsFixedSizeDialogHint)
    progress = QtWidgets.QProgressDialog("Processing Data...", "Abort", 0,
                                         rawlen, parent, window_flags)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.forceShow()

    # make sure it gets at least one value different than rawlen
    progress.setValue(0)

    process_countdown = 0

    next_dest_index = 1
    dest_file = None

    try:
        while True:
            leader_bytes = lzmafile.read(packet_leader.size)

            if not leader_bytes:
                break  # file is finished

            leader = packet_leader.unpack(leader_bytes)
            packet_timestamp = leader[0]
            packet_bytes = lzmafile.read(leader[1])

            if split_timestamps and packet_timestamp > split_timestamps[0]:
                if dest_file is not None:
                    dest_file.close()
                dest_file = None
                del split_timestamps[0]

            if dest_file is None:
                # open a new file
                if dest_file is not None:
                    dest_file.close()
                dest_filename = "{}_{}.apd".format(base_filename,
                                                   next_dest_index)
                next_dest_index += 1
                dest_file = lzma.open(dest_filename, 'wb')

                dest_file.write(struct.pack(">dI", *header_leader))
                dest_file.write(header_bytes)

                logger.debug("opened file %s", dest_filename)

            # write the data into the file
            dest_file.write(leader_bytes)
            dest_file.write(packet_bytes)

            progress.setValue(rawfile.tell())

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
        QtWidgets.QMessageBox.critical(parent, "Error", m)
        return

    progress.reset()
    if dest_file is not None:
        dest_file.close()

    lzmafile.close()
    rawfile.close()

    logger.debug("Finished processing {}.".format(filename))

    os.rename(filename, base_filename + ".apdbak")

    m = "Split into {} files".format(output_file_count)
    QtWidgets.QMessageBox.information(parent, "Finished", m)
