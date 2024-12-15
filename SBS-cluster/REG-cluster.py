import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import csv
from sklearn.decomposition import PCA

# Load the model parameters   params.pt is the result of transR training
model_dict = torch.load("/InterKG/dataset/last-fm/params.pt")
e_embeddings = model_dict['e.weight']

# PCA for solid embedding is reduced to 8 dimensions
pca = PCA(n_components=8)
e_embedding_8d = pca.fit_transform(e_embeddings)

df_embedding = pd.DataFrame(e_embedding_8d)
df_embedding.insert(0, 'index', range(len(df_embedding)))
df_embedding['index'] = df_embedding['index'].astype(str)

with open("/InterKG/pretreatment/final.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    data1 = list(reader)

data2 = {row[0]: ' '.join(row[1:].astype(str)) for row in df_embedding.values}

# Fill in the missing values
for i in range(0, len(data1)):
    for j in range(0, len(data1[i])):
        cell = data1[i][j]
        if cell in data2:
            data1[i][j] = data2[cell]
        else:
            data1[i][j] = '0 0 0 0 0 0 0 0'

# Divide each element into spaces and expand into separate elements
expanded_data = []
for row in data1:
    expanded_row = []
    for cell in row:
        expanded_row.extend(cell.split())
    expanded_data.append(expanded_row)


df_expanded = pd.DataFrame(expanded_data)
df_expanded = df_expanded.drop(index=range(48123, len(df_expanded)))

df_expanded.to_csv('final-embedding.csv', sep=',', index=True, header=True)


# REG-cluster
class DeepCluster(nn.Module):
    def __init__(self, n_clusters, input_dim=72,alpha=1):
        super(DeepCluster, self).__init__()
        self.alpha = alpha
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.Linear(128, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 256),
            nn.Linear(256, 512),
            nn.ReLU(inplace=True),
            nn.Linear(512, 512),
            nn.Linear(512, n_clusters)

        )
        # Initialize the clustering center
        self.center = nn.Parameter(torch.Tensor(n_clusters, input_dim))
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(data.numpy())
        self.center.data.copy_(torch.tensor(kmeans.cluster_centers_))

    def forward(self, inputs):
        f = self.encoder(inputs)
        square_dist = torch.pow(f[:, None, :] - self.center.t(), 2).sum(dim=2)
        nom = torch.pow(1 + square_dist / self.alpha, -(self.alpha + 1) / 2)
        denom = nom.sum(dim=1, keepdim=True)
        q = nom / denom
        return q


def target_distribution(q):
    weight = q ** 2 / q.sum(0)
    return (weight.t() / weight.sum(1)).t()


# Load the data
data = pd.read_csv('final-embedding.csv', header=None, skiprows=[0])
data = data.iloc[:, 1:].astype(float).values
data = np.nan_to_num(data)  # 将NAN和inf值替换为0

data = torch.tensor(data).float()
# Initialize the model and optimizer
n_clusters = 200
model = DeepCluster(n_clusters)
optimizer = optim.Adam(model.parameters(), lr=0.001)


# Train the model
n_epochs =50
batch_size = 256
for epoch in range(n_epochs):
    q = model(data)
    p = target_distribution(q)
    # Calculate the KL divergence
    kl_divergence = nn.KLDivLoss()(torch.log(q), p.detach())
    # Update the model parameters
    optimizer.zero_grad()
    kl_divergence.backward()
    optimizer.step()
    # Outputs the current loss
    if epoch % 10 == 0:
        print('Epoch [{}/{}], KL-Divergence: {:.4f}'.format(epoch + 1, n_epochs, kl_divergence.item()))
# cluster
q = model(data)
cluster_pred = KMeans(n_clusters=n_clusters).fit_predict(q.detach().numpy())
print('Cluster labels: ', cluster_pred)
with open('cluster-200.txt', 'w') as f:
    for i in range(n_clusters):
        f.write('Cluster {}:'.format(i))
        f.write('\n')
        cluster_items = np.where(cluster_pred == i)[0]

        f.write(str(cluster_items)+'\n')
        print('Cluster {}:'.format(i))
        print(cluster_items)
