import numpy as np
import pandas as pd
import json
import itertools
user_dict = dict()  # key is user_id, value is interactions list
with open("/InterKG/dataset/last-fm/train.txt", "r") as file:
    for line in file:
        line = line.strip().split()
        user_id = line[0]
        items = list(set(line[1:]))
        user_dict[user_id] = items


cluster_dict = {}  #  key is cluster_id, value is items list
with open('/InterKG/SBS-cluster/cluster-200.txt', 'r') as file:
    lines = file.readlines()
for line in lines:
    line = line.strip()
    if line.startswith('Cluster'):
        category, items = line.split(':')
        cluster_dict[category] = items.split(',')


item_dict = dict()   #  key is item_id, value is user_id list
for user_id, interactions in user_dict.items():
    for item_id in interactions:
        if item_id not in item_dict:
            item_dict[item_id] = [user_id]
        else:
            item_dict[item_id].append(user_id)


#D_seg
D_seg_in = dict()
D_seg_in = {user_id: [] for user_id in user_dict.keys()}
D_seg_out = dict()
D_seg_out = {user_id: [] for user_id in user_dict.keys()}
D_seg = dict()    #key is user_id value is D-seg
D_seg = {user_id: [] for user_id in user_dict.keys()}
for cluster_id in cluster_dict.keys():
    i=0
    D_seg_in = {user: [] for user in user_dict.keys()}
    D_seg_out = {user: [] for user in user_dict.keys()}
    for item in cluster_dict[cluster_id]:
        for user in user_dict.keys():
            if user in item_dict[item]:
                D_seg_in[user].append(item)
            else:
                D_seg_out[user].append(item)
            D_seg[user] = [list(D_seg_in[user]), list(D_seg_out[user])]
        i=i+1  #items in the current cluster
        print(cluster_id,i,item)
    print("D_seg_in:", D_seg_in)
    print("D_seg_out:", D_seg_out)
    print("D_seg:", D_seg)
 # Write the D_seg output for each loop to a file (each line represents a cluster, the first line is cluster 0)
    with open("D_seg.json", "a") as f:
        json.dump(D_seg, f)
        f.write(",\n")  #


df = pd.read_csv('final.csv', sep=',', header=None)
df.replace(0, 1, inplace=True)
df_copy = df.copy()
df_dict = {}  # key is cluster_id, value is df_copy
for cluster_id in cluster_dict.keys():
    df_copy = df.copy()

    item = [int(i) for i in cluster_dict[cluster_id]]

    df_copy.iloc[~df_copy.index.isin(item), :] = 0

    df_dict[cluster_id] = df_copy

for cluster_id, df_copy in df_dict.items():
    print(f"cluster_id: {cluster_id}, df_copy: {df_copy}")


group_dict={}  # key is group_name，value is item（group_df.index）
group_keys = set() #set of group_name
p1_seg_dict ={}
for df_copy in df_dict.values():
    with open("p1_seg_dict.json", "a") as f:
        f.write("{")
    i=-1
    for col1, col2 in itertools.combinations(df_copy.columns, 2):
        i=i+1
        group_dict = {}
        group_keys = set()
        p1_seg_dict ={}
        groups = df_copy.groupby([col1, col2])

        for group_name, group_df in groups:
            group_key = group_name
            group_value = list(group_df.index)
            if group_key == (0, 0):
                group_dict.pop(group_key, None)
            else:
                group_dict[group_key] = group_value
            group_keys.add(group_key)
            group_keys.discard((0,0))

        P1_list = [list(v) for v in group_dict.values()]
        with open("p1_seg_dict.json", "a") as f:
            f.write(f'"{i}":{json.dumps(P1_list)}')
            f.write(",")
    with open("p1_seg_dict.json", "a") as f:
        f.seek(f.tell() - 1, 0)
        f.truncate()
        f.write("},\n")
        print('P1_list:',P1_list)

# Calculate the similarity of D and p1_seg
with open('D_seg.json', 'r') as f_d, open('p1_seg_dict_update.json', 'r') as f_p1:
    for line_d, line_p1 in zip(f_d, f_p1):
        d_seg_dict = json.loads(line_d.strip(",\n"))
        p1_seg_dict = json.loads(line_p1.strip(",\n"))
        for key1 in d_seg_dict:
            d_set = set([frozenset(region) for region in d_seg_dict[key1]])
            for key2 in p1_seg_dict:
                p_set = set([frozenset(region) for region in p1_seg_dict[key2]])
                intersection = set()
                for dj in d_set:
                    for pi in p_set:
                        if pi & dj:
                            intersection.add(pi & dj)
                numerator = len(p_set) + len(d_set)
                denominator = 2 * len(intersection)
                similarity = numerator / denominator if denominator else 0
                print(similarity)
                with open("D-P1_similarity.txt", "a") as file:
                    file.write(str(similarity) + " ")
        with open("D-P1_similarity.txt", "a") as file:
            file.write("\n")






