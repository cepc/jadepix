#!/usr/bin/env python

'''
plot Iron55 clusters compare hist
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os,copy
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


def plot(fname,title):

    try:
        input = ROOT.TFile(fname)
        cluster_tree = input.Get('Cluster_Tree')
        cluster_entries = cluster_tree.GetEntries()

    except:
        logging.error('input file is invalid!')
        sys.exit()

    cluster_hist_list = []
    size_hist_list = []

    for icluster_hist in xrange(25):
        cluster_hist_list.append(ROOT.TH1F(title+'cluster%d'%(icluster_hist+1),title+'cluster%d'%(icluster_hist+1),600,0,6000))

    for isize_hist in xrange(7):
        size_hist_list.append(ROOT.TH1F(title+'size%d'%(isize_hist+1),title+'size%d'%(isize_hist+1),600,0,6000))
    

    for cluster_entry in xrange(cluster_entries):
        tmp_list = []
        cluster_tree.GetEntry(cluster_entry)
        for index in xrange(25):
            tmp_list.append(cluster_tree.SingleClusterSignal.at(index))

        tmp_list.sort(reverse=True)
        cluster_adc = 0
        for jndex in xrange(25):
            cluster_adc += tmp_list[jndex]
            cluster_hist_list[jndex].Fill(cluster_adc)

        if cluster_tree.Size < 8 :
            size_hist_list[cluster_tree.Size-1].Fill(cluster_tree.TotalClusterSignal)

    cluster_canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,1800,1200)
    cluster_canvas.cd()

    for ihist in xrange(25):

        if ihist == 0:
            cluster_hist_list[24-ihist].Draw('hist')
            cluster_hist_list[24-ihist].GetYaxis().SetRangeUser(0.,20000.)
        else:
            cluster_hist_list[24-ihist].SetLineStyle(9)
            cluster_hist_list[24-ihist].Draw('hist same')
    cluster_canvas.SaveAs('../fig/test1.gif')

        

    size_canvas = ROOT.TCanvas('size_canvas','size_siganl',200,10,1800,1200)
    size_canvas.cd()

    size_hist_list[3].SetLineColor(4)
    size_hist_list[3].Draw('hist')

    for jhist in xrange(7):
        if jhist !=3 :
            size_hist_list[jhist].SetLineColor(jhist+1)
            size_hist_list[jhist].Draw('hist same')

    
    size_canvas.SaveAs('../fig/test2.gif')



if __name__ == '__main__':
    
    plot('../output/CHIPA1_Cluster55_Iron55_thr500.root','A1')


