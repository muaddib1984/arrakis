#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Space Folder39
# Author: muaddib
# Description: remote ingest and decimation for low bw link
# GNU Radio version: 3.9.4.0

from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from xmlrpc.server import SimpleXMLRPCServer
import threading
import numpy as np




class space_folder39(gr.top_block):

    def __init__(self, control_ip='127.0.0.1', control_port=8001, samp_rate=20e6, zmq_in_ip='127.0.0.1', zmq_in_port=5000, zmq_out_ip="127.0.0.1", zmq_out_port='5001'):
        gr.top_block.__init__(self, "Space Folder39", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.control_ip = control_ip
        self.control_port = control_port
        self.samp_rate = samp_rate
        self.zmq_in_ip = zmq_in_ip
        self.zmq_in_port = zmq_in_port
        self.zmq_out_ip = zmq_out_ip
        self.zmq_out_port = zmq_out_port

        ##################################################
        # Variables
        ##################################################
        self.samp_ratio = samp_ratio = samp_rate/1E6
        self.vec_per_sec = vec_per_sec = 4
        self.fft_length = fft_length = 256 * int(pow(2, np.ceil(np.log(samp_ratio)/np.log(2))))

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, "tcp://"+str(zmq_in_ip)+":"+str(zmq_in_port), 100, True, -1, '')
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_float, fft_length, "tcp://"+str(zmq_out_ip)+":"+str(zmq_out_port), 100, True, -1, '')
        self.xmlrpc_serv_ip = SimpleXMLRPCServer(('127.0.0.1', control_port), allow_none=True)
        self.xmlrpc_serv_ip.register_instance(self)
        self.xmlrpc_serv_ip_thread = threading.Thread(target=self.xmlrpc_serv_ip.serve_forever)
        self.xmlrpc_serv_ip_thread.daemon = True
        self.xmlrpc_serv_ip_thread.start()
        self.fft_vxx_0 = fft.fft_vcc(fft_length, True, window.blackmanharris(fft_length), True, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_length)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, fft_length, 10*np.log10(1.0/fft_length))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*fft_length, int(round(samp_rate/fft_length/vec_per_sec)))
        self.blocks_integrate_xx_0 = blocks.integrate_ff(1, fft_length)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_length)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_stream_to_vector_0, 0))


    def get_control_ip(self):
        return self.control_ip

    def set_control_ip(self, control_ip):
        self.control_ip = control_ip

    def get_control_port(self):
        return self.control_port

    def set_control_port(self, control_port):
        self.control_port = control_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_ratio(self.samp_rate/1E6)
        self.blocks_keep_one_in_n_0.set_n(int(round(self.samp_rate/self.fft_length/self.vec_per_sec)))

    def get_zmq_in_ip(self):
        return self.zmq_in_ip

    def set_zmq_in_ip(self, zmq_in_ip):
        self.zmq_in_ip = zmq_in_ip

    def get_zmq_in_port(self):
        return self.zmq_in_port

    def set_zmq_in_port(self, zmq_in_port):
        self.zmq_in_port = zmq_in_port

    def get_zmq_out_ip(self):
        return self.zmq_out_ip

    def set_zmq_out_ip(self, zmq_out_ip):
        self.zmq_out_ip = zmq_out_ip

    def get_zmq_out_port(self):
        return self.zmq_out_port

    def set_zmq_out_port(self, zmq_out_port):
        self.zmq_out_port = zmq_out_port

    def get_samp_ratio(self):
        return self.samp_ratio

    def set_samp_ratio(self, samp_ratio):
        self.samp_ratio = samp_ratio
        self.set_fft_length(256 * int(pow(2, np.ceil(np.log(self.samp_ratio)/np.log(2)))))

    def get_vec_per_sec(self):
        return self.vec_per_sec

    def set_vec_per_sec(self, vec_per_sec):
        self.vec_per_sec = vec_per_sec
        self.blocks_keep_one_in_n_0.set_n(int(round(self.samp_rate/self.fft_length/self.vec_per_sec)))

    def get_fft_length(self):
        return self.fft_length

    def set_fft_length(self, fft_length):
        self.fft_length = fft_length
        self.blocks_keep_one_in_n_0.set_n(int(round(self.samp_rate/self.fft_length/self.vec_per_sec)))



def argument_parser():
    description = 'remote ingest and decimation for low bw link'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-x", "--control-ip", dest="control_ip", type=str, default='127.0.0.1',
        help="Set XMLRPC SERVER IP [default=%(default)r]")
    parser.add_argument(
        "-X", "--control-port", dest="control_port", type=intx, default=8001,
        help="Set XMLRPC SERVER PORT [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(20e6)),
        help="Set SAMPLE RATE [default=%(default)r]")
    parser.add_argument(
        "-z", "--zmq-in-ip", dest="zmq_in_ip", type=str, default='127.0.0.1',
        help="Set ZMQ IN IP ADDR [default=%(default)r]")
    parser.add_argument(
        "-o", "--zmq-out-ip", dest="zmq_out_ip", type=str, default="127.0.0.1",
        help="Set ZMQ OUT IP ADDR [default=%(default)r]")
    parser.add_argument(
        "-O", "--zmq-out-port", dest="zmq_out_port", type=str, default='5001',
        help="Set ZMQ OUT IP PORT [default=%(default)r]")
    return parser


def main(top_block_cls=space_folder39, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(control_ip=options.control_ip, control_port=options.control_port, samp_rate=options.samp_rate, zmq_in_ip=options.zmq_in_ip, zmq_out_ip=options.zmq_out_ip, zmq_out_port=options.zmq_out_port)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
