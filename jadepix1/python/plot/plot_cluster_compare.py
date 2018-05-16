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


def main(cluster33_source_fname,cluster33_noise_fname,cluster55_source_fname,cluster55_noise_fname,cluster77_source_fname,cluster77_noise_fname):
    try:
        #Cluster 3*3
        cluster33_source_file = ROOT.TFile(cluster33_source_fname)
        cluster33_cluster_tree = cluster33_source_file.Get('Cluster_Tree')
        #cluster33_cluster_entries = cluster33_cluster_tree.GetEntries()
        cluster33_cluster_entries = 200000

        cluster33_noise_file = ROOT.TFile(cluster33_noise_fname)
        cluster33_noise_tree = cluster33_noise_file.Get('Cluster_Tree')
        #cluster33_cluster_entries = cluster33_cluster_tree.GetEntries()
        cluster33_noise_entries = 200000

        #Cluster 5*5
        cluster55_source_file = ROOT.TFile(cluster55_source_fname)
        cluster55_cluster_tree = cluster55_source_file.Get('Cluster_Tree')
        #cluster55_cluster_entries = cluster55_cluster_tree.GetEntries()
        cluster55_cluster_entries = 200000

        cluster55_noise_file = ROOT.TFile(cluster55_noise_fname)
        cluster55_noise_tree = cluster55_noise_file.Get('Cluster_Tree')
        #cluster55_cluster_entries = cluster55_cluster_tree.GetEntries()
        cluster55_noise_entries = 200000

        #Cluster 6*6
        cluster77_source_file = ROOT.TFile(cluster77_source_fname)
        cluster77_cluster_tree = cluster77_source_file.Get('Cluster_Tree')
        #cluster77_cluster_entries = cluster77_cluster_tree.GetEntries()
        cluster77_cluster_entries = 200000

        cluster77_noise_file = ROOT.TFile(cluster77_noise_fname)
        cluster77_noise_tree = cluster77_noise_file.Get('Cluster_Tree')
        #cluster77_cluster_entries = cluster77_cluster_tree.GetEntries()
        cluster77_noise_entries = 200000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,2400,1200)
    legend = ROOT.TLegend(0.55,0.7,0.86,0.85)
    legend.SetNColumns(2)
    #legend.SetBorderSize(0)

    bin_number = 600

    cluster33_cluster_hist = ROOT.TH1F('cluster33 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    cluster33_cluster_hist.GetXaxis().SetTitle('ADC')
    cluster33_cluster_hist.GetXaxis().CenterTitle()
    cluster33_cluster_hist.GetYaxis().SetTitle('Counts')
    cluster33_cluster_hist.GetYaxis().CenterTitle()
    cluster33_cluster_hist.SetLineColor(2)
    cluster33_cluster_hist.SetLineWidth(2)

    cluster33_noise_hist = ROOT.TH1F('cluster33 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    cluster33_noise_hist.GetXaxis().SetTitle('ADC')
    cluster33_noise_hist.GetXaxis().CenterTitle()
    cluster33_noise_hist.GetYaxis().SetTitle('Counts')
    cluster33_noise_hist.GetYaxis().CenterTitle()
    cluster33_noise_hist.SetLineColor(2)
    cluster33_noise_hist.SetLineStyle(9)
    cluster33_noise_hist.SetLineWidth(2)


    cluster55_cluster_hist = ROOT.TH1F('cluster55 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    cluster55_cluster_hist.GetXaxis().SetTitle('ADC')
    cluster55_cluster_hist.GetXaxis().CenterTitle()
    cluster55_cluster_hist.GetYaxis().SetTitle('Counts')
    cluster55_cluster_hist.GetYaxis().CenterTitle()
    cluster55_cluster_hist.SetLineColor(3)
    cluster55_cluster_hist.SetLineWidth(2)

    cluster55_noise_hist = ROOT.TH1F('cluster55 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    cluster55_noise_hist.GetXaxis().SetTitle('ADC')
    cluster55_noise_hist.GetXaxis().CenterTitle()
    cluster55_noise_hist.GetYaxis().SetTitle('Counts')
    cluster55_noise_hist.GetYaxis().CenterTitle()
    cluster55_noise_hist.SetLineColor(3)
    cluster55_noise_hist.SetLineStyle(9)
    cluster55_noise_hist.SetLineWidth(2)


    cluster77_cluster_hist = ROOT.TH1F('cluster77 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    cluster77_cluster_hist.GetXaxis().SetTitle('ADC')
    cluster77_cluster_hist.GetXaxis().CenterTitle()
    cluster77_cluster_hist.GetYaxis().SetTitle('Counts')
    cluster77_cluster_hist.GetYaxis().CenterTitle()
    cluster77_cluster_hist.SetLineColor(4)
    cluster77_cluster_hist.SetLineWidth(2)

    cluster77_noise_hist = ROOT.TH1F('cluster77 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    cluster77_noise_hist.GetXaxis().SetTitle('ADC')
    cluster77_noise_hist.GetXaxis().CenterTitle()
    cluster77_noise_hist.GetYaxis().SetTitle('Counts')
    cluster77_noise_hist.GetYaxis().CenterTitle()
    cluster77_noise_hist.SetLineColor(4)
    cluster77_noise_hist.SetLineStyle(9)
    cluster77_noise_hist.SetLineWidth(2)

    # cluster33_peak_adc = 0
    # cluster55_peak_adc = 0
    # cluster55_peak_adc = 0
 

    for cluster33_cluster_entry in xrange(cluster33_cluster_entries):
        cluster33_cluster_tree.GetEntry(cluster33_cluster_entry)
        if (cluster33_cluster_tree.Seed_Channel >= 2) and (cluster33_cluster_tree.Seed_Channel <= 13) and (cluster33_cluster_tree.Seed_Row >= 2) and (cluster33_cluster_tree.Seed_Row <= 45) :
            cluster33_cluster_hist.Fill(cluster33_cluster_tree.ClusterSignal)
    #cluster33_peak_adc = cluster33_cluster_hist.GetMaximumBin()
    cluster33_cluster_hist.Scale(1/cluster33_cluster_hist.Integral())

    for cluster33_noise_entry in xrange(cluster33_noise_entries):
        cluster33_noise_tree.GetEntry(cluster33_noise_entry)
        cluster33_noise_hist.Fill(cluster33_noise_tree.ClusterSignal)
    cluster33_noise_hist.Scale(1/cluster33_noise_hist.Integral())


    for cluster55_cluster_entry in xrange(cluster55_cluster_entries):
        cluster55_cluster_tree.GetEntry(cluster55_cluster_entry)
        if (cluster55_cluster_tree.Seed_Channel >= 2) and (cluster55_cluster_tree.Seed_Channel <= 13) and (cluster55_cluster_tree.Seed_Row >= 2) and (cluster55_cluster_tree.Seed_Row <= 45) :
            cluster55_cluster_hist.Fill(cluster55_cluster_tree.ClusterSignal)
    #cluster55_peak_adc = cluster55_cluster_hist.GetMaximumBin() 
    cluster55_cluster_hist.Scale(1/cluster55_cluster_hist.Integral())

    for cluster55_noise_entry in xrange(cluster55_noise_entries):
        cluster55_noise_tree.GetEntry(cluster55_noise_entry)
        cluster55_noise_hist.Fill(cluster55_noise_tree.ClusterSignal)
    cluster55_noise_hist.Scale(1/cluster55_noise_hist.Integral())


    for cluster77_cluster_entry in xrange(cluster77_cluster_entries):
        cluster77_cluster_tree.GetEntry(cluster77_cluster_entry)
        if (cluster77_cluster_tree.Seed_Channel >= 2) and (cluster77_cluster_tree.Seed_Channel <= 13) and (cluster77_cluster_tree.Seed_Row >= 2) and (cluster77_cluster_tree.Seed_Row <= 45) :
            cluster77_cluster_hist.Fill(cluster77_cluster_tree.ClusterSignal)
    #cluster77_peak_adc = cluster77_cluster_hist.GetMaximumBin() 
    cluster77_cluster_hist.Scale(1/cluster77_cluster_hist.Integral())

    for cluster77_noise_entry in xrange(cluster77_noise_entries):
        cluster77_noise_tree.GetEntry(cluster77_noise_entry)
        cluster77_noise_hist.Fill(cluster77_noise_tree.ClusterSignal)
    cluster77_noise_hist.Scale(1/cluster77_noise_hist.Integral())

    legend.AddEntry(cluster33_cluster_hist,'A4 : 3 #times 3 cluster signal ')
    legend.AddEntry(cluster33_noise_hist,'A4 : 3 #times 3 noise signal')

    legend.AddEntry(cluster55_cluster_hist,'A4 : 5 #times 5 cluster signal ')
    legend.AddEntry(cluster55_noise_hist,'A4 : 5 #times 5 noise signal')

    legend.AddEntry(cluster77_cluster_hist,'A4 : 7 #times 7 cluster signal ')
    legend.AddEntry(cluster77_noise_hist,'A4 : 7 #times 7 noise signal')

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')


    canvas.cd()
    cluster33_noise_hist.Draw('hist')
    cluster55_noise_hist.Draw('hist same')
    cluster77_noise_hist.Draw('hist same')
    cluster77_cluster_hist.Draw('hist same')
    cluster55_cluster_hist.Draw('hist same')
    cluster33_cluster_hist.Draw('hist same')
    legend.Draw()
    canvas.Update()
    canvas.SaveAs('../fig/chip_a4_iron55_cluster357_scale.gif')


    # print('cluster33 peak adc :',cluster33_peak_adc)
    # print('cluster55 peak adc :',cluster55_peak_adc)
    # print('cluster77 peak adc :',cluster77_peak_adc)

    # address = [4,5,6]
    # cce = [cluster33_peak_adc,cluster55_peak_adc,cluster77_peak_adc]
    # print(address)
    # print(cce)
 
    # cce_canvas = ROOT.TCanvas('cce','cce',1000,500)
    # cce_canvas.SetGrid()       
    # cce_graph = ROOT.TGraph()

    # for i in xrange(3):
    #     cce_graph.SetPoint(i+1,address[i],cce[i])

    # cce_graph.RemovePoint(0)

    # cce_canvas.cd()
    # cce_graph.GetXaxis().SetTitle('chip address')
    # cce_graph.GetXaxis().CenterTitle()
    # cce_graph.GetXaxis().SetLimits(0.,10.)
    # cce_graph.GetYaxis().SetTitle('peak adc')
    # cce_graph.SetMarkerColor(38)
    # cce_graph.SetMarkerStyle(21) 
    # cce_graph.SetMarkerSize(1) 

    # cce_graph.Draw('ACP')
    # cce_canvas.Update()
    # cce_canvas.SaveAs('../fig/cce_profile.gif')


if __name__ == '__main__':
    
    main('../output/CHIPA4_Cluster33_Iron55_thr500.root','../output/CHIPA4_noise_33.root','../output/CHIPA4_Cluster55_Iron55_thr500.root','../output/CHIPA4_noise_55.root','../output/CHIPA4_Cluster77_Iron55_thr500.root','../output/CHIPA4_noise_77.root')


