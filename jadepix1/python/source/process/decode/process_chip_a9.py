import sys,os
import re
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
from multiprocessing import Process
from decode_iron55 import Decode

def main(input_dir,output_dir):

    decode_list = []
    process_list = []

    decode_count = 0
    process_count = 0

    for parent,dirnames,filenames in os.walk(input_dir):
        for filename in filenames:

            title_regex = re.compile(r'(.*)(CHIPA9)(.*)(.df)')
            match = title_regex.search(filename)

            if match:

                input = os.path.join(input_dir,filename)
                decode_count += 1
                logging.info('input %d files : %s'%(decode_count,input))

                title = match.group(1)+match.group(2)+match.group(3)
                output = os.path.join(output_dir,'Cluster55_'+title+'_Thr500_ex.root')
                logging.info('output files : %s\n'%(output))

                tmp_decode = Decode(input,output)
                decode_list.append(tmp_decode)

    for idecode in decode_list:
        process_count += 1    
        tmp_process = Process(target = idecode.run,name = 'p%d'%process_count)
        process_list.append(tmp_process)


    for iprocess in process_list:
        iprocess.start()


if __name__ == '__main__':
   
    main('/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180403/','../output/chip_a9/')
