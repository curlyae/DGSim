from data.connect_database import *


def get_icd_disease_info(database_name, table_name, disease_name, primary_key):
    """
        Query the disease information from ICD10cm

    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param disease_name: string
            The ICD10cm disease name being queried
    :param primary_key: string
            The primary key of database table
    :return: query_list
            Information in query_list represent DISEASE_ID, MESH_LIST, DO_LIST, GENE_LIST respectively

    """
    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from {0} where {1} = '{2}' ".format(table_name, primary_key, disease_name))
    c.execute(sql)

    query_info = c.fetchall()
    query_info = query_info[0]
    query_list = list(query_info)

    conn.close()

    return query_list


# print(get_icd_disease_info('disease_gene', 'ICD10CMinfo', 'ICD10CM:J69.0', 'DISEASE_ID'))


def get_mesh_disease_info(database_name, table_name, disease_name, primary_key):
    """
        Query the disease information from MESH

    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param disease_name: string
            The MESH disease name being queried
    :param primary_key: string
            The primary key of database table
    :return: query_list
            Information in query_list represent MESH_ID, GENE_LIST, NUM_OF_GENE respectively

    """
    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from {0} where {1} = '{2}' ".format(table_name, primary_key, disease_name))
    c.execute(sql)

    query_info = c.fetchall()
    query_info = query_info[0]
    query_list = list(query_info)

    conn.close()

    return query_list


# print(get_mesh_disease_info('disease_gene', 'mesh_gene', 'MESH:D003920', 'DISEASE_ID')[0])


def get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, disease_group_name):
    """
        Query the disease information of a ICD10cm disease group
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database_table being queried
    :param primary_key: string
            The primary key of database table
    :param disease_group_name:
            The ICD10cm disease group name being queried
    :return: query_list
            Information in query_list represent GROUP_ID,DISEASE_LIST,NUM_OF_DISEASE respectively.
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from {0} where {1} = '{2}' ".format(table_name, primary_key, disease_group_name))
    c.execute(sql)

    query_info = c.fetchall()
    query_info = query_info[0]
    query_list = list(query_info)

    conn.close()

    return query_list


# print(get_icd_diseasegroup_diseaseinfo('disease_gene', 'group_info', 'GROUP_ID', 'ICD10CM:A81'))


def get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, disease_group_name):
    """
        Query the gene information of a ICD10cm disease group
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The  primary key of database table
    :param disease_group_name: string
            The ICD10cm disease group being queried
    :return: query_list
            Information in query_list represent GROUP_ID,GENE_LIST,NUM_OF_GENE respectively.
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from {0} where {1} = '{2}' ".format(table_name, primary_key, disease_group_name))
    c.execute(sql)

    query_info = c.fetchall()
    query_info = query_info[0]
    disease_query_list = list(query_info)
    # print(disease_query_list)
    disease_list = disease_query_list[1]

    disease_list = disease_list.split(',')

    all_genelist = []
    for disease in disease_list:
        gene_list = get_mesh_disease_info(database_name, 'mesh_gene', '{}'.format(disease), 'DISEASE_ID')[1]
        gene_list = gene_list.split(',')
        for gene in gene_list:
            if gene not in all_genelist:
                all_genelist.append(gene)
    all_gene = ','.join(all_genelist)
    query_list = list()

    query_list.append(disease_query_list[0])
    query_list.append(all_gene)
    query_list.append(len(all_genelist))

    conn.close()

    return query_list


# print(get_icd_diseasegroup_geneinfo('disease_gene', 'group_info', 'GROUP_ID', 'ICD10CM:B20'))


def get_2disease_shared_gene(database_name, table_name, disease1, disease2, primary_key):
    """
        Query the shared gene information between disease1 and disease2

    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param disease1: string
            The ICD10cm disease name being queried
    :param disease2: string
            The ICD10cm disease name being queried
    :param primary_key: string
            The primary key of database table
    :return: query_list
            Information in query_list represent disease1,disease2,shared_gene_list,shared_gene_num
            respectively.
    """

    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("select * from {0} where {1} = '{2}' ".format(table_name, primary_key, disease1))
    c.execute(sql)

    query1_info = c.fetchall()
    query1_info = query1_info[0]
    query1_1ist = list(query1_info)

    sql = ("select * from {0} where {1} = '{2}' ".format(table_name, primary_key, disease2))
    c.execute(sql)

    query2_info = c.fetchall()
    query2_info = query2_info[0]
    query2_1ist = list(query2_info)

    genelist1 = query1_1ist[1]
    genelist1 = genelist1.split(',')
    geneset1 = set(genelist1)

    genelist2 = query2_1ist[1]
    genelist2 = genelist2.split(',')
    geneset2 = set(genelist2)

    shared_geneset = geneset1 & geneset2
    shared_genelist = list(shared_geneset)
    num_of_shared_gene = len(shared_genelist)
    shared_genelist = ','.join(shared_genelist)

    query_list = list()
    query_list.append(disease1)
    query_list.append(disease2)
    query_list.append(shared_genelist)
    query_list.append(num_of_shared_gene)

    conn.close()

    return query_list


