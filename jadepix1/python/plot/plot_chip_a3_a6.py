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


def main(a3_source_fname,a3_noise_fname,a6_source_fname,a6_noise_fname):
    try:
        #A3
        a3_source_file = ROOT.TFile(a3_source_fname)
        a3_cluster_tree = a3_source_file.Get('Cluster_Tree')
        #a3_cluster_entries = a3_cluster_tree.GetEntries()
        a3_cluster_entries = 200000

        a3_noise_file = ROOT.TFile(a3_noise_fname)
        a3_noise_tree = a3_noise_file.Get('Cluster_Tree')
        #a3_cluster_entries = a3_cluster_tree.GetEntries()
        a3_noise_entries = 200000

        #A6
        a6_source_file = ROOT.TFile(a6_source_fname)
        a6_cluster_tree = a6_source_file.Get('Cluster_Tree')
        #a6_cluster_entries = a6_cluster_tree.GetEntries()
        a6_cluster_entries = 200000

        a6_noise_file = ROOT.TFile(a6_noise_fname)
        a6_noise_tree = a6_noise_file.Get('Cluster_Tree')
        #a6_cluster_entries = a6_cluster_tree.GetEntries()
        a6_noise_entries = 200000
  

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,2400,1200)
    legend = ROOT.TLegend(0.55,0.7,0.86,0.85)
    legend.SetNColumns(2)
    #legend.SetBorderSize(0)

    bin_number = 600

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


    for a3_cluster_entry in xrange(a3_cluster_entries):
        a3_cluster_tree.GetEntry(a3_cluster_entry)
        if (a3_cluster_tree.Seed_Channel >= 2) and (a3_cluster_tree.Seed_Channel <= 13) and (a3_cluster_tree.Seed_Row >= 2) and (a3_cluster_tree.Seed_Row <= 45) :
            a3_cluster_hist.Fill(a3_cluster_tree.ClusterSignal)
    a3_source_peak = a3_cluster_hist.GetMaximumBin()
    a3_cluster_hist.Scale(1/a3_cluster_hist.Integral())

    for a3_noise_entry in xrange(a3_noise_entries):
        a3_noise_tree.GetEntry(a3_noise_entry)
        a3_noise_hist.Fill(a3_noise_tree.ClusterSignal)
    a3_noise_peak = a3_noise_hist.GetMaximumBin()
    a3_noise_hist.Scale(1/a3_noise_hist.Integral())


    for a6_cluster_entry in xrange(a6_cluster_entries):
        a6_cluster_tree.GetEntry(a6_cluster_entry)
        if (a6_cluster_tree.Seed_Channel >= 2) and (a6_cluster_tree.Seed_Channel <= 13) and (a6_cluster_tree.Seed_Row >= 2) and (a6_cluster_tree.Seed_Row <= 45) :
            a6_cluster_hist.Fill(a6_cluster_tree.ClusterSignal)
    a6_source_peak = a6_cluster_hist.GetMaximumBin() 
    a6_cluster_hist.Scale(1/a6_cluster_hist.Integral())

    for a6_noise_entry in xrange(a6_noise_entries):
        a6_noise_tree.GetEntry(a6_noise_entry)
        a6_noise_hist.Fill(a6_noise_tree.ClusterSignal)
    a6_noise_peak = a6_noise_hist.GetMaximumBin()
    a6_noise_hist.Scale(1/a6_noise_hist.Integral())

    print('a3 source peak : ',a3_source_peak*10)
    print('a3 noise peak : ',a3_noise_peak*10)
    print('a6 source peak : ',a6_source_peak*10)
    print('a6 noise peak : ',a6_noise_peak*10)

    legend.AddEntry(a3_cluster_hist,'A3 : 5 #times 5 cluster signal ')
    legend.AddEntry(a3_noise_hist,'A3 : 5 #times 5 noise signal')

    legend.AddEntry(a6_cluster_hist,'A6 : 5 #times 5 cluster signal ')
    legend.AddEntry(a6_noise_hist,'A6 : 5 #times 5 noise signal')

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    a6_noise_hist.Draw('hist same')
    a3_noise_hist.Draw('hist same')
    a6_cluster_hist.Draw('hist same')
    a3_cluster_hist.Draw('hist same')
    legend.Draw()
    canvas.Update()
    canvas.SaveAs('../fig/iron55_cluster55_36_scale.gif')


if __name__ == '__main__':
    
    main('../output/CHIPA3_Cluster55_Iron55_thr500.root','../output/CHIPA3_noise_55.root','../output/CHIPA6_Cluster55_Iron55_thr500.root','../output/CHIPA6_noise_55.root')


