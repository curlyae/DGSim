import random
from sim.cal_rdgs import cal_2rdgs
f = open('ICD10分组疾病数量大于等于4.txt', 'r+')
f1 = open('疾病数为4时所有ICD同组疾病组相似度不为0时的基准集.txt', 'w+')
linelist = f.readlines()

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

# 寻找基准集
for key in dt:
    # print(dt[key])
    if len(dt[key]) >= 2:
        disease_group_list = dt[key]
        for disease_group1 in disease_group_list:
            index_disease_group1 = disease_group_list.index(disease_group1)
            for disease_group2 in disease_group_list[index_disease_group1:]:
                if disease_group1 is not disease_group2:
                    sim = cal_2rdgs('disease_gene', 'group_info', 'GROUP_ID', disease_group1, disease_group2)
                    sim_num = float(sim)
                    if sim_num != 0:
                        print(sim)
                        f1.write(disease_group1+'\t'+disease_group2+'\t'+sim+'\t'+'1'+'\n')
                        f1.flush()

