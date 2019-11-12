import pandas as pd

def load_starspace_embeddings(dump_path, prefix='public_', sort_idx=False):
    embeddings_df = pd.read_csv(dump_path, sep='\t', header=None)
    embeddings_df.set_index(0, inplace=True)
    embeddings_df.index = embeddings_df.index.map(lambda x: int(x.replace(prefix, '')))
    if sort_idx:
        embeddings_df.sort_index(inplace=True)
    return embeddings_df

def load_custom_embeddigns(dump_path, index_col='id', sort_idx=False):
    embeddings_df = pd.read_csv(dump_path)
    embeddings_df.set_index(index_col, inplace=True)
    if sort_idx:
        embeddings_df.sort_index(inplace=True)
    return embeddings_df