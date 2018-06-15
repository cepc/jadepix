#!/usr/bin/env python

'''
select some frame samples in root file
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"

import os
import sys,copy
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

        #define thread
        self.seed_threshold = 500
        self.cluster_threshold = 500
        self.size_adc_threshold = 200  

        #configure cluster size
        self.cluster_size = 2

        self.fill_cds_count = 0

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

    def fill_cds(self,frame_adc):

        flag = 0

        #init value
        row_seed = 0
        channel_seed = 0

        tmp_frame_array=np.reshape(frame_adc, newshape=(48, 16, 2))
        tmp_frame=np.zeros((48,16), dtype='int16')

        for row in xrange(0,48):
            for channel in xrange(0,16):

                tmp_adc =tmp_frame_array[row, channel, 0]+tmp_frame_array[row, channel, 1]*256 
                tmp_adc = self.get_int16_abs(tmp_adc)
                tmp_frame[row,channel] = tmp_adc
                tmp_frame.dtype = 'uint16'
                #print(tmp_frame)

        #find seed#
        tmp_seed_adc = np.max(tmp_frame)
        tmp_seed_position = np.where(tmp_frame == tmp_seed_adc)

        row_seed = tmp_seed_position[0][0]
        channel_seed = tmp_seed_position[1][0]
        #seed end#

        # #exclude overlap
        # overlap = False
        # for row_angle in [-1,0,1]:
        #     for channel_angle in [-1,0,1]:
        #         if (row_angle == 0) and (channel_angle == 0):
        #             continue
        #         tmp_row = row_seed + 2*row_angle
        #         tmp_channel = channel_seed + 2*channel_angle
        #         if( (tmp_row>=0) and (tmp_row<48) and (tmp_channel>=0) and (tmp_channel<16) ):
        #             if (tmp_frame[tmp_row,tmp_channel] - tmp_frame[row_seed+row_angle,channel_seed+channel_angle])>200:
        #                 overlap = True
        #                 break
        # #exclude    end#

        if tmp_seed_adc > 1000:
            flag = 1
            self.fill_cds_count += 1
            tmp_th2f = ROOT.TH2F('CDS_Frame_%d'%self.fill_cds_count,'',48,0,48,16,0,16)
            for chanel in xrange(16):
                for row in xrange(48):
                    tmp_th2f.SetBinContent(row+1,chanel+1,tmp_frame[row,chanel])

            self.output.Append(copy.copy(tmp_th2f))

        return flag


    def fill_raw(self,frame_adc,title):

        tmp_th2f = ROOT.TH2F('%s_Raw_Frame_%d'%(title,self.fill_cds_count),'',48,0,48,16,0,16)

        tmp_frame_array=np.reshape(frame_adc, newshape=(48, 16, 2))
        tmp_frame=np.zeros((48,16), dtype='int16')

        for row in xrange(0,48):
            for channel in xrange(0,16):

                tmp_adc =tmp_frame_array[row, channel, 0]+tmp_frame_array[row, channel, 1]*256 
                tmp_adc = self.get_int16_abs(tmp_adc)
                tmp_frame[row,channel] = tmp_adc
                tmp_frame.dtype= 'uint16'

        for chanel in xrange(16):
            for row in xrange(48):
                tmp_th2f.SetBinContent(row+1,chanel+1,tmp_frame[row,chanel])

        self.output.Append(copy.copy(tmp_th2f))
                    
            
    def process_frame(self):
        
        #configure
        data =  open(self.input,'rb')
        print_number = 1000
        try_process_number = 19280
        maxframenumber = 20000

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
                    
                    flag = self.fill_cds(cds_frame_adc)
                    if flag == 1:
                        self.fill_raw(last_frame_adc,'Up')
                        self.fill_raw(frame_adc,'Down')

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

        self.output.Write()
        data.close()

    def run(self):
        start_time = time.clock()
        self.process_frame()
        end_time = time.clock()
        print('Running time: %s Seconds'%(end_time-start_time))


def main():

    if not os.path.exists('./python/output/'):
        os.makedirs('./python/output/')

    input = '/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180329/WeakFe_CHIPA1_180329094037.df'
    output = './python/output/Select_Frames.root'

    decode = Decode(input,output)
    decode.run()


if __name__ == '__main__':
    main()
