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
        #cluster_entries = cluster_tree.GetEntries()
        cluster_entries = 2000000

    except:
        logging.error('input file is invalid!')
        sys.exit()

    cluster_th2f = ROOT.TH2F('CHIP_%s_ClUSTER_2D'%title,'',25,0,25,500,0,5000)
    cluster_th2f.GetXaxis().SetTitle('Number of pixels in cluster')
    cluster_th2f.GetXaxis().CenterTitle()
    cluster_th2f.GetYaxis().SetTitle('ADC')
    cluster_th2f.GetYaxis().CenterTitle()

    size_th2f = ROOT.TH2F('CHIP_%s_SIZE_2D'%title,'',500,0,5000,25,0,25)
    size_th2f.GetXaxis().SetTitle('ADC')
    size_th2f.GetXaxis().CenterTitle()
    size_th2f.GetYaxis().SetTitle('Cluster size')
    size_th2f.GetYaxis().CenterTitle()

    for cluster_entry in xrange(cluster_entries):
        tmp_list = []
        cluster_tree.GetEntry(cluster_entry)
        for index in xrange(25):
            tmp_list.append(cluster_tree.SingleClusterSignal.at(index))

        tmp_list.sort(reverse=True)
        cluster_adc = 0
        for jndex in xrange(25):
            cluster_adc += tmp_list[jndex]
            cluster_th2f.Fill(jndex+1,cluster_adc)

        size_th2f.Fill(cluster_tree.TotalClusterSignal,cluster_tree.Size)

    c_cluster_th2f = copy.copy(cluster_th2f)
    c_size_th2f = copy.copy(size_th2f)

    return c_cluster_th2f,c_size_th2f

def save_root():
    output = ROOT.TFile('./python/output/Iron55_Cluster_ADC_2D.root','recreate')
    for chip_address in xrange(1,7):
        cluster_th2f,size_th2f = plot('./python/output/CHIPA%d_Cluster55_Iron55_thr500.root'%chip_address,'A%d'%chip_address)
        output.Append(cluster_th2f)
        output.Append(size_th2f)
        print('save root A%d'%chip_address)
    output.Write()
    output.Close()


def save_fig():
    tmp_cluster_canvas = ROOT.TCanvas('cluster_canvas','cluster_signal',200,10,2400,1200)
    tmp_size_canvas = ROOT.TCanvas('size_canvas','size_signal',200,10,2400,1200)

    for chip_address in xrange(1,7):
        cluster_th2f,size_th2f = plot('./python/output/CHIPA%d_Cluster55_Iron55_thr500.root'%chip_address,'A%d'%chip_address)

        tmp_cluster_canvas.Clear()
        tmp_cluster_canvas.cd()
        cluster_th2f.SetMinimum(-1)
        cluster_th2f.Draw('COLZ')
        tmp_cluster_canvas.Update()
        tmp_cluster_canvas.SaveAs('./python/fig/Iron55_numberpixs_2D_chip_A%d.pdf'%chip_address)

        tmp_size_canvas.Clear()
        tmp_size_canvas.cd()
        #size_th2f.SetMinimum(-1)
        size_th2f.Draw('COLZ')
        tmp_size_canvas.Update()
        tmp_size_canvas.SaveAs('./python/fig/Iron55_size_2D_chip_A%d.pdf'%chip_address)

        print('save fig A%d'%chip_address)      

# def save_test_fig():
#     tmp_cluster_canvas = ROOT.TCanvas('cluster_canvas','cluster_signal',200,10,2400,1200)
#     tmp_size_canvas = ROOT.TCanvas('size_canvas','size_signal',200,10,2400,1200)
#     legend = ROOT.TLegend(0.65,0.6,0.85,0.85)

#     a1_cluster_th2f,a1_size_th2f = plot('./python/output/CHIPA1_Cluster55_Iron55_thr500.root','A1')
#     a2_cluster_th2f,a2_size_th2f = plot('./python/output/CHIPA2_Cluster55_Iron55_thr500.root','A2')
#     a3_cluster_th2f,a3_size_th2f = plot('./python/output/CHIPA3_Cluster55_Iron55_thr500.root','A3')

#     a1_cluster_th2f.SeFillColor(2)
#     a1_size_th2f.SeFillColor(2)

#     a2_cluster_th2f.SeFillColor(3)
#     a2_size_th2f.SeFillColor(3)

#     a3_cluster_th2f.SeFillColor(4)
#     a3_size_th2f.SeFillColor(4)        

#     legend.AddEntry(a1_cluster_th2f,' CHIP A1 ')
#     legend.AddEntry(a2_cluster_th2f,' CHIP A2 ')
#     legend.AddEntry(a3_cluster_th2f,' CHIP A3 ')

#     tmp_cluster_canvas.cd()
#     a1_cluster_th2f.Draw()
#     a2_cluster_th2f.Draw('same')
#     a3_cluster_th2f.Draw('same')
#     #legend.Draw()
#     tmp_cluster_canvas.Update()
#     tmp_cluster_canvas.SaveAs('./python/fig/test.gif')
    
    

if __name__ == '__main__':
    
    save_root()
    save_fig()
    # save_test_fig()


