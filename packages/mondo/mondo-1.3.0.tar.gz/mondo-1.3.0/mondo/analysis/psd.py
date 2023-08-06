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
import math

import numpy
from PySide2 import QtWidgets
import matplotlib.mlab as mlab

from . import util
from .. import export_csv
from .. import export_script

logger = logging.getLogger(__name__)


def do_psd(sequence, subchannel_index, NFFT, Fs, detrend, window, noverlap):
    # JSN NOTE: much of this function was taken from matplotlib.mlab's
    # internal _spectral_helper(). It has been streamlined by removing
    # unneeded features, and changed to support chunks of data

    freqs = numpy.fft.rfftfreq(NFFT, 1 / Fs)

    windows = 0
    sums = numpy.zeros(freqs.shape)

    for _time, data, _start, _end in sequence:
        x = numpy.asarray(data[:, subchannel_index])

        if len(x) < NFFT:
            continue

        result = mlab.stride_windows(x, NFFT, noverlap, axis=0)
        result = mlab.detrend(result, detrend, axis=0)
        result, windowVals = mlab.apply_window(result, window, axis=0,
                                               return_window=True)
        result = numpy.fft.rfft(result, n=NFFT, axis=0)

        result = (numpy.conjugate(result) * result).real

        # Scale the spectrum by the norm of the window to compensate for
        # windowing loss; see Bendat & Piersol Sec 11.5.2.
        result /= (numpy.abs(windowVals) ** 2).sum()

        windows += result.shape[1]
        result = result.sum(axis=1)
        sums += result

        del result

    sums[1:] *= 2.0  # because it's one sided

    sums /= Fs  # get the spectral density

    sums /= windows

    return sums, freqs


