# Copyright (c) 2018 Electric Power Research Institute, Inc.
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

import builtins
import gc
import logging
import os.path

import numpy
from PySide2 import QtCore, QtGui, QtWidgets
import matplotlib

from . import mondo_rc  # needed for the icon

logger = logging.getLogger(__name__)


ignored_types = [i for i in builtins.__dict__.values() if isinstance(i, type)]
ignored_types.remove(list)
ignored_types.append(type(None))


def is_ignored_type(value):
    if isinstance(value, QtCore.QObject):
        return True
    for t in ignored_types:
        if type(value) == t:
            return True
    return False


class CommandList(list):
    def __init__(self, setup_commands=None):
        self.plotdata = {}
        self.index = 0

        if not setup_commands:
            self.append("import matplotlib")
            self.append("import numpy")
            self.append("import PySide2")
            self.append("")
        else:
            self.extend(setup_commands)
            self.append("")
            self.append("plotdata = numpy.load(__file__ + '.npz')")

    def get_string(self, value):
        if isinstance(value, numpy.ndarray):
            i = 'array_{}'.format(self.index)
            self.index += 1

            self.plotdata[i] = value
            return "plotdata['{}']".format(i)
        else:
            return repr(value)

    def output(self, scriptfile):
        datafile = scriptfile + ".npz"

        logger.debug("Writing script to {}".format(scriptfile))

        with open(scriptfile, "wt", encoding="utf_8") as f:
            for v in self:
                # hack to change fig.show() to plt.show()
                s = str(v)
                if s == "fig.show()":
                    s = "plt.show()"
                f.write(s)
                f.write("\n")

        logger.debug("Writing script data to {}".format(datafile))

        numpy.savez_compressed(datafile, allow_pickle=False, **self.plotdata)

        logger.debug("Finished script output")


class AttributeCommand:
    def __init__(self, cmd_list, base, attr):
        self.cmd_list = cmd_list
        self.base = base
        self.attr = attr

    def __repr__(self):
        return "{}.{}".format(self.base, self.attr)


class CallCommand:
    def __init__(self, cmd_list, base, func, *args, **kwargs):
        self.cmd_list = cmd_list
        self.base = base
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        a = []
        a.extend(self.cmd_list.get_string(x) for x in self.args)
        for k, v in self.kwargs.items():
            a.append(k + "=" + self.cmd_list.get_string(v))
        param_str = ", ".join(a)
        return "{}.{}({})".format(self.base, self.func, param_str)


class GetItemCommand:
    def __init__(self, cmd_list, base, key):
        self.cmd_list = cmd_list
        self.base = base
        self.key = key

    def __repr__(self):
        return "{}[{}]".format(self.base, self.cmd_list.get_string(self.key))


class SetItemCommand:
    def __init__(self, cmd_list, base, key, value):
        self.cmd_list = cmd_list
        self.base = base
        self.key = key
        self.value = value

    def __repr__(self):
        return "{}[{}] = {}".format(self.base,
                                    self.cmd_list.get_string(self.key),
                                    self.cmd_list.get_string(self.value))


class Wrapper:
    def __init__(self, wrapped, name, cmd_list):
        self._wrapped = wrapped
        self._name = name
        self._cmd_list = cmd_list

    def __getattribute__(self, attr):
        wrapped = object.__getattribute__(self, '_wrapped')
        name = object.__getattribute__(self, '_name')
        cmd_list = object.__getattribute__(self, '_cmd_list')
        orig_attr = wrapped.__getattribute__(attr)

        if callable(orig_attr):
            def wrapped_func(*args, **kwargs):
                cmd = CallCommand(cmd_list, name, attr, *args, **kwargs)
                result = orig_attr(*args, **kwargs)
                if is_ignored_type(result):
                    cmd_list.append(cmd)
                    return result
                else:
                    if len(args) + len(kwargs) > 0:
                        cmd_list.append(cmd)
                    return Wrapper(result, cmd, cmd_list)
            return wrapped_func
        else:
            if is_ignored_type(orig_attr):
                return orig_attr
            else:
                new_name = AttributeCommand(cmd_list, name, attr)
                return Wrapper(orig_attr, new_name, cmd_list)

    def __getitem__(self, key):
        wrapped = object.__getattribute__(self, '_wrapped')
        name = object.__getattribute__(self, '_name')
        cmd_list = object.__getattribute__(self, '_cmd_list')
        new_name = GetItemCommand(cmd_list, name, key)
        value = wrapped.__getitem__(key)
        if is_ignored_type(value):
            return value
        else:
            return Wrapper(value, new_name, cmd_list)

    def __setitem__(self, key, value):
        wrapped = object.__getattribute__(self, '_wrapped')
        name = object.__getattribute__(self, '_name')
        cmd_list = object.__getattribute__(self, '_cmd_list')
        cmd_list.append(SetItemCommand(cmd_list, name, key, value))
        return wrapped.__setitem__(key, value)

    def __len__(self):
        wrapped = object.__getattribute__(self, '_wrapped')
        return wrapped.__len__()

    def __iter__(self):
        wrapped = object.__getattribute__(self, '_wrapped')
        return wrapped.__iter__()


def get_script_file(default_name, parent=None):
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
    file_filter = "Python Script (*.py);;All Files (*.*)"
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


def add_export_script_action(figure, cmd_list):
    toolbar = figure.canvas.toolbar
    actionText = QtWidgets.QApplication.translate("ExportScript",
                                                  "Export Script")
    action = QtWidgets.QAction(actionText, toolbar)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/icon/icons/export-script.png"))
    action.setIcon(icon)

    def handle_export():
        base_file = get_script_file("export", parent=toolbar)
        if not base_file:
            return

        cmd_list.output(base_file)

    action.triggered.connect(handle_export)

    toolbar.addAction(action)


def subplots_wrapper(*args, **kwargs):
    cmd_list = CommandList(setup_commands)

    cmd_list.append('')

    cmd_list.append('import matplotlib.pyplot as plt')
    import matplotlib.pyplot as plt

    cmd_list.append('')

    fig, ax = plt.subplots(*args, **kwargs)

    def handle_close(evt):
        fig.clf()
        cmd_list.clear()
        gc.collect()

    fig.canvas.mpl_connect("close_event", handle_close)

    # set the icon (inside the application only; not in the script)
    icon = QtGui.QIcon()
    icon_reader = QtGui.QImageReader(":/mondo.ico")
    while True:
        pixmap = QtGui.QPixmap.fromImage(icon_reader.read())
        icon.addPixmap(pixmap)
        if not icon_reader.jumpToNextImage():
            break
    fig.canvas.manager.window.setWindowIcon(icon)

    fig_wrapper = Wrapper(fig, "fig", cmd_list)
    add_export_script_action(fig, cmd_list)

    if isinstance(ax, numpy.ndarray):
        ax_array = ax
        cmd_list.append(CallCommand(
            cmd_list, "fig, ax_array = plt", "subplots", *args, **kwargs))
        ax_wrapper = numpy.empty(ax.shape, dtype=object)
        for i, ax in numpy.ndenumerate(ax_array):
            ax_name = "ax_array[{}]".format(i)
            ax_wrapper[i] = Wrapper(ax, ax_name, cmd_list)
    else:
        cmd_list.append(CallCommand(
            cmd_list, "fig, ax = plt", "subplots", *args, **kwargs))
        ax_wrapper = Wrapper(ax, "ax", cmd_list)

    return fig_wrapper, ax_wrapper


setup_commands = CommandList()
matplotlib_wrapper = Wrapper(matplotlib, 'matplotlib', setup_commands)
