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


def main(a2_source_fname,a5_source_fname):
    try:

        #A2
        a2_source_file = ROOT.TFile(a2_source_fname)
        a2_size_tree = a2_source_file.Get('Cluster_Tree')
        #a2_size_entries = a2_size_tree.GetEntries()
        a2_size_entries = 200000

        #A5
        a5_source_file = ROOT.TFile(a5_source_fname)
        a5_size_tree = a5_source_file.Get('Cluster_Tree')
        #a5_size_entries = a5_size_tree.GetEntries()
        a5_size_entries = 200000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('canvas','size',200,10,2000,1200)
    legend = ROOT.TLegend(0.75,0.7,0.85,0.85)

    #A2
    a2_size_hist = ROOT.TH1F('a2 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a2_size_hist.GetXaxis().SetTitle('Size')
    a2_size_hist.GetXaxis().CenterTitle()
    a2_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_size_hist.GetYaxis().CenterTitle()
    a2_size_hist.SetLineColor(3)
    a2_size_hist.SetLineWidth(2)

    #A5
    a5_size_hist = ROOT.TH1F('a5 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a5_size_hist.GetXaxis().SetTitle('Size')
    a5_size_hist.GetXaxis().CenterTitle()
    a5_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_size_hist.GetYaxis().CenterTitle()
    a5_size_hist.SetLineColor(7)
    a5_size_hist.SetLineWidth(2)


    for a2_size_entry in xrange(a2_size_entries):
        a2_size_tree.GetEntry(a2_size_entry)
        if (a2_size_tree.Seed_Channel >= 2) and (a2_size_tree.Seed_Channel <= 13) and (a2_size_tree.Seed_Row >= 2) and (a2_size_tree.Seed_Row <= 45) :
            a2_size_hist.Fill(a2_size_tree.Size) 
    a2_size_hist.Scale(1/a2_size_hist.Integral())
    a2_size_hist.GetYaxis().SetRangeUser(0,1)

    for a5_size_entry in xrange(a5_size_entries):
        a5_size_tree.GetEntry(a5_size_entry)
        if (a5_size_tree.Seed_Channel >= 2) and (a5_size_tree.Seed_Channel <= 13) and (a5_size_tree.Seed_Row >= 2) and (a5_size_tree.Seed_Row <= 45) :
            a5_size_hist.Fill(a5_size_tree.Size) 
    a5_size_hist.Scale(1/a5_size_hist.Integral())
    a5_size_hist.GetYaxis().SetRangeUser(0,1)


    legend.AddEntry(a2_size_hist,'    A2')
    legend.AddEntry(a5_size_hist,'    A5')



    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    a2_size_hist.Draw('hist')
    a5_size_hist.Draw('hist same')
    legend.Draw()
    canvas.SaveAs('../fig/iron55_size_25.gif')

if __name__ == '__main__':
    main('../output/CHIPA2_Cluster55_Iron55_thr500.root','../output/CHIPA5_Cluster55_Iron55_thr500.root')




