import os,sys,re,traceback
from datetime import datetime
from string import Template

def generate(title):
    
    template_file = open(r'./python/src/template_job','r')
    tmpl = Template(template_file.read())

    src = './python/src/src_a1_sr90/%s.py'%title

    lines = []
    lines.append(tmpl.substitute(SRC = src))

    if not os.path.exists('./python/run/jobs_a1_sr90/'):
        os.makedirs('./python/run/jobs_a1_sr90/')

    job_file_name = './python/run/jobs_a1_sr90/Job_%s'%title
    job_file = open(job_file_name,'w')

    job_file.writelines(lines)
    job_file.close()

    print('generate job file : ',job_file_name)


def main(input_dir):

    for parent,dirnames,filenames in os.walk(input_dir):
        for filename in filenames:

            title_regex = re.compile(r'(.*)(CHIPA1)(.*)(.df)')
            match = title_regex.search(filename)

            if match:

                title = match.group(1)+match.group(2)+match.group(3)

                generate(title)


if __name__ == '__main__':
    main('/publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180502/')