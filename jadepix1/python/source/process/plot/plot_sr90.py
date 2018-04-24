#!/usr/bin/env python

'''
plot Sr90 clusters compare hist
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os
import ROOT
ROOT.gStyle.SetOptFit(111111)
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

#get abs for int16 number
def get_int16_abs(number):
    if (number & 0x8000) != 0:  
        abs_number = ((number - 1) ^ 0xFFFF)
    else:
        abs_number = number
    return abs_number


def main(cluster55_fname):
    try:

        cluster55_file = ROOT.TFile(cluster55_fname)
        cluster55_cluster_tree = cluster55_file.Get('Cluster_Tree')
        cluster55_cluster_entries = cluster55_cluster_tree.GetEntries()

    except:
        logging.error('input file is invalid!')
        sys.exit()

    cluster_canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,2400,1200)
    #cluster_legend = ROOT.TLegend(0.75,0.7,0.85,0.85)


    cluster55_cluster_hist = ROOT.TH1F('{}^{90}sr cluster signal','{}^{90}Sr  Cluster Signal',512,0,65536)
    cluster55_cluster_hist.GetXaxis().SetTitle('ADC')
    cluster55_cluster_hist.GetXaxis().CenterTitle()
    cluster55_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    cluster55_cluster_hist.GetYaxis().CenterTitle()
    cluster55_cluster_hist.SetLineColor(4)
    cluster55_cluster_hist.SetLineWidth(2)

    for cluster55_cluster_entry in xrange(cluster55_cluster_entries):
        cluster55_cluster_tree.GetEntry(cluster55_cluster_entry)
        tmp = cluster55_cluster_tree.ClusterSignal
        if tmp < 0:
            tmp = 65536+tmp-1 
        cluster55_cluster_hist.Fill(tmp) 
    cluster55_cluster_hist.Scale(1/cluster55_cluster_hist.Integral())

    fit = ROOT.TF1('fit','landau',0,65536)
    cluster55_cluster_hist.Fit(fit,'R+')

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')


    cluster_canvas.cd()
    cluster55_cluster_hist.Draw('hist')
    fit.Draw('same')
    cluster_canvas.Update()
    cluster_canvas.SaveAs('../fig/Sr90_cluster_chip_a1.gif')


if __name__ == '__main__':
    
    main('../output/CHIPA1_Cluster55_Sr90_thr200_test.root')




