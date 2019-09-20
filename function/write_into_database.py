"""
.. note::
    This module provides methods to transfer data from JSON/TXT file into database

"""

import sqlite3
import json
from data.connect_database import *
from function.get_datainfo import *


def icd10cm_info_json_into_database(database_name, table_name, json_file_path):
    """
        Transfer icd10cm data from JSON file into database
        JSON file organizes data as directory format:

        e.g:
        {
            ...
            "ICD10CM:E88.9": {
                "mesh": [
                    "MESH:D008659"
                    ],
                "do": [
                    "DOID:0014667"
                    ],
                "gene_list": [
                    "3630",
                    "2110",
                    "5468",
                    "1828",
                    "1401",
                    "196",
                    "2101",
                    "3356",
                    "51733"
                ]
            },
            ...
        }

        Each key in directory is a ICD10CM disease id,
        and it contains mesh_list , do_list and gene_list.
        Each ICD10CM disease id mappings several mesh, do and gene.

    :param database_name: string
             The database to connect to

    :param table_name:
             The database table name that store GDAs data

    :param json_file_path:
             The path of JSON file

    :return:
    """

    conn = connect_database(database_name)
    c = conn.cursor()
    sql = "create table {0} (DISEASE_ID VARCHAR(50) PRIMARY KEY , MESH_LIST VARCHAR(255), " \
          "DO_LIST VARCHAR(255), GENE_LIST VARCHAR(255))".format(table_name)
    c.execute(sql)

    with open(json_file_path) as f:
        file = json.load(f)
        for disease in file:
            mesh_info = file[disease]['mesh']
            mesh_str = ','.join(mesh_info)

            do_info = file[disease]['do']
            do_str = ','.join(do_info)

            gene_info = file[disease]['gene_list']
            gene_str = ','.join(gene_info)  # 用","连接元素，构建成新的字符串

            sql = "insert into {0}(DISEASE_ID, MESH_LIST, DO_LIST, GENE_LIST) values ('%s','%s','%s','%s')".format(
                table_name) \
                  % (disease, mesh_str, do_str, gene_str)
            c.execute(sql)
            conn.commit()
    conn.close()


# icd10cm_info_json_into_database('disease_gene', 'ICD10CMinfo', '../data/手工校验过的ICD数据一层分组.json')


def icd10cm_gene_info_json_into_database(database_name, table_name, json_file_path):
    """
           Transfer icd10cm and gene data from JSON file into database
           JSON file organizes data as directory format:

           e.g:
           {
               ...
               "ICD10CM:E88.9": {
                   "mesh": [
                       "MESH:D008659"
                       ],
                   "do": [
                       "DOID:0014667"
                       ],
                   "gene_list": [
                       "3630",
                       "2110",
                       "5468",
                       "1828",
                       "1401",
                       "196",
                       "2101",
                       "3356",
                       "51733"
                   ]
               },
               ...
           }

           Each key in directory is a ICD10CM disease id,
           and it contains gene_list and numbers_of_gene
           Each ICD10CM disease id mappings several gene.

       :param database_name: string
                The database to connect to

       :param table_name:
                The database table name that store GDAs data

       :param json_file_path:
                The path of JSON file

       :return:
       """

    conn = connect_database(database_name)
    c = conn.cursor()
    sql = "create table {0} (DISEASE_ID VARCHAR(50) PRIMARY KEY , " \
          "GENE_LIST VARCHAR(255), NUM_OF_GENE INT(10))".format(table_name)
    c.execute(sql)

    with open(json_file_path) as f:
        file = json.load(f)
        for disease in file:
            gene_info = file[disease]['gene_list']
            gene_str = ','.join(gene_info)  # 用","连接元素，构建成新的字符串

            sql = "insert into {0}(DISEASE_ID, GENE_LIST, NUM_OF_GENE) values ('%s','%s',%d)".format(table_name) \
                  % (disease, gene_str, len(file[disease]['gene_list']))
            c.execute(sql)
            conn.commit()
    conn.close()


# icd10cm_gene_info_json_into_database('disease_gene', 'ICD10CM_gene', '../data/手工校验过的ICD数据一层分组.json')


