from sim.cal_rdgs import cal_2rdgs
f = open('ICD10分组疾病数量大于等于4.txt')

linelist = f.readlines()

disease_group_list = []
for line in linelist:
    line = line.strip('\n')
    line = line.split(' ')
    disease_group = line[0]
    disease_group_list.append(disease_group)

# disease_group_list = [1, 2, 3, 4, 5]
print(disease_group_list)
for disease_group1 in disease_group_list:
    index_disease_group1 = disease_group_list.index(disease_group1)
    # print(index_disease_group1)
    for disease_group2 in disease_group_list[index_disease_group1+1:]:
        sim = cal_2rdgs('disease_gene', 'group_info', 'GROUP_ID', disease_group1, disease_group2)
        if sim is not '0.00000':
            print(disease_group1+'\t'+disease_group2+'\t'+sim)