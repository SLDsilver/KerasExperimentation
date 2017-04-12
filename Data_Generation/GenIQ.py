#!/usr/bin/env python2

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from math import log10
from optparse import OptionParser
import numpy
import sys
import os
from random import randint


class top_block(gr.top_block):

    def __init__(self,ind,modNum):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.file_index = file_index = ind
        self.symb_rate = symb_rate = 10e6
        self.samp_rate = samp_rate = 100e6
        self.samps_per_symb = samps_per_symb = int(samp_rate/symb_rate)
        self.SNR = SNR = randint(5,30)
        self.rrc_taps = rrc_taps = 101
        self.rrc_alpha = rrc_alpha = 0.35
        self.noise_volt = noise_volt = pow(samps_per_symb/pow(10.0,SNR/10.0),0.5)
        self.modulation_scheme = modulation_scheme = modNum
        os.system('echo "' + str(modulation_scheme) + '"' + ' >> modScheme' + str(file_index) +'.txt')
        os.system('echo "' + str(modulation_scheme) + ' ' + str(SNR) + '"' + ' >> datasetSpecifics.txt')
        self.VT = VT = 4,6,[ -1.5633e+00+ 5.5460e-01j, -1.3833e+00+ 5.5460e-01j,
        -1.0234e+00+ 5.5460e-01j, -1.2034e+00+ 5.5460e-01j,
        -7.3553e-01+ 5.0751e-02j, -8.0750e-01+ 1.7671e-01j,
        -9.5146e-01+ 4.2863e-01j, -8.7948e-01+ 3.0267e-01j,
        -3.3741e-02+ 5.5460e-01j, -2.1368e-01+ 5.5460e-01j,
        -4.4761e-01+ 4.2863e-01j, -3.9363e-01+ 5.5460e-01j,
        -6.6355e-01+ -7.5211e-02j, -6.0956e-01+ 5.0751e-02j,
        -5.0160e-01+ 3.0267e-01j, -5.5558e-01+ 1.7671e-01j,
        9.5596e-01+ 1.0473e-01j, 1.1359e+00+ 1.0473e-01j,
        1.4958e+00+ 1.0473e-01j, 1.3158e+00+ 1.0473e-01j,
        1.5858e+00+ 5.5460e-01j, 1.7657e+00+ 5.5460e-01j,
        1.5858e+00+ 2.5499e-01j, 1.6757e+00+ 4.0434e-01j,
        1.4621e-01+ 5.5460e-01j, 3.2615e-01+ 5.5460e-01j,
        6.8604e-01+ 5.5460e-01j, 5.0610e-01+ 5.5460e-01j,
        1.4058e+00+ 5.5460e-01j, 1.2259e+00+ 5.5460e-01j,
        8.6599e-01+ 5.5460e-01j, 1.0459e+00+ 5.5460e-01j,
        -1.4508e+00+ 3.6385e-01j, -1.3383e+00+ 1.7221e-01j,
        -1.1134e+00+ -2.1017e-01j, -1.2259e+00+ -1.8529e-02j,
        -6.6355e-01+ -9.7494e-01j, -7.7601e-01+ -7.8420e-01j,
        -1.0009e+00+ -4.0181e-01j, -8.8848e-01+ -5.9255e-01j,
        1.4621e-01+ 1.0473e-01j, 1.1246e-02+ 1.0473e-01j,
        -2.1368e-01+ -7.5211e-02j, -1.2371e-01+ 1.0473e-01j,
        -5.7358e-01+ -7.9499e-01j, -4.8360e-01+ -6.1505e-01j,
        -3.0366e-01+ -2.5516e-01j, -3.9363e-01+ -4.3510e-01j,
        8.5069e-01+ -7.5211e-02j, 7.4632e-01+ -2.5516e-01j,
        5.3579e-01+ -6.1505e-01j, 6.4105e-01+ -4.3510e-01j,
        -3.3741e-02+ -9.7494e-01j, 1.4621e-01+ -9.7494e-01j,
        4.3142e-01+ -7.9499e-01j, 3.2615e-01+ -9.7494e-01j,
        2.8116e-01+ 1.0473e-01j, 4.1612e-01+ 1.0473e-01j,
        2.0649e-01+ -2.5516e-01j, 3.1086e-01+ -7.5211e-02j,
        -2.1368e-01+ -9.7494e-01j, -1.0842e-01+ -7.9499e-01j,
        1.0122e-01+ -4.3510e-01j, -4.0500e-03+ -6.1505e-01j],-0.5949
        self.QPSK = QPSK = 1,2, [-1.0,1.0,-1.0j,1.0j],-1.0
        self.QAM64 = QAM64 = 3,6,[-0.462910049886276 + 0.462910049886276j,-0.462910049886276 + 0.154303349962092j,-0.462910049886276 - 0.154303349962092j,-0.462910049886276 - 0.462910049886276j,-0.154303349962092 + 0.462910049886276j,-0.154303349962092 + 0.154303349962092j,	-0.154303349962092 - 0.154303349962092j,-0.154303349962092 - 0.462910049886276j,0.154303349962092 + 0.462910049886276j,	0.154303349962092 + 0.154303349962092j,	0.154303349962092 - 0.154303349962092j,	0.154303349962092 - 0.462910049886276j,	0.462910049886276 + 0.462910049886276j,	0.462910049886276 + 0.154303349962092j,	0.462910049886276 - 0.154303349962092j,	0.462910049886276 - 0.462910049886276j,	-0.462910049886276 + 0.771516749810460j,-0.154303349962092 + 0.771516749810460j,0.154303349962092 + 0.771516749810460j,	0.462910049886276 + 0.771516749810460j,	-0.771516749810460 + 0.462910049886276j,0.771516749810460 + 0.462910049886276j,	-0.771516749810460 + 0.154303349962092j,0.771516749810460 + 0.154303349962092j,	-0.771516749810460 - 0.154303349962092j,	0.771516749810460 - 0.154303349962092j,	-0.771516749810460 - 0.462910049886276j,0.771516749810460 - 0.462910049886276j,	-0.462910049886276 - 0.771516749810460j,-0.154303349962092 - 0.771516749810460j,	0.154303349962092 - 0.771516749810460j,	0.462910049886276 - 0.771516749810460j,	-1.08012344973464 + 1.08012344973464j,	-0.771516749810460 + 1.08012344973464j,	-0.462910049886276 + 1.08012344973464j,	-0.154303349962092 + 1.08012344973464j,	0.154303349962092 + 1.08012344973464j,	0.462910049886276 + 1.08012344973464j,	0.771516749810460 + 1.08012344973464j,	1.08012344973464 + 1.08012344973464j,	-1.08012344973464 + 0.771516749810460j,	-0.771516749810460 + 0.771516749810460j,0.771516749810460 + 0.771516749810460j,	1.08012344973464 + 0.771516749810460j,-1.08012344973464 + 0.462910049886276j,	-1.08012344973464 + 0.154303349962092j,	-1.08012344973464 - 0.154303349962092j,	-1.08012344973464 - 0.462910049886276j,	1.08012344973464 + 0.462910049886276j,1.08012344973464 + 0.154303349962092j,	1.08012344973464 - 0.154303349962092j,1.08012344973464 - 0.462910049886276j,	-1.08012344973464 - 0.771516749810460j,	-0.771516749810460 - 0.771516749810460j,0.771516749810460 - 0.771516749810460j,	1.08012344973464 - 0.771516749810460j,-1.08012344973464 - 1.08012344973464j,	-0.771516749810460 - 1.08012344973464j,	-0.462910049886276 - 1.08012344973464j,	-0.154303349962092 - 1.08012344973464j,	0.154303349962092 - 1.08012344973464j,0.462910049886276 - 1.08012344973464j,	0.771516749810460 - 1.08012344973464j,	1.08012344973464 - 1.08012344973464j],-0.619047
        self.QAM16 = QAM16 = 2,4,[-0.9487 + 0.9487j,  -0.9487 + 0.3162j,  -0.9487 - 0.3162j,  -0.9487 - 0.9487j,  -0.3162 + 0.9487j,  -0.3162 + 0.3162j,  -0.3162 - 0.3162j,  -0.3162 - 0.9487j,   0.3162 + 0.9487j,0.3162 + 0.3162j,   0.3162 - 0.3162j,   0.3162 - 0.9487j,   0.9487 + 0.9487j,   0.9487 + 0.3162j,   0.9487 - 0.3162j,   0.9487 - 0.9487j],-0.68
        self.BPSK = BPSK = 0,1,[-1.0,1.0],-2.0

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_0 = filter.interp_fir_filter_ccf(samps_per_symb, firdes.root_raised_cosine(
        	samps_per_symb, samp_rate, symb_rate, rrc_alpha, rrc_taps))
        self.digital_chunks_to_symbols_2_0 = digital.chunks_to_symbols_bc((VT[2]), 1)
        self.digital_chunks_to_symbols_2 = digital.chunks_to_symbols_bc((QAM64[2]), 1)
        self.digital_chunks_to_symbols_1 = digital.chunks_to_symbols_bc((QAM16[2]), 1)
        self.digital_chunks_to_symbols_0 = digital.chunks_to_symbols_bc((QPSK[2]), 1)
        self.digital_chunks_to_symbols = digital.chunks_to_symbols_bc((BPSK[2]), 1)
        self.blocks_packed_to_unpacked_2_0 = blocks.packed_to_unpacked_bb(VT[1], gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked_2 = blocks.packed_to_unpacked_bb(QAM64[1], gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked_1 = blocks.packed_to_unpacked_bb(QAM16[1], gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked_0 = blocks.packed_to_unpacked_bb(QPSK[1], gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked = blocks.packed_to_unpacked_bb(BPSK[1], gr.GR_MSB_FIRST)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 10000)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "samples" + str(self.file_index) + ".dat", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=5,
        	num_outputs=1,
        	input_index=modulation_scheme,
        	output_index=0,
        )
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 256, 10000000)), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise_volt, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_1, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_2, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_2_0, 0))
        self.connect((self.blks2_selector_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_packed_to_unpacked, 0), (self.digital_chunks_to_symbols, 0))
        self.connect((self.blocks_packed_to_unpacked_0, 0), (self.digital_chunks_to_symbols_0, 0))
        self.connect((self.blocks_packed_to_unpacked_1, 0), (self.digital_chunks_to_symbols_1, 0))
        self.connect((self.blocks_packed_to_unpacked_2, 0), (self.digital_chunks_to_symbols_2, 0))
        self.connect((self.blocks_packed_to_unpacked_2_0, 0), (self.digital_chunks_to_symbols_2_0, 0))
        self.connect((self.digital_chunks_to_symbols, 0), (self.blks2_selector_0, 0))
        self.connect((self.digital_chunks_to_symbols_0, 0), (self.blks2_selector_0, 1))
        self.connect((self.digital_chunks_to_symbols_1, 0), (self.blks2_selector_0, 2))
        self.connect((self.digital_chunks_to_symbols_2, 0), (self.blks2_selector_0, 3))
        self.connect((self.digital_chunks_to_symbols_2_0, 0), (self.blks2_selector_0, 4))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_add_xx_0, 1))

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_samps_per_symb(int(self.samp_rate/self.symb_rate))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.samps_per_symb, self.samp_rate, self.symb_rate, self.rrc_alpha, self.rrc_taps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samps_per_symb(int(self.samp_rate/self.symb_rate))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.samps_per_symb, self.samp_rate, self.symb_rate, self.rrc_alpha, self.rrc_taps))

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb
        self.set_noise_volt(pow(self.samps_per_symb/pow(10.0,self.SNR/10.0),0.5))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.samps_per_symb, self.samp_rate, self.symb_rate, self.rrc_alpha, self.rrc_taps))

    def get_SNR(self):
        return self.SNR

    def set_SNR(self, SNR):
        self.SNR = SNR
        self.set_noise_volt(pow(self.samps_per_symb/pow(10.0,self.SNR/10.0),0.5))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.samps_per_symb, self.samp_rate, self.symb_rate, self.rrc_alpha, self.rrc_taps))

    def get_rrc_alpha(self):
        return self.rrc_alpha

    def set_rrc_alpha(self, rrc_alpha):
        self.rrc_alpha = rrc_alpha
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.samps_per_symb, self.samp_rate, self.symb_rate, self.rrc_alpha, self.rrc_taps))

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.analog_noise_source_x_0.set_amplitude(self.noise_volt)

    def get_modulation_scheme(self):
        return self.modulation_scheme

    def set_modulation_scheme(self, modulation_scheme):
        self.modulation_scheme = modulation_scheme
        self.blks2_selector_0.set_input_index(int(self.modulation_scheme))

    def get_VT(self):
        return self.VT

    def set_VT(self, VT):
        self.VT = VT
        self.digital_chunks_to_symbols_2_0.set_symbol_table((self.VT[2]))

    def get_QPSK(self):
        return self.QPSK

    def set_QPSK(self, QPSK):
        self.QPSK = QPSK
        self.digital_chunks_to_symbols_0.set_symbol_table((self.QPSK[2]))

    def get_QAM64(self):
        return self.QAM64

    def set_QAM64(self, QAM64):
        self.QAM64 = QAM64
        self.digital_chunks_to_symbols_2.set_symbol_table((self.QAM64[2]))

    def get_QAM16(self):
        return self.QAM16

    def set_QAM16(self, QAM16):
        self.QAM16 = QAM16
        self.digital_chunks_to_symbols_1.set_symbol_table((self.QAM16[2]))

    def get_BPSK(self):
        return self.BPSK

    def set_BPSK(self, BPSK):
        self.BPSK = BPSK
        self.digital_chunks_to_symbols.set_symbol_table((self.BPSK[2]))


def main(mod_num, index, options=None):

    tb = top_block(index,mod_num)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    iterations = 1
    counter = 0
    if len(sys.argv) == 2:
        try:
            iterations = int(sys.argv[1])
        except ValueError:
            print("Invalid argument, must be an int")
    elif len(sys.argv) > 2:
            print("Invalid number of arguments, 0 or 1 expected")

    i = 0
    while i in range(0,iterations):
        if (iterations < 5):
            counter = randint(0,4)
        else:
            counter = counter + 1
            if (counter >=5 ):
                counter = 0
        main(counter, i)
        i = i+1
