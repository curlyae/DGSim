from data.connect_database import *
from function.get_datainfo import *
import numpy as np


def cal_2indijaccard(database_name, table_name, primary_key_name, individual_name1, individual_name2):
    """
        Calculate similarity between two diseases based on Jaccard Index
    :param database_name: string
        The database to connect to
    :param table_name: string
        The database table to be queried
    :param primary_key_name: string
        The primary key used to query disease information in database
    :param individual_name1: string
         A disease for calculating similarity
    :param individual_name2: string
         A disease for calculating similarity
    :return: jaccard_num
         The jaccard similarity between two disease
    """

    conn = connect_database(database_name)

    c = conn.cursor()
    sql1 = ("select * from {0} where {1} = '{2}'".format(table_name, primary_key_name, individual_name1))
    sql2 = ("select * from {0} where {1} = '{2}'".format(table_name, primary_key_name, individual_name2))

    c.execute(sql1)
    infolist1 = c.fetchall()
    c.execute(sql2)
    infolist2 = c.fetchall()

    for member in infolist1:
        tuple_list1 = member[1]  # get the causing gene list from the result of querying
        tuple_list1 = tuple_list1.split(',')
        set_list1 = set(tuple_list1)  # transfer the causing gene list into set, set A
        set_list1_len = len(set_list1)  # the size of the causing gene set A
    for member2 in infolist2:
        tuple_list2 = member2[1]
        tuple_list2 = tuple_list2.split(',')
        set_list2 = set(tuple_list2)  # set B
        set_list2_len = len(set_list2)  # the size of causing gene set B

    set1_and_set2_list = set_list1 & set_list2  # the intersection of set A and set B
    # print(set1_and_set2_list)
    set1_and_set2_list_len = len(set1_and_set2_list)  # the size of the intersection of set A and set B

    jaccard_num = set1_and_set2_list_len / (set_list1_len + set_list2_len - set1_and_set2_list_len)

    jaccard_num = '%.5f' % jaccard_num

    conn.close()

    return jaccard_num

# print(cal_2indijaccard("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003715", "MESH:D003715"))
# print(cal_2indijaccard("disease_gene", "ICD10cm_gene", "DISEASE_ID", "ICD10CM:00.0", "ICD10CM:G91"))


def cal_2indicosine(database_name, table_name, primary_key_name, individual_name1, individual_name2):
    """
        Calculate similarity between two diseases based on Cosine method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param primary_key_name: string
            The primary key used to query disease information in database
    :param individual_name1: string
             A disease for calculating similarity
    :param individual_name2: string
             A disease for calculating similarity
    :return: cosθ
            The Cosine similarity between two disease
    """
    conn = connect_database(database_name)
    c = conn.cursor()
    sql1 = ("select * from {0} where {1} = '{2}'".format(table_name, primary_key_name, individual_name1))
    sql2 = ("select * from {0} where {1} = '{2}'".format(table_name, primary_key_name, individual_name2))

    c.execute(sql1)
    infolist1 = c.fetchall()
    c.execute(sql2)
    infolist2 = c.fetchall()

    ########################################################
    # 原来的部分，只看其出现没出现，设置0/1，不关心其出现的次数
    ########################################################
    # for member1 in infolist1:
    #     tuple_list1 = member1[1]
    #     tuple_list1 = tuple_list1.split(',')
    #     set_list1 = set(tuple_list1)  # 集合A
    #     # print(len(set_list1))
    # for member2 in infolist2:
    #     tuple_list2 = member2[1]
    #     tuple_list2 = tuple_list2.split(',')
    #     set_list2 = set(tuple_list2)  # 集合B
    #     # print(len(set_list2))
    # set1_union_set2_list = set_list1 | set_list2

    for member1 in infolist1:
        vector_list1 = member1[1]
        vector_list1 = vector_list1.split(',')
        set_list1 = set(vector_list1)
    for member2 in infolist2:
        vector_list2 = member2[1]
        vector_list2 = vector_list2.split(',')
        set_list2 = set(vector_list2)

    set1_union_set2_list = set_list1 | set_list2

    vector1 = []
    vector2 = []

    for item in set1_union_set2_list:
        num = 0
        for key in vector_list1:
            if key == item:
                num = num + 1
        vector1.append(num)

    for item in set1_union_set2_list:
        num = 0
        for key in vector_list2:
            if key == item:
                num = num + 1
        vector2.append(num)

    # print(set1_union_set2_list)
    # print(len(set1_union_set2_list))

    # samelist = []
    # for key1 in set_list1:
    #     for key2 in set_list2:
    #         if key1 == key2:
    #             samelist.append(key1)
    # print(samelist)

    ########################################################
    # 原来的部分，只看其出现没出现，设置0/1，不关心其出现的次数
    ########################################################
    # vector1 = []
    # vector2 = []
    #
    # for item in set1_union_set2_list:
    #     if item in set_list1:
    #         vector1.append(1)
    #     elif item not in set_list1:
    #         vector1.append(0)
    #     if item in set_list2:
    #         vector2.append(1)
    #     elif item not in set_list2:
    #         vector2.append(0)

    # print(vector1)
    # print(vector2)
    vectorlen = len(set1_union_set2_list)
    a = b = c = 0
    for i in range(vectorlen):
        a = a + vector1[i] * vector2[i]
        b = b + vector1[i] * vector1[i]
        c = c + vector2[i] * vector2[i]
    cosθ = a / ((b ** 0.5) * (c ** 0.5))
    cosθ = '%.5f' % cosθ

    conn.close()

    return cosθ


