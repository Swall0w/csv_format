import codecs
import sys
import os

import chardet
from io import StringIO
import pandas as pd

def main ():
    readfile = sys.argv[1]
    with open(readfile,mode='rb') as f:
        binary = f.read()
        detect = chardet.detect(binary)
        print(detect)
        print(detect['encoding'])
    text = binary.decode(detect['encoding']).encode('utf-8').decode('utf-8')

    print(text[:100])
    index = text[:20].find('仕訳日記帳')
    if index != -1:
        print('found at ',index)
        index = text[:100].find('日付')
        if index != -1:
            print('rm str: ',text[:index -1])
            text = text[index -1:]
        else:
            pass
    else:
        print('not found')
        
    text = StringIO(text)

    df = pd.read_csv(text,sep=',')
    df.to_csv('result.csv',index=False)

#    sjisfile = sys.argv[1]
#    utf8file = 'result.csv'
#
#    fin = codecs.open(sjisfile,'r','shift-jis')
#    fout = codecs.open(utf8file,'w','utf-8')
#    for row in fin:
#        fout.write(row.encode('utf-8','ignore').decode('shift-jis'))
#    fin.close()
#    fout.close()

if __name__ == '__main__':
    main()


