import json

with open('手工校验过的ICD数据一层分组.json') as f:
    file = json.load(f)

all_mesh = []
all_do = []
for disease in file:
    do = file[disease]['do']
    for item in do:
        if item not in all_do:
            all_do.append(item)

    mesh = file[disease]['mesh']
    for item in mesh:
        if item not in all_mesh:
            all_mesh.append(item)

print(len(all_mesh))
print(len(all_do))