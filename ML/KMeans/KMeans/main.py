import pandas as pd
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
from KMeans import KMeans

def main():
    random_seed = 0
    iteration = 50
    init_method = 'kmeans++'
    X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=random_seed)
    plt.scatter(X[:, 0], X[:, 1], s=4, c='blue')
    kmeans = KMeans()
    #kmeans.fit_range(X, list(range(3, 7)), random_seed=random_seed, iteration=iteration, init_method=init_method)
    
    kmeans.fit(X, 4, random_seed=random_seed, iteration=iteration, init_method=init_method)
    y_pred = kmeans.predict(X)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(X[:, 0], X[:, 1], c=y_pred, s=4, cmap='viridis')
    centers = kmeans.centroids
    ax.scatter(centers[:, 0], centers[:, 1], c='red', s=15, alpha=0.5)
    plt.show()

if __name__ == '__main__':
    main()