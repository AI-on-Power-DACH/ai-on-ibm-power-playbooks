#!/usr/bin/env python3
"""
This script connects to the milvus database, adds a collectaion "test-collection"
and inserts some example data points. Afterwards it queries the database for a query Q.

Used to test and show that a milvus installation is working.

parameters:
    - MILVUS_HOST (string, ENV)         the host uri at which the milvus api is reachable
    - model_name (string, script)       name of the model to use for embeddings (in huggingface format)
    - collection_name (string, script)  name of the collection to query/create in milvus
    - DATA (list[string], script)       list of entries to embedd and add to milvus
    - Q (string, script)                the query for which context is searched in milvus.
    - TOP_K (int>0, script)             number of similar results to return from milvus.
"""

import os 
from pprint import pprint # pretty print

import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient, utility, connections

# milvus connection
# leave first, otherwise the model is loaded before the connection is checked.
milvus_uri = os.getenv("MILVUS_HOST") or "http://127.0.0.1:19530"
mc = MilvusClient(milvus_uri)

connections.connect(alias="version", uri=milvus_uri)
print(f"Milvus version: { utility.get_server_version(using='version') }")
connections.disconnect("version")

print(f"milvus collections: { mc.list_collections() }")

# change these as desired:
model_name = "ibm-granite/granite-3.0-8b-instruct" # any GPT based model
local_model_name = f"{model_name.split('/')[-1]}-local" 
model = local_model_name if os.path.isdir(local_model_name) else model_name

collection_name = "test_collection"
DATA = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.", 
]
Q = "Who was Alan Turing?"
TOP_K = 2 # number of results returned.

# build sentence transformer model for embeddings.
encoder = SentenceTransformer(model, device=torch.device("mps" if torch.mps.is_available() else "cpu"))
embedding_dim = encoder.get_sentence_embedding_dimension()

if not os.path.isdir(local_model_name): 
    # save build sentence transformer for future queries.
    encoder.save_pretrained(local_model_name)


if not mc.has_collection(collection_name):
    # empty databse: create collection and add example data.
    mc.create_collection(
        collection_name,
        embedding_dim,
        auto_id = True,
    )

    embeddings = torch.tensor(encoder.encode(DATA))
    # normalise:
    embeddings = np.array(embeddings / np.linalg.norm(embeddings))
    embeddings = list(map(np.float32, embeddings))

    vector_list = []
    for chunk, vector in zip(DATA, embeddings):
        vector_list.append({
            'text': chunk,
            'vector': vector,
            'subject': 'ai',
        })

    res = mc.insert(collection_name,
        data=vector_list
    )
    print(res)


print("start query encoding")
query_embeddings = torch.tensor(encoder.encode(Q))
query_embeddings = np.array(query_embeddings / np.linalg.norm(query_embeddings))
query_embeddings = list(map(np.float32, query_embeddings))
print("encoding done!")


results = mc.search(
    collection_name,
    data=[query_embeddings],
    output_fields=['*'],
    limit=TOP_K,
    consistency_level="Eventually",
)
# vectors are quite large, remove from output for readability.
results = results[0] # only one query
for res in results:
    datapoint = res.get('entity')
    if not datapoint: continue
    datapoint.pop('vector', None)


print(f"results for query \"{Q}\":")
pprint(results)