#!/usr/bin/env python

import sys,os,copy
import ROOT
ROOT.gStyle.SetOptFit()
ROOT.gStyle.SetStatX(0.9)
ROOT.gStyle.SetStatY(0.9)
ROOT.gStyle.SetStatW(0.08)
ROOT.gStyle.SetStatH(0.12)
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def get_th2f(fname,n):

    f = ROOT.TFile(fname)
    t = f.Get('Noise_Tree')
    tmp_mean_th2f = ROOT.TH2F('CHIP_A%d_MEAN'%n,'CHIP_A%d_MEAN'%n,48,0,48,16,0,16)
    tmp_rms_th2f = ROOT.TH2F('CHIP_A%d_RMS'%n,'CHIP_A%d_RMS'%n,48,0,48,16,0,16)

    for chanel in xrange(16):
        for row in xrange(48):

            tmp_mean = 0.
            tmp_rms = 0.

            t.Draw('Chanel_%d_Row_%d>>tmphist(1000,0,1000)'%(chanel+1,row+1))
            tmp_hist = ROOT.gROOT.FindObject('tmphist')
            tmp_mean = tmp_hist.GetMean()
            tmp_rms = tmp_hist.GetRMS()
            #print('mean : ',tmp_mean,'   rms : ',tmp_rms)
            tmp_mean_th2f.SetBinContent(row+1,chanel+1,tmp_mean)
            tmp_rms_th2f.SetBinContent(row+1,chanel+1,tmp_rms)

    c_mean_th2f = copy.copy(tmp_mean_th2f)
    c_rms_th2f = copy.copy(tmp_rms_th2f)

    return c_mean_th2f,c_rms_th2f

def save_root_file():
    output = ROOT.TFile('../output/JadePix_Noise.root','RECREATE')

    # mean_list = []
    # rms_list = []

    for ichip in xrange(6):
        mean_th2f,rms_th2f = get_th2f('../output/CHIP_A%d_Noise.root'%(ichip+1),ichip+1)
        # mean_list.append(mean_th2f)
        # rms_list.append(rms_th2f)
        output.Append(mean_th2f)
        output.Append(rms_th2f)
        print('*******append*******')
    output.Write()
    output.Close()

def save_fig():

    mean_list = []
    rms_list = []

    mean_canvas = ROOT.TCanvas('JADEPIX_MEAN','JADEPIX_MEAN',200,10,2000,1500)
    rms_canvas = ROOT.TCanvas('JADEPIX_RMS','JADEPIX_RMS',200,10,1000,1500)
    mean_canvas.Divide(2,3)
    rms_canvas.Divide(2,3)


    for ichip in xrange(6):
        mean_th2f,rms_th2f = get_th2f('../output/CHIP_A%d_Noise.root'%(ichip+1),ichip+1)
        print('*******draw ',ichip+1)
        mean_list.append(mean_th2f)
        rms_list.append(rms_th2f)

    for ichip in xrange(6):
        mean_canvas.cd(ichip+1)
        mean_list[ichip].Draw('COLZ')
        mean_list[ichip].SetMaximum(100)
        mean_canvas.Update()
    mean_canvas.SaveAs('../fig/jadepix_mean.gif')

    # for jchip in xrange(6):
    #     rms_canvas.cd(jchip+1)
    #     rms_list[jchip].Draw('COLZ')
    #     rms_list[jchip].SetMaximum(100)
    #     rms_canvas.Update()
    # rms_canvas.SaveAs('../fig/jadepix_rms.gif')


if __name__ == '__main__':
    #save_root_file()
    save_fig()

