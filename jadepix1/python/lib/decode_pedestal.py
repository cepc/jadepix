   #!/usr/bin/env python

'''
MOUDLE : decode pedestal data to cluster with excluding overlap siganl
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
        self.pedestal_tree = ROOT.TTree('Pedestal_Tree','Cluster')

        #init value
        self.pixel = np.zeros([16,48,1],dtype='int16')
        self.count = 0

        #init hist list
        self.hist_list = []

        #creat branches
        for channel in xrange(16):
            for row in xrange(48):
                tmp_name = 'Chanel_%d_Row_%d'%(channel+1,row+1)
                self.pedestal_tree.Branch(tmp_name,self.pixel[channel,row],tmp_name+'/S')
                ROOT.TH1F(tmp_name,tmp_name,500,0,500)


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

        #init temp value
        tmp_adc = 0
        tmp_max_adc = 0
        tmp_frame_array=np.reshape(frame_adc, newshape=(48, 16, 2))
        tmp_frame=np.zeros((48,16), dtype='int16')

        for row in xrange(0,48):
            for channel in xrange(0,16):

                tmp_adc =tmp_frame_array[row, channel, 0]+tmp_frame_array[row, channel, 1]*256 
                #tmp_adc = self.get_int16_abs(tmp_adc)
                #tmp_frame[row,channel] = tmp_adc
                self.pixel[channel,row,0] = tmp_adc

        #print(self.pixel)
        tmp_max_adc = np.amax(self.pixel)
        tmp_min_adc = np.amin(self.pixel)
        # print('MAX : ',tmp_max_adc)
        # print('MIN : ',tmp_min_adc)

        if (tmp_max_adc < 100) and (tmp_min_adc > -100) :
            self.pedestal_tree.Fill()
            self.count += 1
                    
            
    def process_frame(self):
        
        #configure
        data =  open(self.input,'rb')
        print_number = 1000
        try_process_number = 19280
        maxframenumber = 1000000

        #init value
        seek_position = 0
        frame_number = 0
        cds_frame_number = 0
        broken_frame_number = 0
        broken_bulk_number = 0
        broken_flag = False

        #start 
        #while frame_number < maxframenumber:   
        while self.count < maxframenumber:
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

        self.pedestal_tree.GetCurrentFile().Write()
        self.output.Close()
        data.close()

    def run(self):
        start_time = time.clock()
        self.process_frame()
        end_time = time.clock()
        print('Running time: %s Seconds'%(end_time-start_time))

