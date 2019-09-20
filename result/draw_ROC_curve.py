import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def get_roc_auc(path):
    f = open(path, 'r+')
    linelist = f.readlines()
    y_test = []
    y_score = []
    for line in linelist:
        line = line.strip('\n').split('\t')
        test = int(line[3])
        score = float(line[2])
        y_test.append(test)
        y_score.append(score)
    y_test = np.array(y_test)
    y_score = np.array(y_score)
    # print(y_test, y_scores)
    fpr, tpr, threshold = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    return fpr, tpr, threshold, roc_auc


fpr1, tpr1, threshold1, roc_auc1 = get_roc_auc('4-数据集.txt')
fpr2, tpr2, threshold2, roc_auc2 = get_roc_auc('3-数据集.txt')
fpr3, tpr3, threshold3, roc_auc3 = get_roc_auc('2-数据集.txt')
# fpr4, tpr4, threshold4, roc_auc4 = get_roc_auc('.txt')
plt.figure()
lw = 2
plt.figure(figsize=(10, 10))
plt.plot(fpr1, tpr1, color='darkorange', lw=lw, label='disease number >=4 ROC curve (area = %0.4f)' % roc_auc1)
plt.plot(fpr2, tpr2, color='navy', lw=lw, linestyle='--', label='disease number >= 3 ROC curve (area = %0.4f)' % roc_auc2)
plt.plot(fpr3, tpr3, color='cyan', lw=lw, linestyle='-.', label='disease number >= 2 ROC curve (area = %0.4f)' % roc_auc3)
# plt.plot(fpr4, tpr4, color='darkgray', lw=lw, linestyle=':', label='ROC curve (area = %0.4f)' % roc_auc4)
# plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

plt.xlim([-0.05, 1.0])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
