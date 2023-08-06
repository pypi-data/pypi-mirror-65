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

from . import util
from .. import export_script

logger = logging.getLogger(__name__)


def spectrogram_analysis(parent=None):
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
        batch_info, chunk=False, raw_units=True, parent=parent)
    chunked_sequence_info, _unit_info = util.sequence_data(
        batch_info, chunk=True, raw_units=True, parent=parent)
    chunk_list = chunked_sequence_info[channel_index]
    logger.debug("%s", chunk_list)

    sequence = sequence_info[channel_index]

    time, data, _start, _end = sequence[0]

    if len(time) < 256:
        # not enough data to make a decent PSD
        message = "Not enough data points! Only {}!".format(len(time))
        logger.error(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return

    sampling_rate = 1.0 / (time[1] - time[0])

    psd_options = util.get_psd_options([chunk_list], sampling_rate,
                                       parent=parent)
    if psd_options is None:
        return  # user cancelled

    data = data[:, subchannel_index]

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax = export_script.subplots_wrapper()

    try:
        ax.specgram(data, **psd_options)
    except MemoryError:
        message = "Out of memory!"
        logger.exception(message)
        QtWidgets.QMessageBox.critical(parent, "Error", message)
        return

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")

    ax.autoscale(tight=True)

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    fig.show()
