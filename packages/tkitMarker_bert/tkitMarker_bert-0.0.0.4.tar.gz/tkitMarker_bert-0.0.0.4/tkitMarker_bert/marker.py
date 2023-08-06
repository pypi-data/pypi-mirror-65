

import numpy as np
import torch
from transformers import AutoModelForTokenClassification,AutoTokenizer
import os
import re
import tkitFile
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search
# from elasticsearch_dsl import Q
# from config import *
from tqdm import tqdm
import time
import tkitText

class Marker:
    def __init__(self,model_path="../model",device='cpu'):
        self.model_path=model_path
        self.labels_file=os.path.join(model_path,"labels.txt")
        self.device=device
        pass
    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        model = AutoModelForTokenClassification.from_pretrained(self.model_path)
        model.to(self.device)
        f2=open(self.labels_file,'r')
        lablels_dict={}
        for i,line in enumerate(f2):
            # l=line.split(" ")
            l=line.replace("\n",'')
            # print(l)
            lablels_dict[i]=l
        f2.close()
        self.lablels_dict=lablels_dict
        return model,tokenizer
    def cut_text(self,text,lenth):
        """
        分割固定长度字符串
        """
        textArr = re.findall('.{'+str(lenth)+'}', text)
        textArr.append(text[(len(textArr)*lenth):])
        return textArr
    def clear_word(self,word):
        return word.replace("##", "")
    def pre(self,word,text,model,tokenizer):
        model.eval()
        text=word+"[SEP]"+text
        lenth=509-len(word)
        all_ms=[]
        for text_mini in self.cut_text(text,lenth):
            # text_mini=word+"[SEP]"+text_mini
            ids=tokenizer.encode_plus(word,text_mini,max_length=512, add_special_tokens=True)
            # print(ids)
            input_ids = torch.tensor(ids['input_ids']).unsqueeze(0)  # Batch size 1
            labels = torch.tensor([1] * input_ids.size(1)).unsqueeze(0)  # Batch size 1
            outputs = model(input_ids, labels=labels)
            # print(outputs)
            tmp_eval_loss, logits  = outputs[:2]
            # ids=tokenizer.encode(text)
            # print(ids)

            # print("\n".join([i for i in self.lablels_dict.keys()]))
            words=[]
            for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
                # print(m)
                # print(m,ids[i],tokenizer.convert_ids_to_tokens(ids[i]),self.lablels_dict[m])
                word=tokenizer.convert_ids_to_tokens(ids['input_ids'][i])

                if m >=len(self.lablels_dict):
                    mark_lable="X"
                else:
                    mark_lable=self.lablels_dict[m]

                if mark_lable=="E-描述"  and len(words)>0:
                    
                    words.append(word)
                    # words.append(word+mark_lable)
                    # print(words)
                    
                    all_ms.append(self.clear_word("".join(words)))
                    words=[]
                elif mark_lable=="S-描述":
                    words=[]
                    words.append(word)
                    # words.append(word+mark_lable)
                    all_ms.append(self.clear_word("".join(words)))
                    words=[]
                elif mark_lable=="B-描述":
                    words=[]
                    words.append(word)
                    # words.append(word+mark_lable)
                elif mark_lable=="M-描述" and len(words)>0:
                    words.append(word)
                    # words.append(word+mark_lable)
                elif  mark_lable=="O" or mark_lable=="X":
                    words=[]
                    pass
        return all_ms

    def pre_ner(self,text,model,tokenizer):
        model.eval()
        text=text
        lenth=128
        all_ms=[]
        for text_mini in self.cut_text(text,lenth):
            # text_mini=word+"[SEP]"+text_mini
            ids=tokenizer.encode_plus(text_mini,max_length=512, add_special_tokens=True)
            # print(ids)
            input_ids = torch.tensor(ids['input_ids']).unsqueeze(0)  # Batch size 1
            labels = torch.tensor([1] * input_ids.size(1)).unsqueeze(0)  # Batch size 1
            outputs = model(input_ids, labels=labels)
            # print(outputs)
            tmp_eval_loss, logits  = outputs[:2]
            # ids=tokenizer.encode(text)
            # print(ids)

            # print("\n".join([i for i in self.lablels_dict.keys()]))
            words=[]
            for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
                # print(m)
                # print(m,ids[i],tokenizer.convert_ids_to_tokens(ids[i]),self.lablels_dict[m])
                word=tokenizer.convert_ids_to_tokens(ids['input_ids'][i])
                # print(word,self.lablels_dict[m])
                if m >=len(self.lablels_dict):
                    mark_lable="X"
                else:
                    mark_lable=self.lablels_dict[m]

                if mark_lable=="E-实体"  and len(words)>0:
                    
                    words.append(word)
                    # print(words)
                    all_ms.append(self.clear_word("".join(words)))
                    words=[]
                elif mark_lable=="S-实体":
                    words=[]
                    words.append(word)
                    all_ms.append(self.clear_word("".join(words)))
                    words=[]
                elif mark_lable=="B-实体":
                    words=[]
                    words.append(word)
                elif mark_lable=="M-实体"  and len(words)>0:
                    words.append(word)
                elif  mark_lable=="O" or mark_lable=="X":
                    words=[]
                    pass
        return all_ms

