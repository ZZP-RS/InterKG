import json
i=0

with open('p1_seg_dict.json', 'r') as f_d:
    with open('p1_seg_dict_update.json', 'a') as f_update:
        for line_d in f_d:
            d_seg_dict = json.loads(line_d.strip(",\n"))
            for key, value in d_seg_dict.items():

                for i in range(len(value)):

                    value[i] = [str(item) if isinstance(item, int) else [str(subitem) for subitem in item] for item in
                                value[i]]

            json.dump(d_seg_dict, f_update)
            f_update.write(",\n")


def similarity(set1, set2):
    intersection = set1.intersection(set2)
    if not intersection:
        return float('inf')
    sum_of_sizes = len(set1) + len(set2)
    return sum_of_sizes / 2 * len(intersection)

with open('D_seg.json', 'r') as f_d, open('p1_seg_dict_update.json', 'r') as f_p1:
    for line_d, line_p1 in zip(f_d, f_p1):
        i=i+1
        d_seg_dict = json.loads(line_d.strip(",\n"))
        p1_seg_dict = json.loads(line_p1.strip(",\n"))
        for key2, value2 in p1_seg_dict.items():
            p_list = value2
            result_dict = {}

            max_similarity = 0
            max_key1 = None
            min_list_length = float('inf')
            max_dict = {}

            for key1, value1 in d_seg_dict.items():
                d_set = value1[0]
                com_lists = []

                for sublist in p_list:
                    if any(element in sublist for element in d_set):
                        com_lists.extend(sublist)
                if com_lists:
                    if key1 not in result_dict:
                        result_dict[key1] = []
                    result_dict[key1].extend(com_lists)
                    # print(key1,com_lists)
                    d_set2 = set(d_set)
                    com_set = set(com_lists)
                    similarity = similarity(d_set2, com_set)
                    # print(key1, similarity)
                    if similarity > max_similarity :
                        max_similarity = similarity
                        max_key1 = key1
                        min_list_length = len(com_lists)
                        max_dict = {max_key1: com_lists}

            with open(f"max_dict.txt", "a") as f:
                f.write(str(list((max_dict.values()))))
        with open(f"max_dict.txt", "a") as f:
            f.write('\n')


