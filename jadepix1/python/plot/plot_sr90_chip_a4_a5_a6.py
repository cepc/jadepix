#!/usr/bin/env python

'''
plot Sr90 clusters compare hist
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


def main(a4_source_fname,\
         a5_source_fname,\
         a6_source_fname):

    try:
        #A4
        a4_source_file = ROOT.TFile(a4_source_fname)
        a4_cluster_tree = a4_source_file.Get('Cluster_Tree')
        a4_cluster_entries = a4_cluster_tree.GetEntries()
        #a4_cluster_entries = 200000

        #A5
        a5_source_file = ROOT.TFile(a5_source_fname)
        a5_cluster_tree = a5_source_file.Get('Cluster_Tree')
        a5_cluster_entries = a5_cluster_tree.GetEntries()
        #a5_cluster_entries = 200000

        #A6
        a6_source_file = ROOT.TFile(a6_source_fname)
        a6_cluster_tree = a6_source_file.Get('Cluster_Tree')
        a6_cluster_entries = a6_cluster_tree.GetEntries()
        #a6_cluster_entries = 200000


    except:
        logging.error('input file is invalid!')
        sys.exit()

    #def cluster hist
    cluster_canvas = ROOT.TCanvas('cluster_canvas','cluster_signal',200,10,2400,1600)
    cluster_legend = ROOT.TLegend(0.62,0.6,0.82,0.85)
    cluster_legend.SetBorderSize(0)
    cluster_legend.SetTextSize(0.03)

    cluster_bin_number = 300

    a4_cluster_hist = ROOT.TH1F('a4 cluster signal','',cluster_bin_number,0,30000)
    a4_cluster_hist.GetXaxis().SetTitle('ADC')
    a4_cluster_hist.GetXaxis().CenterTitle()
    a4_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_cluster_hist.GetYaxis().CenterTitle()
    a4_cluster_hist.SetLineColor(6)
    a4_cluster_hist.SetLineWidth(1)

    a5_cluster_hist = ROOT.TH1F('a5 cluster signal','',cluster_bin_number,0,30000)
    a5_cluster_hist.GetXaxis().SetTitle('ADC')
    a5_cluster_hist.GetXaxis().CenterTitle()
    a5_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_cluster_hist.GetYaxis().CenterTitle()
    a5_cluster_hist.SetLineColor(7)
    a5_cluster_hist.SetLineWidth(1)

    a6_cluster_hist = ROOT.TH1F('a6 cluster signal','',cluster_bin_number,0,30000)
    a6_cluster_hist.GetXaxis().SetTitle('ADC')
    a6_cluster_hist.GetXaxis().CenterTitle()
    a6_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_cluster_hist.GetYaxis().CenterTitle()
    a6_cluster_hist.SetLineColor(8)
    a6_cluster_hist.SetLineWidth(1)

       
    #def seed hist
    seed_canvas = ROOT.TCanvas('seed_canvas','seed_signal',200,10,2400,1600)
    seed_legend = ROOT.TLegend(0.62,0.6,0.82,0.85)
    seed_legend.SetBorderSize(0)
    seed_legend.SetTextSize(0.03)

    seed_bin_number = 300

    a4_seed_hist = ROOT.TH1F('a4 seed signal','',seed_bin_number,0,30000)
    a4_seed_hist.GetXaxis().SetTitle('ADC')
    a4_seed_hist.GetXaxis().CenterTitle()
    a4_seed_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_seed_hist.GetYaxis().CenterTitle()
    a4_seed_hist.SetLineColor(6)
    a4_seed_hist.SetLineWidth(1)

    a5_seed_hist = ROOT.TH1F('a5 seed signal','',seed_bin_number,0,30000)
    a5_seed_hist.GetXaxis().SetTitle('ADC')
    a5_seed_hist.GetXaxis().CenterTitle()
    a5_seed_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_seed_hist.GetYaxis().CenterTitle()
    a5_seed_hist.SetLineColor(7)
    a5_seed_hist.SetLineWidth(1)

    a6_seed_hist = ROOT.TH1F('a6 seed signal','',seed_bin_number,0,30000)
    a6_seed_hist.GetXaxis().SetTitle('ADC')
    a6_seed_hist.GetXaxis().CenterTitle()
    a6_seed_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_seed_hist.GetYaxis().CenterTitle()
    a6_seed_hist.SetLineColor(8)
    a6_seed_hist.SetLineWidth(1)


    #def size hist
    size_canvas = ROOT.TCanvas('size_canvas','size_signal',200,10,2400,1600)
    size_legend = ROOT.TLegend(0.62,0.6,0.82,0.85)
    size_legend.SetBorderSize(0)
    size_legend.SetTextSize(0.03)

    a4_size_hist = ROOT.TH1F('a4 size distribution','',25,0,25)
    a4_size_hist.GetXaxis().SetTitle('Size')
    a4_size_hist.GetXaxis().CenterTitle()
    a4_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_size_hist.GetYaxis().CenterTitle()
    a4_size_hist.SetLineColor(6)
    #a4_size_hist.SetLineStyle(1)
    a4_size_hist.SetLineWidth(1)

    a5_size_hist = ROOT.TH1F('a5 size distribution','',25,0,25)
    a5_size_hist.GetXaxis().SetTitle('Size')
    a5_size_hist.GetXaxis().CenterTitle()
    a5_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_size_hist.GetYaxis().CenterTitle()
    a5_size_hist.SetLineColor(7)
    #a5_size_hist.SetLineStyle(2)
    a5_size_hist.SetLineWidth(1)

    a6_size_hist = ROOT.TH1F('a6 size distribution','',25,0,25)
    a6_size_hist.GetXaxis().SetTitle('Size')
    a6_size_hist.GetXaxis().CenterTitle()
    a6_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_size_hist.GetYaxis().CenterTitle()
    a6_size_hist.SetLineColor(8)
    #a6_size_hist.SetLineStyle(7)
    a6_size_hist.SetLineWidth(1)

  
    for a4_cluster_entry in xrange(a4_cluster_entries):
        a4_cluster_tree.GetEntry(a4_cluster_entry)
        a4_cluster_hist.Fill(a4_cluster_tree.TotalClusterSignal)
        a4_seed_hist.Fill(a4_cluster_tree.SeedSignal)
        a4_size_hist.Fill(a4_cluster_tree.Size)
    a4_cluster_hist.Scale(1/a4_cluster_hist.Integral())
    a4_seed_hist.Scale(1/a4_seed_hist.Integral())
    a4_size_hist.Scale(1/a4_size_hist.Integral())
    a4_size_hist.GetYaxis().SetRangeUser(0,1)

    for a5_cluster_entry in xrange(a5_cluster_entries):
        a5_cluster_tree.GetEntry(a5_cluster_entry)
        a5_cluster_hist.Fill(a5_cluster_tree.TotalClusterSignal)
        a5_seed_hist.Fill(a5_cluster_tree.SeedSignal)
        a5_size_hist.Fill(a5_cluster_tree.Size)
    a5_cluster_hist.Scale(1/a5_cluster_hist.Integral())
    a5_seed_hist.Scale(1/a5_seed_hist.Integral())
    a5_size_hist.Scale(1/a5_size_hist.Integral())
    a5_size_hist.GetYaxis().SetRangeUser(0,1)

    for a6_cluster_entry in xrange(a6_cluster_entries):
        a6_cluster_tree.GetEntry(a6_cluster_entry)
        a6_cluster_hist.Fill(a6_cluster_tree.TotalClusterSignal)
        a6_seed_hist.Fill(a6_cluster_tree.SeedSignal)
        a6_size_hist.Fill(a6_cluster_tree.Size)
    a6_cluster_hist.Scale(1/a6_cluster_hist.Integral())
    a6_seed_hist.Scale(1/a6_seed_hist.Integral())
    a6_size_hist.Scale(1/a6_size_hist.Integral())
    a6_size_hist.GetYaxis().SetRangeUser(0,1)

    cluster_legend.AddEntry(a4_cluster_hist,'A4 : 5 #times 5 cluster signal ')
    cluster_legend.AddEntry(a5_cluster_hist,'A5 : 5 #times 5 cluster signal ')
    cluster_legend.AddEntry(a6_cluster_hist,'A6 : 5 #times 5 cluster signal ')

    seed_legend.AddEntry(a4_seed_hist,'A4 : 5 #times 5 seed signal ')
    seed_legend.AddEntry(a5_seed_hist,'A5 : 5 #times 5 seed signal ')
    seed_legend.AddEntry(a6_seed_hist,'A6 : 5 #times 5 seed signal ')

    size_legend.AddEntry(a4_size_hist,'A4 : 5 #times 5 size distribution ')
    size_legend.AddEntry(a5_size_hist,'A5 : 5 #times 5 size distribution ')
    size_legend.AddEntry(a6_size_hist,'A6 : 5 #times 5 size distribution ')

    if not os.path.exists('./python/fig/'):
        os.makedirs('./python/fig/')

    cluster_canvas.cd()
    a6_cluster_hist.Draw('hist')
    a5_cluster_hist.Draw('hist same')
    a4_cluster_hist.Draw('hist same')
    cluster_legend.Draw()
    cluster_canvas.Update()
    cluster_canvas.SaveAs('./python/fig/Sr90_Cluster55_456.pdf')

    seed_canvas.cd()
    a6_seed_hist.Draw('hist')
    a5_seed_hist.Draw('hist same')
    a4_seed_hist.Draw('hist same')
    seed_legend.Draw()
    seed_canvas.Update()
    seed_canvas.SaveAs('./python/fig/Sr90_Seed_456.pdf')

    size_canvas.cd()
    a6_size_hist.Draw('hist')
    a5_size_hist.Draw('hist same')
    a4_size_hist.Draw('hist same')
    size_legend.Draw()
    size_canvas.Update()
    size_canvas.SaveAs('./python/fig/Sr90_Size_456.pdf')



if __name__ == '__main__':
    
    main('./python/output/CHIPA4_Cluster55_Sr90_thr500.root',\
         './python/output/CHIPA5_Cluster55_Sr90_thr500.root',\
         './python/output/CHIPA6_Cluster55_Sr90_thr500.root')


