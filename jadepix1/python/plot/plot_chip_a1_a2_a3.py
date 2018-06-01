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


def main(a1_source_fname,\
         a2_source_fname,\
         a3_source_fname):

    try:
        #A1
        a1_source_file = ROOT.TFile(a1_source_fname)
        a1_cluster_tree = a1_source_file.Get('Cluster_Tree')
        a1_cluster_entries = a1_cluster_tree.GetEntries()
        #a1_cluster_entries = 200000

        #A2
        a2_source_file = ROOT.TFile(a2_source_fname)
        a2_cluster_tree = a2_source_file.Get('Cluster_Tree')
        a2_cluster_entries = a2_cluster_tree.GetEntries()
        #a2_cluster_entries = 200000

        #A3
        a3_source_file = ROOT.TFile(a3_source_fname)
        a3_cluster_tree = a3_source_file.Get('Cluster_Tree')
        a3_cluster_entries = a3_cluster_tree.GetEntries()
        #a3_cluster_entries = 200000


    except:
        logging.error('input file is invalid!')
        sys.exit()

    #def cluster hist
    cluster_canvas = ROOT.TCanvas('cluster_canvas','cluster_signal',200,10,2400,1600)
    cluster_legend = ROOT.TLegend(0.62,0.6,0.82,0.85)
    cluster_legend.SetBorderSize(0)
    cluster_legend.SetTextSize(0.03)

    cluster_bin_number = 2000

    a1_cluster_hist = ROOT.TH1F('a1 cluster signal','',cluster_bin_number,0,6000)
    a1_cluster_hist.GetXaxis().SetTitle('ADC')
    a1_cluster_hist.GetXaxis().CenterTitle()
    a1_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_cluster_hist.GetYaxis().CenterTitle()
    a1_cluster_hist.SetLineColor(2)
    a1_cluster_hist.SetLineWidth(1)

    a2_cluster_hist = ROOT.TH1F('a2 cluster signal','',cluster_bin_number,0,6000)
    a2_cluster_hist.GetXaxis().SetTitle('ADC')
    a2_cluster_hist.GetXaxis().CenterTitle()
    a2_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_cluster_hist.GetYaxis().CenterTitle()
    a2_cluster_hist.SetLineColor(3)
    a2_cluster_hist.SetLineWidth(1)

    a3_cluster_hist = ROOT.TH1F('a3 cluster signal','',cluster_bin_number,0,6000)
    a3_cluster_hist.GetXaxis().SetTitle('ADC')
    a3_cluster_hist.GetXaxis().CenterTitle()
    a3_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_cluster_hist.GetYaxis().CenterTitle()
    a3_cluster_hist.SetLineColor(4)
    a3_cluster_hist.SetLineWidth(1)

       
    #def seed hist
    seed_canvas = ROOT.TCanvas('seed_canvas','seed_signal',200,10,2400,1600)
    seed_legend = ROOT.TLegend(0.62,0.6,0.82,0.85)
    seed_legend.SetBorderSize(0)
    seed_legend.SetTextSize(0.03)

    seed_bin_number = 1000

    a1_seed_hist = ROOT.TH1F('a1 seed signal','',seed_bin_number,0,6000)
    a1_seed_hist.GetXaxis().SetTitle('ADC')
    a1_seed_hist.GetXaxis().CenterTitle()
    a1_seed_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_seed_hist.GetYaxis().CenterTitle()
    a1_seed_hist.SetLineColor(2)
    a1_seed_hist.SetLineWidth(1)

    a2_seed_hist = ROOT.TH1F('a2 seed signal','',seed_bin_number,0,6000)
    a2_seed_hist.GetXaxis().SetTitle('ADC')
    a2_seed_hist.GetXaxis().CenterTitle()
    a2_seed_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_seed_hist.GetYaxis().CenterTitle()
    a2_seed_hist.SetLineColor(3)
    a2_seed_hist.SetLineWidth(1)

    a3_seed_hist = ROOT.TH1F('a3 seed signal','',seed_bin_number,0,6000)
    a3_seed_hist.GetXaxis().SetTitle('ADC')
    a3_seed_hist.GetXaxis().CenterTitle()
    a3_seed_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_seed_hist.GetYaxis().CenterTitle()
    a3_seed_hist.SetLineColor(4)
    a3_seed_hist.SetLineWidth(1)


    #def size hist
    size_canvas = ROOT.TCanvas('size_canvas','size_signal',200,10,2400,1600)
    size_legend = ROOT.TLegend(0.62,0.6,0.82,0.85)
    size_legend.SetBorderSize(0)
    size_legend.SetTextSize(0.03)

    a1_size_hist = ROOT.TH1F('a1 size distribution','',25,0,25)
    a1_size_hist.GetXaxis().SetTitle('Size')
    a1_size_hist.GetXaxis().CenterTitle()
    a1_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_size_hist.GetYaxis().CenterTitle()
    a1_size_hist.SetLineColor(2)
    #a1_size_hist.SetLineStyle(1)
    a1_size_hist.SetLineWidth(1)

    a2_size_hist = ROOT.TH1F('a2 size distribution','',25,0,25)
    a2_size_hist.GetXaxis().SetTitle('Size')
    a2_size_hist.GetXaxis().CenterTitle()
    a2_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_size_hist.GetYaxis().CenterTitle()
    a2_size_hist.SetLineColor(3)
    #a2_size_hist.SetLineStyle(2)
    a2_size_hist.SetLineWidth(1)

    a3_size_hist = ROOT.TH1F('a3 size distribution','',25,0,25)
    a3_size_hist.GetXaxis().SetTitle('Size')
    a3_size_hist.GetXaxis().CenterTitle()
    a3_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_size_hist.GetYaxis().CenterTitle()
    a3_size_hist.SetLineColor(4)
    #a3_size_hist.SetLineStyle(7)
    a3_size_hist.SetLineWidth(1)

  
    for a1_cluster_entry in xrange(a1_cluster_entries):
        a1_cluster_tree.GetEntry(a1_cluster_entry)
        a1_cluster_hist.Fill(a1_cluster_tree.TotalClusterSignal)
        a1_seed_hist.Fill(a1_cluster_tree.SeedSignal)
        a1_size_hist.Fill(a1_cluster_tree.Size)
    a1_cluster_hist.Scale(1/a1_cluster_hist.Integral())
    a1_seed_hist.Scale(1/a1_seed_hist.Integral())
    a1_size_hist.Scale(1/a1_size_hist.Integral())
    a1_size_hist.GetYaxis().SetRangeUser(0,1)

    for a2_cluster_entry in xrange(a2_cluster_entries):
        a2_cluster_tree.GetEntry(a2_cluster_entry)
        a2_cluster_hist.Fill(a2_cluster_tree.TotalClusterSignal)
        a2_seed_hist.Fill(a2_cluster_tree.SeedSignal)
        a2_size_hist.Fill(a2_cluster_tree.Size)
    a2_cluster_hist.Scale(1/a2_cluster_hist.Integral())
    a2_seed_hist.Scale(1/a2_seed_hist.Integral())
    a2_size_hist.Scale(1/a2_size_hist.Integral())
    a2_size_hist.GetYaxis().SetRangeUser(0,1)

    for a3_cluster_entry in xrange(a3_cluster_entries):
        a3_cluster_tree.GetEntry(a3_cluster_entry)
        a3_cluster_hist.Fill(a3_cluster_tree.TotalClusterSignal)
        a3_seed_hist.Fill(a3_cluster_tree.SeedSignal)
        a3_size_hist.Fill(a3_cluster_tree.Size)
    a3_cluster_hist.Scale(1/a3_cluster_hist.Integral())
    a3_seed_hist.Scale(1/a3_seed_hist.Integral())
    a3_size_hist.Scale(1/a3_size_hist.Integral())
    a3_size_hist.GetYaxis().SetRangeUser(0,1)

    cluster_legend.AddEntry(a1_cluster_hist,'A1 : 5 #times 5 cluster signal ')
    cluster_legend.AddEntry(a2_cluster_hist,'A2 : 5 #times 5 cluster signal ')
    cluster_legend.AddEntry(a3_cluster_hist,'A3 : 5 #times 5 cluster signal ')

    seed_legend.AddEntry(a1_seed_hist,'A1 : 5 #times 5 seed signal ')
    seed_legend.AddEntry(a2_seed_hist,'A2 : 5 #times 5 seed signal ')
    seed_legend.AddEntry(a3_seed_hist,'A3 : 5 #times 5 seed signal ')

    size_legend.AddEntry(a1_size_hist,'A1 : 5 #times 5 size distribution ')
    size_legend.AddEntry(a2_size_hist,'A2 : 5 #times 5 size distribution ')
    size_legend.AddEntry(a3_size_hist,'A3 : 5 #times 5 size distribution ')

    if not os.path.exists('./python/fig/'):
        os.makedirs('./python/fig/')

    cluster_canvas.cd()
    a3_cluster_hist.Draw('hist')
    a2_cluster_hist.Draw('hist same')
    a1_cluster_hist.Draw('hist same')
    cluster_legend.Draw()
    cluster_canvas.Update()
    cluster_canvas.SaveAs('./python/fig/Iron55_Cluster55_123.pdf')

    seed_canvas.cd()
    a3_seed_hist.Draw('hist')
    a2_seed_hist.Draw('hist same')
    a1_seed_hist.Draw('hist same')
    seed_legend.Draw()
    seed_canvas.Update()
    seed_canvas.SaveAs('./python/fig/Iron55_Seed_123.pdf')

    size_canvas.cd()
    a3_size_hist.Draw('hist')
    a2_size_hist.Draw('hist same')
    a1_size_hist.Draw('hist same')
    size_legend.Draw()
    size_canvas.Update()
    size_canvas.SaveAs('./python/fig/Iron55_Size_123.pdf')



if __name__ == '__main__':
    
    main('./python/output/CHIPA1_Cluster55_Iron55_thr500.root',\
         './python/output/CHIPA2_Cluster55_Iron55_thr500.root',\
         './python/output/CHIPA3_Cluster55_Iron55_thr500.root')


