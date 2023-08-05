import json
import multiprocessing as mp
import time
import re

from itertools import product
from collections import defaultdict

import primer3
import progressbar

def transform_degenerate(seq):
	seq = seq.upper()
	basesub = {'R': 'A',
		'Y': 'C',
		'M': 'A',
		'K': 'G',
		'S': 'G',
		'W': 'A',
		'H': 'A',
		'B': 'G',
		'V': 'G',
		'D': 'G'}
	for base in basesub.keys():
		seq = seq.replace(base, basesub[base])
	return seq

def judge_hairpin(oligo_input):
    oligo = oligo_input['oligo']
    min_Tm = min(oligo['Tm'], oligo_input['min_Tm'])
    hairpin = primer3.calcHairpin(oligo['seq'], output_structure=True)
    if hairpin.tm > min_Tm:
        return([oligo, oligo, round(hairpin.tm, 2), hairpin.ascii_structure])

def judge_two_oligo(oligo_pair):

    oligo_1 = oligo_pair['oligo_1']
    oligo_2 = oligo_pair['oligo_2']
    min_Tm = min(oligo_1['Tm'], oligo_2['Tm'], oligo_pair['min_Tm'])
    Heterodimer = primer3.calcHeterodimer(oligo_1['seq'], oligo_2['seq'], output_structure=True)
    if Heterodimer.tm > min_Tm:
        return([oligo_1, oligo_2, round(Heterodimer.tm,2), Heterodimer.ascii_structure])
    EndStability = primer3.bindings.calcEndStability(oligo_1['seq'], oligo_2['seq'])
    if EndStability.tm > min_Tm:
        return([oligo_1, oligo_2, round(EndStability.tm,2), ''])
    return None

def get_dimers(oligo_seqs, min_Tm=35, cpu=2, monitor=True):

    oligo_seqs = oligo_seqs.strip().splitlines()
    if len(oligo_seqs)<1:
        return {'error': f'No oligo sequences'}
    
    loaded_ids = {}

    # data group
    oligo_objs = []
    for i in oligo_seqs:
        items = i.split()
        if len(items) !=2 :
            return {'error': f'Input must have two columns'}
        (id, seq) = items
        if id not in loaded_ids:
            loaded_ids[id] = 1
        else:
            return {'error': f'Duplictation IDs found: {id}'}
        seq = transform_degenerate(seq)
        if re.search('[^ATGCN]', seq) is not None:
            return {'error': f'Sequence is not valid: {seq}'}
        Tm = round(primer3.calcTm(seq),2)
        oligo_objs.append({'id':id, 'seq':seq, 'Tm':Tm})

    # distribute tasks
    pool = mp.Pool(processes=cpu)
    multi_res = []
    all_tasks_num = 0

    # dimer
    for i in range(0, len(oligo_objs)):
        for j in range(i, len(oligo_objs)):
            oligo_pair = {'oligo_1':oligo_objs[i], 'oligo_2':oligo_objs[j], 'min_Tm':min_Tm}
            all_tasks_num += 1
            multi_res.append(pool.apply_async(judge_two_oligo, (oligo_pair,)))

    # hairpin
    for i in range(0, len(oligo_objs)):
        oligo_input = {'oligo': oligo_objs[i], 'min_Tm':min_Tm}
        all_tasks_num += 1
        multi_res.append(pool.apply_async(judge_hairpin, (oligo_input,)))

    # monitor
    if monitor is True:
        widgets = ['Checking Multiplex: ', progressbar.Counter(),\
            ' Finished', ' (', progressbar.Percentage(), ')', \
                progressbar.Bar(), progressbar.ETA()]
        bar = progressbar.ProgressBar(widgets=widgets, max_value=all_tasks_num).start()

    while True:
        complete_count = sum([1 for x in multi_res if x.ready()])
        if complete_count == all_tasks_num:
            if monitor is True:
                bar.finish()
            break
        if monitor is True:
            bar.update(complete_count)
        time.sleep(0.1)

    # results
    dimers = []
    for result in multi_res:
        result_data = result.get()
        if result_data is not None:
            dimers.append(result_data)
    if len(dimers)>1:
        dimers = sorted(dimers, key=lambda element:element[2], reverse=True)
    return {'dimers':dimers} 

if __name__ == "__main__":
    oligo_seqs = 'S1 TGTGATAGAGCCATGCCTA\nS2 ACACTATCTCGGTACGGAT\nS3 TAGGCATGGCTCTATCACA\nS4 TATTTTTGGCTCTATCACA'
    dimers = get_dimers(oligo_seqs)
    print(json.dumps(dimers, indent=4))