# print(cal_2indicosine("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003920", "MESH:D010859"))
# print(cal_2indicosine("disease_gene", "ICD10cm_gene", "DISEASE_ID", "ICD10CM:00.0", "ICD10CM:G91"))


def cal_2indilin(database_name, table_name, primary_key_name, individual_name1, individual_name2):
    """
        Calculate similarity between two diseases based on Lin's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param primary_key_name: string
            The primary key used to query disease information in database
    :param individual_name1: string
             A disease for calculating similarity
    :param individual_name2: string
             A disease for calculating similarity
    :return: lin_num
            The Lin's method similarity between two disease
    """

    conn = connect_database(database_name)
    c = conn.cursor()
    sql1 = ("select * from {0} where {1} = '{2}'".format(table_name, primary_key_name, individual_name1))
    sql2 = ("select * from {0} where {1} = '{2}'".format(table_name, primary_key_name, individual_name2))

    c.execute(sql1)
    infolist1 = c.fetchall()
    c.execute(sql2)
    infolist2 = c.fetchall()

    for member in infolist1:
        tuple_list1 = member[1]  # get the causing gene list from the result of querying
        tuple_list1 = tuple_list1.split(',')
        set_list1 = set(tuple_list1)  # transfer the causing gene list into set, set A
        set_list1_len = len(set_list1)  # the size of the causing gene set A
    for member2 in infolist2:
        tuple_list2 = member2[1]
        tuple_list2 = tuple_list2.split(',')
        set_list2 = set(tuple_list2)  # set B
        set_list2_len = len(set_list2)  # the size of causing gene set B
    set1_and_set2_list = set_list1 & set_list2  # the intersection of set A and set B
    # print(set1_and_set2_list)
    set1_and_set2_list_len = len(set1_and_set2_list)  # the size of the intersection of set A and set B

    # print(set_list1_len, set_list2_len, set1_and_set2_list_len)
    lin_num = (2 * set1_and_set2_list_len)/(set_list1_len + set_list2_len)

    lin_num = '%.5f' % lin_num

    conn.close()

    return lin_num


# print(cal_2indilin("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003920", "MESH:D010859"))
# print(cal_2indilin("disease_gene", "ICD10cm_gene", "DISEASE_ID", "ICD10CM:00.0", "ICD10CM:G91"))


def cal_2indimathur(database_name, table_name, primary_key_name, individual_name1, individual_name2):
    """
        Calculate similarity between two diseases based on Mathur's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param primary_key_name: string
            The primary key used to query disease information in database
    :param individual_name1: string
             A disease for calculating similarity
    :param individual_name2: string
             A disease for calculating similarity
    :return: mathur_num
            The Mathur's method similarity between two disease
    """
    conn = connect_database(database_name)
    c = conn.cursor()
    sql1 = ("select * from {0} where {1} = '{2}'".format(table_name, primary_key_name, individual_name1))
    sql2 = ("select * from {0} where {1} = '{2}'".format(table_name, primary_key_name, individual_name2))

    c.execute(sql1)
    infolist1 = c.fetchall()
    c.execute(sql2)
    infolist2 = c.fetchall()

    for member in infolist1:
        tuple_list1 = member[1]  # get the causing gene list from the result of querying
        tuple_list1 = tuple_list1.split(',')
        set_list1 = set(tuple_list1)  # transfer the causing gene list into set, set A
        set_list1_len = len(set_list1)  # the size of the causing gene set A

    for member2 in infolist2:
        tuple_list2 = member2[1]
        tuple_list2 = tuple_list2.split(',')
        set_list2 = set(tuple_list2)  # set B
        set_list2_len = len(set_list2)  # the size of causing gene set B

    set1_and_set2_list = set_list1 & set_list2  # the intersection of set A and set B
    # print(set1_and_set2_list)

    set1_and_set2_list_len = len(set1_and_set2_list)  # the size of the intersection of set A and set B

    all_indinum = get_all_gene_num(database_name, table_name)

    mathur_num = (set1_and_set2_list_len/(set_list1_len + set_list2_len - set1_and_set2_list_len)) / ((set_list1_len / all_indinum)*(set_list2_len / all_indinum))

    conn.close()

    return mathur_num


