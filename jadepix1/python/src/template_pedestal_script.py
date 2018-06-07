import sys,os
import re
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
sys.path.append("./python/lib/")  
from decode_pedestal import Decode

def main():

    if not os.path.exists('./output/'):
        os.makedirs('./output/')

    input = '${INPUT}'
    output = '${OUTPUT}'

    decode = Decode(input,output)
    decode.run()


if __name__ == '__main__':
    main()
