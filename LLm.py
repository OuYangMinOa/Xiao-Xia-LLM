# LLM

import os

CACHEFLODER = str(os.getenv('CACHE'))
MODELNAME   = str(os.getenv('MODEL'))
PFTMNAME    = str(os.getenv('PFTM'))

os.environ['TRANSFORMERS_CACHE'] = CACHEFLODER
os.environ['HF_DATASETS_CACHE' ] = CACHEFLODER
os.environ['HF_HOME'           ] = CACHEFLODER

import torch
import transformers

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModel
from peft         import PeftModel
from opencc       import OpenCC

transformers.logging.set_verbosity_error()


def preprocess(text): 
    return OpenCC('hk2s').convert(text)

def postprocess(text):
    return OpenCC('s2t').convert(text)


def LOAD_LLM_MODEL():
    device = torch.device('cuda')
    print("[*] Load model")
    tokenizer = AutoTokenizer.from_pretrained(MODELNAME, trust_remote_code=True)
    model = AutoModel.from_pretrained(MODELNAME, trust_remote_code=True)
    model = PeftModel.from_pretrained(model,PFTMNAME)
    # model = model.half().quantize(4).cuda()
    model = model.half().quantize(4).cuda()
    print(f"[*] Memory usage :{model.get_memory_footprint()/1024**3}GB")

    def answer(text, top_p=0.2, temperature=0.01, sample=True):
        text = text.strip()
        text = preprocess(text)
        encoding = tokenizer(text=[text], truncation=True, padding=True, max_length=2048, return_tensors="pt").to(device) 
        if not sample:
            out = model.generate(**encoding, return_dict_in_generate=False, output_scores=False, max_new_tokens=2048, num_beams=10, length_penalty=0.6)
        else:
            out = model.generate(**encoding, return_dict_in_generate=False, output_scores=False, max_new_tokens=2048, do_sample=True, top_p=top_p, temperature=temperature)
        del encoding
        out_text = tokenizer.batch_decode(out, skip_special_tokens=True)
        return postprocess(out_text[0])[len(text):]
    return answer