def psd_analysis(parent=None):
    ret = util.load_batch(parent=parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    file_infos, header = ret

    channel_index = util.choose_channel(header, parent=parent)
    if channel_index is None:
        return  # error message displayed, or user cancelled

    batch_info = util.decode_batch(file_infos, header, [channel_index],
                                   parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    subchannel_index = util.choose_subchannel(batch_info[channel_index],
                                              allow_all=False)
    if subchannel_index is None:
        return  # user cancelled

    batch_info = util.get_datetime_subset(batch_info, parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    ret = util.warn_about_lost_packets(batch_info, parent=parent)
    if not ret:
        return  # user cancelled

    sequence_info, _unit_info = util.sequence_data(
        batch_info, chunk=True, raw_units=True, parent=parent)

    sequence = sequence_info[channel_index]

    sampling_rate = None
    for time, _data, _start, _end in sequence:
        if len(time) > 2:
            sampling_rate = 1.0 / (time[1] - time[0])
            break

    if sampling_rate is None:
        message = "Could not determine sampling rate!"
        logger.error(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return

    psd_options = util.get_psd_options([sequence], sampling_rate,
                                       parent=parent)
    if psd_options is None:
        return  # user cancelled

    pxx, freqs = do_psd(sequence, subchannel_index, **psd_options)
    pxx_dB = 10 * numpy.log10(pxx)

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax = export_script.subplots_wrapper()

    ax.plot(freqs, pxx_dB)
    ax.grid(True)

    vmin, vmax = ax.viewLim.intervaly
    logi = int(numpy.log10(vmax - vmin))
    if logi == 0:
        logi = 0.1
    step = 10 * logi
    ticks = numpy.arange(math.floor(vmin), math.ceil(vmax) + 1, step)
    ax.set_yticks(ticks)

    labels = ("Frequency (Hz)", "Power Spectral Density (dB)")

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    export_csv.add_export_csv_action(fig, labels, [(freqs, pxx_dB, None)])

    fig.show()


def single_channel_psd_analysis(parent=None):
    channel_index = None  # ask for the channel on the first iteration
    subchannel_index = None  # ask for the subchannel on the first iteration

    sampling_rate = None
    sequences = []
    names = []
    files = set()

    while True:
        # load a batch of files
        ret = util.load_batch(parent=parent)
        if ret is None:
            return  # error message displayed, or user cancelled
        file_infos, header = ret

        # warn the user if any files have been loaded before
        for filename, _dt in file_infos:
            if filename in files:
                message = ("File {} already loaded in another batch!\n"
                           "Proceed with caution!").format(filename)
                logger.warning(message)
                QtWidgets.QMessageBox.warning(parent, "Warning", message)
            files.add(filename)

        # if it's the first time through, choose a channel
        if channel_index is None:
            channel_index = util.choose_channel(header, parent=parent)
            if channel_index is None:
                return  # error message displayed, or user cancelled

        # make sure this batch has a channel of the correct index
        if channel_index >= len(header['channels']):
            message = "Channels inconsistent between batches!"
            logger.error(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return

        batch_info = util.decode_batch(file_infos, header, [channel_index],
                                       parent=parent)
        if batch_info is None:
            return  # error message displayed, or user cancelled

        if subchannel_index is None:
            subchannel_index = util.choose_subchannel(
                batch_info[channel_index], allow_all=False)
            if subchannel_index is None:
                return  # user cancelled

        subchannels = batch_info[channel_index].channel_decoder.subchannels
        if subchannel_index >= subchannels:
            message = "Channels inconsistent between batches!"
            logger.error(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return

        batch_info = util.get_datetime_subset(batch_info, parent=parent)
        if batch_info is None:
            return  # error message displayed, or user cancelled

        ret = util.warn_about_lost_packets(batch_info, parent=parent)
        if not ret:
            return  # user cancelled

        sequence_info, _unit_info = util.sequence_data(
            batch_info, chunk=True, raw_units=True, parent=parent)

        sequence = sequence_info[channel_index]

        sequences.append(sequence)

        batch_sampling_rate = None
        for time, _data, _start, _end in sequence:
            if len(time) > 2:
                batch_sampling_rate = 1.0 / (time[1] - time[0])
                break

        if batch_sampling_rate is None:
            message = "Could not determine sampling rate!"
            logger.error(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return

        if sampling_rate is None:
            sampling_rate = batch_sampling_rate
        elif sampling_rate != batch_sampling_rate:
            message = "Sampling rates inconsistent between batches!"
            logger.error(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return

        # ask the user for a name for this set
        msg = "Display name for this batch (#{}):".format(len(sequences))
        name, ok = QtWidgets.QInputDialog.getText(parent, "Batch Name", msg)
        if not ok:
            return  # user cancelled

        names.append(name.strip())

        # ask the user if they want to load more
        msg = "Load more batches? Loaded {} so far".format(len(sequences))
        ret = QtWidgets.QMessageBox.question(
            parent, "More Batches?", msg,
            buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
            default=QtWidgets.QMessageBox.No)
        if ret != QtWidgets.QMessageBox.Yes:
            break

    psd_options = util.get_psd_options(sequences, sampling_rate, parent=parent)
    if psd_options is None:
        return  # user cancelled

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax = export_script.subplots_wrapper()

    export_data = []

    for i, sequence in enumerate(sequences):
        pxx, freqs = do_psd(sequence, subchannel_index, **psd_options)
        pxx_dB = 10 * numpy.log10(pxx)
        ax.plot(freqs, pxx_dB, label=names[i])
        export_data.append((freqs, pxx_dB, names[i]))

    ax.legend()

    ax.grid(True)

    vmin, vmax = ax.viewLim.intervaly
    logi = int(numpy.log10(vmax - vmin))
    if logi == 0:
        logi = 0.1
    step = 10 * logi
    ticks = numpy.arange(math.floor(vmin), math.ceil(vmax) + 1, step)
    ax.set_yticks(ticks)

    labels = ("Frequency (Hz)", "Power Spectral Density (dB)")

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    export_csv.add_export_csv_action(fig, labels, export_data)

    fig.show()


def single_slice_psd_analysis(parent=None):
    ret = util.load_batch(parent=parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    file_infos, header = ret

    subchannels_list = util.choose_subchannels(header, parent=parent)
    if subchannels_list is None:
        return  # error message displayed, or user cancelled

    channel_indexes = {t[0] for t in subchannels_list}

    batch_info = util.decode_batch(file_infos, header, channel_indexes,
                                   parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    batch_info = util.get_datetime_subset(batch_info, parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    ret = util.warn_about_lost_packets(batch_info, parent=parent)
    if not ret:
        return  # user cancelled

    sequence_info, _unit_info = util.sequence_data(
        batch_info, chunk=True, raw_units=True, parent=parent)

    sampling_rates = {}  # key: channel, value: sampling rate
    for channel_index in channel_indexes:
        sampling_rate = None
        for time, _data, _start, _end in sequence_info[channel_index]:
            if len(time) > 2:
                sampling_rate = 1.0 / (time[1] - time[0])
                break

        if sampling_rate is None:
            message = "Could not determine sampling rate!"
            logger.error(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return

        sampling_rates[channel_index] = sampling_rate

    # create a list of similar channels, which can share psd options
    channel_signatures = {}
    for channel_index in channel_indexes:
        sequence = sequence_info[channel_index]
        sequence_signature = tuple(len(x[0]) for x in sequence)
        channel_signatures[channel_index] = (sampling_rates[channel_index],
                                             sequence_signature)

    remaining_channels = set(channel_indexes)
    sections = []
    channel_groups = []
    for channel_index in sorted(channel_indexes):
        if channel_index in remaining_channels:
            remaining_channels.discard(channel_index)
        else:
            continue

        sig = channel_signatures[channel_index]
        similar_channels = [channel_index]
        for other_channel_index in sorted(remaining_channels):
            if sig == channel_signatures[other_channel_index]:
                similar_channels.append(other_channel_index)
                remaining_channels.discard(other_channel_index)

        group_name = ", ".join((batch_info[i].channel_decoder.channel_name
                                for i in similar_channels))

        # the sequence and rate of all the similar channels are the same
        sequence = sequence_info[similar_channels[0]]
        sampling_rate = sampling_rates[similar_channels[0]]

        sections.append((group_name, [sequence], sampling_rate))
        channel_groups.append(similar_channels)

    all_psd_options = util.get_multiple_psd_options(sections, parent=parent)
    if all_psd_options is None:
        return  # user cancelled

    # unpack psd options, per channel
    channel_psd_options = {}
    for i, psd_options in enumerate(all_psd_options):
        for channel_index in channel_groups[i]:
            channel_psd_options[channel_index] = psd_options

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax = export_script.subplots_wrapper()

    export_data = []

    for channel_index, subchannel_index in subchannels_list:
        channel_decoder = batch_info[channel_index].channel_decoder
        if len(channel_decoder.subchannel_names) > 1:
            name = channel_decoder.subchannel_names[subchannel_index]
        else:
            name = channel_decoder.channel_name

        sequence = sequence_info[channel_index]
        psd_options = channel_psd_options[channel_index]
        pxx, freqs = do_psd(sequence, subchannel_index, **psd_options)
        pxx_dB = 10 * numpy.log10(pxx)
        ax.plot(freqs, pxx_dB, label=name)
        export_data.append((freqs, pxx_dB, name))

    ax.legend()

    ax.grid(True)

    vmin, vmax = ax.viewLim.intervaly
    logi = int(numpy.log10(vmax - vmin))
    if logi == 0:
        logi = 0.1
    step = 10 * logi
    ticks = numpy.arange(math.floor(vmin), math.ceil(vmax) + 1, step)
    ax.set_yticks(ticks)

    labels = ("Frequency (Hz)", "Power Spectral Density (dB)")

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    export_csv.add_export_csv_action(fig, labels, export_data)

    fig.show()


def overlaid_psd_analysis(parent=None):
    sequences = []
    names = []
    sampling_rates = []

    while True:
        # load a batch of files
        ret = util.load_batch(parent=parent)
        if ret is None:
            return  # error message displayed, or user cancelled
        file_infos, header = ret

        # if it's the first time through, choose a channel
        channel_index = util.choose_channel(header, parent=parent)
        if channel_index is None:
            return  # error message displayed, or user cancelled

        batch_info = util.decode_batch(file_infos, header, [channel_index],
                                       parent=parent)
        if batch_info is None:
            return  # error message displayed, or user cancelled

        subchannel_index = util.choose_subchannel(
            batch_info[channel_index], allow_all=False)
        if subchannel_index is None:
            return  # user cancelled

        batch_info = util.get_datetime_subset(batch_info, parent=parent)
        if batch_info is None:
            return  # error message displayed, or user cancelled

        ret = util.warn_about_lost_packets(batch_info, parent=parent)
        if not ret:
            return  # user cancelled

        sequence_info, _unit_info = util.sequence_data(
            batch_info, chunk=True, raw_units=True, parent=parent)

        sequence = sequence_info[channel_index]

        sequences.append(sequence)

        sampling_rate = None
        for time, _data, _start, _end in sequence:
            if len(time) > 2:
                sampling_rate = 1.0 / (time[1] - time[0])
                break

        if sampling_rate is None:
            message = "Could not determine sampling rate!"
            logger.error(message)
            QtWidgets.QMessageBox.critical(parent, "Error", message)
            return

        sampling_rates.append(sampling_rate)

        # ask the user for a name for this set
        msg = "Display name for this batch (#{}):".format(len(sequences))
        name, ok = QtWidgets.QInputDialog.getText(parent, "Batch Name", msg)
        if not ok:
            return  # user cancelled

        names.append(name.strip())

        # ask the user if they want to load more
        msg = "Load more batches? Loaded {} so far".format(len(sequences))
        ret = QtWidgets.QMessageBox.question(
            parent, "More Batches?", msg,
            buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
            default=QtWidgets.QMessageBox.No)
        if ret != QtWidgets.QMessageBox.Yes:
            break

    sections = []
    for i, sequence in enumerate(sequences):
        sections.append((names[i], [sequence], sampling_rates[i]))

    all_psd_options = util.get_multiple_psd_options(sections, parent=parent)
    if all_psd_options is None:
        return  # user cancelled

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax = export_script.subplots_wrapper()

    export_data = []

    for i, sequence in enumerate(sequences):
        psd_options = all_psd_options[i]
        pxx, freqs = do_psd(sequence, subchannel_index, **psd_options)
        pxx_dB = 10 * numpy.log10(pxx)
        ax.plot(freqs, pxx_dB, label=names[i])
        export_data.append((freqs, pxx_dB, names[i]))

    ax.legend()

    ax.grid(True)

    vmin, vmax = ax.viewLim.intervaly
    logi = int(numpy.log10(vmax - vmin))
    if logi == 0:
        logi = 0.1
    step = 10 * logi
    ticks = numpy.arange(math.floor(vmin), math.ceil(vmax) + 1, step)
    ax.set_yticks(ticks)

    labels = ("Frequency (Hz)", "Power Spectral Density (dB)")

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    export_csv.add_export_csv_action(fig, labels, export_data)

    fig.show()
