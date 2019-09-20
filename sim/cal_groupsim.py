import numpy as np
from sim.cal_individualsim import *
from data.connect_database import *
import numpy as np


def cal_2avglinkage(database_name, table_name, primary_key, group_name1, group_name2, indi_method):
    """
        Calculate similarity between two disease groups based on average linkage method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key used to query disease information in database
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: avg_linkage
            The average_linkage similarity between two diseases
    """

    ###############################
    # 得到疾病组的疾病信息
    ###############################

    disease_list1 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name1)[1]
    disease_list2 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name2)[1]
    # print(disease_list1)

    disease_list1 = disease_list1.split(',')
    disease_list2 = disease_list2.split(',')

    # print(disease_list2)

    sim_list = []  # 列表，两两疾病相似值计算后加入该列表中

    for disease1 in disease_list1:
        for disease2 in disease_list2:
            if indi_method == 'jaccard':
                sim = cal_2indijaccard(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'cosine':
                sim = cal_2indicosine(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'lin':
                sim = cal_2indilin(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'mathur':
                sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            else:
                print("wrong individual similarity method!")
                exit(0)

    sim_sum = 0
    for sim_value in sim_list:
        sim_sum = sim_sum + sim_value

    avg_linkage = sim_sum / len(sim_list)

    avg_linkage = '%.5f' % avg_linkage

    return avg_linkage


# print(cal_2avglinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "jaccard"))
# print(cal_2avglinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "cosine"))
# print(cal_2avglinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "lin"))

# print(cal_2avglinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "mathur"))


def cal_groupavglinkage(database_name, table_name, primary_key, group_list1, group_list2, indi_method):
    """
        Calculate the similarity matrix between two lists of disease group based on average linkage
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_list1: string
            A list of disease group for calculating similarity
    :param group_list2: string
            A list of disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: sim
            The average linkage similarity matrix between the two lists of disease group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2avglinkage(database_name, table_name, primary_key , group_name1, group_name2 ,indi_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_groupavglinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90,ICD10CM:A15",
#                           "ICD10CM:A90,ICD10CM:A15", "mathur"))


def cal_2minlinkage(database_name, table_name, primary_key, group_name1, group_name2, indi_method):
    """
        Calculate similarity between two disease groups based on single linkage method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key used to query disease information in database
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: min_linkage
            The min_linkage similarity between two diseases
    """
    ###############################
    # 得到疾病组的疾病信息
    ###############################

    disease_list1 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name1)[1]
    disease_list2 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name2)[1]
    # print(disease_list1)

    disease_list1 = disease_list1.split(',')
    disease_list2 = disease_list2.split(',')

    # print(disease_list2)

    sim_list = []  # 列表，两两疾病相似值计算后加入该列表中

    for disease1 in disease_list1:
        for disease2 in disease_list2:
            if indi_method == 'jaccard':
                sim = cal_2indijaccard(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'cosine':
                sim = cal_2indicosine(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'lin':
                sim = cal_2indilin(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'mathur':
                sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            else:
                print("wrong individual similarity method!")
                exit(0)

    min_linkage = min(sim_list)

    min_linkage = '%.5f' % min_linkage

    return min_linkage


# print(cal_2minlinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "jaccard"))

def cal_groupminlinkage(database_name, table_name, primary_key, group_list1, group_list2, indi_method):
    """
           Calculate the similarity matrix between two lists of disease group based on single linkage
       :param database_name: string
               The database to connect to
       :param table_name: string
               The database table being queried
       :param primary_key: string
               The primary key of database table
       :param group_list1: string
               A list of disease group for calculating similarity
       :param group_list2: string
               A list of disease group for calculating similarity
       :param indi_method: string
               Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
               jaccard/cosine/lin/mathur
       :return: sim
               The single linkage similarity matrix between the two lists of disease group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2minlinkage(database_name, table_name, primary_key, group_name1, group_name2, indi_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_groupminlinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90,ICD10CM:A15",
#                           "ICD10CM:A90,ICD10CM:A15", "jaccard"))


def cal_2maxlinkage(database_name, table_name, primary_key, group_name1, group_name2, indi_method):
    """
        Calculate similarity between two disease groups based on complete linkage method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key used to query disease information in database
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: max_linkage
            The max_linkage similarity between two diseases
    """
    ###############################
    # 得到疾病组的疾病信息
    ###############################

    disease_list1 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name1)[1]
    disease_list2 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name2)[1]
    # print(disease_list1)

    disease_list1 = disease_list1.split(',')
    disease_list2 = disease_list2.split(',')

    # print(disease_list2)

    sim_list = []  # 列表，两两疾病相似值计算后加入该列表中

    for disease1 in disease_list1:
        for disease2 in disease_list2:
            if indi_method == 'jaccard':
                sim = cal_2indijaccard(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'cosine':
                sim = cal_2indicosine(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'lin':
                sim = cal_2indilin(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            elif indi_method == 'mathur':
                sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                sim_list.append(sim)

            else:
                print("wrong individual similarity method!")
                exit(0)

    max_linkage = max(sim_list)

    max_linkage = '%.5f' % max_linkage

    return max_linkage


# print(cal_2maxlinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "jaccard"))


def cal_groupmaxlinkage(database_name, table_name, primary_key, group_list1, group_list2, indi_method):
    """
           Calculate the similarity matrix between two lists of disease group based on complete linkage
       :param database_name: string
               The database to connect to
       :param table_name: string
               The database table being queried
       :param primary_key: string
               The primary key of database table
       :param group_list1: string
               A list of disease group for calculating similarity
       :param group_list2: string
               A list of disease group for calculating similarity
       :param indi_method: string
               Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
               jaccard/cosine/lin/mathur
       :return: sim
               The complete linkage similarity matrix between the two lists of disease group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(grouplist1)
    # n = len(grouplist2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2minlinkage(database_name, table_name, primary_key, group_name1, group_name2, indi_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_groupmaxlinkage("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90,ICD10CM:A15",
#                           "ICD10CM:A90,ICD10CM:A15", "jaccard"))#


def cal_2modulejaccard(database_name, table_name, primary_key, group_name1, group_name2):
    """
        Calculate similarity between two disease groups based on Jaccard Index module method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :return: jaccard_num
            The jaccard Index similarity between two disease group
    """

    gene_list1 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[1]
    gene_list2 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[1]

    shared_gene_list = get_2diseasegroup_shared_gene(database_name, table_name, group_name1, group_name2, primary_key)[2]

    gene_list1 = gene_list1.split(',')
    gene_list2 = gene_list2.split(',')
    shared_gene_list = shared_gene_list.split(',')
    # print(gene_list1)
    # print(gene_list2)
    # print(shared_gene_list)

    gene_list1_len = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[2]
    gene_list2_len = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[2]
    shared_gene_list_len = get_2diseasegroup_shared_gene(database_name, table_name, group_name1, group_name2,
                                                         primary_key)[3]

    # print(gene_list1_len,gene_list2_len, shared_gene_list_len)
    jaccard_num = float(shared_gene_list_len) / (float(gene_list1_len) + float(gene_list2_len) -
                                                 float(shared_gene_list_len))

    jaccard_num = '%.5f' % jaccard_num

    return jaccard_num


# print(cal_2modulejaccard("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15"))


def cal_groupmodulejaccard(database_name, table_name, primary_key, group_list1, group_list2):
    """
        Calculate the similarity matrix between two lists of disease group based on Jaccard Index method
       :param database_name: string
               The database to connect to
       :param table_name: string
               The database table being queried
       :param primary_key: string
               The primary key of database table
       :param group_list1: string
               A list of disease group for calculating similarity
       :param group_list2: string
               A list of disease group for calculating similarity
       :return: sim
               The Jaccard Index similarity matrix between the two lists of disease group
    """
    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')

    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []
    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2modulejaccard(database_name, table_name, primary_key, group_name1, group_name2)
            a.append(s)
        lst.append(a)
    # print(lst)
    sim = np.matrix(lst)

    # print(type(sim))

    return sim


# print(cal_groupmodulejaccard("disease_gene", "group_info", "GROUP_ID","ICD10CM:A90,ICD10CM:A15",
#                              "ICD10CM:A90,ICD10CM:A15" ))
#
def cal_2modulecosine(database_name, table_name, primary_key, group_name1, group_name2):
    """
        Calculate similarity between two disease groups based on Cosine module method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :return: cosine_num
            The Cosine similarity between two disease group
    """
    gene_list1 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[1]
    gene_list2 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[1]

    shared_gene_list = get_2diseasegroup_shared_gene(database_name, table_name, group_name1, group_name2, primary_key)[
        2]

    cosine_list1 = gene_list1.split(',')
    cosine_list2 = gene_list2.split(',')
    shared_gene_list = shared_gene_list.split(',')
    # print(gene_list1)
    # print(gene_list2)
    # print(shared_gene_list)

    cosine_set1 = set(cosine_list1)
    cosine_set2 = set(cosine_list2)

    set1_union_set2 = cosine_set1 | cosine_set2

    vector1 = []
    vector2 = []

    #######################################################
    # 原来的部分，只看其出现没出现，设置0/1，不关心其出现的次数
    #######################################################
    # for item in set1_union_set2:
    #     if item in cosine_set1:
    #         vector1.append(1)
    #     elif item not in cosine_set1:
    #         vector1.append(0)
    #     if item in cosine_set2:
    #         vector2.append(1)
    #     elif item not in cosine_set2:
    #         vector2.append(0)
    # print(vector1)
    # print(vector2)

    for item in set1_union_set2:
        num = 0
        for key in cosine_list1:
            if key == item:
                num = num + 1
        vector1.append(num)

    for item in set1_union_set2:
        num = 0
        for key in cosine_list2:
            if key == item:
                num = num + 1
        vector2.append(num)

    vectorlen = len(set1_union_set2)
    a = b = c = 0
    for i in range(vectorlen):
        a = a + vector1[i] * vector2[i]
        b = b + vector1[i] * vector1[i]
        c = c + vector2[i] * vector2[i]
    cosine_num = a / ((b ** 0.5) * (c ** 0.5))
    cosine_num = '%.5f' % cosine_num

    return cosine_num


# print(cal_2modulecosine("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15"))


def cal_groupmodulecosine(database_name, table_name, primary_key, group_list1, group_list2):
    """
        Calculate the similarity matrix between two lists of disease group based on Cosine method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_list1: string
            A list of disease group for calculating similarity
    :param group_list2: string
            A list of disease group for calculating similarity
    :return: sim
            The Cosine similarity matrix between the two lists of disease group
    """
    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')

    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []
    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2modulecosine(database_name, table_name, primary_key, group_name1, group_name2)
            a.append(s)
        lst.append(a)
    # print(lst)
    sim = np.matrix(lst)

    # print(type(sim))

    return sim


# print(cal_groupmodulecosine("disease_gene", "group_info", "GROUP_ID","ICD10CM:A90,ICD10CM:A15",
#                             "ICD10CM:A90,ICD10CM:A15"))


def cal_2modulelin(database_name, table_name, primary_key, group_name1, group_name2):
    """
        Calculate similarity between two disease groups based on Lin's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :return: lin_num
            The Lin's method similarity between two disease group
    """

    gene_list1 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[1]
    gene_list2 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[1]

    shared_gene_list = get_2diseasegroup_shared_gene(database_name, table_name, group_name1, group_name2, primary_key)[2]

    gene_list1 = gene_list1.split(',')
    gene_list2 = gene_list2.split(',')
    shared_gene_list = shared_gene_list.split(',')
    # print(gene_list1)
    # print(gene_list2)
    # print(shared_gene_list)

    gene_list1_len = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[2]
    gene_list2_len = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[2]
    shared_gene_list_len = get_2diseasegroup_shared_gene(database_name, table_name, group_name1, group_name2,
                                                         primary_key)[3]

    # print(gene_list1_len,gene_list2_len, shared_gene_list_len)

    lin_num = (2 * float(shared_gene_list_len)) / (gene_list1_len + gene_list2_len)
    lin_num = '%.5f' % lin_num

    return lin_num


# print(cal_2modulelin("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15"))


def cal_groupmodulelin(database_name, table_name, primary_key, group_list1, group_list2):
    """
        Calculate the similarity matrix between two lists of disease group based on Lin's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_list1: string
            A list of disease group for calculating similarity
    :param group_list2: string
            A list of disease group for calculating similarity
    :return: sim
            The Lin's method similarity matrix between the two lists of disease group
    """
    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')

    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []
    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2modulecosine(database_name, table_name, primary_key, group_name1, group_name2)
            a.append(s)
        lst.append(a)
    # print(lst)
    sim = np.matrix(lst)

    # print(type(sim))

    return sim


# print(cal_groupmodulelin("disease_gene", "group_info", "GROUP_ID","ICD10CM:A90,ICD10CM:A15",
#                          "ICD10CM:A90,ICD10CM:A15"))


def cal_2modulemathur(database_name, table_name, primary_key, group_name1, group_name2):
    """
        Calculate similarity between two disease groups based on Mathur's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :return: mathur_num
            The Mathur's method similarity between two disease group
    """

    gene_list1 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[1]
    gene_list2 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[1]

    shared_gene_list = get_2diseasegroup_shared_gene(database_name, table_name, group_name1, group_name2, primary_key)[2]

    gene_list1 = gene_list1.split(',')
    gene_list2 = gene_list2.split(',')
    shared_gene_list = shared_gene_list.split(',')
    # print(gene_list1)
    # print(gene_list2)
    # print(shared_gene_list)

    gene_list1_len = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[2]
    gene_list2_len = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[2]
    shared_gene_list_len = get_2diseasegroup_shared_gene(database_name, table_name, group_name1, group_name2,
                                                         primary_key)[3]

    all_gene_num = get_all_gene_num(database_name, "mesh_gene")

    mathur_num = (float(shared_gene_list_len) / (float(gene_list1_len) + float(gene_list2_len) - float(shared_gene_list_len))) / \
                 ((float(gene_list1_len) / all_gene_num) * (float(gene_list2_len) / all_gene_num))

    return mathur_num


# print(cal_2modulemathur("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15"))


def cal_2modulemathurscore(database_name, table_name, primary_key, group_name1, group_name2):
    """
        Calculate similarity between two disease groups based on Mathur's score method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :return: mathur_score
            The Mathur's score method similarity between two disease group
    """

    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from group_mathur where GROUP_ID = '{0}'".format(group_name1))
    c.execute(sql)
    mathur_info1 = c.fetchall()
    mathur_info1 = mathur_info1[0]
    max_sim_group1_i = mathur_info1[1]
    max_sim_group1_i = float(max_sim_group1_i)

    sql = ("select * from group_mathur where GROUP_ID = '{0}'".format(group_name2))
    c.execute(sql)
    mathur_info2 = c.fetchall()
    mathur_info2 = mathur_info2[0]
    max_sim_group2_i = mathur_info2[1]
    max_sim_group2_i = float(max_sim_group2_i)

    mathur = cal_2modulemathur(database_name, table_name, primary_key, group_name1, group_name2)

    mathur_score = mathur / ((max_sim_group1_i + max_sim_group2_i) / 2)

    mathur_score = '%.5f' % mathur_score

    conn.close()

    return mathur_score


# print(cal_2modulemathurscore("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15"))


def cal_groupmodulemathurscore(database_name, table_name, primary_key, group_list1, group_list2):
    """
        Calculate the similarity matrix between two lists of disease group based on Lin's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_list1: string
            A list of disease group for calculating similarity
    :param group_list2: string
            A list of disease group for calculating similarity
    :return: sim
            The Lin's method similarity matrix between the two lists of disease group
    """
    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')

    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []
    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2modulemathurscore(database_name, table_name, primary_key, group_name1, group_name2)
            a.append(s)
        lst.append(a)
    # print(lst)
    sim = np.matrix(lst)

    # print(type(sim))

    return sim


# print(cal_groupmodulemathurscore("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90,ICD10CM:A15",
#                                  "ICD10CM:A90,ICD10CM:A15"))


def cal_2funsimmax(database_name, table_name, primary_key, group_name1, group_name2, indi_method):
    """
        Calculate similarity between two disease groups based on funsimmax method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key used to query disease information in database
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: funsimmax
            The funsimmax similarity between two diseases
    """

    disease_list1 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name1)[1]
    disease_list2 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name2)[1]
    # print(disease_list1)
    # print(disease_list2)

    disease_list1 = disease_list1.split(',')
    disease_list2 = disease_list2.split(',')

    row_num = len(disease_list1)
    column_num = len(disease_list2)
    # print(row_num, column_num)

    lst = []
    for disease1 in disease_list1:
        a = []
        for disease2 in disease_list2:
            if indi_method == 'jaccard':
                sim = cal_2indijaccard(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'cosine':
                sim = cal_2indicosine(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'lin':
                sim = cal_2indilin(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'mathur':
                sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            else:
                print("wrong individual similarity method!")
                exit(0)
        lst.append(a)

    sim_matrix = np.matrix(lst)
    # print(sim_matrix)

    row_simlist = np.max(sim_matrix, 1)
    column_simlist = np.max(sim_matrix, 0)

    # print(row_simlist, column_simlist)

    addrow = 0
    addcolumn = 0

    for item in row_simlist:
        item = float(item)
        addrow = addrow + item

    lst_columnsim = column_simlist.tolist()  # 行/列矩阵最大值，存储的形式不一样注意这里的形式转换

    for item in lst_columnsim[0]:
        item = float(item)
        addcolumn = addcolumn + item

    row_score = addrow / row_num
    column_score = addcolumn / column_num

    funsimmax = max(row_score, column_score)
    funsimmax = '%.5f' % funsimmax

    return funsimmax


# print(cal_2funsimmax("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "jaccard"))
# print(cal_2funsimmax("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "cosine"))
# print(cal_2funsimmax("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "lin"))

def cal_groupfunsimmax(database_name, table_name, primary_key, group_list1, group_list2, indi_method):
    """
        Calculate the similarity matrix between two lists of disease group based on funsimmax method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_list1: string
            A list of disease group for calculating similarity
    :param group_list2: string
            A list of disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: sim
            The funsimmax method similarity matrix between the two lists of disease group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2funsimmax(database_name, table_name, primary_key, group_name1, group_name2, indi_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_groupfunsimmax("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90,ICD10CM:A15",
#                           "ICD10CM:A90,ICD10CM:A15", "jaccard"))


def cal_2funsimavg(database_name, table_name, primary_key, group_name1, group_name2, indi_method):
    """
        Calculate similarity between two disease groups based on funsimavg method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key used to query disease information in database
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: funsimavg
            The funsimavg similarity between two diseases
    """

    disease_list1 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name1)[1]
    disease_list2 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name2)[1]
    # print(disease_list1)
    # print(disease_list2)

    disease_list1 = disease_list1.split(',')
    disease_list2 = disease_list2.split(',')

    row_num = len(disease_list1)
    column_num = len(disease_list2)
    # print(row_num, column_num)

    lst = []
    for disease1 in disease_list1:
        a = []
        for disease2 in disease_list2:
            if indi_method == 'jaccard':
                sim = cal_2indijaccard(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'cosine':
                sim = cal_2indicosine(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'lin':
                sim = cal_2indilin(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'mathur':
                sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            else:
                print("wrong individual similarity method!")
                exit(0)
        lst.append(a)

    sim_matrix = np.matrix(lst)
    # print(sim_matrix)

    row_simlist = np.max(sim_matrix, 1)
    column_simlist = np.max(sim_matrix, 0)

    # print(row_simlist, column_simlist)

    addrow = 0
    addcolumn = 0

    for item in row_simlist:
        item = float(item)
        addrow = addrow + item

    lst_columnsim = column_simlist.tolist()  # 行/列矩阵最大值，存储的形式不一样注意这里的形式转换

    for item in lst_columnsim[0]:
        item = float(item)
        addcolumn = addcolumn + item

    row_score = addrow / row_num
    column_score = addcolumn / column_num

    funsimavg = 0.5 * (row_score + column_score)
    funsimavg = '%.5f' % funsimavg

    return funsimavg


# print(cal_2funsimavg("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "jaccard"))
# print(cal_2funsimavg("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "cosine"))
# print(cal_2funsimavg("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "lin"))

def cal_groupfunsimavg(database_name, table_name, primary_key, group_list1, group_list2, indi_method):
    """
        Calculate the similarity matrix between two lists of disease group based on funsimavg method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_list1: string
            A list of disease group for calculating similarity
    :param group_list2: string
            A list of disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: sim
            The funsimavg method similarity matrix between the two lists of disease group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2funsimavg(database_name, table_name, primary_key, group_name1, group_name2, indi_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_groupfunsimavg("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90,ICD10CM:A15",
#                           "ICD10CM:A90,ICD10CM:A15", "jaccard"))


def cal_2bma(database_name, table_name, primary_key, group_name1, group_name2, indi_method):
    """
        Calculate similarity between two disease groups based on BMA method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key used to query disease information in database
    :param group_name1: string
            A disease group for calculating similarity
    :param group_name2: string
            A disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: bma
            The BMA-based similarity between two diseases
    """

    disease_list1 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name1)[1]
    disease_list2 = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name2)[1]
    # print(disease_list1)
    # print(disease_list2)

    disease_list1 = disease_list1.split(',')
    disease_list2 = disease_list2.split(',')

    row_num = len(disease_list1)
    column_num = len(disease_list2)
    # print(row_num, column_num)

    lst = []
    for disease1 in disease_list1:
        a = []
        for disease2 in disease_list2:
            if indi_method == 'jaccard':
                sim = cal_2indijaccard(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'cosine':
                sim = cal_2indicosine(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'lin':
                sim = cal_2indilin(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            elif indi_method == 'mathur':
                sim = cal_2indimathurscore(database_name, 'mesh_gene', 'DISEASE_ID', disease1, disease2)
                sim = float(sim)
                a.append(sim)

            else:
                print("wrong individual similarity method!")
                exit(0)
        lst.append(a)

    sim_matrix = np.matrix(lst)
    # print(sim_matrix)

    row_simlist = np.max(sim_matrix, 1)
    column_simlist = np.max(sim_matrix, 0)

    # print(row_simlist, column_simlist)

    addrow = 0
    addcolumn = 0

    for item in row_simlist:
        item = float(item)
        addrow = addrow + item

    lst_columnsim = column_simlist.tolist()  # 行/列矩阵最大值，存储的形式不一样注意这里的形式转换

    for item in lst_columnsim[0]:
        item = float(item)
        addcolumn = addcolumn + item

    bma = (addrow + addcolumn) / (row_num + column_num)
    bma = '%.5f' % bma

    return bma


# print(cal_2funsimmax("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "jaccard"))
# print(cal_2funsimmax("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "cosine"))
# print(cal_2funsimmax("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90", "ICD10CM:A15", "lin"))


def cal_groupbma(database_name, table_name, primary_key, group_list1, group_list2, indi_method):
    """
        Calculate the similarity matrix between two lists of disease group based on BMA method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_list1: string
            A list of disease group for calculating similarity
    :param group_list2: string
            A list of disease group for calculating similarity
    :param indi_method: string
            Methods for calculating similarity between two diseases presented in "cal_individualsim.py"
            jaccard/cosine/lin/mathur
    :return: sim
            The BMA-based method similarity matrix between the two lists of disease group
    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')
    # m = len(group_list1)
    # n = len(group_list2)  # 创建的是m*n大小的矩阵
    lst = []

    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2bma(database_name, table_name, primary_key, group_name1, group_name2, indi_method)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_groupbma("disease_gene", "group_info", "GROUP_ID", "ICD10CM:A90,ICD10CM:A15",
#                    "ICD10CM:A90,ICD10CM:A15", "jaccard"))



