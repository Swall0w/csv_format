import codecs
import sys
import os

def main ():
    sjisfile = sys.argv[1]
    utf8file = 'result.csv'

    fin = codecs.open(sjisfile,'r','shift-jis')
    fout = codecs.open(utf8file,'w','utf-8')
    for row in fin:
        fout.write(row.encode('utf-8','ignore').decode('shift-jis'))
    fin.close()
    fout.close()

if __name__ == '__main__':
    main()


