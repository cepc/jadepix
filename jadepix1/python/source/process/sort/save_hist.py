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



def main(a1_source_fname,a1_noise_fname,\
         a2_source_fname,a2_noise_fname,\
         a3_source_fname,a3_noise_fname,\
         a4_source_fname,a4_noise_fname,\
         a5_source_fname,a5_noise_fname,\
         a6_source_fname,a6_noise_fname):

    #create output root file
    if not os.path.exists('../output/'):
        os.makedirs('../output/')

    OUTPUT = ROOT.TFile('../output/CHIP_A1_To_A6_Cluster55_Hist.root','recreate')


    try:
        #A1
        a1_source_file = ROOT.TFile(a1_source_fname)
        a1_cluster_tree = a1_source_file.Get('Cluster_Tree')
        a1_cluster_entries = a1_cluster_tree.GetEntries()
        #a1_cluster_entries = 200000

        a1_noise_file = ROOT.TFile(a1_noise_fname)
        a1_noise_tree = a1_noise_file.Get('Cluster_Tree')
        a1_noise_entries = a1_noise_tree.GetEntries()
        #a1_noise_entries = 200000

        #A2
        a2_source_file = ROOT.TFile(a2_source_fname)
        a2_cluster_tree = a2_source_file.Get('Cluster_Tree')
        a2_cluster_entries = a2_cluster_tree.GetEntries()
        #a2_cluster_entries = 200000

        a2_noise_file = ROOT.TFile(a2_noise_fname)
        a2_noise_tree = a2_noise_file.Get('Cluster_Tree')
        a2_noise_entries = a2_noise_tree.GetEntries()
        #a2_noise_entries = 200000

        #A3
        a3_source_file = ROOT.TFile(a3_source_fname)
        a3_cluster_tree = a3_source_file.Get('Cluster_Tree')
        a3_cluster_entries = a3_cluster_tree.GetEntries()
        #a3_cluster_entries = 200000

        a3_noise_file = ROOT.TFile(a3_noise_fname)
        a3_noise_tree = a3_noise_file.Get('Cluster_Tree')
        a3_noise_entries = a3_noise_tree.GetEntries()
        #a3_noise_entries = 200000

        #A4
        a4_source_file = ROOT.TFile(a4_source_fname)
        a4_cluster_tree = a4_source_file.Get('Cluster_Tree')
        a4_cluster_entries = a4_cluster_tree.GetEntries()
        #a4_cluster_entries = 200000

        a4_noise_file = ROOT.TFile(a4_noise_fname)
        a4_noise_tree = a4_noise_file.Get('Cluster_Tree')
        a4_noise_entries = a4_noise_tree.GetEntries()
        #a4_noise_entries = 200000

        #A5
        a5_source_file = ROOT.TFile(a5_source_fname)
        a5_cluster_tree = a5_source_file.Get('Cluster_Tree')
        a5_cluster_entries = a5_cluster_tree.GetEntries()
        #a5_cluster_entries = 200000

        a5_noise_file = ROOT.TFile(a5_noise_fname)
        a5_noise_tree = a5_noise_file.Get('Cluster_Tree')
        a5_noise_entries = a5_noise_tree.GetEntries()
        #a5_noise_entries = 200000

        #A6
        a6_source_file = ROOT.TFile(a6_source_fname)
        a6_cluster_tree = a6_source_file.Get('Cluster_Tree')
        a6_cluster_entries = a6_cluster_tree.GetEntries()
        a6_cluster_entries = 200000

        a6_noise_file = ROOT.TFile(a6_noise_fname)
        a6_noise_tree = a6_noise_file.Get('Cluster_Tree')
        a6_noise_entries = a6_noise_tree.GetEntries()
        #a6_noise_entries = 200000

    except:
        logging.error('input file is invalid!')
        sys.exit()


    bin_number = 600

    a1_cluster_hist = ROOT.TH1F('a1 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a1_cluster_hist.GetXaxis().SetTitle('ADC')
    a1_cluster_hist.GetXaxis().CenterTitle()
    a1_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_cluster_hist.GetYaxis().CenterTitle()
    # a1_cluster_hist.SetLineColor(2)
    # a1_cluster_hist.SetLineWidth(2)

    a1_noise_hist = ROOT.TH1F('a1 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a1_noise_hist.GetXaxis().SetTitle('ADC')
    a1_noise_hist.GetXaxis().CenterTitle()
    a1_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_noise_hist.GetYaxis().CenterTitle()
    # a1_noise_hist.SetLineColor(2)
    # a1_noise_hist.SetLineStyle(9)
    # a1_noise_hist.SetLineWidth(2)


    a2_cluster_hist = ROOT.TH1F('a2 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a2_cluster_hist.GetXaxis().SetTitle('ADC')
    a2_cluster_hist.GetXaxis().CenterTitle()
    a2_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_cluster_hist.GetYaxis().CenterTitle()
    # a2_cluster_hist.SetLineColor(3)
    # a2_cluster_hist.SetLineWidth(2)

    a2_noise_hist = ROOT.TH1F('a2 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a2_noise_hist.GetXaxis().SetTitle('ADC')
    a2_noise_hist.GetXaxis().CenterTitle()
    a2_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_noise_hist.GetYaxis().CenterTitle()
    # a2_noise_hist.SetLineColor(3)
    # a2_noise_hist.SetLineStyle(9)
    # a2_noise_hist.SetLineWidth(2)


    a3_cluster_hist = ROOT.TH1F('a3 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a3_cluster_hist.GetXaxis().SetTitle('ADC')
    a3_cluster_hist.GetXaxis().CenterTitle()
    a3_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_cluster_hist.GetYaxis().CenterTitle()
    # a3_cluster_hist.SetLineColor(4)
    # a3_cluster_hist.SetLineWidth(2)

    a3_noise_hist = ROOT.TH1F('a3 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a3_noise_hist.GetXaxis().SetTitle('ADC')
    a3_noise_hist.GetXaxis().CenterTitle()
    a3_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_noise_hist.GetYaxis().CenterTitle()
    # a3_noise_hist.SetLineColor(4)
    # a3_noise_hist.SetLineStyle(9)
    # a3_noise_hist.SetLineWidth(2)

    a4_cluster_hist = ROOT.TH1F('a4 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a4_cluster_hist.GetXaxis().SetTitle('ADC')
    a4_cluster_hist.GetXaxis().CenterTitle()
    a4_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_cluster_hist.GetYaxis().CenterTitle()
    # a4_cluster_hist.SetLineColor(6)
    # a4_cluster_hist.SetLineWidth(2)

    a4_noise_hist = ROOT.TH1F('a4 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a4_noise_hist.GetXaxis().SetTitle('ADC')
    a4_noise_hist.GetXaxis().CenterTitle()
    a4_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_noise_hist.GetYaxis().CenterTitle()
    # a4_noise_hist.SetLineColor(6)
    # a4_noise_hist.SetLineStyle(9)
    # a4_noise_hist.SetLineWidth(2)


    a5_cluster_hist = ROOT.TH1F('a5 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a5_cluster_hist.GetXaxis().SetTitle('ADC')
    a5_cluster_hist.GetXaxis().CenterTitle()
    a5_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_cluster_hist.GetYaxis().CenterTitle()
    # a5_cluster_hist.SetLineColor(7)
    # a5_cluster_hist.SetLineWidth(2)

    a5_noise_hist = ROOT.TH1F('a5 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a5_noise_hist.GetXaxis().SetTitle('ADC')
    a5_noise_hist.GetXaxis().CenterTitle()
    a5_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_noise_hist.GetYaxis().CenterTitle()
    # a5_noise_hist.SetLineColor(7)
    # a5_noise_hist.SetLineStyle(9)
    # a5_noise_hist.SetLineWidth(2)


    a6_cluster_hist = ROOT.TH1F('a6 cluster signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a6_cluster_hist.GetXaxis().SetTitle('ADC')
    a6_cluster_hist.GetXaxis().CenterTitle()
    a6_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_cluster_hist.GetYaxis().CenterTitle()
    # a6_cluster_hist.SetLineColor(8)
    # a6_cluster_hist.SetLineWidth(2)

    a6_noise_hist = ROOT.TH1F('a6 noise signal','{}^{55}Fe  Cluster Signal',bin_number,0,6000)
    a6_noise_hist.GetXaxis().SetTitle('ADC')
    a6_noise_hist.GetXaxis().CenterTitle()
    a6_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_noise_hist.GetYaxis().CenterTitle()
    # a6_noise_hist.SetLineColor(8)
    # a6_noise_hist.SetLineStyle(9)
    # a6_noise_hist.SetLineWidth(2)


    # a1_peak_adc = 0
    # a2_peak_adc = 0
    # a2_peak_adc = 0
    # a4_peak_adc = 0
    # a5_peak_adc = 0
    # a5_peak_adc = 0

    for a1_cluster_entry in xrange(a1_cluster_entries):
        a1_cluster_tree.GetEntry(a1_cluster_entry)
        if (a1_cluster_tree.Seed_Channel >= 2) and (a1_cluster_tree.Seed_Channel <= 13) and (a1_cluster_tree.Seed_Row >= 2) and (a1_cluster_tree.Seed_Row <= 45) :
            a1_cluster_hist.Fill(a1_cluster_tree.ClusterSignal)
    #a1_peak_adc = a1_cluster_hist.GetMaximumBin()
    #a1_cluster_hist.Scale(1/a1_cluster_hist.Integral())
    OUTPUT.Append(a1_cluster_hist)

    for a1_noise_entry in xrange(a1_noise_entries):
        a1_noise_tree.GetEntry(a1_noise_entry)
        a1_noise_hist.Fill(a1_noise_tree.ClusterSignal)
    #a1_noise_hist.Scale(1/a1_noise_hist.Integral())
    OUTPUT.Append(a1_noise_hist)

    for a2_cluster_entry in xrange(a2_cluster_entries):
        a2_cluster_tree.GetEntry(a2_cluster_entry)
        if (a2_cluster_tree.Seed_Channel >= 2) and (a2_cluster_tree.Seed_Channel <= 13) and (a2_cluster_tree.Seed_Row >= 2) and (a2_cluster_tree.Seed_Row <= 45) :
            a2_cluster_hist.Fill(a2_cluster_tree.ClusterSignal)
    #a2_peak_adc = a2_cluster_hist.GetMaximumBin() 
    #a2_cluster_hist.Scale(1/a2_cluster_hist.Integral())
    OUTPUT.Append(a2_cluster_hist)

    for a2_noise_entry in xrange(a2_noise_entries):
        a2_noise_tree.GetEntry(a2_noise_entry)
        a2_noise_hist.Fill(a2_noise_tree.ClusterSignal)
    #a2_noise_hist.Scale(1/a2_noise_hist.Integral())
    OUTPUT.Append(a2_noise_hist)

    for a3_cluster_entry in xrange(a3_cluster_entries):
        a3_cluster_tree.GetEntry(a3_cluster_entry)
        if (a3_cluster_tree.Seed_Channel >= 2) and (a3_cluster_tree.Seed_Channel <= 13) and (a3_cluster_tree.Seed_Row >= 2) and (a3_cluster_tree.Seed_Row <= 45) :
            a3_cluster_hist.Fill(a3_cluster_tree.ClusterSignal)
    #a3_peak_adc = a3_cluster_hist.GetMaximumBin() 
    #a3_cluster_hist.Scale(1/a3_cluster_hist.Integral())
    OUTPUT.Append(a3_noise_hist)

    for a3_noise_entry in xrange(a3_noise_entries):
        a3_noise_tree.GetEntry(a3_noise_entry)
        a3_noise_hist.Fill(a3_noise_tree.ClusterSignal)
    #a3_noise_hist.Scale(1/a3_noise_hist.Integral())
    OUTPUT.Append(a3_cluster_hist)


    for a4_cluster_entry in xrange(a4_cluster_entries):
        a4_cluster_tree.GetEntry(a4_cluster_entry)
        if (a4_cluster_tree.Seed_Channel >= 2) and (a4_cluster_tree.Seed_Channel <= 13) and (a4_cluster_tree.Seed_Row >= 2) and (a4_cluster_tree.Seed_Row <= 45) :
            a4_cluster_hist.Fill(a4_cluster_tree.ClusterSignal)
    #a4_peak_adc = a4_cluster_hist.GetMaximumBin()
    #a4_cluster_hist.Scale(1/a4_cluster_hist.Integral())
    OUTPUT.Append(a4_cluster_hist)

    for a4_noise_entry in xrange(a4_noise_entries):
        a4_noise_tree.GetEntry(a4_noise_entry)
        a4_noise_hist.Fill(a4_noise_tree.ClusterSignal)
    #a4_noise_hist.Scale(1/a4_noise_hist.Integral())
    OUTPUT.Append(a4_noise_hist)


    for a5_cluster_entry in xrange(a5_cluster_entries):
        a5_cluster_tree.GetEntry(a5_cluster_entry)
        if (a5_cluster_tree.Seed_Channel >= 2) and (a5_cluster_tree.Seed_Channel <= 13) and (a5_cluster_tree.Seed_Row >= 2) and (a5_cluster_tree.Seed_Row <= 45) :
            a5_cluster_hist.Fill(a5_cluster_tree.ClusterSignal)
    #a5_peak_adc = a5_cluster_hist.GetMaximumBin() 
    #a5_cluster_hist.Scale(1/a5_cluster_hist.Integral())
    OUTPUT.Append(a5_cluster_hist)

    for a5_noise_entry in xrange(a5_noise_entries):
        a5_noise_tree.GetEntry(a5_noise_entry)
        a5_noise_hist.Fill(a5_noise_tree.ClusterSignal)
    #a5_noise_hist.Scale(1/a5_noise_hist.Integral())
    OUTPUT.Append(a5_noise_hist)


    for a6_cluster_entry in xrange(a6_cluster_entries):
        a6_cluster_tree.GetEntry(a6_cluster_entry)
        if (a6_cluster_tree.Seed_Channel >= 2) and (a6_cluster_tree.Seed_Channel <= 13) and (a6_cluster_tree.Seed_Row >= 2) and (a6_cluster_tree.Seed_Row <= 45) :
            a6_cluster_hist.Fill(a6_cluster_tree.ClusterSignal)
    #a6_peak_adc = a6_cluster_hist.GetMaximumBin() 
    #a6_cluster_hist.Scale(1/a6_cluster_hist.Integral())
    OUTPUT.Append(a6_cluster_hist)

    for a6_noise_entry in xrange(a6_noise_entries):
        a6_noise_tree.GetEntry(a6_noise_entry)
        a6_noise_hist.Fill(a6_noise_tree.ClusterSignal)
    #a6_noise_hist.Scale(1/a6_noise_hist.Integral())
    OUTPUT.Append(a6_noise_hist)


    OUTPUT.Write()
    OUTPUT.Close()


    # print('a1 peak adc :',a1_peak_adc)
    # print('a2 peak adc :',a2_peak_adc)
    # print('a3 peak adc :',a3_peak_adc)

    # address = [4,5,6]
    # cce = [a1_peak_adc,a2_peak_adc,a3_peak_adc]
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

    f1 = '../output/CHIPA1_Cluster55_Iron55_thr500.root'
    f1n= '../output/CHIPA1_noise_55.root'

    f2 = '../output/CHIPA2_Cluster55_Iron55_thr500.root'
    f2n= '../output/CHIPA2_noise_55.root'

    f3 = '../output/CHIPA3_Cluster55_Iron55_thr500.root'
    f3n= '../output/CHIPA3_noise_55.root'

    f4 = '../output/CHIPA4_Cluster55_Iron55_thr500.root'
    f4n='../output/CHIPA4_noise_55.root'

    f5 = '../output/CHIPA5_Cluster55_Iron55_thr500.root'
    f5n= '../output/CHIPA5_noise_55.root'

    f6 = '../output/CHIPA6_Cluster55_Iron55_thr500.root'
    f6n= '../output/CHIPA6_noise_55.root'

    #main(f1,f2,f3,f4,f5,f6)
    main(f1,f1n,f2,f2n,f3,f3n,f4,f4n,f5,f5n,f6,f6n)


