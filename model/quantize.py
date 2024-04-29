import importlib
import os

# Base Model : https://huggingface.co/SadokBarbouche/planned.AI-gemma-2b-it
# Quantized Model : https://huggingface.co/SadokBarbouche/planned.AI-gemma-2b-it-quantized

if importlib.import_module("mlx_lm") is None:
    os.system("pip install mlx-lm")

os.system("python -m mlx_lm.convert --hf-path SadokBarbouche/planned.AI-gemma-2b-it -q --upload-repo SadokBarbouche/planned.AI-gemma-2b-it-quantized")