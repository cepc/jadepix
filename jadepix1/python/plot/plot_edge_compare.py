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


def main(source_fname):
    try:

        source_file = ROOT.TFile(source_fname)
        cluster_tree = source_file.Get('Cluster_Tree')
        cluster_entries = cluster_tree.GetEntries()
        #cluster_entries = 200000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,2400,1200)
    legend = ROOT.TLegend(0.65,0.6,0.85,0.85)
    #legend.SetBorderSize(0)

    bin_number = 600

    normal_cluster_hist = ROOT.TH1F('normal cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    normal_cluster_hist.GetXaxis().SetTitle('ADC')
    normal_cluster_hist.GetXaxis().CenterTitle()
    normal_cluster_hist.GetYaxis().SetTitle('Counts')
    normal_cluster_hist.GetYaxis().CenterTitle()
    normal_cluster_hist.SetLineColor(1)
    normal_cluster_hist.SetLineWidth(2)

    ex_cluster_hist = ROOT.TH1F('ex cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    ex_cluster_hist.GetXaxis().SetTitle('ADC')
    ex_cluster_hist.GetXaxis().CenterTitle()
    ex_cluster_hist.GetYaxis().SetTitle('Counts')
    ex_cluster_hist.GetYaxis().CenterTitle()
    ex_cluster_hist.SetLineColor(2)
    ex_cluster_hist.SetLineWidth(2)

    # edge_cluster_hist = ROOT.TH1F('edge cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    # edge_cluster_hist.GetXaxis().SetTitle('ADC')
    # edge_cluster_hist.GetXaxis().CenterTitle()
    # edge_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    # edge_cluster_hist.GetYaxis().CenterTitle()
    # edge_cluster_hist.SetLineColor(4)
    # edge_cluster_hist.SetLineWidth(2)

    edge20_cluster_hist = ROOT.TH1F('edge20 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    edge20_cluster_hist.GetXaxis().SetTitle('ADC')
    edge20_cluster_hist.GetXaxis().CenterTitle()
    edge20_cluster_hist.GetYaxis().SetTitle('Counts')
    edge20_cluster_hist.GetYaxis().CenterTitle()
    edge20_cluster_hist.SetLineColor(4)
    edge20_cluster_hist.SetLineWidth(2)
    #edge20_cluster_hist.SetLineStyle(7)

    edge15_cluster_hist = ROOT.TH1F('edge15 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    edge15_cluster_hist.GetXaxis().SetTitle('ADC')
    edge15_cluster_hist.GetXaxis().CenterTitle()
    edge15_cluster_hist.GetYaxis().SetTitle('Counts')
    edge15_cluster_hist.GetYaxis().CenterTitle()
    edge15_cluster_hist.SetLineColor(8)
    edge15_cluster_hist.SetLineWidth(2)
    #edge15_cluster_hist.SetLineStyle(9)

    edge_other_cluster_hist = ROOT.TH1F('other edge cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    edge_other_cluster_hist.GetXaxis().SetTitle('ADC')
    edge_other_cluster_hist.GetXaxis().CenterTitle()
    edge_other_cluster_hist.GetYaxis().SetTitle('Counts')
    edge_other_cluster_hist.GetYaxis().CenterTitle()
    edge_other_cluster_hist.SetLineColor(6)
    edge_other_cluster_hist.SetLineWidth(2)
    #edge_other_cluster_hist.SetLineStyle(3)



    for cluster_entry in xrange(cluster_entries):
        cluster_tree.GetEntry(cluster_entry)
        normal_cluster_hist.Fill(cluster_tree.ClusterSignal)
        if (cluster_tree.Seed_Channel >= 2) and (cluster_tree.Seed_Channel <= 13) and (cluster_tree.Seed_Row >= 2) and (cluster_tree.Seed_Row <= 45) :
            ex_cluster_hist.Fill(cluster_tree.ClusterSignal)
        else:
            #edge_cluster_hist.Fill(cluster_tree.ClusterSignal)

            if ((cluster_tree.Seed_Channel == 1) and (cluster_tree.Seed_Row > 1) and (cluster_tree.Seed_Row < 46)) or\
               ((cluster_tree.Seed_Channel == 14) and (cluster_tree.Seed_Row > 1) and (cluster_tree.Seed_Row < 46)) or\
               ((cluster_tree.Seed_Row == 1) and (cluster_tree.Seed_Channel > 1) and (cluster_tree.Seed_Channel < 14)) or\
               ((cluster_tree.Seed_Row == 46) and (cluster_tree.Seed_Channel > 1) and (cluster_tree.Seed_Channel < 14)):
                edge20_cluster_hist.Fill(cluster_tree.ClusterSignal)
            else:
                if ((cluster_tree.Seed_Channel == 0) and (cluster_tree.Seed_Row > 1) and (cluster_tree.Seed_Row < 46)) or\
                   ((cluster_tree.Seed_Channel == 15) and (cluster_tree.Seed_Row > 1) and (cluster_tree.Seed_Row < 46)) or\
                   ((cluster_tree.Seed_Row == 0) and (cluster_tree.Seed_Channel > 1) and (cluster_tree.Seed_Channel < 14)) or\
                   ((cluster_tree.Seed_Row == 47) and (cluster_tree.Seed_Channel > 1) and (cluster_tree.Seed_Channel < 14)):
                    edge15_cluster_hist.Fill(cluster_tree.ClusterSignal)

                else:
                    edge_other_cluster_hist.Fill(cluster_tree.ClusterSignal)

                
    legend.AddEntry(normal_cluster_hist,'A4 : 5 #times 5 normal cluster signal ')
    legend.AddEntry(ex_cluster_hist,'A4 : 5 #times 5 exclude edge hit cluster signal ')
    #legend.AddEntry(edge_cluster_hist,'A4 : 5 #times 5 edge hit cluster signal')
    legend.AddEntry(edge20_cluster_hist,'A4 : 5 #times 5 edge20 hit cluster signal')
    legend.AddEntry(edge15_cluster_hist,'A4 : 5 #times 5 edge15 hit cluster signal')
    legend.AddEntry(edge_other_cluster_hist,'A4 : 5 #times 5 other edge hit cluster signal')

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')

    canvas.cd()
    normal_cluster_hist.Draw('hist')
    ex_cluster_hist.Draw('hist same')
    #edge_cluster_hist.Draw('hist same')
    edge20_cluster_hist.Draw('hist same')
    edge15_cluster_hist.Draw('hist same')
    edge_other_cluster_hist.Draw('hist same')
    legend.Draw()
    canvas.Update()
    canvas.SaveAs('../fig/iron55_cluster55_edge_compare.gif')


if __name__ == '__main__':
    
    main('../output/CHIPA4_Cluster55_Iron55_thr500.root')


