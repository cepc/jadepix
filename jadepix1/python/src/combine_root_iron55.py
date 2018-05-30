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
        self.cluster_tree = ROOT.TTree('Cluster_Tree','Cluster')

        #init value
        self.seed_channel = np.zeros(1, dtype='int16')
        self.seed_row = np.zeros(1, dtype='int16')
        self.seed_adc = np.zeros(1, dtype='int16')
        self.total_cluster_adc = np.zeros(1, dtype='uint16')
        self.single_cluster_adc = ROOT.std.vector(int)()
        self.size = np.zeros(1, dtype='int16')

        #creat branches
        self.cluster_tree.Branch('Seed_Channel',self.seed_channel,'Seed_Channel/S')
        self.cluster_tree.Branch('Seed_Row',self.seed_row,'Seed_Row/S')
        self.cluster_tree.Branch('SeedSignal',self.seed_adc,'SeedSignal/S')
        self.cluster_tree.Branch('TotalClusterSignal',self.total_cluster_adc,'TotalClusterSignal/s')
        self.cluster_tree.Branch('SingleClusterSignal',self.single_cluster_adc)
        self.cluster_tree.Branch('Size',self.size,'Size/S')


    def fill(self,fname):

        try:
            tmp_file = ROOT.TFile(fname)
            tmp_tree = tmp_file.Get('Cluster_Tree')
            tmp_entries = tmp_tree.GetEntries()

        except:
            logging.error('input file is invalid!')
            sys.exit()

        for ientry in xrange(tmp_entries):
            tmp_tree.GetEntry(ientry)
            self.seed_channel[0] = tmp_tree.Seed_Channel
            self.seed_row[0] = tmp_tree.Seed_Row
            self.total_cluster_adc[0] = tmp_tree.TotalClusterSignal

            self.single_cluster_adc.clear()
            seed_signal = 0
            for index in xrange(25):
                self.single_cluster_adc.push_back(tmp_tree.SingleClusterSignal.at(index))
                if tmp_tree.SingleClusterSignal.at(index) > seed_signal :
                    seed_signal = tmp_tree.SingleClusterSignal.at(index)

            self.seed_adc[0] = seed_signal
            self.size[0] =tmp_tree.Size
            self.cluster_tree.Fill()

        logging.info('combined :  '+fname)


    def run(self):

        for parent,dirnames,filenames in os.walk(self.input_dir):
            count = 0
            for filename in filenames:
                fname = os.path.join(parent,filename)
                count += 1
                logging.info('find %d files : %s'%(count,fname))
                self.fill(fname)

        self.cluster_tree.GetCurrentFile().Write()
        self.output.Close()


if __name__ == '__main__':

    if len(sys.argv) < 2:  
        print('No chip address specified!')  
        sys.exit() 

    if len(sys.argv) == 2:
        if sys.argv[1].startswith('-a'):
            chip_address = sys.argv[1][1:]
            print('Set chip address to %s'%chip_address.upper())

            input_dir = './python/output/output_%s_iron55'%chip_address.lower()
            output_name = './python/output/CHIP%s_Cluster55_Iron55_thr500.root'%chip_address.upper()

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

                input_dir = './python/output/output_%s_iron55'%chip_address.lower()
                output_name = './python/output/CHIP%s_Cluster55_Iron55_thr500.root'%chip_address.upper()

                COMBINE = Combine(input_dir,output_name)
                COMBINE.run()

        else:
            print('Chip address is invalid!')
            sys.exit()    




