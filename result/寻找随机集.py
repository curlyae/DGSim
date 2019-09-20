import random
from sim.cal_rdgs import cal_2rdgs
f = open('ICD10分组疾病数量大于等于4.txt', 'r+')
f1 = open('疾病数为4时所有ICD同组疾病组相似度不为0时的随机集.txt', 'w+')

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

# 寻找随机集
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
    sim = cal_2rdgs('disease_gene', 'group_info', 'GROUP_ID', random_disease_group1, random_disease_group2)
    sim_num = float(sim)
    f1.write(random_disease_group1+'\t'+random_disease_group2+'\t'+sim+'\t'+'0'+'\n')
    f1.flush()