
## 1. Introduction
This code is for the paper "Relation Beyond Relation: interrelationship mining for Knowledge Graph-based Recommendations" submitted to IJCAI2025.

## 2. Environment Requirement
```
This code requires deployment on Python 3.7.10, and requires packages as follows:

* torch == 1.6.0
* numpy == 1.21.4
* pandas == 1.3.5
* scipy == 1.5.2
* tqdm == 4.62.3
* scikit-learn == 1.0.1
```

## 3. The detailed steps of InterKG
### 3.1 pretreatment
1. run pivot_table.py to get the multi-user decision table

### 3.2 Semantic-based Self-training Clustering
1. run SBS-cluster.py to executing the clustering  (In this step, we use the parameters pretrained by TransR as input.)

### 3.3 InterKG
1. run Selector.py to chose relations (In this step,we can get D_seg.json and p1_seg_dict.json.)
2. run Generator.py to get the new relations and entities 
3. run new-KG.py to get the new final Knowledge Graph


## 4. Datasets 
We provided three datasets along with their corresponding KG to validate InterKG: last-fm, MovieLens1M, and amazon-book. 
|       Datasets       | Last-FM | MovieLens1M |Amazon-book | 
|:------------:|:-------:|:-----------:|-------------|
|        KG      |Freebase|Freebase|Freebase|
|    users     |  23566  |    6040        | 70679    |
|    items     |  48123  |    3655        |24915    | 
| interactions | 3034796 |   997579      |847733    | 
|   entities   |  58266  |    64731       | 88572    |
|  relations   |    9    |     9           | 39      |
|   triples    | 464567  |   41688       | 2557746   |

