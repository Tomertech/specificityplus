#!/usr/bin/env python3
"""Script for generating experiments.txt""" 

examples = 22000
split_into = 110

models = ["gpt2-medium", "gpt2-xl", "EleutherAI/gpt-J-6B", "EleutherAI/gpt-neox-20b"]

hparams_ROME = {"gpt2-medium":"gpt2-medium.json", "gpt2-xl":"gpt2-xl.json", "EleutherAI/gpt-J-6B":"EleutherAI_gpt-j-6B.json", "EleutherAI/gpt-neox-20b":"EleutherAI_gpt-neox-20b.json"}
hparams_MEND = {"gpt2-medium":"gpt2-medium_CF.json", "gpt2-xl":"gpt2-xl_CF.json", "EleutherAI/gpt-J-6B":"EleutherAI_gpt-j-6B_CF.json", "EleutherAI/gpt-neox-20b":"EleutherAI_gpt-neox-20b_CF.json"}
hparams_IDENTITY = {"gpt2-medium":"gpt2-medium_constr.json", "gpt2-xl":"gpt2-xl_constr.json", "EleutherAI/gpt-J-6B":"EleutherAI_gpt-j-6B_constr.json", "EleutherAI/gpt-neox-20b":"EleutherAI_gpt-neox-20b_constr.json"}
hparams_FT = {"gpt2-medium":"gpt2-medium_constr.json", "gpt2-xl":"gpt2-xl_constr.json", "EleutherAI/gpt-J-6B":"EleutherAI_gpt-j-6B_constr.json", "EleutherAI/gpt-neox-20b":"EleutherAI_gpt-neox-20b_constr.json"}

hparams_dict = {"ROME":hparams_ROME, "MEND":hparams_MEND, "IDENTITY":hparams_IDENTITY, "FT":hparams_FT}

filename = {"gpt2-medium":"exp_gpt2medium.txt", "gpt2-xl":"exp_gpt2xl.txt", "EleutherAI/gpt-J-6B":"exp_gptj6b.txt", "EleutherAI/gpt-neox-20b":"exp_gptneox20b.txt"}

dataset_size = examples // split_into
if dataset_size * split_into != examples:
    raise ValueError("Dataset size must be divisible by split_into")


#get starting indexes
start_indexes = [i * examples // split_into for i in range(split_into)]

ALGS = ["ROME","FT", "MEND", "IDENTITY"]
for model in models:
    file_path = "experiment-scripts/" + filename[model]
    output_file = open(file_path, "w")

    base_call = (f"python experiments/evaluate.py --model_name {model} \
 --ds_name cf --dataset_size {dataset_size}")
    for alg_name in ALGS:
        for start_i in start_indexes:  
            # Note that we don't set a seed for rep - a seed is selected at random
            # and recorded in the output data by the python script
            hparams_fname = hparams_dict[alg_name][model]
            expt_call = (
                f"{base_call} "
                f"--start_index {start_i} "
                f"--alg_name {alg_name} "
                f"--hparams_fname {hparams_fname}"
            )

            call = "cd git/memitpp" + " && " + expt_call

            print(call, file=output_file)
    output_file.close()