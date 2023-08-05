import torch
from bert_seq2seq.seq2seq_model import Seq2SeqModel
from bert_seq2seq.bert_encoder import BertEncoder

def load_bert(vocab_path, model_name="roberta", model_class="seq2seq", target_size=0):
    """
    model_path: 模型位置
    这是个统一的接口，用来加载模型的
    model_class : seq2seq or encoder
    """
    if model_class == "seq2seq":
        bert_model = Seq2SeqModel(vocab_path, model_name=model_name)
        return bert_model
    elif model_class == "encoder":
        if target_size == 0:
            raise Exception("必须传入参数 target_size，才能确定预测多少分类")
        bert_model = BertEncoder(vocab_path, target_size, model_name=model_name)
        return bert_model
    else :
        raise Exception("model_name_err")

def load_model_params(model, pretrain_model_path):
        
        checkpoint = torch.load(pretrain_model_path)
        # 模型刚开始训练的时候, 需要载入预训练的BERT
        checkpoint = {k[5:]: v for k, v in checkpoint.items()
                                            if k[:4] == "bert" and "pooler" not in k}
        model.load_state_dict(checkpoint, strict=False)
        torch.cuda.empty_cache()
        print("{} loaded!".format(pretrain_model_path))

def load_recent_model(model, recent_model_path):
    checkpoint = torch.load(recent_model_path)
    model.load_state_dict(checkpoint)
    torch.cuda.empty_cache()
    print(str(recent_model_path) + "loaded!")





    
    



