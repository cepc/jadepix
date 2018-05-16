#!/usr/bin/env python

'''
plot Iron55 clusters compare hist
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


def main(a1_source_fname,a1_noise_fname,\
         a2_source_fname,a2_noise_fname,\
         a3_source_fname,a3_noise_fname):

    try:
        #A1
        a1_source_file = ROOT.TFile(a1_source_fname)
        a1_cluster_tree = a1_source_file.Get('Cluster_Tree')
        a1_cluster_entries = a1_cluster_tree.GetEntries()
        #a1_cluster_entries = 200000

        a1_noise_file = ROOT.TFile(a1_noise_fname)
        a1_noise_tree = a1_noise_file.Get('Cluster_Tree')
        a1_noise_entries = a1_cluster_tree.GetEntries()
        #a1_noise_entries = 200000

        #A2
        a2_source_file = ROOT.TFile(a2_source_fname)
        a2_cluster_tree = a2_source_file.Get('Cluster_Tree')
        a2_cluster_entries = a2_cluster_tree.GetEntries()
        #a2_cluster_entries = 200000

        a2_noise_file = ROOT.TFile(a2_noise_fname)
        a2_noise_tree = a2_noise_file.Get('Cluster_Tree')
        a2_noise_entries = a2_cluster_tree.GetEntries()
        #a2_noise_entries = 200000

        #A3
        a3_source_file = ROOT.TFile(a3_source_fname)
        a3_cluster_tree = a3_source_file.Get('Cluster_Tree')
        a3_cluster_entries = a3_cluster_tree.GetEntries()
        #a3_cluster_entries = 200000

        a3_noise_file = ROOT.TFile(a3_noise_fname)
        a3_noise_tree = a3_noise_file.Get('Cluster_Tree')
        a3_noise_entries = a3_cluster_tree.GetEntries()
        #a3_noise_entries = 200000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,2400,1200)
    legend = ROOT.TLegend(0.65,0.6,0.85,0.85)
    #legend.SetNColumns(2)
    #legend.SetBorderSize(0)

    bin_number = 600

    a1_cluster_hist = ROOT.TH1F('a1 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a1_cluster_hist.GetXaxis().SetTitle('ADC')
    a1_cluster_hist.GetXaxis().CenterTitle()
    a1_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_cluster_hist.GetYaxis().CenterTitle()
    a1_cluster_hist.SetLineColor(2)
    a1_cluster_hist.SetLineWidth(2)

    a1_noise_hist = ROOT.TH1F('a1 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a1_noise_hist.GetXaxis().SetTitle('ADC')
    a1_noise_hist.GetXaxis().CenterTitle()
    a1_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_noise_hist.GetYaxis().CenterTitle()
    a1_noise_hist.SetLineColor(2)
    a1_noise_hist.SetLineStyle(9)
    a1_noise_hist.SetLineWidth(2)


    a2_cluster_hist = ROOT.TH1F('a2 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a2_cluster_hist.GetXaxis().SetTitle('ADC')
    a2_cluster_hist.GetXaxis().CenterTitle()
    a2_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_cluster_hist.GetYaxis().CenterTitle()
    a2_cluster_hist.SetLineColor(3)
    a2_cluster_hist.SetLineWidth(2)

    a2_noise_hist = ROOT.TH1F('a2 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a2_noise_hist.GetXaxis().SetTitle('ADC')
    a2_noise_hist.GetXaxis().CenterTitle()
    a2_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_noise_hist.GetYaxis().CenterTitle()
    a2_noise_hist.SetLineColor(3)
    a2_noise_hist.SetLineStyle(9)
    a2_noise_hist.SetLineWidth(2)


    a3_cluster_hist = ROOT.TH1F('a3 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a3_cluster_hist.GetXaxis().SetTitle('ADC')
    a3_cluster_hist.GetXaxis().CenterTitle()
    a3_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_cluster_hist.GetYaxis().CenterTitle()
    a3_cluster_hist.SetLineColor(4)
    a3_cluster_hist.SetLineWidth(2)

    a3_noise_hist = ROOT.TH1F('a3 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a3_noise_hist.GetXaxis().SetTitle('ADC')
    a3_noise_hist.GetXaxis().CenterTitle()
    a3_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_noise_hist.GetYaxis().CenterTitle()
    a3_noise_hist.SetLineColor(4)
    a3_noise_hist.SetLineStyle(9)
    a3_noise_hist.SetLineWidth(2)

    a1_peak_adc = 0
    a2_peak_adc = 0
    a2_peak_adc = 0
 

    for a1_cluster_entry in xrange(a1_cluster_entries):
        a1_cluster_tree.GetEntry(a1_cluster_entry)
        a1_cluster_hist.Fill(a1_cluster_tree.TotalClusterSignal)
    a1_peak_adc = a1_cluster_hist.GetMaximumBin()
    a1_cluster_hist.Scale(1/a1_cluster_hist.Integral())

    for a1_noise_entry in xrange(a1_noise_entries):
        a1_noise_tree.GetEntry(a1_noise_entry)
        a1_noise_hist.Fill(a1_noise_tree.ClusterSignal)
    a1_noise_hist.Scale(1/a1_noise_hist.Integral())


    for a2_cluster_entry in xrange(a2_cluster_entries):
        a2_cluster_tree.GetEntry(a2_cluster_entry)
        a2_cluster_hist.Fill(a2_cluster_tree.TotalClusterSignal)
    a2_peak_adc = a2_cluster_hist.GetMaximumBin() 
    a2_cluster_hist.Scale(1/a2_cluster_hist.Integral())

    for a2_noise_entry in xrange(a2_noise_entries):
        a2_noise_tree.GetEntry(a2_noise_entry)
        a2_noise_hist.Fill(a2_noise_tree.ClusterSignal)
    a2_noise_hist.Scale(1/a2_noise_hist.Integral())


    for a3_cluster_entry in xrange(a3_cluster_entries):
        a3_cluster_tree.GetEntry(a3_cluster_entry)
        a3_cluster_hist.Fill(a3_cluster_tree.TotalClusterSignal)
    a3_peak_adc = a3_cluster_hist.GetMaximumBin() 
    a3_cluster_hist.Scale(1/a3_cluster_hist.Integral())

    for a3_noise_entry in xrange(a3_noise_entries):
        a3_noise_tree.GetEntry(a3_noise_entry)
        a3_noise_hist.Fill(a3_noise_tree.ClusterSignal)
    a3_noise_hist.Scale(1/a3_noise_hist.Integral())

    legend.AddEntry(a1_cluster_hist,'A1 : 5 #times 5 cluster signal ')
    #legend.AddEntry(a1_noise_hist,'A1 : 5 #times 5 noise signal')

    legend.AddEntry(a2_cluster_hist,'A2 : 5 #times 5 cluster signal ')
    #legend.AddEntry(a2_noise_hist,'A2 : 5 #times 5 noise signal')

    legend.AddEntry(a3_cluster_hist,'A3 : 5 #times 5 cluster signal ')
    #legend.AddEntry(a3_noise_hist,'A3 : 5 #times 5 noise signal')

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    print('a1_peak_adc : ',a1_peak_adc)
    print('a2_peak_adc : ',a2_peak_adc)
    print('a3_peak_adc : ',a3_peak_adc)


    canvas.cd()
    # a3_noise_hist.Draw('hist')
    # a2_noise_hist.Draw('hist same')
    # a1_noise_hist.Draw('hist same')
    a3_cluster_hist.Draw('hist')
    a2_cluster_hist.Draw('hist same')
    a1_cluster_hist.Draw('hist same')
    legend.Draw()
    canvas.Update()
    canvas.SaveAs('../fig/Iron55_Cluster55_123.gif')



if __name__ == '__main__':
    
    main('../output/CHIPA1_Cluster55_Iron55_thr500.root','../output/CHIPA1_noise_55.root','../output/CHIPA2_Cluster55_Iron55_thr500.root','../output/CHIPA2_noise_55.root','../output/CHIPA3_Cluster55_Iron55_thr500.root','../output/CHIPA3_noise_55.root')


