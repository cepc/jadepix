#!/usr/bin/env python

'''
Combine root files for Iron55
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os
import numpy as np
import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetStatX(0.9)
ROOT.gStyle.SetStatY(0.9)
ROOT.gStyle.SetStatW(0.08)
ROOT.gStyle.SetStatH(0.12)
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# console.setFormatter(logging.Formatter(' %(asctime)s - %(levelname)s- %(message)s'))
# logging.getLogger('').addHandler(console)

class Combine():

    def __init__(self,input_dir,output_name):

        self.input_dir = input_dir
        self.output = ROOT.TFile(output_name,'recreate')

        #creat clusters tree
        self.pedestal_tree = ROOT.TTree('Pedestal_Tree','Pedestal_Tree')

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



    def fill(self,fname):

        try:
            tmp_file = ROOT.TFile(fname)
            tmp_tree = tmp_file.Get('Pedestal_Tree')
            tmp_entries = tmp_tree.GetEntries()

        except:
            logging.error('input file is invalid!')
            sys.exit()

        for ientry in xrange(tmp_entries):
            tmp_tree.GetEntry(ientry)

            for channel in xrange(16):
                for row in xrange(48):

                    value_name = 'self.tmp_tree.Chanel_%d_Row_%d'%(channel+1,row+1)
                    pixel_value = locals(value_name)
                    self.pixel[channel,row] =  pixel_value 

        self.pedestal_tree.Fill()

        logging.info('combined :  '+fname)


    def run(self):

        for parent,dirnames,filenames in os.walk(self.input_dir):
            count = 0
            for filename in filenames:
                fname = os.path.join(parent,filename)
                count += 1
                logging.info('find %d files : %s'%(count,fname))
                self.fill(fname)

        self.pedestal_tree.GetCurrentFile().Write()
        self.output.Close()


if __name__ == '__main__':

    if len(sys.argv) < 2:  
        print('No chip address specified!')  
        sys.exit() 

    if len(sys.argv) == 2:
        if sys.argv[1].startswith('-a'):
            chip_address = sys.argv[1][1:]
            print('Set chip address to %s'%chip_address.upper())

            input_dir = './python/output/output_%s_pedestal'%chip_address.lower()
            output_name = './python/output/CHIP%s_Pedestal.root'%chip_address.upper()

            COMBINE = Combine(input_dir,output_name)
            COMBINE.run()

        else:
            print('Chip address is invalid!')
            sys.exit()   
            
    if len(sys.argv) == 3:
        if (sys.argv[1].startswith('-a') and sys.argv[2].startswith('-a')):
            chip_address_start = sys.argv[1][1:]
            chip_address_end = sys.argv[2][1:]
            chip_address_start_number = int(sys.argv[1][2:])
            chip_address_end_number = int(sys.argv[2][2:])

            if (chip_address_start_number > chip_address_end_number):
                print('chip_address_end_number have to large than chip_address_start_number!')
                sys.exit()

            print('Set chip address from %s to %s .'%(chip_address_start.upper(),chip_address_end.upper()))

            for address_number in xrange(chip_address_start_number,chip_address_end_number+1):                
                chip_address = 'a%d'%address_number

                input_dir = './python/output/output_%s_pedestal'%chip_address.lower()
                output_name = './python/output/CHIP%s_Pedestal.root'%chip_address.upper()

                COMBINE = Combine(input_dir,output_name)
                COMBINE.run()

        else:
            print('Chip address is invalid!')
            sys.exit()    




