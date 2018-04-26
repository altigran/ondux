import logging
import sys
from pprint import pprint
from utils import functions as F

logger = logging.getLogger(__name__)


class PSM:
    '''
    Represent a probabilistic HMM-like graph model called PSM
    (Positioning and Sequencing Model)

    PSM has the following properties:
        t_matrix: stores the probability of observing a transition
        from a label to another label.
        p_matrix: stores the probability of observing a label in
        the set of candidate labels that occupies the k-th position
        in a candidate record.
    '''

    def __init__(self, matched_blocks, k_base):
        attribute_list = k_base.get_attributes()
        matrix_size = len(attribute_list)+1
        self.t_matrix = []
        self.init_t_matrix(attribute_list, matrix_size, matched_blocks)

    def init_t_matrix(self, attribute_list, matrix_size, matched_blocks):
        '''Initialize transitions matrix'''
        attribute_index = {}
        for i, attr in enumerate(attribute_list):
            attribute_index[attr] = {'id': i + 1, 'transitions': 0}

        self.t_matrix = [[0 for i in range(matrix_size)] for j in range(matrix_size)]

        for i in range(matrix_size-1):
            self.t_matrix[0][i+1] = attribute_list[i]
            self.t_matrix[i+1][0] = attribute_list[i]

        # Set the number of transitions from label i to label j
        for block in matched_blocks:
            for n in range(len(block)-1):
                current_label = block[n][1]
                next_label = block[n+1][1]
                if current_label == 'none' or next_label == 'none':
                    continue

                i = attribute_index[current_label]['id']
                j = attribute_index[next_label]['id']

                attribute_index[current_label]['transitions'] += 1
                self.t_matrix[i][j] += 1

        # Divides the number of transitions from label i to label j
        # by the total number of transitions starting from label i
        for i in range(matrix_size-1):
            for j in range(matrix_size-1):
                if self.t_matrix[i+1][j+1]>0:
                    self.t_matrix[i+1][j+1] /= attribute_index[self.t_matrix[i+1][0]]['transitions']
