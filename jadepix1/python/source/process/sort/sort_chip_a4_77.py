#!/usr/bin/env python

'''
plot Chip A4 Iron55 clusters hist
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

#create output root file
if not os.path.exists('../output/'):
    os.makedirs('../output/')

OUTPUT = ROOT.TFile('../output/CHIPA4_Cluster77_Iron55_thr500.root','recreate')

#creat clusters tree
CLUSTER_TREE = ROOT.TTree('Cluster_Tree','Cluster')


SEED_CHANNEL = np.zeros(1, dtype='int16')
SEED_ROW = np.zeros(1, dtype='int16')
SEED_ADC = np.zeros(1, dtype='int16')
CLUSTER_ADC = np.zeros(1, dtype='int16')
SIZE = np.zeros(1, dtype='int16')

CLUSTER_TREE.Branch('Seed_Channel',SEED_CHANNEL,'Seed_Channel/S')
CLUSTER_TREE.Branch('Seed_Row',SEED_ROW,'Seed_Row/S')
CLUSTER_TREE.Branch('SeedSignal',SEED_ADC,'SeedSignal/S')
CLUSTER_TREE.Branch('ClusterSignal',CLUSTER_ADC,'ClusterSignal/S')
CLUSTER_TREE.Branch('Size',SIZE,'Size/S')



def fill(fname):

    global OUTPUT,CLUSTER_TREE,SEED_ADC,CLUSTER_ADC,SIZE

    try:
        tmp_file = ROOT.TFile(fname)
        tmp_tree = tmp_file.Get('Cluster_Tree')
        tmp_entries = tmp_tree.GetEntries()

    except:
        logging.error('input file is invalid!')
        sys.exit()

    for ientry in xrange(tmp_entries):
        tmp_tree.GetEntry(ientry)
        SEED_CHANNEL[0] = tmp_tree.Seed_Channel
        SEED_ROW[0] = tmp_tree.Seed_Row
        SEED_ADC[0] = tmp_tree.SeedSignal
        CLUSTER_ADC[0] = tmp_tree.ClusterSignal
        SIZE[0] =tmp_tree.Size
        CLUSTER_TREE.Fill()

    logging.info('sorted :  '+fname)



def main(rootdir):

    global CLUSTER_TREE,OUTPUT

    for parent,dirnames,filenames in os.walk(rootdir):
        count = 0
        for filename in filenames:
            fname = os.path.join(parent,filename)
            count += 1
            logging.info('find %d files : %s'%(count,fname))
            fill(fname)

    CLUSTER_TREE.GetCurrentFile().Write()
    OUTPUT.Close()


if __name__ == '__main__':
   
    main('../output/chip_a4_77')