# print(cal_2indimathur("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003924", "MESH:D003924"))
# print(cal_2indimathur("disease_gene", "ICD10cm_gene", "DISEASE_ID", "ICD10CM:A30", "ICD10CM:A31.1"))

def cal_2indimathurscore(database_name, table_name, primary_key_name, individual_name1, individual_name2):
    """
        Calculate similarity between two diseases based on Mathur's score method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param primary_key_name: string
            The primary key used to query disease information in database
    :param individual_name1: string
             A disease for calculating similarity
    :param individual_name2: string
             A disease for calculating similarity
    :return: mathur_score
            The Mathur's score method similarity between two disease
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    if table_name is "mesh_gene":
        sql = ("select * from mesh_mathur where DISEASE_ID = '{0}'".format(individual_name1))
        # print(sql)
        c.execute(sql)
        mathur_info1 = c.fetchall()
        mathur_info1 = mathur_info1[0]
        max_sim_indi1_i = mathur_info1[1]
        max_sim_indi1_i = float(max_sim_indi1_i)
        # print(mathur_info1)
        # print(max_sim_indi1_i)

        sql = ("select * from mesh_mathur where DISEASE_ID = '{0}'".format(individual_name2))
        # print(sql)
        c.execute(sql)
        mathur_info2 = c.fetchall()
        mathur_info2 = mathur_info2[0]
        max_sim_indi2_i = mathur_info2[1]
        max_sim_indi2_i = float(max_sim_indi2_i)
        # print(mathur_info2)
        # print(max_sim_indi2_i)

    elif table_name is "ICD10CM_gene":
        sql = ("select * from ICD10cm_mathur where DISEASE_ID = '{0}'".format(individual_name1))
        # print(sql)
        c.execute(sql)
        mathur_info1 = c.fetchall()
        # print(mathur_info1)
        mathur_info1 = mathur_info1[0]
        max_sim_indi1_i = mathur_info1[1]
        max_sim_indi1_i = float(max_sim_indi1_i)
        # print(mathur_info1)
        # print(max_sim_indi1_i)

        sql = ("select * from ICD10cm_mathur where DISEASE_ID = '{0}'".format(individual_name2))
        c.execute(sql)
        mathur_info2 = c.fetchall()
        mathur_info2 = mathur_info2[0]
        max_sim_indi2_i = mathur_info2[1]
        max_sim_indi2_i = float(max_sim_indi2_i)
        # print(mathur_info2)
        # print(max_sim_indi2_i)

    mathur = cal_2indimathur(database_name, table_name, primary_key_name, individual_name1, individual_name2)

    mathur_score = mathur / ((max_sim_indi1_i + max_sim_indi2_i) / 2)

    mathur_score = '%.5f' % mathur_score

    conn.close()

    return mathur_score


# print(cal_2indimathurscore("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003920", "MESH:D003924"))
# print(cal_2indimathurscore("disease_gene", "ICD10CM_gene", "DISEASE_ID", "ICD10CM:A30", "ICD10CM:A31.1"))
# print(cal_2indimathurscore("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003920", "MESH:D003924"))


def cal_indigroupjaccard(database_name, table_name, primary_key_name, individual_group1, individual_group2):
    """
        Calculate similarity metrix between two list of diseases based on Jaccard Index
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param primary_key_name: string
            The primary key used to query disease information in the database
    :param individual_group1: string
            A disease group for calculating similarity
    :param individual_group2: string
            A disease group for calculating similarity
    :return: sim
            The similarity matrix based on Jaccard Index between the two lists of disease
    """

    individual_group1 = individual_group1.split(',')
    individual_group2 = individual_group2.split(',')

    # m = len(individual_group1)
    # n = len(individual_group2)  # 创建的是m*n大小的矩阵

    lst = []
    for individual_name1 in individual_group1:
        a = []
        for individual_name2 in individual_group2:
            s = cal_2indijaccard(database_name, table_name, primary_key_name, individual_name1, individual_name2)
            a.append(s)
        lst.append(a)

    sim = np.matrix(lst)

    return sim


# print(cal_indigroupjaccard("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003920,MESH:D003924",
#                            "MESH:D008113,MESH:D009369,MESH:D009765"))
#
# print(cal_indigroupjaccard("disease_gene", "ICD10CM_gene", "DISEASE_ID", "ICD10CM:00.0,ICD10CM:A01.0",
#                            "ICD10CM:A01.00,ICD10CM:A15,ICD10CM:A15.0"))
#


def cal_indigroupcosine(database_name, table_name, primary_key_name, individual_group1, individual_group2):
    """
        Calculate similarity metrix between two list of diseases based on Cosine method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param primary_key_name: string
            The primary key used to query disease information in the database
    :param individual_group1: string
            A disease group for calculating similarity
    :param individual_group2: string
            A disease group for calculating similarity
    :return: sim
            The similarity matrix based on Cosine method between the two lists of disease
    """
    individual_group1 = individual_group1.split(',')
    individual_group2 = individual_group2.split(',')

    # m = len(individual_group1)
    # n = len(individual_group2)  # 创建的是m*n大小的矩阵

    lst = []
    for individual_name1 in individual_group1:
        a = []
        for individual_name2 in individual_group2:
            s = cal_2indicosine(database_name, table_name, primary_key_name, individual_name1, individual_name2)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_indigroupcosine("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003920,MESH:D003924",
#                           "MESH:D008113,MESH:D009369,MESH:D009765"))
#
# print(cal_indigroupcosine("disease_gene", "ICD10CM_gene", "DISEASE_ID", "ICD10CM:00.0,ICD10CM:A01.0",
#                           "ICD10CM:A01.00,ICD10CM:A15,ICD10CM:A15.0"))


def cal_indigrouplin(database_name, table_name, primary_key_name, individual_group1, individual_group2):
    """
        Calculate similarity metrix between two list of diseases based on Lin's method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param primary_key_name: string
            The primary key used to query disease information in the database
    :param individual_group1: string
            A disease group for calculating similarity
    :param individual_group2: string
            A disease group for calculating similarity
    :return: sim
            The similarity matrix based on Lin's method between the two lists of disease
    """

    individual_group1 = individual_group1.split(',')
    individual_group2 = individual_group2.split(',')

    # m = len(individual_group1)
    # n = len(individual_group2)  # 创建的是m*n大小的矩阵


    lst = []
    for individual_name1 in individual_group1:
        a = []
        for individual_name2 in individual_group2:
            s = cal_2indilin(database_name, table_name, primary_key_name, individual_name1, individual_name2)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim


# print(cal_indigrouplin("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003920,MESH:D003924",
#                        "MESH:D008113,MESH:D009369,MESH:D009765"))
#
# print(cal_indigrouplin("disease_gene", "ICD10CM_gene", "DISEASE_ID", "ICD10CM:00.0,ICD10CM:A01.0",
#                        "ICD10CM:A01.00,ICD10CM:A15,ICD10CM:A15.0"))


def cal_indigroupmathurscore(database_name, table_name, primary_key_name, individual_group1, individual_group2):
    """
        Calculate similarity metrix between two list of diseases based on Mathur's score method
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param primary_key_name: string
            The primary key used to query disease information in the database
    :param individual_group1: string
            A disease group for calculating similarity
    :param individual_group2: string
            A disease group for calculating similarity
    :return: sim
            The similarity matrix based on Mathur's score method between the two lists of disease
    """

    individual_group1 = individual_group1.split(',')
    individual_group2 = individual_group2.split(',')

    # m = len(individual_group1)
    # n = len(individual_group2)  # 创建的是m*n大小的矩阵

    lst = []
    for individual_name1 in individual_group1:
        a = []
        for individual_name2 in individual_group2:
            s = cal_2indimathurscore(database_name, table_name, primary_key_name, individual_name1, individual_name2)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    return sim

#
# print(cal_indigroupmathurscore("disease_gene", "mesh_gene", "DISEASE_ID", "MESH:D003920,MESH:D003924",
#                                "MESH:D008113,MESH:D009369"))
#
# print(cal_indigroupmathurscore("disease_gene", "ICD10CM_gene", "DISEASE_ID", "ICD10CM:00.0,ICD10CM:A01.0",
#                                "ICD10CM:A01.00,ICD10CM:A15"))
#

