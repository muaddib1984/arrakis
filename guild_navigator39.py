#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Guild Navigator39
# Author: muaddib
# Description: remote visualizatino for space folder application
# GNU Radio version: 3.9.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
import sip
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
import threading
import numpy as np



from gnuradio import qtgui

class guild_navigator39(gr.top_block, Qt.QWidget):

    def __init__(self, control_ip='127.0.0.1', control_port=8002, rf_bw=10e6, rf_freq=750e6, rf_gain=50.0, samp_rate=10e6, zmq_in_ip='127.0.0.1', zmq_in_port=5001):
        gr.top_block.__init__(self, "Guild Navigator39", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Guild Navigator39")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "guild_navigator39")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.control_ip = control_ip
        self.control_port = control_port
        self.rf_bw = rf_bw
        self.rf_freq = rf_freq
        self.rf_gain = rf_gain
        self.samp_rate = samp_rate
        self.zmq_in_ip = zmq_in_ip
        self.zmq_in_port = zmq_in_port

        ##################################################
        # Variables
        ##################################################
        self.samp_ratio = samp_ratio = samp_rate/1E6
        self.vps = vps = 1
        self.vec_per_sec = vec_per_sec = 4
        self.samp_rate_gui = samp_rate_gui = samp_rate
        self.rf_gain_gui = rf_gain_gui = 50
        self.rf_freq_gui = rf_freq_gui = 750e6
        self.rf_bw_gui = rf_bw_gui = rf_bw
        self.fft_length = fft_length = 256 * int(pow(2, np.ceil(np.log(samp_ratio)/np.log(2))))
        self.avg = avg = 0

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_float, fft_length, "tcp://"+str(zmq_in_ip)+":"+str(zmq_in_port), 100, True, -1, '')
        self.xmlrpc_serv_ip = SimpleXMLRPCServer(('127.0.0.1', control_port), allow_none=True)
        self.xmlrpc_serv_ip.register_instance(self)
        self.xmlrpc_serv_ip_thread = threading.Thread(target=self.xmlrpc_serv_ip.serve_forever)
        self.xmlrpc_serv_ip_thread.daemon = True
        self.xmlrpc_serv_ip_thread.start()
        self.xmlrpc_client_0_0_0_0_0_0_0 = ServerProxy('http://'+'127.0.0.1'+':8001')
        self.xmlrpc_client_0_0_0_0_0_0 = ServerProxy('http://'+'127.0.0.1'+':8001')
        self.xmlrpc_client_0_0_0_0_0 = ServerProxy('http://'+'127.0.0.1'+':8001')
        self.xmlrpc_client_0_0_0_0 = ServerProxy('http://'+'127.0.0.1'+':8000')
        self.xmlrpc_client_0_0_0 = ServerProxy('http://'+'127.0.0.1'+':8000')
        self.xmlrpc_client_0_0 = ServerProxy('http://'+'127.0.0.1'+':8000')
        self.xmlrpc_client_0 = ServerProxy('http://'+'127.0.0.1'+':8000')
        # Create the options list
        self._vps_options = [1, 2, 4, 8, 16]
        # Create the labels list
        self._vps_labels = ['1', '2', '4', '8', '16']
        # Create the combo box
        self._vps_tool_bar = Qt.QToolBar(self)
        self._vps_tool_bar.addWidget(Qt.QLabel("VECTORS PER SECOND" + ": "))
        self._vps_combo_box = Qt.QComboBox()
        self._vps_tool_bar.addWidget(self._vps_combo_box)
        for _label in self._vps_labels: self._vps_combo_box.addItem(_label)
        self._vps_callback = lambda i: Qt.QMetaObject.invokeMethod(self._vps_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._vps_options.index(i)))
        self._vps_callback(self.vps)
        self._vps_combo_box.currentIndexChanged.connect(
            lambda i: self.set_vps(self._vps_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._vps_tool_bar, 1, 4, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._samp_rate_gui_options = [1000000.0, 5000000.0, 10000000.0, 20000000.0, 40000000.0]
        # Create the labels list
        self._samp_rate_gui_labels = ['1Msps', '5Msps', '5Msps', '20Msps', '40Msps']
        # Create the combo box
        self._samp_rate_gui_tool_bar = Qt.QToolBar(self)
        self._samp_rate_gui_tool_bar.addWidget(Qt.QLabel("SAMPLE RATE" + ": "))
        self._samp_rate_gui_combo_box = Qt.QComboBox()
        self._samp_rate_gui_tool_bar.addWidget(self._samp_rate_gui_combo_box)
        for _label in self._samp_rate_gui_labels: self._samp_rate_gui_combo_box.addItem(_label)
        self._samp_rate_gui_callback = lambda i: Qt.QMetaObject.invokeMethod(self._samp_rate_gui_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._samp_rate_gui_options.index(i)))
        self._samp_rate_gui_callback(self.samp_rate_gui)
        self._samp_rate_gui_combo_box.currentIndexChanged.connect(
            lambda i: self.set_samp_rate_gui(self._samp_rate_gui_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._samp_rate_gui_tool_bar, 1, 2, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rf_gain_gui_range = Range(0, 80, 1, 50, 200)
        self._rf_gain_gui_win = RangeWidget(self._rf_gain_gui_range, self.set_rf_gain_gui, "RF GAIN", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rf_gain_gui_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rf_freq_gui_range = Range(64e6, 6e9, 100e3, 750e6, 200)
        self._rf_freq_gui_win = RangeWidget(self._rf_freq_gui_range, self.set_rf_freq_gui, "RF FREQ", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rf_freq_gui_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._rf_bw_gui_options = [1000000.0, 1920000.0, 5000000.0, 10000000.0, 20000000.0]
        # Create the labels list
        self._rf_bw_gui_labels = ['1Msps', '1.92Msps', '5Msps', '10Msps', '20Msps']
        # Create the combo box
        self._rf_bw_gui_tool_bar = Qt.QToolBar(self)
        self._rf_bw_gui_tool_bar.addWidget(Qt.QLabel("RF BANDWIDTH" + ": "))
        self._rf_bw_gui_combo_box = Qt.QComboBox()
        self._rf_bw_gui_tool_bar.addWidget(self._rf_bw_gui_combo_box)
        for _label in self._rf_bw_gui_labels: self._rf_bw_gui_combo_box.addItem(_label)
        self._rf_bw_gui_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rf_bw_gui_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._rf_bw_gui_options.index(i)))
        self._rf_bw_gui_callback(self.rf_bw_gui)
        self._rf_bw_gui_combo_box.currentIndexChanged.connect(
            lambda i: self.set_rf_bw_gui(self._rf_bw_gui_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._rf_bw_gui_tool_bar, 0, 2, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            fft_length,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(-140, 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(100)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["cyan", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win, 2, 0, 5, 6)
        for r in range(2, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._avg_options = [0, 1]
        # Create the labels list
        self._avg_labels = ['AVERAGE', 'RAW']
        # Create the combo box
        self._avg_tool_bar = Qt.QToolBar(self)
        self._avg_tool_bar.addWidget(Qt.QLabel("AVERAGE/RAW" + ": "))
        self._avg_combo_box = Qt.QComboBox()
        self._avg_tool_bar.addWidget(self._avg_combo_box)
        for _label in self._avg_labels: self._avg_combo_box.addItem(_label)
        self._avg_callback = lambda i: Qt.QMetaObject.invokeMethod(self._avg_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._avg_options.index(i)))
        self._avg_callback(self.avg)
        self._avg_combo_box.currentIndexChanged.connect(
            lambda i: self.set_avg(self._avg_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._avg_tool_bar, 0, 4, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_vector_sink_f_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "guild_navigator39")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_control_ip(self):
        return self.control_ip

    def set_control_ip(self, control_ip):
        self.control_ip = control_ip

    def get_control_port(self):
        return self.control_port

    def set_control_port(self, control_port):
        self.control_port = control_port

    def get_rf_bw(self):
        return self.rf_bw

    def set_rf_bw(self, rf_bw):
        self.rf_bw = rf_bw
        self.set_rf_bw_gui(self.rf_bw)

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_gui(self.samp_rate)
        self.set_samp_ratio(self.samp_rate/1E6)

    def get_zmq_in_ip(self):
        return self.zmq_in_ip

    def set_zmq_in_ip(self, zmq_in_ip):
        self.zmq_in_ip = zmq_in_ip

    def get_zmq_in_port(self):
        return self.zmq_in_port

    def set_zmq_in_port(self, zmq_in_port):
        self.zmq_in_port = zmq_in_port

    def get_samp_ratio(self):
        return self.samp_ratio

    def set_samp_ratio(self, samp_ratio):
        self.samp_ratio = samp_ratio
        self.set_fft_length(256 * int(pow(2, np.ceil(np.log(self.samp_ratio)/np.log(2)))))

    def get_vps(self):
        return self.vps

    def set_vps(self, vps):
        self.vps = vps
        self._vps_callback(self.vps)
        self.xmlrpc_client_0_0_0_0_0_0.set_vec_per_sec(self.vps)

    def get_vec_per_sec(self):
        return self.vec_per_sec

    def set_vec_per_sec(self, vec_per_sec):
        self.vec_per_sec = vec_per_sec

    def get_samp_rate_gui(self):
        return self.samp_rate_gui

    def set_samp_rate_gui(self, samp_rate_gui):
        self.samp_rate_gui = samp_rate_gui
        self._samp_rate_gui_callback(self.samp_rate_gui)
        self.xmlrpc_client_0_0_0_0.set_samp_rate(self.samp_rate_gui)
        self.xmlrpc_client_0_0_0_0_0.set_samp_rate(self.samp_rate_gui)

    def get_rf_gain_gui(self):
        return self.rf_gain_gui

    def set_rf_gain_gui(self, rf_gain_gui):
        self.rf_gain_gui = rf_gain_gui
        self.xmlrpc_client_0.set_rf_gain(self.rf_gain_gui)

    def get_rf_freq_gui(self):
        return self.rf_freq_gui

    def set_rf_freq_gui(self, rf_freq_gui):
        self.rf_freq_gui = rf_freq_gui
        self.xmlrpc_client_0_0.set_rf_freq(self.rf_freq_gui)

    def get_rf_bw_gui(self):
        return self.rf_bw_gui

    def set_rf_bw_gui(self, rf_bw_gui):
        self.rf_bw_gui = rf_bw_gui
        self._rf_bw_gui_callback(self.rf_bw_gui)
        self.xmlrpc_client_0_0_0.set_rf_bw(self.rf_bw_gui)

    def get_fft_length(self):
        return self.fft_length

    def set_fft_length(self, fft_length):
        self.fft_length = fft_length

    def get_avg(self):
        return self.avg

    def set_avg(self, avg):
        self.avg = avg
        self._avg_callback(self.avg)
        self.xmlrpc_client_0_0_0_0_0_0_0.set_avg(self.avg)



def argument_parser():
    description = 'remote visualizatino for space folder application'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-x", "--control-ip", dest="control_ip", type=str, default='127.0.0.1',
        help="Set XMLRPC SERVER IP [default=%(default)r]")
    parser.add_argument(
        "-X", "--control-port", dest="control_port", type=intx, default=8002,
        help="Set XMLRPC SERVER PORT [default=%(default)r]")
    parser.add_argument(
        "-b", "--rf-bw", dest="rf_bw", type=eng_float, default=eng_notation.num_to_str(float(10e6)),
        help="Set RF BANDWITDH [default=%(default)r]")
    parser.add_argument(
        "-f", "--rf-freq", dest="rf_freq", type=eng_float, default=eng_notation.num_to_str(float(750e6)),
        help="Set RF FREQUENCY [default=%(default)r]")
    parser.add_argument(
        "-g", "--rf-gain", dest="rf_gain", type=eng_float, default=eng_notation.num_to_str(float(50.0)),
        help="Set RF GAIN [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(10e6)),
        help="Set SAMPLE RATE [default=%(default)r]")
    parser.add_argument(
        "-z", "--zmq-in-ip", dest="zmq_in_ip", type=str, default='127.0.0.1',
        help="Set ZMQ IN IP ADDR [default=%(default)r]")
    return parser


def main(top_block_cls=guild_navigator39, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(control_ip=options.control_ip, control_port=options.control_port, rf_bw=options.rf_bw, rf_freq=options.rf_freq, rf_gain=options.rf_gain, samp_rate=options.samp_rate, zmq_in_ip=options.zmq_in_ip)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
