#!/usr/bin/env python

import os,sys,re,traceback
from datetime import datetime
from string import Template

def generate(chip_address,title,input,output):
    
    template_file = open(r'./python/src/template_iron55_script.py','r')
    tmpl = Template(template_file.read())
    lines = []
    lines.append(tmpl.substitute(INPUT = input,\
                                 OUTPUT= output))
    if not os.path.exists('./python/src/src_%s_iron55/'%chip_address):
        os.makedirs('./python/src/src_%s_iron55/'%chip_address)
    python_file_name = './python/src/src_%s_iron55/%s.py'%(chip_address,title)
    python_file = open(python_file_name,'w')
    python_file.writelines(lines)
    python_file.close()
    print('generate python file : ',python_file_name)


def run(chip_address,input_dir,output_dir):

    for parent,dirnames,filenames in os.walk(input_dir):
        for filename in filenames:
            title_regex = re.compile(r'(.*)(CHIP%s)(.*)(.df)'%chip_address.upper())
            match = title_regex.search(filename)
            if match:
                input = os.path.join(input_dir,filename)
                title = match.group(1)+match.group(2)+match.group(3)
                output = os.path.join(output_dir,'Cluster55_'+title+'_Thr200_ex.root')
                generate(chip_address.lower(),title,input,output)


if __name__ == '__main__':

    source_data_dir = {'a1':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180329/'],
                       'a2':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180331/'],
                       'a3':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180331/'],
                       'a4':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180329/'],
                       'a5':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180331/','/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180403/'],
                       'a6':['/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180331/']}

    if len(sys.argv) < 2:  
        print('No chip address specified!')  
        sys.exit() 

    if len(sys.argv) == 2:
        if sys.argv[1].startswith('-a'):
            chip_address = sys.argv[1][1:]
            print('Set chip address to %s'%chip_address.upper())

            if not os.path.exists('./python/output/output_%s_iron55/'%chip_address.lower()):
                os.makedirs('./python/output/output_%s_iron55/'%chip_address.lower())
                
            for input_dir in source_data_dir[chip_address.lower()]:
                run(chip_address,input_dir,'./python/output/output_%s_iron55/'%chip_address.lower())

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
                if not os.path.exists('./python/output/output_%s_iron55/'%chip_address.lower()):
                    os.makedirs('./python/output/output_%s_iron55/'%chip_address.lower())
                    
                for input_dir in source_data_dir[chip_address.lower()]:
                    run(chip_address,input_dir,'./python/output/output_%s_iron55/'%chip_address.lower())

        else:
            print('Chip address is invalid!')
            sys.exit()

