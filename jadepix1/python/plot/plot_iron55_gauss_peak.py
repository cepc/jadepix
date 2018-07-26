#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
Get iron55 peaks
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os,copy
import numpy as np
import ROOT
ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetStatX(0.9)
ROOT.gStyle.SetStatY(0.9)
ROOT.gStyle.SetStatW(0.08)
ROOT.gStyle.SetStatH(0.12)
from prettytable import PrettyTable 
import pandas
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# console.setFormatter(logging.Formatter(' %(asctime)s - %(levelname)s- %(message)s'))
# logging.getLogger('').addHandler(console)

def get_peak(hist,xmin,xmax):

    gauss_fit = ROOT.TF1('gauss_fit','gaus',xmin,xmax)
    hist.Fit('gauss_fit','R+')
    mean = gauss_fit.GetParameter(1)
    mean_error = gauss_fit.GetParError(1)

    peak = '%.1f'%mean + '±' + '%.1f'%mean_error

    return peak


def main(root_data):

    chip_number = len(root_data)

    output = ROOT.TFile('./python/output/Iron55_Hist_Fit_Peak.root','recreate')

    chip_address_list = []
    cluster_hist_list = []
    seed_hist_list = []
    size_hist_list = []


    for chip_address in xrange(1,chip_number+1):

        chip_address_list.append('A%d'%chip_address)

        try:
            #get TTree
            tmp_source_file = ROOT.TFile(root_data['a%d'%chip_address][0])
            tmp_cluster_tree = tmp_source_file.Get('Cluster_Tree')
            tmp_cluster_entries = tmp_cluster_tree.GetEntries()
  
        except:
            logging.error('input file is invalid!')
            sys.exit()

        #def cluster hist
        cluster_bin_number = 6000
        tmp_cluster_hist = ROOT.TH1F('a%d_cluster_signal'%chip_address,'a%d_cluster_signal'%chip_address,cluster_bin_number,0,6000)
        tmp_cluster_hist.GetXaxis().SetTitle('ADC')
        tmp_cluster_hist.GetXaxis().CenterTitle()
        tmp_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
        tmp_cluster_hist.GetYaxis().CenterTitle()

        #def seed hist
        seed_bin_number = 6000
        tmp_seed_hist = ROOT.TH1F('a%d_seed_signal'%chip_address,'a%d_seed_signal'%chip_address,seed_bin_number,0,6000)
        tmp_seed_hist.GetXaxis().SetTitle('ADC')
        tmp_seed_hist.GetXaxis().CenterTitle()
        tmp_seed_hist.GetYaxis().SetTitle('Normalized Counts')
        tmp_seed_hist.GetYaxis().CenterTitle()

        #def size hist
        tmp_size_hist = ROOT.TH1F('a%d_size_distribution'%chip_address,'a%d_size_distribution'%chip_address,25,0,25)
        tmp_size_hist.GetXaxis().SetTitle('Size')
        tmp_size_hist.GetXaxis().CenterTitle()
        tmp_size_hist.GetYaxis().SetTitle('Normalized Counts')
        tmp_size_hist.GetYaxis().CenterTitle()
    
        #read data
        for tmp_cluster_entry in xrange(tmp_cluster_entries):
            tmp_cluster_tree.GetEntry(tmp_cluster_entry)
            tmp_cluster_hist.Fill(tmp_cluster_tree.TotalClusterSignal)
            tmp_seed_hist.Fill(tmp_cluster_tree.SeedSignal)
            tmp_size_hist.Fill(tmp_cluster_tree.Size)

        cluster_hist_list.append(copy.copy(tmp_cluster_hist))
        seed_hist_list.append(copy.copy(tmp_seed_hist))
        size_hist_list.append(copy.copy(tmp_size_hist))

        print('***** Read A%d Data *****'%chip_address)


    cluster_peak_list_1 = []
    cluster_peak_list_1.append(get_peak(cluster_hist_list[0],3400,3600))
    cluster_peak_list_1.append(get_peak(cluster_hist_list[1],3000,3200))
    cluster_peak_list_1.append(get_peak(cluster_hist_list[2],2200,2400))
    cluster_peak_list_1.append(get_peak(cluster_hist_list[3],3450,3650))
    cluster_peak_list_1.append(get_peak(cluster_hist_list[4],2700,2900))
    cluster_peak_list_1.append(get_peak(cluster_hist_list[5],1700,1900))

    cluster_peak_list_2 = []
    cluster_peak_list_2.append(get_peak(cluster_hist_list[0],3800,4100))
    cluster_peak_list_2.append(get_peak(cluster_hist_list[1],3350,3700))
    cluster_peak_list_2.append(0.)
    cluster_peak_list_2.append(get_peak(cluster_hist_list[3],3800,4200))
    cluster_peak_list_2.append(get_peak(cluster_hist_list[4],3020,3400))
    cluster_peak_list_2.append(0.)    

    seed_peak_list_1 = []
    seed_peak_list_1.append(get_peak(seed_hist_list[0],3400,3500))
    seed_peak_list_1.append(get_peak(seed_hist_list[1],3000,3100))
    seed_peak_list_1.append(get_peak(seed_hist_list[2],2170,2230))
    seed_peak_list_1.append(get_peak(seed_hist_list[3],3470,3570))
    seed_peak_list_1.append(get_peak(seed_hist_list[4],2730,2800))
    seed_peak_list_1.append(get_peak(seed_hist_list[5],1670,1720))

    seed_peak_list_2 = []
    seed_peak_list_2.append(get_peak(seed_hist_list[0],3700,3900))
    seed_peak_list_2.append(get_peak(seed_hist_list[1],3300,3450))
    seed_peak_list_2.append(get_peak(seed_hist_list[2],2370,2500))
    seed_peak_list_2.append(get_peak(seed_hist_list[3],3800,4000))
    seed_peak_list_2.append(get_peak(seed_hist_list[4],2950,3150))
    seed_peak_list_2.append(get_peak(seed_hist_list[5],1840,1920))


    peak_table = PrettyTable()
    peak_table.add_column('Chip address',chip_address_list)
    peak_table.add_column('Cluster Peak (Ka)',cluster_peak_list_1)
    peak_table.add_column('Cluster Peak (Kb)',cluster_peak_list_2)
    peak_table.add_column('Seed Peak (Ka)',seed_peak_list_1)
    peak_table.add_column('Seed Peak (Kb)',seed_peak_list_2)
    print('\n\n********************************\n********************************')
    print(peak_table)

    dataframe = pandas.DataFrame({'Chip address' : chip_address_list,
                                  'Cluster Peak (Ka)' : cluster_peak_list_1,
                                  'Cluster Peak (Kb)' : cluster_peak_list_2,
                                  'Seed Peak (Ka)' : seed_peak_list_1,
                                  'Seed Peak (Kb)' : seed_peak_list_2})
    dataframe.to_csv("./python/output/Iron55_Gauss_Peak.csv",index=False,sep=',',encoding='utf_8_sig')

    for append_address in xrange(0,chip_number):
        output.Append(cluster_hist_list[append_address])
        output.Append(seed_hist_list[append_address])
        output.Append(size_hist_list[append_address])

    output.Write()
    output.Close()


if __name__ == '__main__':

    root_data = { 'a1' : ['./python/output/CHIPA1_Cluster55_Iron55_thr500.root'],
                  'a2' : ['./python/output/CHIPA2_Cluster55_Iron55_thr500.root'],
                  'a3' : ['./python/output/CHIPA3_Cluster55_Iron55_thr500.root'],
                  'a4' : ['./python/output/CHIPA4_Cluster55_Iron55_thr500.root'],
                  'a5' : ['./python/output/CHIPA5_Cluster55_Iron55_thr500.root'],
                  'a6' : ['./python/output/CHIPA6_Cluster55_Iron55_thr500.root']}

    
    main(root_data)


