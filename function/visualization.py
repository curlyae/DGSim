from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from function.get_datainfo import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sim import cal_groupsim, cal_rdgs


def draw_relation_graph(database_name, table_name, primary_key, group_name) -> Graph:
    """
        A function to draw relation graph of disease group
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param group_name: string
            A disease group name
    :return: c:
            Pyecharts.charts.basic_charts.graph.Graph
    """

    nodes = []
    links = []
    disease_list = get_icd_diseasegroup_diseaseinfo(database_name, table_name, primary_key, group_name)[1]
    disease_list = disease_list.split(',')
    # print(disease_list)

    for disease in disease_list:
        disease_node = {
            "name": disease,
            "symbolSize": 50
        }

        if disease_node not in nodes:
            nodes.append(disease_node)

        gene_list = get_mesh_disease_info(database_name, 'mesh_gene', disease, 'DISEASE_ID')[1]
        gene_list = gene_list.split(',')
        for gene in gene_list:
            gene_node = {
                'name': gene,
                'symbolSize': 10
            }

            if gene_node not in nodes:
                nodes.append(gene_node)

        for gene in gene_list:
            links.append({"source": disease, "target": gene})

    print(nodes)
    print(links)

    c = (
        Graph(init_opts=opts.InitOpts(width="1440px", height="900px")).add("", nodes, links, repulsion=3000)
        .set_global_opts(title_opts=opts.TitleOpts(title="gene-disease association network"))
    )

    return c


draw_relation_graph('disease_gene', 'group_info', 'GROUP_ID', 'ICD10CM:Q87').render()


def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    """
       Create a heatmap from a numpy array and two lists of labels.

    :param data: numpy array
             A 2D numpy array of shape (N, M)

    :param row_labels: list/array
             A list or array of length N with the labels for the rows.

    :param col_labels:  list/array
             A list or array og length M with the labels for the columns.

    option arguments:
    :param ax: matplotlib.axes.Axes
             A matplotlib.axes.Axes instance to which the heatmap is plotted.
             If not provided, use current axes or create a new one.

    :param cbar_kw: dictionary
             A dictionary with arguments to :meth:'matplotlib.Figure.colorbar'.

    :param cbarlabel: string
             The label for the colorbar

    All other arguments are directly passed on to the imshow call.

    :param kwargs:

    :return:
    """
    if not ax:
        ax = plt.gca()

    # Plot the heatmap   绘制热图
    im = ax.imshow(data, **kwargs)

    # Create colorbar    创建颜色条
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...    显示所有的刻度
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.  用相应的列表条目分别标记行和列
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.   让水平轴标签显示在顶部
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.  旋转刻度标签并设置其对齐方式。
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.  关闭spines 创建白色的网格
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.5f}", textcolors=["black", "white"], threshold=None, **textkw):
    """
       A function to annotate a heatmap

    :param im: string
             The AxesImage to be labeled.

    :param data:
             Data used to annotate. If None, the image's data is used.

    :param valfmt: string
             The format of the annotations inside the heatmap.
             This should either use the string format method,e.g.
             "${x:.2f}", or be a :class:'matplotlib.ticker.Formatter'
             .
    :param textcolors: list
             A list or array of two color specifications. The first is
             used for values below a threshold, the second for those above.

    :param threshold:
             Value in data units according to which the colors from textcolors are applied.
             If None (the default) uses the middle of the colormap as separation.

    :param textkw:
             Further arguments are passed on to the created text labels.

    :return:

    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.

    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


def draw_heatmap(database_name, table_name, primary_key, method, indi_method, group_list1, group_list2):
    """
        A function to draw heatmap with annotation
    :param database_name: string
            The database to connect to
    :param table_name: string
            The database table being queried
    :param primary_key: string
            The primary key of database table
    :param method: string
            Methods can be used to calculate group similarity
            rdgs/averagelinkage/minlinkage/maxlinkage/module_jaccard/module_cosine/module_lin/module_mathurscore/
            funsimmax/funsimavg/bma
    :param indi_method: string
            Methods can be used to calculate two disease similarity
            jaccard/cosine/lin/mathur
    :param group_list1: string
            A list of disease group for calculating similarity
    :param group_list2: string
            A list of disease group for calculating similarity
    :return:
    """

    if method == 'rdgs':
        similarity_matrix = cal_rdgs.cal_grouprdgs(database_name, table_name, primary_key, group_list1, group_list2)

    elif method == 'avglinkage':
        similarity_matrix = cal_groupsim.cal_groupavglinkage(database_name, table_name, primary_key, group_list1,
                                                             group_list2, indi_method)

    elif method == 'minlinkage':
        similarity_matrix = cal_groupsim.cal_groupminlinkage(database_name, table_name, primary_key, group_list1,
                                                             group_list2, indi_method)

    elif method == 'maxlinkage':
        similarity_matrix = cal_groupsim.cal_groupmaxlinkage(database_name, table_name, primary_key, group_list1,
                                                             group_list2, indi_method)

    elif method == 'module_jaccard':
        similarity_matrix = cal_groupsim.cal_groupmodulejaccard(database_name, table_name, primary_key,
                                                                group_list1, group_list2)

    elif method == 'module_cosine':
        similarity_matrix = cal_groupsim.cal_groupmodulecosine(database_name, table_name, primary_key,
                                                               group_list1, group_list2)

    elif method == 'module_lin':
        similarity_matrix = cal_groupsim.cal_groupmodulelin(database_name, table_name, primary_key,
                                                            group_list1, group_list2)

    elif method == 'module_mathurscore':
        similarity_matrix = cal_groupsim.cal_groupmodulemathurscore(database_name, table_name, primary_key,
                                                                    group_list1, group_list2)

    elif method == 'funsimmax':
        similarity_matrix = cal_groupsim.cal_groupfunsimmax(database_name, table_name, primary_key,
                                                            group_list1, group_list2, indi_method)

    elif method == 'funsimavg':
        similarity_matrix = cal_groupsim.cal_groupfunsimavg(database_name, table_name, primary_key,
                                                            group_list1, group_list2, indi_method)

    elif method == 'bma':
        similarity_matrix = cal_groupsim.cal_groupbma(database_name, table_name, primary_key,
                                                      group_list1, group_list2, indi_method)

    else:
        print("wrong!")

        exit(0)

    similarity_matrix_array1 = np.array(similarity_matrix)

    similarity = []
    for i in similarity_matrix_array1:
        num_list = []
        for j in i:
            j = float(j)
            num_list.append(j)
        similarity.append(num_list)
    similarity = np.array(similarity)
    # print(similarity)

    disease_group1_name = group_list1.split(',')
    disease_group2_name = group_list2.split(',')

    fig, ax = plt.subplots()

    im, cbar = heatmap(similarity, disease_group1_name, disease_group2_name, ax=ax,
                       cmap="YlGn",
                       cbarlabel="similarity between two disease groups using {0}".format(method))

    texts = annotate_heatmap(im, valfmt="{x:.5f}")

    fig.tight_layout()
    plt.show()


# draw_heatmap("disease_gene", "group_info", "GROUP_ID", "funsimmax", "jaccard",
#              "ICD10CM:D47,ICD10CM:D75,ICD10CM:D72,ICD10CM:D69,ICD10CM:D58",
#              "ICD10CM:D47,ICD10CM:D75,ICD10CM:D72,ICD10CM:D69,ICD10CM:D58")











