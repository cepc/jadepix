import os,sys,re,traceback
from datetime import datetime
from string import Template

def generate(title,input,output):
    
    template_file = open(r'./python/src/template_sr90_script.py','r')
    tmpl = Template(template_file.read())
    lines = []
    lines.append(tmpl.substitute(INPUT = input,\
                                 OUTPUT= output))

    if not os.path.exists('./python/src/src_a1_sr90/'):
        os.makedirs('./python/src/src_a1_sr90/')

    python_file_name = './python/src/src_a1_sr90/%s.py'%title
    python_file = open(python_file_name,'w')

    python_file.writelines(lines)
    python_file.close()

    print('generate python file : ',python_file_name)


def main(input_dir,output_dir):

    for parent,dirnames,filenames in os.walk(input_dir):
        for filename in filenames:

            title_regex = re.compile(r'(.*)(CHIPA1)(.*)(.df)')
            match = title_regex.search(filename)

            if match:

                input = os.path.join(input_dir,filename)

                title = match.group(1)+match.group(2)+match.group(3)
                output = os.path.join(output_dir,'Cluster55_'+title+'_Thr200_ex.root')

                generate(title,input,output)


if __name__ == '__main__':

    if not os.path.exists('./python/output/output_a1_sr90/'):
        os.makedirs('./python/output/output_a1_sr90/')

    main('/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180502/','./python/output/output_a1_sr90')