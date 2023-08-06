#!/usr/bin/env python3
import json
import pandas as pd
import glob

## TODO: make file list from file org
## get naming conventions straight from file org (e.g., workers folder file in t_n files)
## get large df and start running stats etc. to send summary to C+S

for file in file_list:
    outfile=[]


outfile=[]
def readMTurkJSON(self, outfile, Turker):
    json1_file=open(str(self))
    json1_str=json1_file.read()
    json1_data=json.loads(json1_str)
    json1_data_nowrap=json1_data['answers']
    sting, scend, answ =[],[], []
    for i in json1_data_nowrap:
        answ.append(i[u'answer'])
        sting.append(i[u'question']['setting'])
        scend.append(i[u'question']['scenario'])
    x=pd.DataFrame({'answer':answ,'instructions':sting,'prompt':scend})
    x['worker']=str(Turker)
    outfile.append(x)
    return
