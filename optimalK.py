# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 16:35:17 2018

@author: armine.baghdasaryan
"""


from sklearn.cluster import KMeans
import numpy as np


def getOptimalK(data, n):

    distortions = []
    K = range(2, n+1)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(data)
        kmeanModel.fit(data)
        distortions.append(kmeanModel.inertia_)

    length = len(distortions)

    variance = np.mean(distortions) / np.mean(data)


    optK = None
    for i in range(length):
        if i != length - 1:
            if distortions[i] - distortions[i + 1] < variance:
                optK = i + 1

                break

    return optK
