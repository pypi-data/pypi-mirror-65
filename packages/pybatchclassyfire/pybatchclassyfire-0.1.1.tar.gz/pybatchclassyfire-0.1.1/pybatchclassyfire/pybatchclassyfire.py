#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Mon Aug 13 16:19:11 2018

@author: Madeleine Ernst (https://github.com/madeleineernst)
"""
# Standard library imports
import os
import re
import sys
import time

# Third party imports 
import collections
from collections import Counter
from collections import OrderedDict
import csv  
import functools
from functools import reduce
from joblib import Parallel, delayed
import json
import multiprocessing
from networkx import *
import operator
import pandas as pd
from pandas.api.types import is_numeric_dtype
import requests
import requests_cache

pd.options.mode.chained_assignment = None 
requests_cache.install_cache('demo_cache')

"""
@author: Ricardo Silva (https://github.com/rsilvabioinfo)
"""

def make_classy_table(jsondic):  
    
    dmetadatalist = []
    
    for idx,entry in enumerate(jsondic):
        
        mdict = {}
        
        if (entry != {} and entry != None):
    
            if sum([bool(re.match('smiles', x)) for x in entry.keys()]) > 0 and entry['smiles'] is not None:
                mdict['smiles'] = entry['smiles']
            if sum([bool(re.match('inchikey', x)) for x in entry.keys()]) > 0 and entry['inchikey'] is not None:
                mdict['inchikey'] = entry['inchikey']
            if sum([bool(re.match('kingdom', x)) for x in entry.keys()]) > 0 and entry['kingdom'] is not None:
                mdict['kingdom'] = entry['kingdom']['name']
            if sum([bool(re.match('superclass', x)) for x in entry.keys()]) > 0 and entry['superclass'] is not None :
                mdict['superclass'] = entry['superclass']['name']
            if sum([bool(re.match('class', x)) for x in entry.keys()]) > 0 and entry['class'] is not None :
                mdict['class'] = entry['class']['name']
            if sum([bool(re.match('subclass', x)) for x in entry.keys()]) > 0 and entry['subclass'] is not None:
                mdict['subclass'] = entry['subclass']['name']
            if sum([bool(re.match('direct_parent', x)) for x in entry.keys()]) > 0 and entry['direct_parent'] is not None:
                mdict['direct_parent'] = entry['direct_parent']['name']
            if sum([bool(re.match('molecular_framework', x)) for x in entry.keys()]) > 0 and entry['molecular_framework'] is not None:
                mdict['molecular_framework'] = entry['molecular_framework']
        else:
            
            mdict['smiles'] = "None"
            mdict['inchikey'] = "None"
            mdict['kingdom'] = "None"
            mdict['superclass'] = "None"
            mdict['class'] = "None"
            mdict['subclass'] = "None"
            mdict['direct_parent'] = "None"
            mdict['molecular_framework'] = "None"
            
        dmetadatalist.append(mdict)
    
    df_metares = pd.DataFrame.from_dict(dmetadatalist)  
    return(df_metares)

"""
@author: Ming Wang (https://github.com/mwang87)
"""

def get_structure_class_entity(inchikey):
    print(inchikey)
    entity = None
    try:
        entity = json.loads(get_entity(inchikey))
    except KeyboardInterrupt:
        raise
    except:
        new_inchi_no_stereo = inchikey.split("-")[0] + "-UHFFFAOYSA-N"
        try:
            entity = json.loads(get_entity(new_inchi_no_stereo))
        except KeyboardInterrupt:
            raise
        except:
            return entity

    return entity


def get_structure_class(inchikey):
    return_dict = {}
    print(inchikey)
    try:
        entity = json.loads(get_entity(inchikey))
    except KeyboardInterrupt:
        raise
    except:
        new_inchi_no_stereo = inchikey.split("-")[0] + "-UHFFFAOYSA-N"
        try:
            entity = json.loads(get_entity(new_inchi_no_stereo))
        except:
            print(inchikey, "Not Cached")
            return_dict["inchikey"] = inchikey
            return_dict["superclass"] = "None"
            return_dict["class"] = "None"
            return_dict["subclass"] = "None"
            return return_dict

    try:
        print(json.dumps(entity))
        return_dict["inchikey"] = inchikey
        if "superclass" in entity:
            return_dict["superclass"] = entity["superclass"]["name"]
        else:
            return_dict["superclass"] = "None"

        if "class" in entity:
            return_dict["class"] = entity["class"]["name"]
        else:
            return_dict["class"] = "None"

        if "subclass" in entity and entity["subclass"] != None:
            return_dict["subclass"] = entity["subclass"]["name"]
        else:
            return_dict["subclass"] = "None"

        return return_dict
    except:
        return_dict["inchikey"] = inchikey
        return_dict["superclass"] = "None"
        return_dict["class"] = "None"
        return_dict["subclass"] = "None"
        return return_dict

"""A client for the ClassyFire API which enables efficient querying with
 chemical database files
 
 All scripts below hare based on pyclassyfire written by James Jeffryes 
 https://github.com/JamesJeffryes/pyclassyfire
 
 """

url = "http://classyfire.wishartlab.com"
proxy_url =  "https://gnps-classyfire.ucsd.edu"
chunk_size = 1000
sleep_interval = 60


def structure_query(compound, label='pyclassyfire'):
    """Submit a compound information to the ClassyFire service for evaluation
    and receive a id which can be used to used to collect results

    :param compound: The compound structures as line delimited inchikey or
         smiles. Optionally a tab-separated id may be prepended for each
         structure.
    :type compound: str
    :param label: A label for the query
    :type label:
    :return: A query ID number
    :rtype: int

    >>> structure_query('CCC', 'smiles_test')
    >>> structure_query('InChI=1S/C3H4O3/c1-2(4)3(5)6/h1H3,(H,5,6)')

    """
    r = requests.post(url + '/queries.json', data='{"label": "%s", '
                      '"query_input": "%s", "query_type": "STRUCTURE"}'
                                                  % (label, compound),
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()['id']


def iupac_query(compound, label='pyclassyfire'):
    """Submit a IUPAC compound name to the ClassyFire service for evaluation
     and receive a id which can be used to used to collect results.

    :param compound: The line delimited compound names. Optionally a
         tab-separated id may be prepended for each compound.
    :type compound: str
    :param label: A label for the query
    :type label:
    :return: A query ID number
    :rtype: int

    >>> iupac_query('ethane', 'iupac_test')
    >>> iupac_query('C001\\tethane\\nC002\\tethanol', 'iupac_test')

    """
    r = requests.post(url + '/queries.json', data='{"label": "%s", '
                      '"query_input": "%s", "query_type": "IUPAC_NAME"}'
                                                  % (label, compound),
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()['id']


def get_results(query_id, return_format="json", blocking=False):
    """Given a query_id, fetch the classification results.

    :param query_id: A numeric query id returned at time of query submission
    :type query_id: str
    :param return_format: desired return format. valid types are json, csv or sdf
    :type return_format: str
    :return: query information
    :rtype: str

    >>> get_results('595535', 'csv')
    >>> get_results('595535', 'json')
    >>> get_results('595535', 'sdf')

    """
    if blocking == False:
        r = requests.get('%s/queries/%s.%s' % (url, query_id, return_format),
                         headers={"Content-Type": "application/%s" % return_format})
        r.raise_for_status()
        return r.text
    else:
        while True:
            r = requests.get('%s/queries/%s.%s' % (url, query_id, return_format),
                             headers={"Content-Type": "application/%s" % return_format})
            r.raise_for_status()
            result_json = r.json()
            if result_json["classification_status"] != "In Queue":
                return r.text
            else:
                print("WAITING")
                time.sleep(10)


def get_entity(inchikey, return_format="json", gnps_proxy = False):
    """Given a InChIKey for a previously queried structure, fetch the
     classification results.

    :param inchikey: An InChIKey for a previously calculated chemical structure
    :type inchikey: str
    :param return_format: desired return format. valid types are json, csv or sdf
    :type return_format: str
    :return: query information
    :rtype: str

    >>> get_entity("ATUOYWHBWRKTHZ-UHFFFAOYSA-N", 'csv')
    >>> get_entity("ATUOYWHBWRKTHZ-UHFFFAOYSA-N", 'json')
    >>> get_entity("ATUOYWHBWRKTHZ-UHFFFAOYSA-N", 'sdf')

    """
    inchikey = inchikey.replace('InChIKey=', '')
    
    if gnps_proxy == True:
        
        r = requests.get('%s/entities/%s.%s' % (proxy_url, inchikey, return_format),
                     headers={
                         "Content-Type": "application/%s" % return_format})
        print('%s/entities/%s.%s' % (proxy_url, inchikey, return_format))
        
    else:
        
        r = requests.get('%s/entities/%s.%s' % (url, inchikey, return_format),
                     headers={
                         "Content-Type": "application/%s" % return_format})
        print('%s/entities/%s.%s' % (url, inchikey, return_format))
        
    r.raise_for_status()
    return r.text


def get_chemont_node(chemontid):
    """Return data for the TaxNode with ID chemontid.

    :param chemontid: the ChemOnt ID of the entity.
    :type chemontid: str
    :return: The classification results for the entity as json.
    :rtype: str

    >>> get_chemont_node('CHEMONTID:0004253')

    """
    chemontid = chemontid.replace("CHEMONTID:", "C")
    r = requests.get('%s/tax_nodes/%s.json' % (url, chemontid),
                     headers={"Content-Type": "application/json" })
    r.raise_for_status()
    return r.text


def tabular_query(inpath, structure_key, dialect='excel', outpath=None,
                  outfields=('taxonomy', 'description', 'substituents')):
    """Given a path to a compound set in tabular form (comma or tab delimited)
     annotate all compounds and write results to an expanded table.

    :param inpath: path to compound file to be annotated
    :type inpath: str
    :param structure_key: column heading which contains the compounds InChIKey
         or SMILES
    :type structure_key: str
    :param dialect: dialect for parsing table (generally 'excel' for csv,
         'excel-tab' for tsv)
    :type dialect: str
    :param outpath: Path to desired output location
    :type outpath: str
    :param outfields: Fields to append to table from ClassyFire output
    :type outfields: tuple(string)

    >>> tabular_query('/tabulated_data.tsv', 'structure', 'excel-tab')

    """
    tax_fields = ('kingdom', 'superclass', 'class', 'subclass')
    query_ids = []
    infile = open(inpath, 'rU')
    if not outpath:
        outpath = _prevent_overwrite(inpath)
    comps = []
    for line in csv.DictReader(infile, dialect=dialect):
        comps.append(line[structure_key])
        if not len(comps) % chunk_size:
            query_ids.append(structure_query('\\n'.join(comps)))
            comps = []
    if comps:
        query_ids.append(structure_query('\\n'.join(comps)))
    print('%s queries submitted to ClassyFire API' % len(query_ids))
    i = 0
    infile.seek(0)
    with open(outpath, 'w') as outfile:
        reader = csv.DictReader(infile, dialect=dialect)
        writer = csv.DictWriter(outfile, reader.fieldnames+list(outfields),
                                dialect=dialect)
        writer.writeheader()
        while i < len(query_ids):
            result = json.loads(get_results(query_ids[i]))
            if result["classification_status"] == "Done":
                for j, line in enumerate(reader):
                    if result['entities'] and str(j+1) == result['entities'][0]['identifier'].split('-')[1]:
                        hit = result['entities'].pop(0)
                        if 'taxonomy' in outfields:
                            hit['taxonomy'] = ";".join(
                                ['%s:%s' % (hit[x]['name'], hit[x]['chemont_id'])
                                 for x in tax_fields if hit[x]])
                        for field in outfields:
                            if isinstance(hit[field], list):
                                line[field] = ';'.join(hit[field])
                            else:
                                line[field] = hit[field]
                    writer.writerow(line)
                i += 1
            else:
                print("%s percent complete" % round(i/len(query_ids)*100))
                time.sleep(sleep_interval)
    infile.close()


def sdf_query(inpath, outpath=None):
    """Given a path to a compound set in a sdf file, annotate all compounds
     and write results as attributes in a sdf file.

    :param inpath: path to compound file to be annotated
    :type inpath: str
    :param outpath: Path to desired output location
    :type outpath: str

    >>> sdf_query('/sdf_data.sdf')

    """
    from rdkit.Chem import AllChem
    query_ids = []
    if not outpath:
        outpath = _prevent_overwrite(inpath)
    comps = []
    for mol in AllChem.SDMolSupplier(inpath):
        if mol:
            comps.append(AllChem.MolToSmiles(mol))
        if not len(comps) % chunk_size:
            query_ids.append(structure_query('/n'.join(comps)))
            comps = []
    if comps:
        query_ids.append(structure_query('\\n'.join(comps)))
    print('%s queries submitted to ClassyFire API' % len(query_ids))
    i = 0
    with open(outpath, 'w') as outfile:
        while i < len(query_ids):
            result = json.loads(get_results(query_ids[i]))
            if result["classification_status"] == "Done":
                outfile.write(get_results(query_ids[i], return_format='sdf'))
                i += 1
            else:
                print("%s percent complete" % round(i / len(query_ids) * 100))
                time.sleep(sleep_interval)


def _prevent_overwrite(write_path, suffix='_annotated'):
    """Prevents overwrite of existing output files by appending a suffix when
    needed

    :param write_path: potential write path
    :type write_path: string
    :return:
    :rtype:
    """
    while os.path.exists(write_path):
        sp = write_path.split('.')
        if len(sp) > 1:
            sp[-2] += suffix
            write_path = '.'.join(sp)
        else:
            write_path += suffix
    return write_path

def run_shell_command(script_to_run):
	os.system(script_to_run)
	return "DONE"

# Wraps running in parallel a set of shell scripts
def run_parallel_shellcommands(input_shell_commands, parallelism_level):
	return run_parallel_job(run_shell_command, input_shell_commands, parallelism_level)

# Wraps the parallel job running, simplifying code
def run_parallel_job(input_function, input_parameters_list, parallelism_level):
	if parallelism_level == 1:
		output_results_list = []
		for input_param in input_parameters_list:
			result_object = input_function(input_param)
			output_results_list.append(result_object)
		return output_results_list
	else:
		results = Parallel(n_jobs = parallelism_level)(delayed(input_function)(input_object) for input_object in input_parameters_list)
		return results

def get_classifications(inchifile):

    with open(inchifile) as csvfile:
        all_inchi_keys = []
    
        reader = csv.DictReader(csvfile)
        row_count = 0
        for row in reader:
            row_count += 1
    
            if row_count % 1000 == 0:
                print(row_count)
    
            all_inchi_keys.append(row["InChIKey"].split("=")[1])
    
            continue
    
        #all_inchi_keys = all_inchi_keys[-1000:]
        all_json = run_parallel_job(get_structure_class_entity, all_inchi_keys, parallelism_level = 50)
    
        open("all_json.json", "w").write(json.dumps(all_json))


def get_classifications_open(inchifile):

    with open(inchifile) as csvfile:
        all_inchi_keys = []
    
        reader = csv.DictReader(csvfile)
        row_count = 0
        for row in reader:
            row_count += 1
    
            if row_count % 1000 == 0:
                print(row_count)
    
            all_inchi_keys.append(row)
    
            continue
    
        #all_inchi_keys = all_inchi_keys[-1000:]
        all_json = run_parallel_job(get_structure_class_entity, all_inchi_keys, parallelism_level = 50)
    
        open("all_json.json", "w").write(json.dumps(all_json))


def get_structure_classifications(inchifile):

    with open(inchifile) as csvfile:
        all_inchi_keys = []
    
        reader = csv.DictReader(csvfile)
        row_count = 0
        for row in reader:
            row_count += 1
    
            if row_count % 1000 == 0:
                print(row_count)
    
            all_inchi_keys.append()
    
            continue
    
        #all_inchi_keys = all_inchi_keys[-1000:]
        all_json = run_parallel_job(structure_query, all_inchi_keys, parallelism_level = 50)
    
        open("all_json_structure.json", "w").write(json.dumps(all_json))
        

"""Functions written to perform batch query of ClassyFire classifications using both scripts form pymolnetenhancer and pyclassyfire.
 Adressing the issues of paginated JSON results and request 429 errors.
 
 @author: Pierre-Marie Allard (https://gitlab.unige.ch/Pierre-Marie.Allard)
 
 
 """

def get_classifications_cf_mod(all_inchi_keys):
    """a slightly modified version of the original get_classification() which will take list object as input
    
    """

    all_json = run_parallel_job(get_structure_class_entity, all_inchi_keys, parallelism_level = 80)

    open("all_json.json", "w").write(json.dumps(all_json))
    
    
def batch_query(inpath, structure_key, dialect='excel'):
    """Given a path to a compound set in tabular form (comma or tab delimited)
     launches a structure_query() for all compounds and returns a list of query_ids
    
    :param inpath: path to compound file to be annotated
    :type inpath: str
    :param structure_key: column heading which contains the compounds InChIKey
         or SMILES
    :type structure_key: str
    :param dialect: dialect for parsing table (generally 'excel' for csv,
         'excel-tab' for tsv)
    :type dialect: str
    
    >>> tabular_query('/tabulated_data.tsv', 'structure', 'excel-tab')
    
    """
    #tax_fields = ('kingdom', 'superclass', 'class', 'subclass')
    query_ids = []
    infile = open(inpath, 'rU', encoding="utf-8")
    #if not outpath:
    #    outpath = _prevent_overwrite(inpath)
    comps = []
    for line in csv.DictReader(infile, dialect=dialect):
        comps.append(line[structure_key])
        if not len(comps) % chunk_size:
            query_ids.append(structure_query('\\n'.join(comps)))
            comps = []
            time.sleep(10)
    if comps:
        query_ids.append(structure_query('\\n'.join(comps)))
        time.sleep(10)
    print('%s queries submitted to ClassyFire API' % len(query_ids))
    
    return query_ids



def get_results_multientry_multipage_patient(query_ids_list, return_format="json"):
    
    start_time = time.time()
    
    global_requests = []
    
    for query_id in query_ids_list:
    
        r = requests.get('%s/queries/%s.%s' % (url, query_id, return_format),
                         headers={"Content-Type": "application/%s" % return_format})
        r.raise_for_status()

        result = json.loads(r.text)
        num_pages = result["number_of_pages"]


        
        
        requests_dict = {}
        requests_list = []
        jsoned_requests = [] 
        
        i = 0
        j = 0

        #for i in range(1, 6):
        for i in range(1, num_pages + 1):

            if result["classification_status"] == "Done":
                ind_request = requests.get('%s/queries/%s.%s?page=%s' % (url, query_id, return_format, i),
                                 headers={"Content-Type": "application/%s" % return_format})
                #ind_request.raise_for_status()
                
                if ind_request.status_code == 500:
                    continue
                else:
                    requests_list.append(ind_request)

                    time.sleep(0.1)
                    print('Parsed page %s of query id %s' % (i, query_id))
                    i += 1
            else:
                time.sleep(10)
                continue

        for jsonObj in requests_list:
            requests_dict = json.loads(jsonObj.text)
            jsoned_requests.append(requests_dict)

        for j in range(1, len(jsoned_requests)):
            jsoned_requests[0]['entities'].extend(jsoned_requests[j]['entities'])
            
        print('Retrieved entry id n° %s' % query_id)
        print(jsoned_requests)
        print(jsoned_requests[0]['classification_status'])
        
        global_requests.append(jsoned_requests[0])
        print("Program ran in --- %s seconds ---" % (time.time() - start_time))
    
    return global_requests
    
    
import os
import json
from functools import singledispatch


@singledispatch
def remove_null_bool(ob):
    return ob

@remove_null_bool.register(list)
def _process_list(ob):
    return [remove_null_bool(v) for v in ob if v is not None]

@remove_null_bool.register(dict)
def _process_list(ob):
    return {k: remove_null_bool(v) for k, v in ob.items() if v is not None}



def cleanse(in_file, out_file):
    with open(in_file, 'r') as source:
        source_json = json.load(source)
    with open(out_file, 'w') as out_source:
        json.dump(remove_null_bool(source_json), out_source)
 
