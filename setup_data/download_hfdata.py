## run on headnode

from datasets import load_dataset

#get huggingface data
ds_names = ["wikipedia"]#["wikitext", "wikipedia"]
for ds_name in ds_names:
    load_dataset(ds_name, dict(wikitext="wikitext-103-raw-v1", wikipedia="20220301.en")[ds_name])
