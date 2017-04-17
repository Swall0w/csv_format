import codecs
import sys
import os

import chardet
from io import StringIO
import pandas as pd
import re
import unicodedata
import string

def csvformator(readfile):
    Date = '日付'
    Journal = '借方名称'
    Price = '金額'
    outputfile = 'new_'+readfile
    with open(readfile,mode='rb') as f:
        binary = f.read()
        detect = chardet.detect(binary)
        print(detect)
    text = binary.decode(detect['encoding']).encode('utf-8','ignore').decode('utf-8')
    index = text[:20].find('仕訳日記帳')
    if index != -1:
        print('found at ',index)
        index = text[:100].find(Date)
        if index != -1:
            print('rm str: ',text[:index -1])
            text = text[index -1:]
        else:
            pass
    else:
        print('not found')

    # convert str object to pandas dataframe
    text = StringIO(text)
    df = pd.read_csv(text,sep=',')

    # date format
    datename =''
    for item in df.columns.tolist():
        index = item.find(Date)
        if index != -1:
            datename = item
        else:
            pass
    df[Date] = df[datename].apply(lambda x:conv_time_format(x))
    if datename != Date:
        del df[datename]

    # Journal format
    journalname = ''
    for item in df.columns.tolist():
        if item in ['借方名称','借方科目名称']:
            journalname = item
        else:
            pass
    if journalname != Journal:
        print('renamed ',journalname,' to ',Journal)
        df[Journal] = df[journalname]
        del df[journalname]
    df[Journal] = df[Journal].apply(lambda x: rm_all_white_space(str(x)))

    # Price format
    pricename =''
    for item in df.columns.tolist():
        index = item.find(Price)
        if index != -1:
            if item == Price:
                pricename = item
            else:
                index1 = item.find('借方')
                if index1 != -1:
                    pricename = item
                else:
                    pass
        else:
            pass
    if pricename != Price:
        print('renamed ',pricename,' to ',Price)
        df[Price] = df[pricename]
        del df[pricename]

    df.to_csv(outputfile,index=False)

def rm_all_white_space(text):
    text = unicodedata.normalize("NFKC", text)
    table = str.maketrans("", "", string.punctuation  + "「」、。・")
    text = text.translate(table)
    return ''.join([s.strip()for s in text])

def conv_time_format(x):
    date_pattern1 = '(\d{4})/(\d{1,2})/(\d{1,2})'
    date_pattern2 = 'H(\d{2})\.(\d{1,2})\.(\d{1,2})'

    pattern = re.compile(date_pattern1)
    result = pattern.search(x)
    if result:
        y, m, d = result.groups()
        return "{year}-{month}-{day}".format(year=y,month=m,day=d)
    else:
        pattern = re.compile(date_pattern2)
        result = pattern.search(x)
        if result:
            y, m, d = result.groups()
            y = str(int(y)+1988)
            return "{year}-{month}-{day}".format(year=y,month=m,day=d)
        else:
            return None

if __name__ == '__main__':
    #print(sys.argv[1:])
    for item in sys.argv[1:]:
        csvformator(item)


