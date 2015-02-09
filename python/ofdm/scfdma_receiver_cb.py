#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr

class scfdma_receiver_cb(gr.hier_block2):
    """
    docstring for block scfdma_receiver_cb
    """
    def __init__(self, N=12, M=256, start_index=10, mapping=0, modulation=16, cp_ratio=0.25):
        gr.hier_block2.__init__(self,
            "scfdma_receiver_cb",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.start_index = start_index
        self.modulation = modulation
        self.cp_ratio = cp_ratio
        self.M = M
        self.N = N
        self.mapping = mapping

        ##################################################
        # Blocks
        ##################################################
        self.ofdm_scfdma_subcarrier_demapper_vcvc_0 = ofdm.scfdma_subcarrier_demapper_vcvc(N, M, start_index, mapping)
        self.ofdm_fbmc_symbol_estimation_vcb_0 = ofdm.fbmc_symbol_estimation_vcb(N, modulation)
        self.fft_vxx_0_0 = fft.fft_vcc(N, False, (), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(M, True, (), True, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, M)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_gr_complex, M, int(M*(1+cp_ratio)), int(cp_ratio*M))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.ofdm_scfdma_subcarrier_demapper_vcvc_0, 0))    
        self.connect((self.fft_vxx_0_0, 0), (self.ofdm_fbmc_symbol_estimation_vcb_0, 0))    
        self.connect((self.ofdm_fbmc_symbol_estimation_vcb_0, 0), (self, 0))    
        self.connect((self.ofdm_scfdma_subcarrier_demapper_vcvc_0, 0), (self.fft_vxx_0_0, 0))    
        self.connect((self, 0), (self.blocks_keep_m_in_n_0, 0))    


    def get_start_index(self):
        return self.start_index

    def set_start_index(self, start_index):
        self.start_index = start_index

    def get_modulation(self):
        return self.modulation

    def set_modulation(self, modulation):
        self.modulation = modulation

    def get_cp_ratio(self):
        return self.cp_ratio

    def set_cp_ratio(self, cp_ratio):
        self.cp_ratio = cp_ratio
        self.blocks_keep_m_in_n_0.set_offset(int(self.cp_ratio*self.M))
        self.blocks_keep_m_in_n_0.set_n(int(self.M*(1+self.cp_ratio)))

    def get_M(self):
        return self.M

    def set_M(self, M):
        self.M = M
        self.blocks_keep_m_in_n_0.set_offset(int(self.cp_ratio*self.M))
        self.blocks_keep_m_in_n_0.set_m(self.M)
        self.blocks_keep_m_in_n_0.set_n(int(self.M*(1+self.cp_ratio)))

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N

