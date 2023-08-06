# -*- coding: utf-8 -*-
"""
title: "Merlin-py initial draft"
author: "Kellen O'Connor"
date: "January 2020"
"""

import os
import tabula
import pandas as pd
import numpy as np
from os.path import expanduser
home = expanduser("~")
pd.set_option('display.max_colwidth', 255)
import camelot
import time
from multiprocessing import Pool


def pindex (path, field, avoid):
    folder = path
    files = os.listdir(folder)[0:]
    ID_L1 = []
    ID_L2 = []
    ID_L3 = []
    ID_L4 = []
    num_files = len([f for f in os.listdir(folder)if os.path.isfile(os.path.join(path, f))])
    progress_count=0
    for i, file in enumerate(files):
        ID_L1.append(files[i][:4])
        ID_L2.append(files[i][5:14])
    for i, file in enumerate(files):
        path = folder + "/" + files[i]
        print('Reading file..'+files[i])
        ID_L3.append("flagged")
        ID_L4.append(0)
    PAGEINDEX = []
    for i, file in enumerate(files):
        progress_count=progress_count+1
        path = folder + "/" + files[i]
        print("Working on... "+files[i]+"  "+str(progress_count)+"/"+str(num_files))
        ID_L5 = []
        ID_L6 = []
        x = []
        y = []
        if ID_L4[i] == 1:
            PAGEINDEX.append(ID_L6)
        else:
            x = tabula.read_pdf(path, pages = "all", multiple_tables = True,
                                area=(0, 0, 30, 100), relative_area=True,
                                pandas_options={'header': None})
            if isinstance(x, list):
                for xpage in range(0,len(x)):
                    y.append(x[xpage].to_string())
                for ypage in range(0,len(y)):
                    if y[ypage].find(field) > -1 and y[ypage].find(avoid) == -1:
                        ID_L5.append(ypage)
                        ID_L6 = [p for p in ID_L5 if p > 23]
                temp = ID_L5 if len(ID_L5) > 0 else [1,2]
                temp.append(temp[-1] + 1)
                ID_L6 = ID_L5 if len(ID_L5)==0 else temp
                PAGEINDEX.append(ID_L6)
            else:
                PAGEINDEX.append(ID_L6)
    return files, ID_L3, ID_L4, PAGEINDEX

def create_dfindex (index_results):
    index_results=np.array(index_results, dtype=object)
    index_shape=index_results.shape
    field_d=index_shape[0]
    field_number=index_shape[1]
    table_pages=pd.DataFrame(columns = ['filename', 'filetype','non_990','needed_pages'])
    num = 0
    while num < field_number:
        filename=index_results[0][num]
        filetype=index_results[1][num]
        non_990=index_results[2][num]
        needed_pages=index_results[3][num]
        table_pages.loc[num] = [filename, filetype, non_990, needed_pages]
        num=num+1
    table_pages['needed_page_length']=table_pages['needed_pages'].str.len()
    return table_pages

def get_table_index (path, field, avoid, name):
    index_results=pindex(path, field, avoid)
    table=create_dfindex(index_results)
    table['needed_pages'] = table['needed_pages'].astype(str)
    table['needed_pages'] = table['needed_pages'].str.replace(r"\[","")
    table['needed_pages'] = table['needed_pages'].str.replace(r"\]","")
    table.to_csv(name)
    return table


def data_scan(table,path,out_shape, output_path, miss_path):
    missed_list=[]
    progress_count=0
    num_pdf=str(len(table))
    table.dropna(subset=['needed_pages'])
    for index, row in table.iterrows():
        cycle_time=time.clock()
        ned_pg=row['needed_pages']
        ned_pg=str(ned_pg)
        if ned_pg=='nan':
            ned_pg=''
        ned_pg_len=len(ned_pg)
        if ned_pg_len!=0:
            file=path+row['filename']
            tbls=camelot.read_pdf(file,pages=ned_pg)
            message="Tables found matching search condition in file "+row['filename']
            print(message)
            progress_count=progress_count + 1
            print("Worker PDF Count: "+str(progress_count)+"/"+num_pdf)
            for  i in tbls:
                temp_df=i.df
                if temp_df.shape[1]==out_shape:
                    temp_df = temp_df.replace(to_replace='\n', value=' ', regex= True)
                    temp_df = temp_df.drop(temp_df[temp_df[1]=='(b)EIN'].index)
                    temp_df = temp_df.drop(temp_df[temp_df[1]=='(b) EIN'].index)
                    temp_df['file'] = row['filename']
                    temp_df.to_csv(output_path, mode='a', header='False')
                    print("Tables found matching selected shape in file "+row['filename'])
                else:
                    temp_df.to_csv(miss_path, mode='a', header='False')
                    print("No tables matching selected shape in file "+row['filename'])
        else:
            print('Issue with '+row['filename']+'... Its likely that it didnt meet the search critera.')
            missed_list.append(row['filename'])
        cycle_end=time.clock()
        print(cycle_end - cycle_time)

def multi_run_wrapper(args):
  return data_scan(*args)
def tabdata_pull(contents_path, pdf_path, hit, miss, ProcCount, shape, output_path, miss_path):
    from os.path import expanduser
    home = expanduser("~")
    if ProcCount==2:
        print("Dual core execution selected, table of contents creation remains single core but camelot scanning will be multi-processed across two cores.")
    if ProcCount==4:
        print("Quad core execution selected, table of contents creation remains single core but camelot scanning will be multi-processed across four cores.")
    if os.path.exists(contents_path):
      os.remove(contents_path)
      print('Removing existing table of pdf-table-of-contents')
    else:
      print('No pdf-table-of-contents exists, creating new list')
    #Creates table of contents at /home/c1kto01/pdf-scrape-tableofcontents.csv#
    get_table_index(pdf_path,hit,miss,contents_path)
    #Splits data based on how many processors we want to use..#
    if ProcCount==2:
        s1, s2 = data_split(contents_path, ProcCount)
    elif ProcCount==4:
        s1, s2, s3, s4 = data_split(contents_path, ProcCount)
    else:
        print("Package supports dual or quad core execution only, further multiprocessing support will be added in the future.")
    if os.path.exists(output_path):
      os.remove(output_path)
      print('Removing old data output...')
    if os.path.exists(miss_path):
      os.remove(miss_path)
      print('Removing old data garbage collection...')
    if ProcCount==4:
      p=Pool(ProcCount)
      p.map(multi_run_wrapper,[(s1,pdf_path, shape, output_path, miss_path),(s2,pdf_path, shape, output_path, miss_path),(s3,pdf_path, shape, output_path, miss_path),(s4,pdf_path, shape, output_path, miss_path)])
    elif ProcCount==2:
      p=Pool(ProcCount)
      p.map(multi_run_wrapper,[(s1,pdf_path, shape, output_path, miss_path),(s2,pdf_path, shape, output_path, miss_path)])