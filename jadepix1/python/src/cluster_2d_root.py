#!/usr/bin/env python

'''
Create cluster 2D results to root file
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os,copy
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


def get_th2f(fname,title):

    try:
        input = ROOT.TFile(fname)
        cluster_tree = input.Get('Cluster_Tree')
        #cluster_entries = cluster_tree.GetEntries()
        cluster_entries = 2000000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    cluster_th2f = ROOT.TH2F('CHIP_%s_CLUSTER_2D'%title,'',25,0,25,500,0,5000)
    cluster_th2f.GetXaxis().SetTitle('Number of pixels in cluster')
    cluster_th2f.GetXaxis().CenterTitle()
    cluster_th2f.GetYaxis().SetTitle('ADC')
    cluster_th2f.GetYaxis().CenterTitle()

    size_th2f = ROOT.TH2F('CHIP_%s_SIZE_2D'%title,'',500,0,5000,25,0,25)
    size_th2f.GetXaxis().SetTitle('ADC')
    size_th2f.GetXaxis().CenterTitle()
    size_th2f.GetYaxis().SetTitle('Cluster size')
    size_th2f.GetYaxis().CenterTitle()

    for cluster_entry in xrange(cluster_entries):
        tmp_list = []
        cluster_tree.GetEntry(cluster_entry)
        for index in xrange(25):
            tmp_list.append(cluster_tree.SingleClusterSignal.at(index))

        tmp_list.sort(reverse=True)
        cluster_adc = 0
        for jndex in xrange(25):
            cluster_adc += tmp_list[jndex]
            cluster_th2f.Fill(jndex+1,cluster_adc)

        size_th2f.Fill(cluster_tree.TotalClusterSignal,cluster_tree.Size)

    c_cluster_th2f = copy.copy(cluster_th2f)
    c_size_th2f = copy.copy(size_th2f)

    return c_cluster_th2f,c_size_th2f

def save_root():
    output = ROOT.TFile('./python/output/Iron55_Cluster_ADC_2D.root','recreate')
    for chip_address in xrange(1,7):
        cluster_th2f,size_th2f = get_th2f('./python/output/CHIPA%d_Cluster55_Iron55_thr500.root'%chip_address,'A%d'%chip_address)
        output.Append(cluster_th2f)
        output.Append(size_th2f)
        print('save root A%d'%chip_address)
    output.Write()
    output.Close()


if __name__ == '__main__':
    
    save_root()