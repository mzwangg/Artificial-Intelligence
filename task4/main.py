# 导入相关的包
import warnings

warnings.filterwarnings('ignore')
import os

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
import pandas as pd
import numpy as np

# 数据集的路径
data_path = "./datasets/5f9ae242cae5285cd734b91e-momodel/sms_pub.csv"
# 读取数据
sms = pd.read_csv(data_path, encoding='utf-8')
# 显示前 5 条数据
sms.head()

from sklearn.model_selection import train_test_split

X = np.array(sms.msg_new)
y = np.array(sms.label)
# posX= X[np.where(y==1)]
# posy= y[np.where(y==1)]
# for i in range(4):
#     X=np.append(X,posX)
#     y=np.append(y,posy)

x1 = X[np.where(y==1)]
y1 = y[np.where(y==1)]
x0 = np.random.choice(X[np.where(y==0)],len(x1))
y0 = np.zeros(len(x1))
X = np.append(x0,x1)
y = np.append(y0,y1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.1)
print("总共的数据大小", X.shape)
print("训练集数据大小", X_train.shape)
print("测试集数据大小", X_test.shape)

import os

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

# ---------- 停用词库路径，若有变化请修改 -------------
stopwords_path = r'scu_stopwords.txt'


# ---------------------------------------------------

def read_stopwords(stopwords_path):
    stopwords = []
    # ----------- 请完成读取停用词的代码 ------------
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stopwords = f.read()
    stopwords = stopwords.splitlines()
    # ----------------------------------------------

    return stopwords


# 读取停用词
stopwords = read_stopwords(stopwords_path)

# ----------------- 导入相关的库 -----------------
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import ComplementNB

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MaxAbsScaler

# pipline_list用于传给Pipline作为参数
pipeline_list = [
    # --------------------------- 需要完成的代码 ------------------------------

    # ========================== 以下代码仅供参考 =============================
    ('cv', TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", stop_words=stopwords, max_df=0.25)),
    ('MaxAbsScaler', MaxAbsScaler()),
    ('classifier', MultinomialNB())
    # ========================================================================

    # ------------------------------------------------------------------------
]

# 搭建 pipeline
pipeline = Pipeline(pipeline_list)

# 训练 pipeline
pipeline.fit(X_train, y_train)

# 对测试集的数据集进行预测
y_pred = pipeline.predict(X_test)

# 在测试集上进行评估
from sklearn import metrics

print("在测试集上的混淆矩阵：")
print(metrics.confusion_matrix(y_test, y_pred))
print("在测试集上的分类结果报告：")
print(metrics.classification_report(y_test, y_pred))
print("在测试集上的 f1-score ：")
print(metrics.f1_score(y_test, y_pred))

# 在所有的样本上训练一次，充分利用已有的数据，提高模型的泛化能力
pipeline.fit(X, y)
# 保存训练的模型，请将模型保存在 results 目录下