def mesh_gene_info_txt_into_database(database_name, table_name, txt_file_path):
    """
       Transfer  MESH_GENE GDAs data from .txt file to database
       Every line in GDAs represents a gene-disease association
       e.g:
            50518 MESH:D003920
            50518 MESH:D003924
       number string is the ID of gene
       MESH string is the ID of disease,obtained from MeSH(Medical Subject Headings)
       The degree of a disease is the number of genes associated with that disease,
       while the degree of a gene is the number of diseases annotated with that gene

    :param database_name: string
             The database to connect to

    :param table_name: string
             The database table name that store GDAs data

    :param txt_file_path: string
             The path of GDAs file

    :return:
    """

    f = open(txt_file_path, 'r+')
    linelist = f.readlines()

    gdas_dt = {}

    for line in linelist:
        line = line.strip('\n')
        line = line.split(' ')
        if line[0].isdigit() is True:
            gdas_dt.setdefault('{0}'.format(line[1]), []).append(line[0])
        if line[1].isdigit() is True:
            gdas_dt.setdefault('{0}'.format(line[0]), []).append(line[1])

    # 将字典写入json文件中
    # json_str = json.dumps(gdas_dt, indent=4)
    # with open('../data/{0}_dt.json'.format(table_name), 'w') as f:
    #     f.write(json_str)

    conn = connect_database(database_name)
    c = conn.cursor()
    sql = "create table {0} (DISEASE_ID VARCHAR(50) PRIMARY KEY, GENE_LIST VARCHAR(255), NUM_OF_GENE INT(10))".format(
        table_name)

    c.execute(sql)

    for disease in gdas_dt:
        infolist = gdas_dt[disease]
        str = ','.join(infolist)  # 用","连接元素，构建成新的字符串

        sql = "insert into {0}(DISEASE_ID,NUM_OF_GENE,GENE_LIST) values('%s',%d,'%s')".format(table_name) \
              % (disease, len(gdas_dt[disease]), str)
        c.execute(sql)
        conn.commit()
    conn.close()


# mesh_gene_info_txt_into_database('disease_gene', 'mesh_gene', '../data/mesh_gene.txt')

def group_info_txt_into_database(database_name, table_name, txt_file_path):
    """
        Transfer ICD10CM group information from TXT into database
        Every line in txt contains a group information.

        e.g:
        ICD10CM:A48    ['MESH:D007877', 'MESH:D012772']
        ICD10CM:A49    ['MESH:D001424']
        ...

        The first string represents the name of this group.
        The second string represents diseases contains in this group

    :param database_name: string
             The database to connect to
    :param table_name: string
             The database table name that store group data
    :param txt_file_path: string
             The path of group information file
    :return:
    """
    conn = connect_database(database_name)
    c = conn.cursor()
    sql = "create table {0} (GROUP_ID VARCHAR(50) PRIMARY KEY, DISEASE_LIST VARCHAR(255)," \
          "NUM_OF_DISEASE INT(10))".format(table_name)
    c.execute(sql)

    f = open(txt_file_path, 'r+')

    linelist = f.readlines()
    for line in linelist:
        list = []
        line = line.strip('\n')
        line = line.split('    ')
        group_name = line[0]
        disease_list = line[1]
        disease_list = disease_list.strip('[]')
        disease_list = disease_list.split(', ')
        for disease in disease_list:
            disease = eval(disease)  # 去掉字符串两端的单引号
            list.append(disease)

        num_of_disease = len(list)
        disease_str = ','.join(list)

        sql = "insert into {0} (GROUP_ID,DISEASE_LIST,NUM_OF_DISEASE) VALUES ('%s','%s',%d)".format(table_name) \
              % (group_name, disease_str, num_of_disease)
        c.execute(sql)
        conn.commit()
    conn.close()


# group_info_txt_into_database('disease_gene', 'group_info', '../data/手工矫正的ICD数据.txt')


