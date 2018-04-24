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


def main(a3_source_fname,a6_source_fname):
    try:

        #A3
        a3_source_file = ROOT.TFile(a3_source_fname)
        a3_size_tree = a3_source_file.Get('Cluster_Tree')
        #a3_size_entries = a3_size_tree.GetEntries()
        a3_size_entries = 200000

        #A6
        a6_source_file = ROOT.TFile(a6_source_fname)
        a6_size_tree = a6_source_file.Get('Cluster_Tree')
        #a6_size_entries = a6_size_tree.GetEntries()
        a6_size_entries = 200000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('canvas','size',200,10,2000,1200)
    legend = ROOT.TLegend(0.75,0.7,0.85,0.85)

    #A3
    a3_size_hist = ROOT.TH1F('a3 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a3_size_hist.GetXaxis().SetTitle('Size')
    a3_size_hist.GetXaxis().CenterTitle()
    a3_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_size_hist.GetYaxis().CenterTitle()
    a3_size_hist.SetLineColor(4)
    a3_size_hist.SetLineWidth(2)

    #A6
    a6_size_hist = ROOT.TH1F('a6 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a6_size_hist.GetXaxis().SetTitle('Size')
    a6_size_hist.GetXaxis().CenterTitle()
    a6_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_size_hist.GetYaxis().CenterTitle()
    a6_size_hist.SetLineColor(8)
    a6_size_hist.SetLineWidth(2)


    for a3_size_entry in xrange(a3_size_entries):
        a3_size_tree.GetEntry(a3_size_entry)
        if (a3_size_tree.Seed_Channel >= 2) and (a3_size_tree.Seed_Channel <= 13) and (a3_size_tree.Seed_Row >= 2) and (a3_size_tree.Seed_Row <= 45) :
            a3_size_hist.Fill(a3_size_tree.Size) 
    a3_size_hist.Scale(1/a3_size_hist.Integral())
    a3_size_hist.GetYaxis().SetRangeUser(0,1)

    for a6_size_entry in xrange(a6_size_entries):
        a6_size_tree.GetEntry(a6_size_entry)
        if (a6_size_tree.Seed_Channel >= 2) and (a6_size_tree.Seed_Channel <= 13) and (a6_size_tree.Seed_Row >= 2) and (a6_size_tree.Seed_Row <= 45) :
            a6_size_hist.Fill(a6_size_tree.Size) 
    a6_size_hist.Scale(1/a6_size_hist.Integral())
    a6_size_hist.GetYaxis().SetRangeUser(0,1)


    legend.AddEntry(a3_size_hist,'    A3')
    legend.AddEntry(a6_size_hist,'    A6')



    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    a3_size_hist.Draw('hist')
    a6_size_hist.Draw('hist same')
    legend.Draw()
    canvas.SaveAs('../fig/iron55_size_36.gif')

if __name__ == '__main__':
    main('../output/CHIPA3_Cluster55_Iron55_thr500.root','../output/CHIPA6_Cluster55_Iron55_thr500.root')




