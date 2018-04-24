#!/usr/bin/env python

'''
cce
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os
import numpy as np
import ROOT
# ROOT.gStyle.SetOptStat(0)
# ROOT.gStyle.SetStatX(0.9)
# ROOT.gStyle.SetStatY(0.9)
# ROOT.gStyle.SetStatW(0.08)
# ROOT.gStyle.SetStatH(0.12)
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# console.setFormatter(logging.Formatter(' %(asctime)s - %(levelname)s- %(message)s'))
# logging.getLogger('').addHandler(console)


def gauss_fun(const,mean,sigma,x):  
    y = const*np.exp(-(x-mean)**2/(2*sigma**2))
    return y


def double_gauss_fit(model,hist,max_peak,min_peak):
    
    if model == 1:
        t1 = 1
        t2 = 1
        t3 = 0 
        t4 = 1
    if model == 2:
        t1 = 1
        t2 = 1
        t3 = 1
        t4 = 1

    gauss1 = ROOT.TF1('gauss1','gaus',max_peak-200*t1,max_peak+100*t2)
    gauss2 = ROOT.TF1('gauss2','gaus',min_peak-50*t3,min_peak+100*t4)

    gauss1.SetParameter(1,max_peak)
    gauss2.SetParameter(1,min_peak)

    hist.Fit(gauss1,'R0')
    hist.Fit(gauss2,'R0+')

    p = []
    for ip1 in xrange(3):
        p.append(gauss1.GetParameter(ip1))
    for ip2 in xrange(3):
        p.append(gauss2.GetParameter(ip2))

    double_gauss = ROOT.TF1('double_gauss','gaus(0)+gaus(3)',max_peak-100*t1,min_peak+100)
    double_gauss.SetParameters(p[0],p[1],p[2],p[3],p[4],p[5])
    hist.Fit(double_gauss,'R0+')
    for ip in xrange(6):
        p[ip] = double_gauss.GetParameter(ip)

    #print(p)
    draw_gauss1 = ROOT.TF1('draw_gauss1','gaus',0,6000)
    draw_gauss1.SetParameters(p[0],p[1],p[2])
    draw_gauss1.SetLineColor(1)
    draw_gauss1.SetLineStyle(9)

    draw_gauss2 = ROOT.TF1('draw_gauss2','gaus',0,6000)
    draw_gauss2.SetParameters(p[3],p[4],p[5])
    draw_gauss2.SetLineColor(1)
    draw_gauss2.SetLineStyle(9)

    draw_double_gauss = ROOT.TF1('draw_double_gauss','gaus(0)+gaus(3)',0,6000)
    draw_double_gauss.SetParameters(p[0],p[1],p[2],p[3],p[4],p[5])
    draw_double_gauss.SetLineColor(1)
    draw_double_gauss.SetLineStyle(9)

    return p,draw_gauss1,draw_gauss2,draw_double_gauss


def calculate_cce(model,p,hist,title):

    gaus1_hist = ROOT.TH1F('gaus1','gaus1',600,0,6000)
    for ibin in xrange(1,601):
        tmp_c1 = gauss_fun(p[0],p[1],p[2],ibin*10)
        gaus1_hist.SetBinContent(ibin,tmp_c1)

    gaus2_hist = ROOT.TH1F('gaus2','gaus2',600,0,6000)
    for jbin in xrange(1,601):
        tmp_c2 = gauss_fun(p[3],p[4],p[5],jbin*10)
        gaus2_hist.SetBinContent(jbin,tmp_c2)

    i1 = gaus1_hist.Integral()
    i2 = gaus2_hist.Integral()
    i = hist.Integral()
    # print(i1)
    # print(i2)
    # print(i)
    if model == 1:
        cce = i1/i
    if model == 2:
        cce = (i1+i2)/i
    print(title+' cce : ',cce)
    return cce 


def save_fig(model,gaus1,gaus2,double_gauss,hist,title):
    canvas = ROOT.TCanvas('%s_canvas'%title,'fit',200,10,2000,1200)
    canvas.cd()
    gaus1.SetTitle('%s_Fit'%title)
    gaus1.Draw('C')
    if model == 2:
        gaus2.Draw('same')
    hist.Draw('hist same')
    canvas.Update()
    canvas.SaveAs('../fig/%s_fit.gif'%title)

    d_canvas = ROOT.TCanvas('%s_d_canvas'%title,'double gauss fit',200,10,2000,1200)
    d_canvas.cd()
    double_gauss.SetTitle('%s_Double_Gauss_Fit'%title)
    double_gauss.Draw('C')
    hist.Draw('hist same')
    d_canvas.Update()
    d_canvas.SaveAs('../fig/%s_double_gauss_fit.gif'%title)


def process(model,title,hist,max_peak,min_peak):

    p,gaus1,gaus2,double_gauss = double_gauss_fit(model,hist,max_peak,min_peak)
    cce = calculate_cce(model,p,hist,title)
    save_fig(model,gaus1,gaus2,double_gauss,hist,title)

    
def main():

    f = ROOT.TFile('../output/CHIP_A1_To_A6_Cluster55_Hist.root')


    a1_cluster_hist = f.Get('a1 cluster signal')
    a1_cluster_hist.GetXaxis().SetTitle('ADC')
    a1_cluster_hist.GetXaxis().CenterTitle()
    a1_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_cluster_hist.GetYaxis().CenterTitle()
    a1_cluster_hist.SetLineColor(2)
    a1_cluster_hist.SetLineWidth(2)

    a1_noise_hist = f.Get('a1 noise signal')
    a1_noise_hist.GetXaxis().SetTitle('ADC')
    a1_noise_hist.GetXaxis().CenterTitle()
    a1_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a1_noise_hist.GetYaxis().CenterTitle()
    a1_noise_hist.SetLineColor(2)
    a1_noise_hist.SetLineStyle(9)
    a1_noise_hist.SetLineWidth(2) 


    a2_cluster_hist = f.Get('a2 cluster signal')
    a2_cluster_hist.GetXaxis().SetTitle('ADC')
    a2_cluster_hist.GetXaxis().CenterTitle()
    a2_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_cluster_hist.GetYaxis().CenterTitle()
    a2_cluster_hist.SetLineColor(3)
    a2_cluster_hist.SetLineWidth(2)

    a2_noise_hist = f.Get('a2 noise signal')
    a2_noise_hist.GetXaxis().SetTitle('ADC')
    a2_noise_hist.GetXaxis().CenterTitle()
    a2_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a2_noise_hist.GetYaxis().CenterTitle()
    a2_noise_hist.SetLineColor(3)
    a2_noise_hist.SetLineStyle(9)
    a2_noise_hist.SetLineWidth(2)


    a3_cluster_hist = f.Get('a3 cluster signal')
    a3_cluster_hist.GetXaxis().SetTitle('ADC')
    a3_cluster_hist.GetXaxis().CenterTitle()
    a3_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_cluster_hist.GetYaxis().CenterTitle()
    a3_cluster_hist.SetLineColor(4)
    a3_cluster_hist.SetLineWidth(2)

    a3_noise_hist = f.Get('a3 noise signal')
    a3_noise_hist.GetXaxis().SetTitle('ADC')
    a3_noise_hist.GetXaxis().CenterTitle()
    a3_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a3_noise_hist.GetYaxis().CenterTitle()
    a3_noise_hist.SetLineColor(4)
    a3_noise_hist.SetLineStyle(9)
    a3_noise_hist.SetLineWidth(2)


    a4_cluster_hist = f.Get('a4 cluster signal')
    a4_cluster_hist.GetXaxis().SetTitle('ADC')
    a4_cluster_hist.GetXaxis().CenterTitle()
    a4_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_cluster_hist.GetYaxis().CenterTitle()
    a4_cluster_hist.SetLineColor(6)
    a4_cluster_hist.SetLineWidth(2)

    a4_noise_hist = f.Get('a4 noise signal')
    a4_noise_hist.GetXaxis().SetTitle('ADC')
    a4_noise_hist.GetXaxis().CenterTitle()
    a4_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a4_noise_hist.GetYaxis().CenterTitle()
    a4_noise_hist.SetLineColor(6)
    a4_noise_hist.SetLineStyle(9)
    a4_noise_hist.SetLineWidth(2) 


    a5_cluster_hist = f.Get('a5 cluster signal')
    a5_cluster_hist.GetXaxis().SetTitle('ADC')
    a5_cluster_hist.GetXaxis().CenterTitle()
    a5_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_cluster_hist.GetYaxis().CenterTitle()
    a5_cluster_hist.SetLineColor(7)
    a5_cluster_hist.SetLineWidth(2)

    a5_noise_hist = f.Get('a5 noise signal')
    a5_noise_hist.GetXaxis().SetTitle('ADC')
    a5_noise_hist.GetXaxis().CenterTitle()
    a5_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a5_noise_hist.GetYaxis().CenterTitle()
    a5_noise_hist.SetLineColor(7)
    a5_noise_hist.SetLineStyle(9)
    a5_noise_hist.SetLineWidth(2)


    a6_cluster_hist = f.Get('a6 cluster signal')
    a6_cluster_hist.GetXaxis().SetTitle('ADC')
    a6_cluster_hist.GetXaxis().CenterTitle()
    a6_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_cluster_hist.GetYaxis().CenterTitle()
    a6_cluster_hist.SetLineColor(8)
    a6_cluster_hist.SetLineWidth(2)

    a6_noise_hist = f.Get('a6 noise signal')
    a6_noise_hist.GetXaxis().SetTitle('ADC')
    a6_noise_hist.GetXaxis().CenterTitle()
    a6_noise_hist.GetYaxis().SetTitle('Normalized Counts')
    a6_noise_hist.GetYaxis().CenterTitle()
    a6_noise_hist.SetLineColor(8)
    a6_noise_hist.SetLineStyle(9)
    a6_noise_hist.SetLineWidth(2)


    #######
    a1_iron55_peak = a1_cluster_hist.GetMaximumBin()*10
    a1_noise_peak = a1_noise_hist.GetMaximumBin()*10
    print('a1 iron55 peak : ',a1_iron55_peak)
    print('a1 noise peak : ',a1_noise_peak)

    a2_iron55_peak = a2_cluster_hist.GetMaximumBin()*10
    a2_noise_peak = a2_noise_hist.GetMaximumBin()*10
    print('a2 iron55 peak : ',a2_iron55_peak)
    print('a2 noise peak : ',a2_noise_peak)

    a3_iron55_peak = a3_cluster_hist.GetMaximumBin()*10
    a3_noise_peak = a3_noise_hist.GetMaximumBin()*10
    print('a3 iron55 peak : ',a3_iron55_peak)
    print('a3 noise peak : ',a3_noise_peak)

    a4_iron55_peak = a4_cluster_hist.GetMaximumBin()*10
    a4_noise_peak = a4_noise_hist.GetMaximumBin()*10
    print('a4 iron55 peak : ',a4_iron55_peak)
    print('a4 noise peak : ',a4_noise_peak)

    a5_iron55_peak = a5_cluster_hist.GetMaximumBin()*10
    a5_noise_peak = a5_noise_hist.GetMaximumBin()*10
    print('a5 iron55 peak : ',a5_iron55_peak)
    print('a5 noise peak : ',a5_noise_peak)

    a6_iron55_peak = a6_cluster_hist.GetMaximumBin()*10
    a6_noise_peak = a6_noise_hist.GetMaximumBin()*10
    print('a6 iron55 peak : ',a6_iron55_peak)
    print('a6 noise peak : ',a6_noise_peak)
    ########

    process(2,'CHIP_A1',a1_cluster_hist,3520,3849)
    process(2,'CHIP_A2',a2_cluster_hist,3100,3384)
    process(1,'CHIP_A3',a3_cluster_hist,2310,2280)
    process(2,'CHIP_A4',a4_cluster_hist,3520,3846)
    process(2,'CHIP_A5',a5_cluster_hist,2810,3070)
    process(1,'CHIP_A6',a6_cluster_hist,1790,1948)


if __name__=='__main__':
    main()