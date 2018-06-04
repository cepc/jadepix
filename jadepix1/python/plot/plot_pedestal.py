#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
plot pedestal
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os,copy
import ROOT
#ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetStatX(0.9)
ROOT.gStyle.SetStatY(0.9)
ROOT.gStyle.SetStatW(0.08)
ROOT.gStyle.SetStatH(0.12)
from prettytable import PrettyTable 
import pandas
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

def get_gauss_parameter(hist,xmin,xmax):
    gauss_fit = ROOT.TF1('gauss_fit','gaus',xmin,xmax)
    hist.Fit('gauss_fit','R')

    gauss_mean = gauss_fit.GetParameter(1)
    gauss_sigma = gauss_fit.GetParameter(2)
    gauss_mean_error = gauss_fit.GetParError(1)
    gauss_sigma_error = gauss_fit.GetParError(2)

    # gauss_mean_str = '%.1f'%gauss_mean + '±' + '%.1f'%gauss_mean_error
    # gauss_sigma_str = '%.1f'%gauss_sigma + '±' + '%.1f'%gauss_sigma_error

    return gauss_mean,gauss_sigma,gauss_mean_error,gauss_sigma_error


def get_th2f(fname,n):

    f = ROOT.TFile(fname)
    t = f.Get('Pedestal_Tree')
    tmp_mean_th2f = ROOT.TH2F('CHIP_A%d_Pedestal_Mean'%n,'',48,0,48,16,0,16)
    tmp_rms_th2f = ROOT.TH2F('CHIP_A%d_Pedestal_RMS'%n,'',48,0,48,16,0,16)
    tmp_gauss_mean_th2f = ROOT.TH2F('CHIP_A%d_Gauss_Mean'%n,'',48,0,48,16,0,16)
    tmp_gauss_sigma_th2f = ROOT.TH2F('CHIP_A%d_Gauss_Sigma'%n,'',48,0,48,16,0,16)

    tmp_hist_list = []

    tmp_address_list = []
    tmp_gauss_mean_list = []
    tmp_gauss_sigma_list = []

    for chanel in xrange(16):
        for row in xrange(48):

            tmp_mean = 0.
            tmp_rms = 0.
            tmp_gauss_mean = 0.
            tmp_gauss_sigma = 0.
            tmp_gauss_mean_error = 0.
            tmp_gauss_sigma_error = 0.

            t.Draw('Chanel_%d_Row_%d>>tmphist(200,-100,100)'%(chanel+1,row+1))
            tmp_hist = ROOT.gROOT.FindObject('tmphist')
            tmp_hist.SetNameTitle('Chanel_%d_Row_%d'%(chanel+1,row+1),'Chanel_%d_Row_%d'%(chanel+1,row+1))

            tmp_mean = tmp_hist.GetMean()
            tmp_rms = tmp_hist.GetRMS()
            tmp_gauss_mean,tmp_gauss_sigma,tmp_gauss_mean_error,tmp_gauss_sigma_error = get_gauss_parameter(tmp_hist,-100,100)

            tmp_mean_th2f.SetBinContent(row+1,chanel+1,tmp_mean)
            tmp_rms_th2f.SetBinContent(row+1,chanel+1,tmp_rms)
            tmp_gauss_mean_th2f.SetBinContent(row+1,chanel+1,tmp_gauss_mean)
            tmp_gauss_sigma_th2f.SetBinContent(row+1,chanel+1,tmp_gauss_sigma)

            tmp_hist_list.append(copy.copy(tmp_hist))

            tmp_address_list.append('Chanel_%d_Row_%d'%(chanel+1,row+1))
            tmp_gauss_mean_list.append('%.2f'%tmp_gauss_mean + '±' + '%.2f'%tmp_gauss_mean_error)
            tmp_gauss_sigma_list.append('%.2f'%tmp_gauss_sigma + '±' + '%.2f'%tmp_gauss_sigma_error)


    dataframe = pandas.DataFrame({'Address' : tmp_address_list,
                                  'Gauss Fit Mean' : tmp_gauss_mean_list,
                                  'Gauss Fit Sigma' : tmp_gauss_sigma_list})
    dataframe.to_csv('./python/output/Iron55_Chip_A%d_Gauss_Fit.csv'%n,index=False,sep=',',encoding='utf_8_sig')



    c_mean_th2f = copy.copy(tmp_mean_th2f)
    c_rms_th2f = copy.copy(tmp_rms_th2f)
    c_gauss_mean_th2f = copy.copy(tmp_gauss_mean_th2f)
    c_gauss_sigma_th2f = copy.copy(tmp_gauss_sigma_th2f)

    return c_mean_th2f,c_rms_th2f,c_gauss_mean_th2f,c_gauss_sigma_th2f,tmp_hist_list



