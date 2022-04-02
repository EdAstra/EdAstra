import json
import torch
import gensim
from gensim.models import KeyedVectors
from torchtext.data.utils import get_tokenizer
from collections import Counter
from torchtext import vocab
from torchtext.data.datasets_utils import (
    _RawTextIterableDataset,
    _wrap_split_argument,
    _add_docstring_header,
    _create_dataset_directory,
)

import numpy as np
from numpy import dot
from numpy.linalg import norm

para_array = np.array(paragraph_vector)
cos_sim_max = -1000000

print('Loading BWV model')

wv_from_bin = KeyedVectors.load_word2vec_format('BioWordVec_PubMed_MIMICIII_d200.vec.bin', binary=True)
print('Finished loading BWV model')

print('Getting embedding vectors for tokens in vocab')

for key in wv_from_bin.index_to_key:
    wv_array = np.array(wv_from_bin[key])
    cos_sim = dot(para_array, wv_array)/(norm(para_array)*norm(wv_array))
    if cos_sim > cos_sim_max*.98:
        print(key, cos_sim)
        if cos_sim > cos_sim_max:
            cos_sim_max = cos_sim

for node_name, node_name_tokens in nodes:
	node_vector = #List of 100 zeros
	