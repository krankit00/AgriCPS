from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

def cluster(data, eps, min_samples):
    points = np.array(data)
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    labels_unique = np.unique(labels)
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print("number of estimated clusters : %d" % n_clusters_)
    unique_labels = set(labels)
    colors = [plt.cm.rainbow(each) for each in np.linspace(0, 1, len(unique_labels))]

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise ##IGNORED.
            col = "None"
        else:
          class_member_mask = labels == k

          xy = points[class_member_mask & core_samples_mask]
          plt.plot(
              xy[:, 0],
              xy[:, 1],
              "o",
              markerfacecolor=tuple(col),
              markeredgecolor="k",
              markersize=2.5,
              linewidth=0.25,
              label = "_nolegend_"
          )
          mean_cluster = np.mean(xy, axis=0)
          plt.text(mean_cluster[0], mean_cluster[1], str(k+1), fontsize=7, bbox=dict(boxstyle="round",
                   ec="k",
                   fc="w",
                   ))
    plt.title("Estimated number of clusters: %d" % n_clusters_)
    return db