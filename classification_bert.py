import transformers as ppb
import numpy as np
import torch
import pickle
import os
from sklearn.linear_model import LogisticRegression
import pandas as pd


# For DistilBERT:
model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')

## Want BERT instead of distilBERT? Uncomment the following line:
#model_class, tokenizer_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')

# Load pretrained model/tokenizer
tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
model = model_class.from_pretrained(pretrained_weights)

def is_causal(batch_1):
    batch_1 = pd.DataFrame({0: batch_1})[0]
    tokenized = batch_1.apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))

    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)

    padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)  
    attention_mask = torch.tensor(attention_mask)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
    bert_output = last_hidden_states[0][:,0,:].numpy()

    path = os.path.dirname(os.path.abspath(__file__))
    lr_clf = pickle.load(open(f"{path}/bert_model.skl", 'rb'))

    predictions = list(lr_clf.predict(bert_output))

    return predictions