# get_2disease_shared_gene('disease_gene', 'ICD10CM_gene', 'ICD10CM:A30', 'ICD10CM:A31.1', 'DISEASE_ID')

# print(get_2disease_shared_gene('disease_gene', 'ICD10CM_gene', 'ICD10CM:A30', 'ICD10CM:A31.1', 'DISEASE_ID')[3])


def get_2diseasegroup_shared_gene(database_name, table_name, ICD10cm_disease_group1, ICD10cm_disease_group2, primary_key):
    """
        Query the shared gene information between ICD10cm_disease_group1 and ICD10cm_disease_group2

    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param ICD10cm_disease_group1: string
            The ICD10cm disease group name being queried
    :param ICD10cm_disease_group2: string
            The ICD10cm disease group name being queried
    :param primary_key: string
             The primary key of database table
    :return: query_info
            Information in query_list represent ICD10cm_disease_group1 ,ICD10cm_disease_group2 ,shared_gene_list,
            shared_gene_num respectively.
    """
    gene_list1 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, ICD10cm_disease_group1)[1]
    gene_list2 = get_icd_diseasegroup_geneinfo(database_name, table_name, primary_key, ICD10cm_disease_group2)[1]
    gene_list1 = gene_list1.split(',')
    gene_list2 = gene_list2.split(',')
    geneset1 = set(gene_list1)
    geneset2 = set(gene_list2)

    shared_gene_set = geneset1 & geneset2
    shared_gene_list = list(shared_gene_set)
    num_of_shared_gene = len(shared_gene_list)
    shared_gene_list = ','.join(shared_gene_list)

    query_info = list()
    query_info.append(ICD10cm_disease_group1)
    query_info.append(ICD10cm_disease_group2)
    query_info.append(shared_gene_list)
    query_info.append(num_of_shared_gene)

    return query_info


# print(get_2diseasegroup_shared_gene('disease_gene', 'group_info', 'ICD10CM:A15', 'ICD10CM:A90', 'GROUP_ID'))


def get_all_gene_num(database_name, table_name):
    """
        Query the gene number of all GDAs (mesh-gene)

    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :return: all_gene_num
            The number of all the genes
    """

    conn = connect_database(database_name)
    c = conn.cursor()
    all_gene_list = list()

    sql = ("select * from {0}".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    for query_line in query_list:
        tuple_list = query_line[1]
        tuple_list = tuple_list.split(',')
        for gene in tuple_list:
            if gene not in all_gene_list:
                all_gene_list.append(gene)

    all_gene_num = len(all_gene_list)

    return all_gene_num


# print(get_all_gene_num("disease_gene", "mesh_gene"))

# print(get_all_gene_num("disease_gene", "ICD10cm_gene"))


def get_all_mesh_disease_num(database_name, table_name):
    """
        Query the MESH disease number of all GDAs (mesh-gene)
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :return: all_mesh_num
            The number of all the genes
    """

    conn = connect_database(database_name)
    c = conn.cursor()
    all_mesh_list = list()

    sql = ("select * from {0}".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    for query_line in query_list:
        mesh = query_line[0]
        if mesh not in all_mesh_list:
            all_mesh_list.append(mesh)
    all_mesh_num = len(all_mesh_list)

    return all_mesh_num


# print(get_all_mesh_disease_num("disease_gene", "mesh_gene"))


def get_all_ICD10cm_disease_num(database_name, table_name):
    """
          Query the MESH disease number of all GDAs (mesh-gene)
      :param database_name: string
              The database to connect to
      :param table_name: string
              The database table being queried
      :return: all_ICD10cm_disease_num
              The number of all the ICD10cm diseases
      """

    conn = connect_database(database_name)
    c = conn.cursor()
    all_ICD10cm_disease_list = list()

    sql = ("select * from {0}".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    for query_line in query_list:
        icd10cm_disease = query_line[0]
        if icd10cm_disease not in all_ICD10cm_disease_list:
            all_ICD10cm_disease_list.append(icd10cm_disease)

    all_ICD10cm_disease_num = len(all_ICD10cm_disease_list)

    return all_ICD10cm_disease_num


# print(get_all_ICD10cm_disease_num("disease_gene", "ICD10CMinfo"))


def get_all_ICD10cm_disease_group_num(database_name, table_name):
    """
          Query the MESH disease number of all GDAs (mesh-gene)
      :param database_name: string
              The database to connect to
      :param table_name: string
              The database table being queried
      :return: all_ICD10cm_disease_group_num
              The number of all the ICD10cm disease groups
      """

    conn = connect_database(database_name)
    c = conn.cursor()
    all_ICD10cm_disease_group_list = list()

    sql = ("select * from {0}".format(table_name))
    c.execute(sql)

    query_list = c.fetchall()

    for query_line in query_list:
        icd10cm_disease_group = query_line[0]
        if icd10cm_disease_group not in all_ICD10cm_disease_group_list:
            all_ICD10cm_disease_group_list.append(icd10cm_disease_group)

    all_ICD10cm_disease_group_num = len(all_ICD10cm_disease_group_list)

    return all_ICD10cm_disease_group_num


# print(get_all_ICD10cm_disease_group_num("disease_gene", "group_info"))