def save_root_file():
    output = ROOT.TFile('./python/output/JadePix_Pedestal.root','RECREATE')

    for ichip in xrange(6):
        mean_th2f,rms_th2f,gauss_mean_th2f,gauss_sigma_th2f,hist_list= get_th2f('./python/output/CHIP_A%d_Pedestal.root'%(ichip+1),ichip+1)
        
        output.cd()
        output.Append(mean_th2f)
        output.Append(rms_th2f)
        output.Append(gauss_mean_th2f)
        output.Append(gauss_sigma_th2f)
        print('*******append*******')

        output.mkdir('CHIP_A%d_hist_fit'%(ichip+1))
        output.cd('CHIP_A%d_hist_fit'%(ichip+1))
        for hist in hist_list:
            hist.Write()

    output.Write()
    output.Close()



def save_fig():

    mean_list = []
    rms_list = []
    gauss_mean_list = []
    gauss_sigma_list = []

    mean_canvas = ROOT.TCanvas('JADEPIX_MEAN','JADEPIX_MEAN',200,10,1000,500)
    rms_canvas = ROOT.TCanvas('JADEPIX_RMS','JADEPIX_RMS',200,10,1000,500)
    gauss_mean_canvas = ROOT.TCanvas('JADEPIX_GAUSS_MEAN','JADEPIX_GAUSS_MEAN',200,10,1000,500)
    gauss_sigma_canvas = ROOT.TCanvas('JADEPIX_GAUSS_SIGMA','JADEPIX_GAUSS_SIGMA',200,10,1000,500)


    for index in xrange(6):
        mean_th2f,rms_th2f,gauss_mean_th2f,gauss_sigma_th2f,hist_list = get_th2f('./python/output/CHIP_A%d_Pedestal.root'%(ichip+1),ichip+1)
        print('*******draw ',ichip+1)
        mean_list.append(mean_th2f)
        rms_list.append(rms_th2f)
        gauss_mean_list.append(gauss_mean_th2f)
        gauss_sigma_list.append(gauss_sigma_th2f)

    for ichip in xrange(6):

        mean_canvas.cd()
        mean_canvas.Clear()
        mean_list[ichip].SetMaximum(0.3)
        mean_list[ichip].Draw('COLZ')
        mean_canvas.Update()
        mean_canvas.SaveAs('./python/fig/Pedestal_mean_chip_a%d.pdf'%(ichip+1))

        rms_canvas.cd()
        rms_canvas.Clear()
        rms_list[ichip].SetMaximum(50.)
        rms_list[ichip].Draw('COLZ')
        rms_canvas.Update()
        rms_canvas.SaveAs('./python/fig/Pedestal_rms_chip_a%d.pdf'%(ichip+1))

        gauss_mean_canvas.cd()
        gauss_mean_canvas.Clear()
        gauss_mean_list[ichip].SetMaximum(1.)
        gauss_mean_list[ichip].Draw('COLZ')
        gauss_mean_canvas.Update()
        gauss_mean_canvas.SaveAs('./python/fig/Pedestal_gauss_mean_chip_a%d.pdf'%(ichip+1))

        gauss_sigma_canvas.cd()
        gauss_sigma_canvas.Clear()
        gauss_sigma_list[ichip].SetMaximum(50)
        gauss_sigma_list[ichip].Draw('COLZ')
        gauss_sigma_canvas.Update()
        gauss_sigma_canvas.SaveAs('./python/fig/Pedestal_gauss_sigma_chip_a%d.pdf'%(ichip+1))


if __name__ == '__main__':
    save_root_file()
    #save_fig()

