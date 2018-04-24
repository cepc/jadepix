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


def main(a4_source_fname,a5_source_fname,a6_source_fname):
    try:

        #A4
        a4_source_file = ROOT.TFile(a4_source_fname)
        a4_size_tree = a4_source_file.Get('Cluster_Tree')
        #a4_size_entries = a4_size_tree.GetEntries()
        a4_size_entries = 200000

        #A5
        a5_source_file = ROOT.TFile(a5_source_fname)
        a5_size_tree = a5_source_file.Get('Cluster_Tree')
        #a5_size_entries = a5_size_tree.GetEntries()
        a5_size_entries = 200000

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

    #A4
    a4_size_hist = ROOT.TH1F('a4 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a4_size_hist.GetXaxis().SetTitle('Size')
    a4_size_hist.GetXaxis().CenterTitle()
    a4_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_size_hist.GetYaxis().CenterTitle()
    a4_size_hist.SetLineColor(6)
    a4_size_hist.SetLineWidth(2)

    #A5
    a5_size_hist = ROOT.TH1F('a5 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a5_size_hist.GetXaxis().SetTitle('Size')
    a5_size_hist.GetXaxis().CenterTitle()
    a5_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_size_hist.GetYaxis().CenterTitle()
    a5_size_hist.SetLineColor(7)
    a5_size_hist.SetLineWidth(2)

    #A6
    a6_size_hist = ROOT.TH1F('a6 size distribution','{}^{55}Fe  Size Distribution',5,1,6)
    a6_size_hist.GetXaxis().SetTitle('Size')
    a6_size_hist.GetXaxis().CenterTitle()
    a6_size_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_size_hist.GetYaxis().CenterTitle()
    a6_size_hist.SetLineColor(8)
    a6_size_hist.SetLineWidth(2)


    for a4_size_entry in xrange(a4_size_entries):
        a4_size_tree.GetEntry(a4_size_entry)
        if (a4_size_tree.Seed_Channel >= 2) and (a4_size_tree.Seed_Channel <= 13) and (a4_size_tree.Seed_Row >= 2) and (a4_size_tree.Seed_Row <= 45) :
            a4_size_hist.Fill(a4_size_tree.Size) 
    a4_size_hist.Scale(1/a4_size_hist.Integral())
    a4_size_hist.GetYaxis().SetRangeUser(0,1)

    for a5_size_entry in xrange(a5_size_entries):
        a5_size_tree.GetEntry(a5_size_entry)
        if (a5_size_tree.Seed_Channel >= 2) and (a5_size_tree.Seed_Channel <= 13) and (a5_size_tree.Seed_Row >= 2) and (a5_size_tree.Seed_Row <= 45) :
            a5_size_hist.Fill(a5_size_tree.Size) 
    a5_size_hist.Scale(1/a5_size_hist.Integral())
    a5_size_hist.GetYaxis().SetRangeUser(0,1)

    for a6_size_entry in xrange(a6_size_entries):
        a6_size_tree.GetEntry(a6_size_entry)
        if (a6_size_tree.Seed_Channel >= 2) and (a6_size_tree.Seed_Channel <= 13) and (a6_size_tree.Seed_Row >= 2) and (a6_size_tree.Seed_Row <= 45) :
            a6_size_hist.Fill(a6_size_tree.Size) 
    a6_size_hist.Scale(1/a6_size_hist.Integral())
    a6_size_hist.GetYaxis().SetRangeUser(0,1)

    legend.AddEntry(a4_size_hist,'    A4')
    legend.AddEntry(a5_size_hist,'    A5')
    legend.AddEntry(a6_size_hist,'    A6')


    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    a4_size_hist.Draw('hist')
    a5_size_hist.Draw('hist same')
    a6_size_hist.Draw('hist same')
    legend.Draw()
    canvas.SaveAs('../fig/iron55_size_456.gif')

if __name__ == '__main__':
    main('../output/CHIPA4_Cluster55_Iron55_thr500.root','../output/CHIPA5_Cluster55_Iron55_thr500.root','../output/CHIPA6_Cluster55_Iron55_thr500.root')




