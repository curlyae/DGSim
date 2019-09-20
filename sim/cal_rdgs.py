from function.get_datainfo import *
from data.connect_database import *

import numpy as np


def cal_2rdgs(database_name, table_name, primary_key, group_name1, group_name2):
    """
        Calculate the similarity between two disease groups based on R-DGS
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
    :return: sim
            The similarity between two disease groups
    """

    ################################################################
    #  conect to the database and return the query information
    ################################################################
    conn = connect_database(database_name)
    c = conn.cursor()

    sql1 = ("select * from {0} where {1} = '{2}' ".format(table_name, primary_key, group_name1))
    sql2 = ("select * from {0} where {1} = '{2}' ".format(table_name, primary_key, group_name2))

    c.execute(sql1)
    infolist1 = c.fetchall()

    c.execute(sql2)
    infolist2 = c.fetchall()

    # print(infolist1)
    # print(infolist2)

    #######################################################################
    # find the gene number of each disease group(group1_item_num，group2_item_num)
    ########################################################################
    group_1_item_num = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[2]
    group_2_item_num = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[2]
    # print(group_1_item_num)
    # print(group_2_item_num)
    # print(get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name1)[1])
    # print(get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, group_name2)[1])
    ###############################################################
    # find the gene number of all the GDAs
    ###############################################################
    all_gene_num = get_all_gene_num(database_name, "mesh_gene")
    # print(all_gene_num)

    ###############################################################
    # bulid the random model of GROUP_NAME1, GROUP_NAME2, calculate C_random
    ###############################################################

    c_random = (group_1_item_num * group_2_item_num) / all_gene_num

    # print(c_random)

    ###############################################################
    # calculate the gene number of (GROUP_NAME1 intersection GROUP_NAME2), calculate  C_real
    ###############################################################

    c_real = get_2diseasegroup_shared_gene(database_name, table_name, group_name1, group_name2, primary_key)[3]

    # print(c_real)

    ###############################################################
    # calculate sij = c_real/c_random
    ###############################################################

    s = float(c_real) / float(c_random)

    ###############################################################
    # normalization Si,j by min-max normalization method
    ###############################################################

    min_score = 0

    max_score = float(all_gene_num) / min(float(group_1_item_num), float(group_2_item_num))

    # print(max_score)

    sim = (s - min_score) / (max_score - min_score)

    sim = '%.5f' % sim

    conn.close()

    return sim


# print(cal_2rdgs("disease_gene", "group_info", "GROUP_ID", "ICD10CM:E71", "ICD10CM:E74"))


def cal_grouprdgs(database_name, table_name, primary_key, group_list1, group_list2):
    """
        Calculate similarity matrix between two disease group lists based on R-DGS
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
            The similarity matrix between the two lists of disease group

    """

    group_list1 = group_list1.split(',')
    group_list2 = group_list2.split(',')

    # for i in range(1, m):
    #     locals()['list' + str(i)] = []
    #     x = ['list'+str[i]]
    #     print(x)

    lst = []
    for group_name1 in group_list1:
        a = []
        for group_name2 in group_list2:
            s = cal_2rdgs(database_name, table_name, primary_key, group_name1, group_name2)
            a.append(s)
        lst.append(a)
    sim = np.matrix(lst)

    # print(type(sim))

    return sim

    # for i in range(1, m):
    #     print('{}={}'.format('list'+str(i), ['list'+str(i)]))

    # for groupname1 in grouplist1:
    #     i = 1
    #     for groupname2 in grouplist2:
    #         s = cal_2rdgs(database_name, allinfo_tablename, groupname1, groupname2)
    #         ['list'+str(i)].append(s)
    #     i = i + 1
    #
    # lst = []
    # for i in range(1, m):
    #     lst = lst.append(['list'+str(i)])
    # sim = np.matrix(lst)
    # print(sim)
    # print(grouplist1)
    # print(grouplist2)


# print(cal_grouprdgs("disease_gene", "group_info", "GROUP_ID",
#                     "ICD10CM:A90,ICD10CM:A15", "ICD10CM:A90,ICD10CM:A15"))