#!/usr/bin/env python

'''
plot size distribution
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-03-05 Mon 19:00]"


import sys,os
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


def main(a1_source_fname,a2_source_fname,a3_source_fname):
    try:

        #A1
        a1_source_file = ROOT.TFile(a1_source_fname)
        a1_size_tree = a1_source_file.Get('Cluster_Tree')
        #a1_size_entries = a1_size_tree.GetEntries()
        a1_size_entries = 200000

        #A2
        a2_source_file = ROOT.TFile(a2_source_fname)
        a2_size_tree = a2_source_file.Get('Cluster_Tree')
        #a2_size_entries = a2_size_tree.GetEntries()
        a2_size_entries = 200000

        #A3
        a3_source_file = ROOT.TFile(a3_source_fname)
        a3_size_tree = a3_source_file.Get('Cluster_Tree')
        #a3_size_entries = a3_size_tree.GetEntries()
        a3_size_entries = 200000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('canvas','size',200,10,2000,1200)
    legend = ROOT.TLegend(0.75,0.7,0.85,0.85)

    #A1
    a1_size_hist = ROOT.TH1F('a1 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a1_size_hist.GetXaxis().SetTitle('Size')
    a1_size_hist.GetXaxis().CenterTitle()
    a1_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_size_hist.GetYaxis().CenterTitle()
    a1_size_hist.SetLineColor(2)
    a1_size_hist.SetLineWidth(2)

    #A2
    a2_size_hist = ROOT.TH1F('a2 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a2_size_hist.GetXaxis().SetTitle('Size')
    a2_size_hist.GetXaxis().CenterTitle()
    a2_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_size_hist.GetYaxis().CenterTitle()
    a2_size_hist.SetLineColor(3)
    a2_size_hist.SetLineWidth(2)

    #A3
    a3_size_hist = ROOT.TH1F('a3 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a3_size_hist.GetXaxis().SetTitle('Size')
    a3_size_hist.GetXaxis().CenterTitle()
    a3_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_size_hist.GetYaxis().CenterTitle()
    a3_size_hist.SetLineColor(4)
    a3_size_hist.SetLineWidth(2)


    for a1_size_entry in xrange(a1_size_entries):
        a1_size_tree.GetEntry(a1_size_entry)
        if (a1_size_tree.Seed_Channel >= 2) and (a1_size_tree.Seed_Channel <= 13) and (a1_size_tree.Seed_Row >= 2) and (a1_size_tree.Seed_Row <= 45) :
            a1_size_hist.Fill(a1_size_tree.Size) 
    a1_size_hist.Scale(1/a1_size_hist.Integral())
    a1_size_hist.GetYaxis().SetRangeUser(0,1)

    for a2_size_entry in xrange(a2_size_entries):
        a2_size_tree.GetEntry(a2_size_entry)
        if (a2_size_tree.Seed_Channel >= 2) and (a2_size_tree.Seed_Channel <= 13) and (a2_size_tree.Seed_Row >= 2) and (a2_size_tree.Seed_Row <= 45) :
            a2_size_hist.Fill(a2_size_tree.Size) 
    a2_size_hist.Scale(1/a2_size_hist.Integral())
    a2_size_hist.GetYaxis().SetRangeUser(0,1)

    for a3_size_entry in xrange(a3_size_entries):
        a3_size_tree.GetEntry(a3_size_entry)
        if (a3_size_tree.Seed_Channel >= 2) and (a3_size_tree.Seed_Channel <= 13) and (a3_size_tree.Seed_Row >= 2) and (a3_size_tree.Seed_Row <= 45) :
            a3_size_hist.Fill(a3_size_tree.Size) 
    a3_size_hist.Scale(1/a3_size_hist.Integral())
    a3_size_hist.GetYaxis().SetRangeUser(0,1)

    legend.AddEntry(a1_size_hist,'    A1')
    legend.AddEntry(a2_size_hist,'    A2')
    legend.AddEntry(a3_size_hist,'    A3')


    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    a1_size_hist.Draw('hist')
    a2_size_hist.Draw('hist same')
    a3_size_hist.Draw('hist same')
    legend.Draw()
    canvas.SaveAs('../fig/iron55_size_123.gif')

if __name__ == '__main__':
    main('../output/CHIPA1_Cluster55_Iron55_thr500.root','../output/CHIPA2_Cluster55_Iron55_thr500.root','../output/CHIPA3_Cluster55_Iron55_thr500.root')




