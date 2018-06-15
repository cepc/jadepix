#!/usr/bin/env python

import os,sys,re,traceback
from datetime import datetime
from string import Template

def generate(chip_address,title):
    
    template_file = open(r'./python/src/template_job','r')
    tmpl = Template(template_file.read())

    src = './python/src/src_%s_pedestal/%s.py'%(chip_address,title)

    if not os.path.exists('./python/run/jobs_%s_pedestal/'%chip_address):
        os.makedirs('./python/run/jobs_%s_pedestal/'%chip_address)

    lines = []
    lines.append(tmpl.substitute(SRC = src))

    job_file_name = './python/run/jobs_%s_pedestal/Job_%s'%(chip_address,title)
    job_file = open(job_file_name,'w')

    job_file.writelines(lines)
    job_file.close()

    print('generate job file : ',job_file_name)


def run(chip_address,input_dir):

    for parent,dirnames,filenames in os.walk(input_dir):
        for filename in filenames:
            title_regex = re.compile(r'(.*)(CHIP%s)(.*)(.df)'%chip_address.upper())
            match = title_regex.search(filename)

            if match:
                title = match.group(1)+match.group(2)+match.group(3)
                generate(chip_address.lower(),title)


if __name__ == '__main__':

    source_data_dir = {'a1':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180329/'],\
                       'a2':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180331/'],\
                       'a3':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180331/'],\
                       'a4':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180329/'],\
                       'a5':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180331/','/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180403/'],\
                       'a6':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180331/']}

    if len(sys.argv) < 2:  
        print('No chip address specified!')  
        sys.exit() 

    if len(sys.argv) == 2:
        if sys.argv[1].startswith('-a'):
            chip_address = sys.argv[1][1:]
            print('Set chip address to %s'%chip_address.upper())

            for input_dir in source_data_dir[chip_address.lower()]:  
                run(chip_address,input_dir)

        else:
            print('Chip address is invalid!')
            sys.exit()   
            
    if len(sys.argv) == 3:
        if (sys.argv[1].startswith('-a') and sys.argv[2].startswith('-a')):
            chip_address_start = sys.argv[1][1:]
            chip_address_end = sys.argv[2][1:]
            chip_address_start_number = int(sys.argv[1][2:])
            chip_address_end_number = int(sys.argv[2][2:])

            if (chip_address_start_number > chip_address_end_number):
                print('chip_address_end_number have to large than chip_address_start_number!')
                sys.exit()

            print('Set chip address from %s to %s .'%(chip_address_start.upper(),chip_address_end.upper()))

            for address_number in xrange(chip_address_start_number,chip_address_end_number+1):                
                chip_address = 'a%d'%address_number
                for input_dir in source_data_dir[chip_address.lower()]:  
                    run(chip_address,input_dir)

        else:
            print('Chip address is invalid!')
            sys.exit()

    