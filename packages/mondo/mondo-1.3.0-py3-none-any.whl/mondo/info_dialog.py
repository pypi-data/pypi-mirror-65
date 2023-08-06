import logging

from PySide2 import QtGui, QtWidgets

import asphodel

from .ui_info_dialog import Ui_InfoDialog

logger = logging.getLogger(__name__)


class InfoDialog(QtWidgets.QDialog, Ui_InfoDialog):
    def __init__(self, device_info, parent=None):
        super().__init__(parent)

        self.device_info = device_info

        self.setupUi(self)

        self.font = QtGui.QFont("Monospace", 10)
        self.font.setStyleHint(QtGui.QFont.TypeWriter)
        self.plainTextEdit.setFont(self.font)

        s = self.create_device_info_string()
        self.plainTextEdit.setPlainText(s)

    def create_device_info_string(self):
        d = self.device_info
        s = ""

        s += "Serial Number: {}\n".format(d['serial_number'])
        s += "User Tag 1: {}\n".format(d['user_tag_1'])
        s += "User Tag 2: {}\n".format(d['user_tag_2'])
        try:
            s += "Location String: {}\n".format(d['location_string'])
        except KeyError:
            pass  # file is too old to contain location string
        s += "Max Outgoing Param Len: {}\n".format(
            d['max_outgoing_param_length'])
        s += "Max Incoming Param Len: {}\n".format(
            d['max_incoming_param_length'])
        s += "Stream Packet Length: {}\n".format(d['stream_packet_length'])
        s += "Protocol Version: {}\n".format(d['protocol_version'])
        s += "Board Info: {} rev {}\n".format(*d['board_info'])
        s += "Build Info: {}\n".format(d['build_info'])
        s += "Build Date: {}\n".format(d['build_date'])
        s += "Chip Family: {}\n".format(d['chip_family'])
        s += "Chip Model: {}\n".format(d['chip_model'])
        s += "Chip ID: {}\n".format(d['chip_id'])
        s += "Tag Locations: {}\n".format(
            ", ".join(map(lambda x: str(tuple(x)), d['tag_locations'])))
        s += "Bootloader Info: {}\n".format(d['bootloader_info'])
        s += "\n"
        s += "Library Protocol Version: {}\n".format(
            d['library_protocol_version'])
        s += "Library Build Info: {}\n".format(d['library_build_info'])
        s += "Library Build Date: {}\n".format(d['library_build_date'])
        s += "\n"
        s += "Stream Filler Bits: {}\n".format(d['stream_filler_bits'])
        s += "Stream ID Bits: {}\n".format(d['stream_id_bits'])
        s += "\n"
        s += "Streams\n"

        for i, stream in enumerate(d['streams']):
            s += "  Stream {}\n".format(i)
            channels = stream.channel_index_list[:stream.channel_count]
            s += "    channels: [{}]\n".format(", ".join(map(str, channels)))
            s += "    filler_bits={}, counter_bits={}\n".format(
                stream.filler_bits, stream.counter_bits)
            s += "    rate={:g}, rate_error={:g}%\n".format(
                stream.rate, stream.rate_error * 100.0)
            s += "    warm_up_delay={:g}\n".format(stream.warm_up_delay)
            try:
                rate_info = d['stream_rate_info'][i]
                if rate_info is None or not rate_info.available:
                    s += "    no rate channel\n"
                else:
                    s += "    rate_channel={}, rate_invert={}\n".format(
                        rate_info.channel_index, rate_info.invert)
                    s += "    rate_scale={}, rate_offset={}\n".format(
                        rate_info.scale, rate_info.offset)
            except IndexError:
                # doesn't have rate inforamiton for this stream
                pass

        s += "\n"
        s += "Channels\n"

        for i, channel in enumerate(d['channels']):
            s += "  Channel {}\n".format(i)
            s += "    name: {}\n".format(channel.name.decode("utf-8"))

            stream_ids = []
            for stream_id, stream in enumerate(d['streams']):
                channels = stream.channel_index_list[:stream.channel_count]
                if i in channels:
                    stream_ids.append(stream_id)
            if len(stream_ids) == 1:
                stream_id = stream_ids[0]
                s += "    stream: {}\n".format(stream_id)
                sampling_rate = d['streams'][stream_id].rate * channel.samples
                s += "    rate={:g}\n".format(sampling_rate)
            elif len(stream_ids) == 1:
                s += "    stream: None\n"
            else:
                s += "    streams: [{}]\n".format(", ".join(stream_ids))

            try:
                t_str = asphodel.channel_type_names[channel.channel_type]
                channel_type_str = "{} ({})" .format(channel.channel_type,
                                                     t_str)
            except IndexError:
                channel_type_str = str(channel.channel_type)
            s += "    channel_type={}\n".format(channel_type_str)

            try:
                t_str = asphodel.unit_type_names[channel.unit_type]
                unit_type_str = "{} ({})" .format(channel.unit_type, t_str)
            except IndexError:
                unit_type_str = str(channel.unit_type)
            s += "    unit_type={}\n".format(unit_type_str)

            s += "    filler_bits={}, data_bits={}\n".format(
                channel.filler_bits, channel.data_bits)
            s += "    samples={}, bits_per_sample={}\n".format(
                channel.samples, channel.bits_per_sample)
            s += "    minimum={:g}, maximum={:g}, resolution={:g}\n".format(
                channel.minimum, channel.maximum, channel.resolution)
            coefficients = channel.coefficients[:channel.coefficients_length]
            coefficients_str = ", ".join(map("{:g}".format, coefficients))
            s += "    coefficients: [{}]\n".format(coefficients_str)
            s += "    Chunk Count: {}\n".format(channel.chunk_count)
            for chunk_id in range(channel.chunk_count):
                chunk_len = channel.chunk_lengths[chunk_id]
                chunk = channel.chunks[chunk_id][:chunk_len]
                chunk_str = ",".join(map("{:02x}".format, chunk))
                s += "      Chunk {}: [{}]\n".format(chunk_id, chunk_str)

        s += "\n"
        s += "Supplies\n"

        for i, (name, supply) in enumerate(d['supplies']):
            s += "  Supply {}\n".format(i)
            s += "    name: {}\n".format(name)

            try:
                t_str = asphodel.unit_type_names[supply.unit_type]
                unit_type_str = "{} ({})" .format(supply.unit_type, t_str)
            except IndexError:
                unit_type_str = str(supply.unit_type)
            s += "    unit_type={}\n".format(unit_type_str)
            s += "    is_battery={}, nominal={}\n".format(supply.is_battery,
                                                          supply.nominal)
            s += "    scale={:g}, offset={:g}\n".format(supply.scale,
                                                        supply.offset)

        s += "\n"
        s += "Control Variables\n"

        for i, (name, ctrl_var, _setting) in enumerate(d['ctrl_vars']):
            s += "  Control Variable {}\n".format(i)
            s += "    name: {}\n".format(name)

            try:
                t_str = asphodel.unit_type_names[ctrl_var.unit_type]
                unit_type_str = "{} ({})" .format(ctrl_var.unit_type, t_str)
            except IndexError:
                unit_type_str = str(ctrl_var.unit_type)
            s += "    unit_type={}\n".format(unit_type_str)
            s += "    minimum={}, maximum={}\n".format(ctrl_var.minimum,
                                                       ctrl_var.maximum)
            s += "    scale={:g}, offset={:g}\n".format(ctrl_var.scale,
                                                        ctrl_var.offset)

        s += "\n"
        s += "NVM\n"

        s += "\n".join(asphodel.format_nvm_data(d['nvm']))

        return s
