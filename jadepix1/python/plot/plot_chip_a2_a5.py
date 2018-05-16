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


def main(a2_source_fname,a2_noise_fname,a5_source_fname,a5_noise_fname):
    try:
        #A2
        a2_source_file = ROOT.TFile(a2_source_fname)
        a2_cluster_tree = a2_source_file.Get('Cluster_Tree')
        #a2_cluster_entries = a2_cluster_tree.GetEntries()
        a2_cluster_entries = 200000

        a2_noise_file = ROOT.TFile(a2_noise_fname)
        a2_noise_tree = a2_noise_file.Get('Cluster_Tree')
        #a2_cluster_entries = a2_cluster_tree.GetEntries()
        a2_noise_entries = 200000

        #A5
        a5_source_file = ROOT.TFile(a5_source_fname)
        a5_cluster_tree = a5_source_file.Get('Cluster_Tree')
        #a5_cluster_entries = a5_cluster_tree.GetEntries()
        a5_cluster_entries = 200000

        a5_noise_file = ROOT.TFile(a5_noise_fname)
        a5_noise_tree = a5_noise_file.Get('Cluster_Tree')
        #a5_cluster_entries = a5_cluster_tree.GetEntries()
        a5_noise_entries = 200000
  

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,2400,1200)
    legend = ROOT.TLegend(0.55,0.7,0.86,0.85)
    legend.SetNColumns(2)
    #legend.SetBorderSize(0)

    bin_number = 600

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


    for a2_cluster_entry in xrange(a2_cluster_entries):
        a2_cluster_tree.GetEntry(a2_cluster_entry)
        if (a2_cluster_tree.Seed_Channel >= 2) and (a2_cluster_tree.Seed_Channel <= 13) and (a2_cluster_tree.Seed_Row >= 2) and (a2_cluster_tree.Seed_Row <= 45) :
            a2_cluster_hist.Fill(a2_cluster_tree.ClusterSignal)
    a2_source_peak = a2_cluster_hist.GetMaximumBin()
    a2_cluster_hist.Scale(1/a2_cluster_hist.Integral())

    for a2_noise_entry in xrange(a2_noise_entries):
        a2_noise_tree.GetEntry(a2_noise_entry)
        a2_noise_hist.Fill(a2_noise_tree.ClusterSignal)
    a2_noise_peak = a2_noise_hist.GetMaximumBin()
    a2_noise_hist.Scale(1/a2_noise_hist.Integral())


    for a5_cluster_entry in xrange(a5_cluster_entries):
        a5_cluster_tree.GetEntry(a5_cluster_entry)
        if (a5_cluster_tree.Seed_Channel >= 2) and (a5_cluster_tree.Seed_Channel <= 13) and (a5_cluster_tree.Seed_Row >= 2) and (a5_cluster_tree.Seed_Row <= 45) :
            a5_cluster_hist.Fill(a5_cluster_tree.ClusterSignal)
    a5_source_peak = a5_cluster_hist.GetMaximumBin() 
    a5_cluster_hist.Scale(1/a5_cluster_hist.Integral())

    for a5_noise_entry in xrange(a5_noise_entries):
        a5_noise_tree.GetEntry(a5_noise_entry)
        a5_noise_hist.Fill(a5_noise_tree.ClusterSignal)
    a5_noise_peak = a5_noise_hist.GetMaximumBin()
    a5_noise_hist.Scale(1/a5_noise_hist.Integral())

    print('a2 source peak : ',a2_source_peak*10)
    print('a2 noise peak : ',a2_noise_peak*10)

    print('a5 source peak : ',a5_source_peak*10)
    print('a5 noise peak : ',a5_noise_peak*10)

    legend.AddEntry(a2_cluster_hist,'A2 : 5 #times 5 cluster signal ')
    legend.AddEntry(a2_noise_hist,'A2 : 5 #times 5 noise signal')

    legend.AddEntry(a5_cluster_hist,'A5 : 5 #times 5 cluster signal ')
    legend.AddEntry(a5_noise_hist,'A5 : 5 #times 5 noise signal')

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    a5_noise_hist.Draw('hist same')
    a2_noise_hist.Draw('hist same')
    a5_cluster_hist.Draw('hist same')
    a2_cluster_hist.Draw('hist same')
    legend.Draw()
    canvas.Update()
    canvas.SaveAs('../fig/iron55_cluster55_25_scale.gif')


if __name__ == '__main__':
    
    main('../output/CHIPA2_Cluster55_Iron55_thr500.root','../output/CHIPA2_noise_55.root','../output/CHIPA5_Cluster55_Iron55_thr500.root','../output/CHIPA5_noise_55.root')


