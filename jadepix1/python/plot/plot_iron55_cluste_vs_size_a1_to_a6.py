#!/usr/bin/env python

'''
plot Iron55 clusters 2D
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


def plot(fname):

    try:
        file = ROOT.TFile(fname)

        cluster_canvas = ROOT.TCanvas('cluster_canvas','cluster_signal',200,10,4800,3600)
        size_canvas = ROOT.TCanvas('size_canvas','size_signal',200,10,4800,3600)

        cluster_canvas.Divide(2,3)
        size_canvas.Divide(2,3)

        for chip_address in xrange(1,4):

            tmp_cluster_th2f = file.Get('CHIP_A%d_CLUSTER_2D'%chip_address)
            tmp_cluster_th2f.SetTitle('CHIP A%d'%chip_address)
            cluster_canvas.cd(2*chip_address-1)
            tmp_cluster_th2f.Draw('colz')

            tmp_size_th2f = file.Get('CHIP_A%d_SIZE_2D'%chip_address)
            tmp_size_th2f.SetTitle('CHIP A%d'%chip_address)
            size_canvas.cd(2*chip_address-1)
            tmp_size_th2f.Draw('colz') 

        for chip_address in xrange(4,7):

            tmp_cluster_th2f = file.Get('CHIP_A%d_CLUSTER_2D'%chip_address)
            tmp_cluster_th2f.SetTitle('CHIP A%d'%chip_address)
            cluster_canvas.cd(2*chip_address-6)
            tmp_cluster_th2f.Draw('colz')

            tmp_size_th2f = file.Get('CHIP_A%d_SIZE_2D'%chip_address)
            tmp_size_th2f.SetTitle('CHIP A%d'%chip_address)
            size_canvas.cd(2*chip_address-6)
            tmp_size_th2f.Draw('colz') 

        cluster_canvas.SaveAs('./python/fig/Iron55_numberpixs_2D.pdf')
        size_canvas.SaveAs('./python/fig/Iron55_size_2D.pdf')    

    except:
        logging.error('input file is invalid!')
        sys.exit()



    # cluster_legend = ROOT.TLegend(0.75,0.75,0.90,0.90)
    # size_legend = ROOT.TLegend(0.75,0.75,0.90,0.90)

    # a1_cluster_th2f = copy.copy(cluster_th2f_list[0])
    # a1_cluster_th2f.SetFillColor(2)
    # a1_cluster_th2f.SetMarkerColor(2)
    # cluster_legend.AddEntry(a1_cluster_th2f,' CHIP A1 ','f')       
    # a1_cluster_th2f.Draw()

    # a2_cluster_th2f = copy.copy(cluster_th2f_list[1])
    # a2_cluster_th2f.SetFillColor(3)
    # a2_cluster_th2f.SetMarkerColor(3)
    # cluster_legend.AddEntry(a2_cluster_th2f,' CHIP A2 ','f')       
    # a2_cluster_th2f.Draw('same')

    # a3_cluster_th2f = copy.copy(cluster_th2f_list[2])
    # a3_cluster_th2f.SetFillColor(4)
    # a3_cluster_th2f.SetMarkerColor(4)
    # cluster_legend.AddEntry(a3_cluster_th2f,' CHIP A3 ','f')       
    # a3_cluster_th2f.Draw('same')

    # cluster_legend.Draw()
    # tmp_cluster_canvas.Update()
    # tmp_cluster_canvas.SaveAs('./python/fig/test.gif')


if __name__ == '__main__':
    plot('./python/output/Iron55_Cluster_ADC_2D.root')