def write_indi_mathur_max_into_database(database_name, table_name, mathur_table_name):
    """
        This function is used to write mathur number of individual disease into database table
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table to be queried
    :param mathur_table_name: string
            The database table used to store mathur data
    :return:
    """

    conn = connect_database(database_name)
    c = conn.cursor()

    sql = "create table {0} (DISEASE_ID VARCHAR(50) PRIMARY KEY , MATHUR_NUM VARCHAR(10))".format(mathur_table_name)

    c.execute(sql)

    sql = ("select * from {}".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    all_gene_num = get_all_gene_num(database_name, table_name)

    for disease_info1 in query_list:
        max_mathur = 0  # 代表与disease1相似度最大的疾病，相似度的值
        for disease_info2 in query_list:
            disease_a_name = disease_info1[0]
            disease_x_name = disease_info2[0]
            disease_a_genelist = disease_info1[1]
            disease_x_genelist = disease_info2[1]
            disease_a_genelistlen = disease_info1[2]
            disease_x_genelistlen = disease_info2[2]
            disease_a_genelist = disease_a_genelist.split(',')
            set_list1 = set(disease_a_genelist)
            disease_x_genelist = disease_x_genelist.split(',')
            set_list2 = set(disease_x_genelist)

            set1_and_set2_list = set_list1 & set_list2  # the intersection of set A and set B
            # print(set1_and_set2_list)

            set1_and_set2_list_len = len(set1_and_set2_list)  # the size of the intersection of set A and set B

            mathur_num = (set1_and_set2_list_len / (disease_a_genelistlen + disease_x_genelistlen -
                           set1_and_set2_list_len)) /\
                         ((disease_a_genelistlen / all_gene_num) *
                          (disease_x_genelistlen / all_gene_num))
            print(mathur_num)
            if mathur_num > max_mathur:
                max_mathur = mathur_num
        print('\t')

        sql = "insert into {0} (DISEASE_ID, MATHUR_NUM) values ('%s','%s')".format(mathur_table_name) % (disease_a_name, max_mathur)

        c.execute(sql)
        conn.commit()

    conn.close()


# write_indi_mathur_max_into_database("disease_gene", "mesh_gene", "mesh_mathur")


def write_group_mathur_max_into_database(database_name, table_name, group_mathur_table_name):
    """
        This function is used to write mathur number of disease group into database table
    :param database_name: string
            The database to connect to
    :param table_name:
    :param group_mathur_table_name:
    :return:
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    sql = "create table {0} (GROUP_ID VARCHAR (50) PRIMARY key , MATHUR_NUM VARCHAR (10))".format(group_mathur_table_name)

    c.execute(sql)

    sql = ("select * from {}".format(table_name))

    c.execute(sql)

    query_list = c.fetchall()

    all_gene_num = get_all_gene_num(database_name, "mesh_gene")

    for group_info1 in query_list:
        max_mathur = 0
        for group_info2 in query_list:
            # if group_info1[0] is not group_info2[0]:
            group_a_name = group_info1[0]
            group_x_name = group_info2[0]
            group_a_genelist = get_icd_diseasegroup_geneinfo(database_name, table_name, "GROUP_ID", group_a_name)[1]
            group_x_genelist = get_icd_diseasegroup_geneinfo(database_name, table_name, "GROUP_ID", group_x_name)[1]
            group_a_genelistlen = get_icd_diseasegroup_geneinfo(database_name, table_name, "GROUP_ID", group_a_name)[2]
            group_x_genelistlen = get_icd_diseasegroup_geneinfo(database_name, table_name, "GROUP_ID", group_x_name)[2]

            group_a_genelist = group_a_genelist.split(',')
            set_list1 = set(group_a_genelist)
            group_x_genelist = group_x_genelist.split(',')
            set_list2 = set(group_x_genelist)

            set1_and_set2_list = set_list1 & set_list2  # the intersection of set A and set B

            set1_and_set2_list_len = len(set1_and_set2_list) # the size of the intersection of set A and set B

            mathur_num = (set1_and_set2_list_len / (group_a_genelistlen + group_x_genelistlen -
                           set1_and_set2_list_len)) / \
                         ((group_a_genelistlen / all_gene_num) *
                          (group_x_genelistlen / all_gene_num))
            print(mathur_num)
            if mathur_num > max_mathur:
                max_mathur = mathur_num
        print('\t')

        sql = "insert into {0} (GROUP_ID, MATHUR_NUM) values ('%s', '%s')".format(group_mathur_table_name) % (group_a_name, max_mathur)

        c.execute(sql)
        conn.commit()

    conn.close()


write_group_mathur_max_into_database("disease_gene", "group_info", "group_mathur")


