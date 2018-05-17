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


def main(a4_source_fname,a4_noise_fname,\
         a5_source_fname,a5_noise_fname,\
         a6_source_fname,a6_noise_fname):

    try:
        #A4
        a4_source_file = ROOT.TFile(a4_source_fname)
        a4_cluster_tree = a4_source_file.Get('Cluster_Tree')
        a4_cluster_entries = a4_cluster_tree.GetEntries()
        #a4_cluster_entries = 200000

        a4_noise_file = ROOT.TFile(a4_noise_fname)
        a4_noise_tree = a4_noise_file.Get('Cluster_Tree')
        a4_noise_entries = a4_cluster_tree.GetEntries()
        #a4_noise_entries = 200000

        #A5
        a5_source_file = ROOT.TFile(a5_source_fname)
        a5_cluster_tree = a5_source_file.Get('Cluster_Tree')
        a5_cluster_entries = a5_cluster_tree.GetEntries()
        #a5_cluster_entries = 200000

        a5_noise_file = ROOT.TFile(a5_noise_fname)
        a5_noise_tree = a5_noise_file.Get('Cluster_Tree')
        a5_noise_entries = a5_cluster_tree.GetEntries()
        #a5_noise_entries = 200000

        #A6
        a6_source_file = ROOT.TFile(a6_source_fname)
        a6_cluster_tree = a6_source_file.Get('Cluster_Tree')
        a6_cluster_entries = a6_cluster_tree.GetEntries()
        #a6_cluster_entries = 200000

        a6_noise_file = ROOT.TFile(a6_noise_fname)
        a6_noise_tree = a6_noise_file.Get('Cluster_Tree')
        a6_noise_entries = a6_cluster_tree.GetEntries()
        #a6_noise_entries = 200000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,2400,1200)
    legend = ROOT.TLegend(0.65,0.6,0.85,0.85)
    #legend.SetNColumns(2)
    #legend.SetBorderSize(0)

    bin_number = 600

    a4_cluster_hist = ROOT.TH1F('a4 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a4_cluster_hist.GetXaxis().SetTitle('ADC')
    a4_cluster_hist.GetXaxis().CenterTitle()
    a4_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_cluster_hist.GetYaxis().CenterTitle()
    a4_cluster_hist.SetLineColor(6)
    a4_cluster_hist.SetLineWidth(2)

    a4_noise_hist = ROOT.TH1F('a4 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a4_noise_hist.GetXaxis().SetTitle('ADC')
    a4_noise_hist.GetXaxis().CenterTitle()
    a4_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_noise_hist.GetYaxis().CenterTitle()
    a4_noise_hist.SetLineColor(6)
    a4_noise_hist.SetLineStyle(9)
    a4_noise_hist.SetLineWidth(2)


    a5_cluster_hist = ROOT.TH1F('a5 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a5_cluster_hist.GetXaxis().SetTitle('ADC')
    a5_cluster_hist.GetXaxis().CenterTitle()
    a5_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_cluster_hist.GetYaxis().CenterTitle()
    a5_cluster_hist.SetLineColor(7)
    a5_cluster_hist.SetLineWidth(2)

    a5_noise_hist = ROOT.TH1F('a5 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a5_noise_hist.GetXaxis().SetTitle('ADC')
    a5_noise_hist.GetXaxis().CenterTitle()
    a5_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_noise_hist.GetYaxis().CenterTitle()
    a5_noise_hist.SetLineColor(7)
    a5_noise_hist.SetLineStyle(9)
    a5_noise_hist.SetLineWidth(2)


    a6_cluster_hist = ROOT.TH1F('a6 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a6_cluster_hist.GetXaxis().SetTitle('ADC')
    a6_cluster_hist.GetXaxis().CenterTitle()
    a6_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_cluster_hist.GetYaxis().CenterTitle()
    a6_cluster_hist.SetLineColor(8)
    a6_cluster_hist.SetLineWidth(2)

    a6_noise_hist = ROOT.TH1F('a6 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a6_noise_hist.GetXaxis().SetTitle('ADC')
    a6_noise_hist.GetXaxis().CenterTitle()
    a6_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_noise_hist.GetYaxis().CenterTitle()
    a6_noise_hist.SetLineColor(8)
    a6_noise_hist.SetLineStyle(9)
    a6_noise_hist.SetLineWidth(2)

    a4_peak_adc = 0
    a5_peak_adc = 0
    a5_peak_adc = 0
 

    for a4_cluster_entry in xrange(a4_cluster_entries):
        a4_cluster_tree.GetEntry(a4_cluster_entry)
        a4_cluster_hist.Fill(a4_cluster_tree.TotalClusterSignal)
    a4_peak_adc = a4_cluster_hist.GetMaximumBin()
    a4_cluster_hist.Scale(1/a4_cluster_hist.Integral())

    for a4_noise_entry in xrange(a4_noise_entries):
        a4_noise_tree.GetEntry(a4_noise_entry)
        a4_noise_hist.Fill(a4_noise_tree.ClusterSignal)
    a4_noise_hist.Scale(1/a4_noise_hist.Integral())


    for a5_cluster_entry in xrange(a5_cluster_entries):
        a5_cluster_tree.GetEntry(a5_cluster_entry)
        a5_cluster_hist.Fill(a5_cluster_tree.TotalClusterSignal)
    a5_peak_adc = a5_cluster_hist.GetMaximumBin() 
    a5_cluster_hist.Scale(1/a5_cluster_hist.Integral())

    for a5_noise_entry in xrange(a5_noise_entries):
        a5_noise_tree.GetEntry(a5_noise_entry)
        a5_noise_hist.Fill(a5_noise_tree.ClusterSignal)
    a5_noise_hist.Scale(1/a5_noise_hist.Integral())


    for a6_cluster_entry in xrange(a6_cluster_entries):
        a6_cluster_tree.GetEntry(a6_cluster_entry)
        a6_cluster_hist.Fill(a6_cluster_tree.TotalClusterSignal)
    a6_peak_adc = a6_cluster_hist.GetMaximumBin() 
    a6_cluster_hist.Scale(1/a6_cluster_hist.Integral())

    for a6_noise_entry in xrange(a6_noise_entries):
        a6_noise_tree.GetEntry(a6_noise_entry)
        a6_noise_hist.Fill(a6_noise_tree.ClusterSignal)
    a6_noise_hist.Scale(1/a6_noise_hist.Integral())

    legend.AddEntry(a4_cluster_hist,'A4 : 5 #times 5 cluster signal ')
    #legend.AddEntry(a4_noise_hist,'A4 : 5 #times 5 noise signal')

    legend.AddEntry(a5_cluster_hist,'A5 : 5 #times 5 cluster signal ')
    #legend.AddEntry(a5_noise_hist,'A5 : 5 #times 5 noise signal')

    legend.AddEntry(a6_cluster_hist,'A6 : 5 #times 5 cluster signal ')
    #legend.AddEntry(a6_noise_hist,'A6 : 5 #times 5 noise signal')

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    print('a4 peak adc :',a4_peak_adc)
    print('a5 peak adc :',a5_peak_adc)
    print('a6 peak adc :',a6_peak_adc)



    canvas.cd()
    # a6_noise_hist.Draw('hist')
    # a5_noise_hist.Draw('hist same')
    # a4_noise_hist.Draw('hist same')
    a6_cluster_hist.Draw('hist')
    a5_cluster_hist.Draw('hist same')
    a4_cluster_hist.Draw('hist same')
    legend.Draw()
    canvas.Update()
    canvas.SaveAs('../fig/Iron55_Cluster55_456.gif')


if __name__ == '__main__':
    
    main('../output/CHIPA4_Cluster55_Iron55_thr500.root','../output/CHIPA4_noise_55.root','../output/CHIPA5_Cluster55_Iron55_thr500.root','../output/CHIPA5_noise_55.root','../output/CHIPA6_Cluster55_Iron55_thr500.root','../output/CHIPA6_noise_55.root')


