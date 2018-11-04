import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample

class KMeans:
    def __init__(self):
        self.centroids = []

    # Forgy and Random Partition method: https://en.wikipedia.org/wiki/K-means_clustering#Initialization_methods
    # For EM and standard KMeans, the Forgy method of initialization is preferable
    # For K-harmonic means and fuzzy KMeans, Random Partition method is preferable
    def initialize(self, X, k, random_seed, method='naive'):
        if method == 'naive':
            # Randomly pick k data points to be the centroids of the k clusters
            centroids = resample(X, n_samples=k, random_state=random_seed, replace=False)
        elif method == 'kmeans++': # https://en.wikipedia.org/wiki/K-means%2B%2B
            # Step 1: Choose one center uniformly at random from among the data points
            centroids = resample(X, n_samples=1, random_state=random_seed, replace=False)
            N = len(X)
            # Sampling the 1~k centroids
            for i in range(1, k):
                distances = [ -1 ] * N
                # Step 2: For each data point x, compute D(x)
                for j in range(N):
                    # The distance between x and the nearest center that has already been chosen
                    distances[j] = min(np.linalg.norm(X[j] - centroid) for centroid in centroids)

                # Step 3: Choose one new data point at randome as a new center,
                # using a weighted probability distribution where a point x is chosen with probability proportional to D(x)^2
                square_distances = [ distance ** 2 for distance in distances ]
                total_square_distance = sum(square_distances)
                # Naturally excluded already selected data points, because their probability is 0
                probabilities = [ square_distance / total_square_distance for square_distance in square_distances ]

                new_centroid_index = np.random.choice(range(N), size=1, replace=False, p=probabilities)[0]

                centroids = np.append(centroids, [ X[new_centroid_index] ], axis=0)

        return centroids

    def scree_plot(self, K_range, wss2bss):
        df = pd.DataFrame({'K': K_range, 'wss / bss': wss2bss})
        df.plot(x='K', y='wss / bss', title='Scree Plot')

    # Only available when dimension == 2    
    def cluster_plot(self, X, centroids, X_clusters):
        if len(X[0]) == 2:
            # Plot data points
            df = pd.DataFrame([ [X[i][0], X[i][1], X_clusters[i]] for i in range(len(X)) ],
                           columns=['x', 'y', 'cluster'])
            ax = df.plot.scatter(x='x', y='y', c='cluster', s=4, cmap='viridis')

            # Highlight centroids
            df2 = pd.DataFrame([ [centroids[i][0], centroids[i][1], i] for i in range(len(centroids)) ],
                            columns=['x', 'y', 'cluster'])
            df2.plot.scatter(x='x', y='y', c='red', alpha=0.5, ax=ax, s=15)
            plt.show()

    def EM(self, X, centroids):
        N = len(X)
        # E-step: Reassign data points to form new clusters
        X_clusters = [ -1 ] * N
        for i in range(N):
            distances = [ np.linalg.norm(X[i] - centroid) for centroid in centroids ]
            distance, cluster = min((distance, cluster) for (cluster, distance) in enumerate(distances))
            X_clusters[i] = cluster

        # M-step: Update centroids based on E-step assignment: PRML P425 (9.4)
        K = len(centroids)
        cluster_points_sum = [ 0 ] * K
        cluster_points_count = [ 0 ] * K
        for i in range(N):
            k = X_clusters[i]
            cluster_points_sum[k] += X[i]
            cluster_points_count[k] += 1

        new_centroids = [ cluster_points_sum[k] / cluster_points_count[k] for k in range(K) ]
        
        return X_clusters, new_centroids

    def calculate_wss2bss(self, X, X_clusters, centroids):
        N = len(X)
        K = len(centroids)
        # wss: Within cluster Sums of Squares
        wss = sum(np.linalg.norm(X[i] - centroids[X_clusters[i]]) ** 2 for i in range(N))

        # bss: Between cluster Sums of Squares
        X_mean = np.mean(X) # Sample mean
        bss = sum(np.linalg.norm(centroids[X_clusters[i]] - X_mean) ** 2 for i in range(N))

        return wss / bss

    def fit_range(self, X, K_range, random_seed=42, iteration=30, init_method='naive'):
        wss2bss_list = []
        for k in K_range:
            _, _, wss2bss = self.fit(X, k, random_seed=random_seed, iteration=iteration, init_method=init_method)
            wss2bss_list.append(wss2bss)

        if len(K_range) > 1:
            self.scree_plot(K_range, wss2bss_list)

    def fit(self, X, k, random_seed=42, iteration=30, init_method='naive'):
        print('Fitting with k == {}...\n'.format(k))
        centroids = self.initialize(X, k, random_seed, method=init_method)
        print('Initialized centroids:\n')
        print(centroids)
        for i in range(1, iteration + 1):
            # centroids: new centroids calculated by all data points within a cluster
            X_clusters, centroids = self.EM(X, centroids)

        wss2bss = self.calculate_wss2bss(X, X_clusters, centroids)

        self.cluster_plot(X, centroids, X_clusters)
        self.centroids = np.asarray(centroids)

        return centroids, X_clusters, wss2bss

    def predict(self, X):
        N = len(X)
        y_pred = [ -1 ] * N
        for i in range(N):
            distances = [ np.linalg.norm(X[i] - centroid) for centroid in self.centroids ]
            distance, cluster = min((distance, cluster) for (cluster, distance) in enumerate(distances))
            y_pred[i] = cluster

        return y_pred    