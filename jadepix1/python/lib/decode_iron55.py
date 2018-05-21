#!/usr/bin/env python

'''
MOUDLE : decode source data to cluster with excluding overlap siganl
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"

import os
import sys
import re
import numpy as np
import time
import ROOT
import logging
logging.basicConfig(level=logging.DEBUG,format= ' %(asctime)s - %(levelname)s- %(message)s')

class Decode():

    def __init__(self,input,output):

        #define input and output
        self.input = input
        self.output = ROOT.TFile(output,'recreate')

        #creat clusters tree
        self.cluster_tree = ROOT.TTree('Cluster_Tree','Cluster')

        #init value

        self.seed_channel = np.zeros(1, dtype='int16')
        self.seed_row = np.zeros(1, dtype='int16')
        self.seed_adc = np.zeros(1, dtype='int16')

        self.total_cluster_adc = np.zeros(1, dtype='int16')

        self.single_cluster_adc = ROOT.std.vector(int)()

        self.size = np.zeros(1, dtype='int16')

        #creat branches
        self.cluster_tree.Branch('Seed_Channel',self.seed_channel,'Seed_Channel/S')
        self.cluster_tree.Branch('Seed_Row',self.seed_row,'Seed_Row/S')
        self.cluster_tree.Branch('SeedSignal',self.seed_adc,'SeedSignal/S')
        self.cluster_tree.Branch('TotalClusterSignal',self.total_cluster_adc,'TotalClusterSignal/S')
        self.cluster_tree.Branch('SingleClusterSignal',self.single_cluster_adc)
        self.cluster_tree.Branch('Size',self.size,'Size/S')

        #define thread
        self.seed_threshold = 500
        self.cluster_threshold = 500
        self.size_adc_threshold = 200  

        #configure cluster size
        self.cluster_size = 2

    def get_int16_abs(self,number):
        
        if (number & 0x8000) != 0:  
            abs_number = ((number - 1) ^ 0xFFFF)
        else:
            abs_number = number

        return abs_number        

    def bytes_to_int(self,thebytes):
        uint_data = np.frombuffer(thebytes, dtype=np.uint8)
        int_data = uint_data.astype('int16')
        return int_data

    def process_raw(self,framebytes):
        clear_frame_bytes = b''
        origin_frame_bytes = framebytes                                          
        tmp = re.findall(b'....(.{32})....',origin_frame_bytes,re.DOTALL)    
        clear_frame_bytes = b''.join(tmp)
        return clear_frame_bytes

    def fill_root(self,frame_adc):

        #init value
        row_seed = 0
        channel_seed = 0

        #init temp value
        tmp_adc = 0
        tmp_seed_adc = 0
        tmp_cluster_adc = 0
        tmp_size = 0

        tmp_frame_array=np.reshape(frame_adc, newshape=(48, 16, 2))
        tmp_frame=np.zeros((48,16), dtype='int16')

        for row in xrange(0,48):
            for channel in xrange(0,16):

                tmp_adc =tmp_frame_array[row, channel, 0]+tmp_frame_array[row, channel, 1]*256 
                tmp_adc = self.get_int16_abs(tmp_adc)
                tmp_frame[row,channel] = tmp_adc

        #find seed#
        tmp_seed_adc = np.max(tmp_frame)
        tmp_seed_position = np.where(tmp_frame == tmp_seed_adc)

        row_seed = tmp_seed_position[0][0]
        channel_seed = tmp_seed_position[1][0]
        #seed end#

                # print(tmp_frame)
                # print('SEED ADC : ',tmp_seed_adc)
                # print('SEED POS : ',tmp_seed_position)
                # print('SEED ROW : ',row_seed)
                # print('SEED CHA : ',channel_seed)

        #exclude overlap
        overlap = False
        for row_angle in [-1,0,1]:
            for channel_angle in [-1,0,1]:
                if (row_angle == 0) and (channel_angle == 0):
                    continue
                tmp_row = row_seed + 2*row_angle
                tmp_channel = channel_seed + 2*channel_angle
                if( (tmp_row>=0) and (tmp_row<48) and (tmp_channel>=0) and (tmp_channel<16) ):
                    if (tmp_frame[tmp_row,tmp_channel] - tmp_frame[row_seed+row_angle,channel_seed+channel_angle])>200:
                        overlap = True
                        break
        #exclude    end#

        if not overlap:

            row_cluster_start = row_seed - self.cluster_size
            row_cluster_end = row_seed + self.cluster_size

            channel_cluster_start = channel_seed - self.cluster_size
            channel_cluster_end = channel_seed + self.cluster_size

            if tmp_seed_adc > self.seed_threshold:
                self.single_cluster_adc.clear()
                for row_pos in xrange(row_cluster_start,row_cluster_end+1):
                    for channel_pos in xrange(channel_cluster_start,channel_cluster_end+1):

                        
                        if( (row_pos>=0) and (row_pos<48) and (channel_pos>=0) and (channel_pos<16)):
                        
                            tmp_cluster_adc += tmp_frame[row_pos,channel_pos]


                            #print(int(tmp_frame[row_pos,channel_pos]))
                            self.single_cluster_adc.push_back(int(tmp_frame[row_pos,channel_pos]))
                            
                            #count size#
                            if tmp_frame[row_pos,channel_pos] > self.size_adc_threshold:
                                tmp_size += 1
                            #count end#
                if (channel_seed >= 2) and (channel_seed <= 13) and (row_seed >= 2) and (row_seed <= 45) :
                    if tmp_cluster_adc < 6000 :
                        self.seed_channel[0] = channel_seed
                        self.seed_row[0] = row_seed
                        self.seed_adc[0] = tmp_seed_adc
                        self.total_cluster_adc[0] = tmp_cluster_adc
                        self.size[0] = tmp_size
                        self.cluster_tree.Fill()
                    
            
    def process_frame(self):
        
        #configure
        data =  open(self.input,'rb')
        print_number = 10
        try_process_number = 19280
        maxframenumber = 1000000000000

        #init value
        seek_position = 0
        frame_number = 0
        cds_frame_number = 0
        broken_frame_number = 0
        broken_bulk_number = 0
        broken_flag = False

        #start 
        while frame_number < maxframenumber:   

            data.seek(seek_position)
            try_process_data = data.read(try_process_number)

            if len(try_process_data) != try_process_number:
                logging.critical('\033[33;1m find total %d frames!\033[0m'%frame_number)
                logging.critical('\033[32;1m find total %d cds frames!\033[0m'%cds_frame_number)
                logging.critical('\033[31;1m find total %d broken frames!\033[0m'%broken_frame_number)
                logging.critical('\033[35;1m find total %d broken bulk!\033[0m'%broken_bulk_number)
                logging.critical(' END !')
                break

            m =re.search(b'(\xaa\xaa\xaa\xaa)(.*?)(\xf0\xf0\xf0\xf0)',try_process_data,re.DOTALL)

            if m:
                if len(m.group(2)) == 1920:
                    frame_number += 1
                    frame_bytes = m.group(2)  
                    clear_frame_bytes = self.process_raw(m.group(2))
                    frame_adc = self.bytes_to_int(clear_frame_bytes)

                else:
                    data.seek(seek_position+m.start())
                    tmp_process_data = data.read(1928)
                    tmp_m = re.search(b'(\xaa\xaa\xaa\xaa)(.{1920})(\xf0\xf0\xf0\xf0)',tmp_process_data,re.DOTALL)

                    if tmp_m:
                        frame_number += 1
                        frame_bytes = tmp_m.group(2)
                        clear_frame_bytes = self.process_raw(tmp_m.group(2))
                        frame_adc = self.bytes_to_int(clear_frame_bytes)

                    else:
                        broken_frame_number += 1
                        broken_flag = True
                        logging.info('\033[31;1m find %d broken frames!\033[0m'%broken_frame_number)
                        logging.info('\033[31;1m position: (%d %d) \033[0m'%(seek_position+m.start(),seek_position+m.end()))
                        logging.info('\033[31;1m broken length  : %d\033[0m'%len(m.group()))

                ### cds start ####
                if frame_number > 1 :

                    cds_frame_adc = frame_adc-last_frame_adc
                    self.fill_root(cds_frame_adc)
                    cds_frame_number += 1              
                ### cds end ####

                if frame_number % print_number == 0:
                    logging.info('Find %d frames !'%frame_number)
                    logging.info('position: (%d %d)'%(seek_position+m.start(),seek_position+m.end()))
                    logging.info('Get %d cds frames'%cds_frame_number)

                seek_position += (m.start()+(len(m.group())))

                last_frame_adc = frame_adc

            else:
                print('There is no frame in ( %d %d )'%(seek_position,seek_position+try_process_number))
                broken_flag = True
                broken_bulk_number += 1
                seek_position += try_process_number

        logging.critical('\033[33;1m find total %d frames!\033[0m'%frame_number)
        logging.critical('\033[32;1m find total %d cds frames!\033[0m'%cds_frame_number)
        logging.critical('\033[31;1m find total %d broken frames!\033[0m'%broken_frame_number)
        logging.critical('\033[35;1m find total %d broken bulk!\033[0m'%broken_bulk_number)

        self.cluster_tree.GetCurrentFile().Write()
        self.output.Close()
        data.close()

    def run(self):
        start_time = time.clock()
        self.process_frame()
        end_time = time.clock()
        print('Running time: %s Seconds'%(end_time-start_time))


