import logging
from pprint import pprint

from blocking.block import Block
from utils import functions as F

logger = logging.getLogger(__name__)

def extract_blocks(input_file, k_base):
    '''Extract block structure for each value in input file'''
    normalized_input = [F.remove_stop_words(F.normalize_str(v))
                        for v in F.read_input(input_file)]
    blocks = []
    for record in normalized_input:
        blocks.append(build_blocks(record.split(), k_base) )
    return blocks

def build_blocks(terms, k_base):
    '''Build a set of blocks for a string'''
    blocks_list = []
    blocks_list.append(Block(terms[0]))
    i = 0
    j = 1
    while j < len(terms):
        if not co_occurs(terms[j], terms[j-1], k_base):
            blocks_list.append(Block(''))
            i += 1
        if blocks_list[i].value in '':
            blocks_list[i].value += terms[j]
        else:
            blocks_list[i].value += ' ' + terms[j]
        j += 1
    return blocks_list

def co_occurs(current_term, previous_term, k_base):
    '''Verify if the current term and next term are known
    to co-occur in some occurrence in the knowledge base'''
    if current_term in k_base.inverted_k_base and previous_term in k_base.inverted_k_base:
        current_attr = k_base.inverted_k_base[current_term]
        previous_attr = k_base.inverted_k_base[previous_term]
        for c_attr in current_attr:
            for p_attr in previous_attr:
                if c_attr[0] == p_attr[0]:
                    return True
    return False
