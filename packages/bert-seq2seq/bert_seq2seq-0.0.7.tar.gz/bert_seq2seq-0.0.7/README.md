# bert_seq2seq
一个轻量级的小框架。

pytorch实现bert做seq2seq任务，使用unilm方案。注意本项目可以做bert seq2seq 任何任务，比如对联，写诗，自动摘要等等等等，只要你下载数据集，并且写好对应train.py，即可，只需要改动很少代码，便可以重新训练新任务，如果喜欢的话欢迎star～ 如果遇到问题也可以提issue，保证会回复。

本框架目前可以做各种任务，一共分为三种：
1. seq2seq 比如写诗，对联，自动摘要等。
2. cls_classifier 通过提取句首的cls向量去做分类，比如情感分析，文本分类。
3. sequence_labeling 序列标注任务，比如命名实体识别，词性标注。
三种任务分别加载三种不同的模型，通过``` model_class="encoder"``` 参数去设置，具体看源码：
```python
def load_bert(vocab_path, model_name="roberta", model_class="seq2seq", target_size=0):
    """
    model_path: 模型位置
    这是个统一的接口，用来加载模型的
    model_class : seq2seq or cls or sequence_labeling
    """
    if model_class == "seq2seq":
        bert_model = Seq2SeqModel(vocab_path, model_name=model_name)
        return bert_model
    elif model_class == "cls":
        if target_size == 0:
            raise Exception("必须传入参数 target_size，才能确定预测多少分类")
        bert_model = BertClsClassifier(vocab_path, target_size, model_name=model_name)
        return bert_model
    elif model_class == "sequence_labeling":
        ## 序列标注模型
        if target_size == 0:
            raise Exception("必须传入参数 target_size，才能确定预测多少分类")
        bert_model = BertSeqLabeling(vocab_path, target_size, model_name=model_name)
        return bert_model
    else :
        raise Exception("model_name_err")
```

部分代码参考了 https://github.com/huggingface/transformers/ 和 https://github.com/bojone/bert4keras 
非常感谢！！！

### 安装 
1. 安装本框架 ```pip install bert-seq2seq```
2. 安装pytorch 
3. 安装tqdm 可以用来显示进度条 ```pip install tqdm```
### 运行
1. 下载想训练的数据集，可以专门建个corpus文件夹存放。
2. 使用roberta模型，模型和字典文件需要去 https://drive.google.com/file/d/1iNeYFhCBJWeUsIlnW_2K6SMwXkM4gLb_/view 这里下载。 具体可以参考这个github仓库～ https://github.com/ymcui/Chinese-BERT-wwm
3. 如果使用普通的bert模型，下载bert中文预训练权重 "bert-base-chinese": "https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-chinese-pytorch_model.bin", 下载bert中文字典 "bert-base-chinese": "https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-chinese-vocab.txt".
4. 去example文件夹下面运行对应的trainer.py，针对不同任务，运行不同train.py文件，进行训练。
5. 每次对于一个新的任务，只需要改动很少一部分代码，配置好模型位置，字典位置，写好数据处理构造输入输出(也就是read_corpus函数)即可。举个例子：
```python
class PoemTrainer:
    def __init__(self):
        # 加载数据
        data_dir = "./corpus/Poetry"
        self.vocab_path = "./state_dict/roberta_wwm_vocab.txt" # roberta模型字典的位置
        self.sents_src, self.sents_tgt = read_corpus(data_dir, self.vocab_path)
        self.model_name = "roberta" # 选择模型名字
        self.model_path = "./state_dict/roberta_wwm_pytorch_model.bin" # roberta模型位置
        self.recent_model_path = "" # 用于把已经训练好的模型继续训练
        self.model_save_path = "./bert_model.bin" #训练好的模型保存在哪
        self.batch_size = 16
        self.lr = 1e-5
```
在对应的train文件里面，只要配置好这些必要的信息，基本就可以开始训练了。开始一个新任务只需要10分钟改代码的时间。

### 效果
效果感觉还是很不错的～ 
#### 写诗
![image.png](http://www.zhxing.online/image/acb592f918894ca6b62435d2464d3cb0.png)
#### 新闻摘要文本分类（14分类）
![image.png](http://www.zhxing.online/image/724f93b03c19404fba4f684eac4695bc.png)
输出：
![image.png](http://www.zhxing.online/image/4175b02f928f43fc84e9c866aba3ee2d.png)
#### 对联
![image.png](http://www.zhxing.online/image/42eec322d6cc419da0efdc45c02d9f25.png)
![image.png](http://www.zhxing.online/image/25c1967ecfb14c5c9e68da7e3615ccf5.png)

![image.png](http://www.zhxing.online/image/540a4f1be41d4a3cbd2ccf1b26895868.png)

想看文章，可以去我网站～ http://www.blog.zhxing.online/#/readBlog?blogId=315 
多谢支持。另外，网站上面还有一些介绍unilm论文和特殊的mask如何实现的文章，可以去网站里搜索一下。http://www.blog.zhxing.online/#/

### 更新记录

2020.04.07: 添加了一个ner的example。

2020.04.07: 更新了pypi，并且加入了ner等序列标注任务的模型。

2020.04.04: 更新了pypi上面的代码，目前最新版本 0.0.6，请用最新版本，bug会比较少。

2020.04.04: 修复了部分bug，添加了新闻标题文本分类的例子

2020.04.02: 修改了beam-search中对于写诗的重复字和押韵惩罚程度，可能效果会更好。

2020.04.02: 添加了周公解梦的task

2020.04.02: 添加了对对联的task

2020.04.01: 添加了写诗的task

2020.04.01: 重构了代码，开始训练一个新的任务花费时间更少。

python setup.py sdist
twine upload dist/bert_seq2seq-0.0.1.tar.gz

