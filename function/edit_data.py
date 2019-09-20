from data.connect_database import *

"""
.. note::
    This module provides methods to maintain database

"""


def update_data(database_name, table_name):
    """
        This function is used to update information in database

    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being updated
    :return:
    """
    conn = connect_database(database_name)
    c =conn.cursor()

    if table_name is 'mesh_gene':
        update_info = input("please enter update information(DISEASE_ID,GENE_LIST,NUM_OF_GENE),split by ' ':")
        update_info = update_info.split(' ')
        disease_id = update_info[0]
        gene_list = update_info[1]
        num_of_gene = update_info[2]

        sql = ("update {0} set GENE_LIST ='{1}',NUM_OF_GENE = '{2}' where DISEASE_ID = {3}".format(table_name, gene_list, num_of_gene, disease_id))

        c.execute(sql)
        conn.commit()

    elif table_name is('ICD10CMinfo'):
        update_info = input("please enter update information(DISEASE_ID,MESH_LIST,DO_LIST,GENE_LIST),split by ' ':")
        update_info = update_info.split(' ')
        disease_id = update_info[0]
        mesh_list = update_info[1]
        do_list = update_info[2]
        gene_list = update_info[3]

        sql = ("update {0} set MESH_LIST ='{1}',DO_LIST = '{2}',GENE_LIST = '{3}' "
               "where DISEASE_ID = {4}".format(table_name, mesh_list, do_list, gene_list, disease_id))
        c.execute(sql)
        conn.commit()

    elif table_name is('ICD10CM_gene'):
        update_info = input("please enter update information(DISEASE_ID,GENE_LIST,NUM_OF_GENE),split by ' ':")
        update_info = update_info.split(' ')
        disease_id = update_info[0]
        gene_list = update_info[1]
        num_of_gene = update_info[2]

        sql = ("update {0} set GENE_LIST ='{1}',NUM_OF_GENE = '{2}' "
               "where DISEASE_ID = {3}".format(table_name, gene_list, num_of_gene, disease_id))
        # c.execute(sql)
        conn.commit()

    elif table_name is('group_info'):
        update_info = input("please enter update information(GROUP_ID,DISEASE_LIST,NUM_OF_DISEASE),split by ' ':")
        update_info = update_info.split(' ')
        group_id = update_info[0]
        disease_list = update_info[1]
        num_of_disease = update_info[2]

        sql = ("update {0} set DISEASE_LIST ='{1}',NUM_OF_DISEASE = '{2}' "
               "where GROUP_ID = {3}".format(table_name, disease_list, num_of_disease, group_id))
        c.execute(sql)
        conn.commit()
    else:
        print("no such table exists in '{0}' database".format(database_name))

    conn.close()

    return 0


# update_data("disease_gene", 'mesh_gene')
# update_data("disease_gene", 'ICD10CMinfo')
# update_data("disease_gene", 'ICD10CM_gene')
# update_data("disease_gene", 'group_info')
# update_data("disease_gene","111")

def insert_data(database_name, table_name):
    """
        This function is used to insert data into database
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being inserted
    :return:
    """
    conn = connect_database(database_name)
    c = conn.cursor()

    if table_name is 'mesh_gene':
        update_info = input("please enter insert information(DISEASE_ID,GENE_LIST,NUM_OF_GENE),split by ' ':")
        update_info = update_info.split(' ')
        disease_id = update_info[0]
        gene_list = update_info[1]
        num_of_gene = update_info[2]

        sql = ("insert into {0} (DISEASE_ID,GENE_LIST,NUM_OF_GENE) values ({1},{2},{3})".format
               (table_name, disease_id, gene_list, num_of_gene))

        c.execute(sql)
        conn.commit()

    elif table_name is ('ICD10CMinfo'):
        update_info = input("please enter insert information(DISEASE_ID,MESH_LIST,DO_LIST,GENE_LIST),split by ' ':")
        update_info = update_info.split(' ')
        disease_id = update_info[0]
        mesh_list = update_info[1]
        do_list = update_info[2]
        gene_list = update_info[3]

        sql = ("insert into {0} (DISEASE_ID,MESH_LIST,DO_LIST,GENE_LIST) values ({1},{2},{3},{4})".format
               (table_name, disease_id, mesh_list, do_list, gene_list))
        c.execute(sql)
        conn.commit()

    elif table_name is ('ICD10CM_gene'):
        update_info = input("please enter insert information(DISEASE_ID,GENE_LIST,NUM_OF_GENE),split by ' ':")
        update_info = update_info.split(' ')
        disease_id = update_info[0]
        gene_list = update_info[1]
        num_of_gene = update_info[2]

        sql = ("insert into {0} (DISEASE_ID,GENE_LIST,NUM_OF_GENE) values ({1},{2},{3})".format
               (table_name, disease_id, gene_list, num_of_gene))
        c.execute(sql)
        conn.commit()

    elif table_name is ('group_info'):
        update_info = input("please enter insert information(GROUP_ID,DISEASE_LIST,NUM_OF_DISEASE),split by ' ':")
        update_info = update_info.split(' ')
        group_id = update_info[0]
        disease_list = update_info[1]
        num_of_disease = update_info[2]

        sql = ("insert into {0} (GROUP_ID,DISEASE_LIST,NUM_OF_DISEASE) values ({1},{2},{3})".format
               (table_name, group_id, disease_list, num_of_disease))
        c.execute(sql)
        conn.commit()
    else:
        print("no such table exists in '{0}' database".format(database_name))

    conn.close()

    return 0


# insert_data("disease_gene", 'mesh_gene')
# insert_data("disease_gene", 'ICD10CMinfo')
# insert_data("disease_gene", 'ICD10CM_gene')
# insert_data("disease_gene", 'group_info')
# insert_data("disease_gene", "111")


def delete_data(database_name, table_name, primary_key, primary_key_content):
    """
        This function is to delete information from database
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being deleted
    :param primary_key: string
            The primary key of the database table
    :param primary_key_content: string
            The specific primary key content to be deleted
    :return:
    """

    conn = connect_database(database_name)
    c = conn.cursor()

    sql = ("delete from '{0}' where {1} = '{2}'".format(table_name, primary_key, primary_key_content))

    c.execute(sql)
    conn.commit()

    conn.close()

    return 0


# delete_data("disease_gene", "group_info", "GROUP_ID", "2")
