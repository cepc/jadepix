#!/usr/bin/env python

'''
plot Chip A1 Iron55 clusters hist
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

class Sort():

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

        logging.info('sorted :  '+fname)


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

    # SORT = Sort('../output/chip_a1','../output/CHIPA1_Cluster55_Iron55_thr500.root')
    # SORT = Sort('../output/chip_a2','../output/CHIPA2_Cluster55_Iron55_thr500.root')
    # SORT = Sort('../output/chip_a3','../output/CHIPA3_Cluster55_Iron55_thr500.root')
    # SORT = Sort('../output/chip_a4','../output/CHIPA4_Cluster55_Iron55_thr500.root')
    # SORT = Sort('../output/chip_a5','../output/CHIPA5_Cluster55_Iron55_thr500.root')
    # SORT = Sort('../output/chip_a6','../output/CHIPA6_Cluster55_Iron55_thr500.root')

    SORT = Sort('../output/chip_a1_sr','../output/CHIPA1_Cluster55_Sr90_thr500.root')
    # SORT = Sort('../output/chip_a2_sr','../output/CHIPA2_Cluster55_Sr90_thr500.root')
    # SORT = Sort('../output/chip_a3_sr','../output/CHIPA3_Cluster55_Sr90_thr500.root')
    # SORT = Sort('../output/chip_a4_sr','../output/CHIPA4_Cluster55_Sr90_thr500.root')
    # SORT = Sort('../output/chip_a5_sr','../output/CHIPA5_Cluster55_Sr90_thr500.root')
    # SORT = Sort('../output/chip_a6_sr','../output/CHIPA6_Cluster55_Sr90_thr500.root')
    
    SORT.run()




