import matplotlib.pyplot as plt



# def autolabel(rects):
#     for rect in rects:
#         height = rect.get_height()
#         plt.text(rect.get_x()+rect.get_width()/2.- 0.2, 1.03*height, '%s' % int(height))



# name_list = ['Jaccard Index', 'Cosine Similarity', 'Lin']
# num_list = [0.7834, 0.7483, 0.7770]
# autolabel(plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list))
# plt.ylim(ymax=1.0, ymin=0)
# plt.ylabel("Average of AUC")
# plt.xlabel("individual method(group method = avg-linkage)")
# plt.show()



name_list = ['avg-*', 'min-*', 'max-*','funSimMax', 'funSimAvg', 'bma', 'R_DGS']
num_list = [0.7834, 0.5000, 0.8642, 0.8126, 0.8116, 0.8115, 0.8278 ]
rects = plt.bar(range(len(num_list)), num_list, color='rgby')
# X轴标题
index = [0, 1, 2, 3, 4, 5, 6]
index = [float(c) + 0.08 for c in index]
plt.ylim(ymax=1.0, ymin=0)
plt.xticks(index, name_list)
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom')
plt.ylabel("Average of AUC")
plt.xlabel("group method(individual method = Jaaccard), *=linkage")
plt.show()