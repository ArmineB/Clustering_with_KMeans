

import pandas as pd


"""
Created on Wed Aug  1 16:35:17 2018

@author: armine.baghdasaryan
"""

from sklearn.cluster import KMeans


def kMeans(dataFrame, features, k):

    data = dataFrame[features].values
    kmeanModel = KMeans(n_clusters=k).fit(data)
    clusters = [[] for i in range(k)]
    labels = kmeanModel.labels_
    length = len(labels)
    for i in range(length):
        clusters[labels[i]].append(i)

    return clusters


def getIdWithClusters(clusters, dataFrame):
    data = dataFrame.values
    cluster_d = {}
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            # cluster_d[clusters[i][j]] = i + 1
            cluster_d[data[clusters[i][j]][0]] = i + 1

    columns = ['Cluster']
    df_ = pd.DataFrame(data=list(cluster_d.values()), columns=columns)
    df_.insert(loc=0, column=list(dataFrame)[0], value=list(cluster_d.keys()))

    df_.sort_index(inplace=True)
    return df_


def describeData(features, allData, clusters):

    dataF = allData[features]
    data = dataF.values
    columns = features
    dd = pd.DataFrame()
    length = len(clusters)
    for i in range(length):
        d1 = pd.DataFrame(data[clusters[i]], columns=columns).describe().loc[['count', 'mean', 'max', 'min']]
        d1.insert(loc=0, column='Cluster', value=[i + 1] * 4)
        dd = dd.append(d1)

    return dd


