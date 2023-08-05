import tkitText
from transformers import BertTokenizer, BertForNextSentencePrediction
import torch
# import random
class NextSents:
    """
    处理各种csv数据
    """
    def __init__(self,model_path):
        self.model_path=model_path
        pass
    def load_model(self):
        self.tokenizer = BertTokenizer.from_pretrained(self.model_path)
        self.model = BertForNextSentencePrediction.from_pretrained(self.model_path)
        # return model,tokenizer
    def pre_one(self,text_a,text_b):
        """
        预测一条数据
        输入 句子a，句子b
        返回值
        预测结果，是下一句的概率
        """
        ptext=text_a+"[SEP]"+text_b
        input_ids = torch.tensor(self.tokenizer.encode(ptext, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
        outputs = self.model(input_ids)
        # print(outputs)
        seq_relationship_scores = outputs[0]
        # print(seq_relationship_scores)
        # print(seq_relationship_scores.softmax(dim = 1).tolist()[0][1])
        # print(sent)
        # print(torch.argmax(seq_relationship_scores).tolist())
        return torch.argmax(seq_relationship_scores).tolist(),seq_relationship_scores.softmax(dim = 1).tolist()[0][1]
    def pre_from_sents(self,text_a,sents):
        for sent in sents:
            yield  self.pre_one(text_a,sent)
    # 获取列表的第1个元素
    def takeSecond(self,elem):
        return elem[0]
    def  pre_from_text(self,text_a,text):
        """
        返回文本中可以作为下一句的句子
        """
        tt=tkitText.Text()
 
        c=[]
        for sent in tt.sentence_segmentation_v1(text):
            p,r=self.pre_one(text_a,sent)
            # print(p,r)
            # if p==1:
            c.append((r,sent))
        # 指定第1个元素排序
        c.sort(key=self.takeSecond,reverse=True)
        return c


