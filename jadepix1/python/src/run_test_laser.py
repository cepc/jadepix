#!/usr/bin/env python

import sys,os
import re
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
sys.path.append("./python/lib/")  
from decode_laser import Decode

def main():


    input = '/home/yangtao/test/laser_test_intensity_40_180725175238.df'
    output = 'test_55_cluster.root'

    decode = Decode(input,output)
    decode.run()


if __name__ == '__main__':
    main()