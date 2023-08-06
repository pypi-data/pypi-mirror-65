# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 02:09:08 2019

@author: Meysam
"""

from collections import defaultdict
import argparse
import logging
from time import strftime
import storage
from collections import Counter
import pymysql
import operator
import re
import time
import io
import pandas as pd
import os
import sys
import subprocess
import optparse
import tempfile
import codecs
from time import sleep
def dataframe(query):

                    conn=storage.connect()
                    return pd.read_sql_query(query,conn)
def calculatecounts(starttime,endtime,cts):
                    logging.basicConfig(level=logging.DEBUG,
                                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                        datefmt='%m-%d %H:%M',
                                        filename='log/{}.log'.format(strftime('%d_%m_%Y_%T')),
                                        filemode='w')
                    console = logging.StreamHandler()
                    console.setLevel(logging.INFO)
                    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
                    console.setFormatter(formatter)
                    logging.getLogger('').addHandler(console)
                    logging.info('start reading from database')
                    starttime=time.time()
                    q=("""select text,shdate from posts where shdate BETWEEN ('{}') and ('{}');""".format(start,end))
                    dftw = dataframe(q)
                    shep=str(dftw.shape)
                    logging.info('dataframe shape is : '+shep)
                    endtime = time.time()
                    div=endtime-starttime
                    logging.info('second takes to fetch data from database'+str(div))
                    start1=time.time()
                    logging.info('starting to clean input dataframe')
                    logging.info('start to extract hashtags from texts and count how many times they appear together')
                    dftw=dftw.dropna(subset=['text'])
                    dftw['text']=dftw['text'].replace('\n','',regex=True)
                    dftw['text']=dftw['text'].replace(' ','',regex=True)
                    dftw['text']=dftw['text'].str.strip()
                    dftw=dftw.drop(dftw[dftw['text']==''].index)
                    com = defaultdict(lambda : defaultdict(int))
                    for index,row in dftw.iterrows():
                        x = row['text']
                        
                        #x=x.decode('utf-8')

                        #terms_only = [re.findall(r'(\#\w+)',x)]
                        terms=re.compile('(?i)(?<=\#)\w+',re.UNICODE)
                        terms_only=[i for i in terms.findall(x)]
                        #terms_only=re.findall(r"#(\w+)", x)
                        # Build co-occurrence matrix
                        for i in range(len(terms_only)-1):
                            for j in range(i+1, len(terms_only)):
                                w1, w2 = sorted([terms_only[i], terms_only[j]])
                                if w1 != w2:
                                    com[w1][w2]=com[w1][w2]+1

                    start2=time.time()
                    div_two=str(start2-start1)
                    logging.info('seconds take to extract hashtags and count them together'+str(div_two))
                    com_max = []
                    logging.info('For each term, look for the most common co-occurrent terms')
                    for t1 in com:
                        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:]
                        for t2, t2_count in t1_max_terms:
                            com_max.append(((t1, t2), t2_count))
                    logging.info('Get the most frequent co-occurrences')
                    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
                    logging.info('start creating output.txt with hashtags nad their counts')
                    myfile=io.open('output.txt','w')
                    for item in terms_max:
                        if (item[1] >= int(cts)):
                              num=str(item[1])
                              word1=item[0][0]
                              word2=item[0][1]
                              myfile.write(word1)
                              myfile.write('\t'+word2)
                              myfile.write('\t'+num+'\n')
                    myfile.close()
                    logging.info('start converting output.txt to out.net files that contains output.txt info in pajek format')
                    sleep(10)
def edgelist_to_pajek(input_filename, output_filename="", directed=False, weighted=True, buffer_size=10000):
     # Sort out I/O                                                             
                        if output_filename:
                            output_file = open(output_filename, "w")
                        else:
                            output_file = sys.stdout

                        node_idx_map = {}
                        # Write vertices section and produce map from original nodeIDs to
                        # contiguous integer ids that start from one.           
                        with Tempfile() as unique_nodes_file:
                            unique_nodes_command = "<%s awk '{ print $1; print $2; }' | sort -n --buffer-size=%dM >%s" % (input_filename, buffer_size, unique_nodes_file.name)
                            unique_nodes_command = "<" + input_filename + " " + unique_nodes_command
                            run_command(unique_nodes_command)
                            with open(unique_nodes_file.name) as f:                                                                                             
                                        distinct_content=set(f.readlines())
                            distinct_content=sorted(distinct_content)                                                                                           
                            to_file=""                                                                                                                          
                            for element in distinct_content:                                                                                                    
                                        to_file=to_file+element                                                                                                 
                            with open('final.txt','w') as w:                                                                                                    
                                w.write(to_file)
                            sleep(10)
                            num_nodes = int(run_command("wc -l %s" % 'final.txt').split()[0])
                            output_file.write("*Vertices\t%d\n" % num_nodes)
                            with open('final.txt') as nodes_file:
                                    for idx, line in enumerate(nodes_file):
                                        node_id = str(line.rstrip("\n"))
                                        pajek_idx = idx + 1 # Pajek indexing starts with 1
                                        output_file.write('\t%d "%s"\n' % (pajek_idx, node_id))
                                        # Might be slow to add to dict this way, one at a time
                                        node_idx_map[node_id] = pajek_idx

                        # Now write edges                                       
                        if directed:
                            output_file.write("*Arcs\n")
                        else:
                            output_file.write("*Edges\n")

                        input_file = open(input_filename)
                        for i, line in enumerate(input_file):
                            try:
                                if weighted:

                                    n1, n2, weight = line.strip().split()
                                    output_file.write("\t%s\t%s\t%d\n" % (node_idx_map[str(n1)],
                                                                             node_idx_map[str(n2)],
                                                                             int(weight)))
                                else:
                                    n1, n2 = map(int, line.strip().split()[:2])
                                    output_file.write("\t%d\t%d\n" % (node_idx_map[n1],
                                                                      node_idx_map[n2]))
                            except ValueError:
                                raise ValueError( "Problem parsing input file on line %d, which reads: \n\t%s\nIf you selected the -w option for weighted edegs, make sure this line has an edge weight" % (i + 1, line))
                        input_file.close()
                        output_file.close()


def run_command(command):

                                """ Warning: Will hang if stderr or stdout is large """
                                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                retcode = process.wait()
                                if retcode != 0:
                                   raise Exception( "Problem running command: " + command)
                                stdout, stderr = process.communicate()
                                return stdout

class Tempfile:
                                def __enter__(self):
                                    self.file = tempfile.NamedTemporaryFile(delete=False)
                                    return self.file
                                def __exit__(self, type, value, traceback):
                                    try:
                                        os.remove(self.file.name)
                                    except OSError:
                                        pass


def main(cmd,start,end,c):

    start=start
    end=end
    cts=int(c) if c is not None else 50
    calculatecounts(start,end,cts)
    edgelist_to_pajek('output.txt',
                      output_filename ='out.net',
                      directed =False,
                      weighted =True,
                      buffer_size =10000)

