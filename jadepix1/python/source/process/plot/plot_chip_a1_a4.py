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


def main(a1_source_fname,a1_noise_fname,a4_source_fname,a4_noise_fname):
    try:
        #A1
        a1_source_file = ROOT.TFile(a1_source_fname)
        a1_cluster_tree = a1_source_file.Get('Cluster_Tree')
        #a1_cluster_entries = a1_cluster_tree.GetEntries()
        a1_cluster_entries = 200000

        a1_noise_file = ROOT.TFile(a1_noise_fname)
        a1_noise_tree = a1_noise_file.Get('Cluster_Tree')
        #a1_cluster_entries = a1_cluster_tree.GetEntries()
        a1_noise_entries = 200000

        #A4
        a4_source_file = ROOT.TFile(a4_source_fname)
        a4_cluster_tree = a4_source_file.Get('Cluster_Tree')
        #a4_cluster_entries = a4_cluster_tree.GetEntries()
        a4_cluster_entries = 200000

        a4_noise_file = ROOT.TFile(a4_noise_fname)
        a4_noise_tree = a4_noise_file.Get('Cluster_Tree')
        #a4_cluster_entries = a4_cluster_tree.GetEntries()
        a4_noise_entries = 200000
  

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,2400,1200)
    legend = ROOT.TLegend(0.55,0.7,0.86,0.85)
    legend.SetNColumns(2)
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


    for a1_cluster_entry in xrange(a1_cluster_entries):
        a1_cluster_tree.GetEntry(a1_cluster_entry)
        if (a1_cluster_tree.Seed_Channel >= 2) and (a1_cluster_tree.Seed_Channel <= 13) and (a1_cluster_tree.Seed_Row >= 2) and (a1_cluster_tree.Seed_Row <= 45) :
            a1_cluster_hist.Fill(a1_cluster_tree.ClusterSignal)
    a1_source_peak = a1_cluster_hist.GetMaximumBin()
    a1_cluster_hist.Scale(1/a1_cluster_hist.Integral())

    for a1_noise_entry in xrange(a1_noise_entries):
        a1_noise_tree.GetEntry(a1_noise_entry)
        a1_noise_hist.Fill(a1_noise_tree.ClusterSignal)
    a1_noise_peak = a1_noise_hist.GetMaximumBin()
    a1_noise_hist.Scale(1/a1_noise_hist.Integral())


    for a4_cluster_entry in xrange(a4_cluster_entries):
        a4_cluster_tree.GetEntry(a4_cluster_entry)
        if (a4_cluster_tree.Seed_Channel >= 2) and (a4_cluster_tree.Seed_Channel <= 13) and (a4_cluster_tree.Seed_Row >= 2) and (a4_cluster_tree.Seed_Row <= 45) :
            a4_cluster_hist.Fill(a4_cluster_tree.ClusterSignal)
    a4_source_peak = a4_cluster_hist.GetMaximumBin() 
    a4_cluster_hist.Scale(1/a4_cluster_hist.Integral())

    for a4_noise_entry in xrange(a4_noise_entries):
        a4_noise_tree.GetEntry(a4_noise_entry)
        a4_noise_hist.Fill(a4_noise_tree.ClusterSignal)
    a4_noise_peak = a4_noise_hist.GetMaximumBin()
    a4_noise_hist.Scale(1/a4_noise_hist.Integral())

    print('a1 source peak : ',a1_source_peak*10)
    print('a1 noise peak : ',a1_noise_peak*10)

    print('a4 source peak : ',a4_source_peak*10)
    print('a4 noise peak : ',a4_noise_peak*10)

    legend.AddEntry(a1_cluster_hist,'A1 : 5 #times 5 cluster signal ')
    legend.AddEntry(a1_noise_hist,'A1 : 5 #times 5 noise signal')

    legend.AddEntry(a4_cluster_hist,'A4 : 5 #times 5 cluster signal ')
    legend.AddEntry(a4_noise_hist,'A4 : 5 #times 5 noise signal')

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    a1_noise_hist.Draw('hist same')
    a4_noise_hist.Draw('hist same')
    a4_cluster_hist.Draw('hist same')
    a1_cluster_hist.Draw('hist same')
    legend.Draw()
    canvas.Update()
    canvas.SaveAs('../fig/iron55_cluster55_14_scale.gif')


if __name__ == '__main__':
    
    main('../output/CHIPA1_Cluster55_Iron55_thr500.root','../output/CHIPA1_noise_55.root','../output/CHIPA4_Cluster55_Iron55_thr500.root','../output/CHIPA4_noise_55.root')


