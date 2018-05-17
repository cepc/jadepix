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


def main(a1_source_fname,a4_source_fname):
    try:

        #A1
        a1_source_file = ROOT.TFile(a1_source_fname)
        a1_size_tree = a1_source_file.Get('Cluster_Tree')
        #a1_size_entries = a1_size_tree.GetEntries()
        a1_size_entries = 200000

        #A4
        a4_source_file = ROOT.TFile(a4_source_fname)
        a4_size_tree = a4_source_file.Get('Cluster_Tree')
        #a4_size_entries = a4_size_tree.GetEntries()
        a4_size_entries = 200000

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

    #A4
    a4_size_hist = ROOT.TH1F('a4 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a4_size_hist.GetXaxis().SetTitle('Size')
    a4_size_hist.GetXaxis().CenterTitle()
    a4_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_size_hist.GetYaxis().CenterTitle()
    a4_size_hist.SetLineColor(6)
    a4_size_hist.SetLineWidth(2)


    for a1_size_entry in xrange(a1_size_entries):
        a1_size_tree.GetEntry(a1_size_entry)
        if (a1_size_tree.Seed_Channel >= 2) and (a1_size_tree.Seed_Channel <= 13) and (a1_size_tree.Seed_Row >= 2) and (a1_size_tree.Seed_Row <= 45) :
            a1_size_hist.Fill(a1_size_tree.Size) 
    a1_size_hist.Scale(1/a1_size_hist.Integral())
    a1_size_hist.GetYaxis().SetRangeUser(0,1)

    for a4_size_entry in xrange(a4_size_entries):
        a4_size_tree.GetEntry(a4_size_entry)
        if (a4_size_tree.Seed_Channel >= 2) and (a4_size_tree.Seed_Channel <= 13) and (a4_size_tree.Seed_Row >= 2) and (a4_size_tree.Seed_Row <= 45) :
            a4_size_hist.Fill(a4_size_tree.Size) 
    a4_size_hist.Scale(1/a4_size_hist.Integral())
    a4_size_hist.GetYaxis().SetRangeUser(0,1)


    legend.AddEntry(a1_size_hist,'    A1')
    legend.AddEntry(a4_size_hist,'    A4')



    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    a1_size_hist.Draw('hist')
    a4_size_hist.Draw('hist same')
    legend.Draw()
    canvas.SaveAs('../fig/iron55_size_14.gif')

if __name__ == '__main__':
    main('../output/CHIPA1_Cluster55_Iron55_thr500.root','../output/CHIPA4_Cluster55_Iron55_thr500.root')




