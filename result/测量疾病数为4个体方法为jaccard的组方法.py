import random
from sim.cal_groupsim import cal_2avglinkage,cal_2minlinkage,cal_2maxlinkage,cal_2funsimavg,cal_2funsimmax,cal_2bma
from sim.cal_rdgs import cal_2rdgs
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

def jizhunji(path, method):
    y_test_jizhun = []  # 0/1 真假
    y_score_jizhun = []  # 相似性得分
    f = open(path, 'r+')
    linelist = f.readlines()
    for line in linelist:
        line = line.strip('\n')
        line = line.split(' ')
        # print(line)
        disease_group1 = line[0]
        disease_group2 = line[1]
        # print(disease_group1, disease_group2)
        if method == 'avglinkage':
            sim = cal_2avglinkage('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(disease_group1), '{}'.format(disease_group2), 'jaccard')
        if method == 'minlinkage':
            sim = cal_2minlinkage('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(disease_group1), '{}'.format(disease_group2), 'jaccard')
        if method == 'maxlinkage':
            sim = cal_2maxlinkage('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(disease_group1), '{}'.format(disease_group2), 'jaccard')
        if method == 'funsimmax':
            sim = cal_2funsimmax('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(disease_group1), '{}'.format(disease_group2), 'jaccard')
        if method == 'funsimavg':
            sim = cal_2funsimavg('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(disease_group1), '{}'.format(disease_group2), 'jaccard')
        if method == 'bma':
            sim = cal_2bma('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(disease_group1), '{}'.format(disease_group2), 'jaccard')
        if method == 'rdgs':
            sim = cal_2rdgs('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(disease_group1), '{}'.format(disease_group2))
        sim = float(sim)
        y_test_jizhun.append(1)
        y_score_jizhun.append(sim)

    return y_test_jizhun, y_score_jizhun


def suijiji(path, method):
    f = open(path, 'r+')
    linelist = f.readlines()
    y_test_suiji = []  # 0/1
    y_score_suiji = [] # 相似性得分

    dt = {}
    for line in linelist:
        line = line.strip('\n')
        line = line.split(' ')
        disease_group_name = line[0]
        if disease_group_name[:9] not in dt:
            dt[disease_group_name[:9]] = []

    for line in linelist:
        line = line.strip('\n')
        line = line.split(' ')
        disease_group_name = line[0]
        if disease_group_name[:9] in dt:
            dt[disease_group_name[:9]].append(disease_group_name)

    j = 0
    while j < 440:
        j = j + 1
        while 1:
            random_key1 = random.sample(dt.keys(), 1)
            random_key1 = random_key1[0]
            random_key2 = random.sample(dt.keys(), 1)
            random_key2 = random_key2[0]
            if random_key1 is not random_key2:
                # print(random_key1, random_key2)
                break
        random_big_disease_group1 = dt[random_key1]
        random_big_disease_group2 = dt[random_key2]

        random_disease_group1 = random.sample(random_big_disease_group1, 1)
        random_disease_group1 = random_disease_group1[0]
        random_disease_group2 = random.sample(random_big_disease_group2, 1)
        random_disease_group2 = random_disease_group2[0]
        if method == 'avglinkage':
            sim = cal_2avglinkage('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(random_disease_group1), '{}'.format(random_disease_group2), 'jaccard')
        if method == 'minlinkage':
            sim = cal_2minlinkage('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(random_disease_group1), '{}'.format(random_disease_group2), 'jaccard')
        if method == 'maxlinkage':
            sim = cal_2maxlinkage('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(random_disease_group1), '{}'.format(random_disease_group2), 'jaccard')
        if method == 'funsimmax':
            sim = cal_2funsimmax('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(random_disease_group1), '{}'.format(random_disease_group2), 'jaccard')
        if method == 'funsimavg':
            sim = cal_2funsimavg('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(random_disease_group1), '{}'.format(random_disease_group2), 'jaccard')
        if method == 'bma':
            sim = cal_2bma('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(random_disease_group1), '{}'.format(random_disease_group2), 'jaccard')
        if method == 'rdgs':
            sim = cal_2rdgs('disease_gene', 'group_info', 'GROUP_ID', '{}'.format(random_disease_group1), '{}'.format(random_disease_group2))
        sim = float(sim)
        y_score_suiji.append(sim)
        y_test_suiji.append(0)

    return y_test_suiji, y_score_suiji


# print(suijiji('ICD10分组疾病数量大于等于4.txt'),'jaccard')

def get_fpr_tpr_threshold_rocauc(jizhun_path, suiji_path, method):
    y_test = []
    y_score = []
    y_test_jizhun, y_score_jizhun = jizhunji(jizhun_path, method)
    y_test_suiji, y_score_suiji = suijiji(suiji_path, method)
    y_test = y_test_jizhun + y_test_suiji
    y_score = y_score_jizhun + y_score_suiji
    # print(y_test, y_score)
    y_test = np.array(y_test)
    y_score = np.array(y_score)

    fpr, tpr, threshold = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    # print(roc_auc)
    return fpr, tpr, threshold, roc_auc

# 画图的部分
# print(get_fpr_tpr_threshold_rocauc('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'jaccard'))
#
fpr1, tpr1, threshold1, roc_auc1 = get_fpr_tpr_threshold_rocauc('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'avglinkage')
# print(fpr1, tpr1)
fpr2, tpr2, threshold2, roc_auc2 = get_fpr_tpr_threshold_rocauc('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'minlinkage')
fpr3, tpr3, threshold3, roc_auc3 = get_fpr_tpr_threshold_rocauc('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'maxlinkage')
fpr4, tpr4, threshold4, roc_auc4 = get_fpr_tpr_threshold_rocauc('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'funsimmax')
fpr5, tpr5, threshold5, roc_auc5 = get_fpr_tpr_threshold_rocauc('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'funsimavg')
fpr6, tpr6, threshold6, roc_auc6 = get_fpr_tpr_threshold_rocauc('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'bma')
fpr7, tpr7, threshold7, roc_auc7 = get_fpr_tpr_threshold_rocauc('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'rdgs')

font1 = {'weight': 'normal', 'size': 16}
plt.figure()
lw = 2
plt.figure(figsize=(10, 10))
plt.plot(fpr1, tpr1, color='darkorange', lw=lw, label='avglinkage ROC curve (area = %0.4f)' % roc_auc1)
plt.plot(fpr2, tpr2, color='navy', lw=lw, label='minlinkage ROC curve (area = %0.4f)' % roc_auc2)
plt.plot(fpr3, tpr3, color='cyan', lw=lw, label='maxlinkage ROC curve (area = %0.4f)' % roc_auc3)
plt.plot(fpr4, tpr4, color='black', lw=lw, label='funsimmax ROC curve (area = %0.4f)' % roc_auc4)
plt.plot(fpr5, tpr5, color='gold', lw=lw, label='funsimavg ROC curve (area = %0.4f)' % roc_auc5)
plt.plot(fpr6, tpr6, color='green', lw=lw, label='bma ROC curve (area = %0.4f)' % roc_auc6)
plt.plot(fpr7, tpr7, color='brown', lw=lw, label='R-DGS ROC curve (area = %0.4f)' % roc_auc7)

# plt.plot(fpr4, tpr4, color='darkgray', lw=lw, linestyle=':', label='ROC curve (area = %0.4f)' % roc_auc4)
# plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

plt.xlim([-0.05, 1.0])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate', font1)
plt.ylabel('True Positive Rate', font1)
plt.title('Receiver operating characteristic example', font1)
plt.legend(loc="lower right", prop=font1)
plt.show()


# def cal_100_avg(jizhunji_path, suijiji_path, method):
#     roc_list = []
#     for i in range(0, 10):
#         fpr, tpr, threshold, roc_auc = get_fpr_tpr_threshold_rocauc(jizhunji_path, suijiji_path, method)
#         roc_list.append(roc_auc)
#
#     roc_sum = 0
#     for num in roc_list:
#         roc_sum = roc_sum + num
#
#     roc_avg = roc_sum / len(roc_list)
#
#     return roc_avg
#
#
# print(cal_100_avg('4-基准集.txt', 'ICD10分组疾病数量大于等于4.txt', 'rdgs'))
