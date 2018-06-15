#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
Fit Sr90 signal
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os
import ROOT
ROOT.gStyle.SetOptStat(11)
ROOT.gStyle.SetOptFit(111)
ROOT.gStyle.SetStatX(0.9)
ROOT.gStyle.SetStatY(0.9)
ROOT.gStyle.SetStatW(0.18)
ROOT.gStyle.SetStatH(0.22)
from prettytable import PrettyTable 
import pandas
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# console.setFormatter(logging.Formatter(' %(asctime)s - %(levelname)s- %(message)s'))
# logging.getLogger('').addHandler(console)

def landau_fit(hist,xmin,xmax):

    landau_fit = ROOT.TF1('landau_fit','landau',xmin,xmax)
    hist.Fit(landau_fit,'R0+')

    p = []
    e = []
    for ip in xrange(3):
        p.append(landau_fit.GetParameter(ip))
        e.append(landau_fit.GetParError(ip))

    draw_landau = ROOT.TF1('draw_landau','landau',500,10000)
    draw_landau.SetParameters(p[0],p[1],p[2])
    #hist.Fit(draw_landau,'R+')
    mpv = p[1]
    mpv_error = e[1]
    mpv_str = '%.1f'%mpv + '±' + '%.1f'%mpv_error

    return draw_landau,mpv_str

def main(root_data):

    chip_number = len(root_data)

    chip_address_list = []
    mpv_list = []

    for chip_address in xrange(1,chip_number+1): 

        chip_address_list.append('A%d'%chip_address)

        try:
            #get TTree
            tmp_source_file = ROOT.TFile(root_data['a%d'%chip_address][0])
            tmp_cluster_tree = tmp_source_file.Get('Cluster_Tree')
            tmp_cluster_entries = tmp_cluster_tree.GetEntries()

        except:
            logging.error('input file is invalid!')
            sys.exit()

        canvas = ROOT.TCanvas('canvas_%d'%chip_address,'cluster_siganl',200,10,2000,1200)

        bin_number = 1400
        tmp_cluster_hist = ROOT.TH1F('CHIP A%d {}^{90}sr cluster signal'%chip_address,'',bin_number,0,10000)
        tmp_cluster_hist.GetXaxis().SetTitle('ADC')
        tmp_cluster_hist.GetXaxis().CenterTitle()
        tmp_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
        tmp_cluster_hist.GetYaxis().CenterTitle()
        tmp_cluster_hist.SetLineColor(4)
        tmp_cluster_hist.SetLineWidth(1)

        for tmp_cluster_entry in xrange(tmp_cluster_entries):
            tmp_cluster_tree.GetEntry(tmp_cluster_entry)
            tmp = tmp_cluster_tree.TotalClusterSignal
            tmp_cluster_hist.Fill(tmp) 
        tmp_cluster_hist.Scale(1/tmp_cluster_hist.Integral())


        xmin = 500
        xmax = 10000

        fit,mpv = landau_fit(tmp_cluster_hist,xmin,xmax)
        mpv_list.append(mpv)

        if not os.path.exists('./python/fig/'):
            os.makedirs('./python/fig/')

        canvas.cd()
        tmp_cluster_hist.Draw('hist')
        fit.Draw('same')
        canvas.Update()
        canvas.SaveAs('./python/fig/Sr90_Chip_A%d_Fit.pdf'%chip_address)

    mpv_table = PrettyTable()
    mpv_table.add_column('Chip address',chip_address_list)
    mpv_table.add_column('MPV',mpv_list)
    print('\n\n********************************\n********************************')
    print(mpv_table)

    dataframe = pandas.DataFrame({'Chip address' : chip_address_list,
                                  'MPV' : mpv_list})
    dataframe.to_csv("./python/output/Sr90_MPV.csv",index=False,sep=',',encoding='utf_8_sig')


if __name__ == '__main__':

    root_data = { 'a1' : ['./python/output/CHIPA1_Cluster55_Sr90_thr500.root'],
                  'a2' : ['./python/output/CHIPA2_Cluster55_Sr90_thr500.root'],
                  'a3' : ['./python/output/CHIPA3_Cluster55_Sr90_thr500.root'],
                  'a4' : ['./python/output/CHIPA4_Cluster55_Sr90_thr500.root'],
                  'a5' : ['./python/output/CHIPA5_Cluster55_Sr90_thr500.root'],
                  'a6' : ['./python/output/CHIPA6_Cluster55_Sr90_thr500.root']}

    main(root_data)
    


