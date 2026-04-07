"""
K-Means Clustering on RFM Data
Author: Yaradoni Prathapa
Run AFTER rfm_analysis.py has generated data/rfm_scores.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 150
os.makedirs("outputs", exist_ok=True)

# ── 1. LOAD RFM SCORES ────────────────────────────────────────────────────────
rfm = pd.read_csv("data/rfm_scores.csv")
print(f"Loaded RFM data: {rfm.shape}")

# ── 2. SCALE FEATURES FOR CLUSTERING ─────────────────────────────────────────
features = rfm[["Recency", "Frequency", "Monetary"]].copy()

# Log-transform skewed features
features["Recency"]   = np.log1p(features["Recency"])
features["Frequency"] = np.log1p(features["Frequency"])
features["Monetary"]  = np.log1p(features["Monetary"])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# ── 3. ELBOW METHOD — Find Optimal K ─────────────────────────────────────────
inertias = []
silhouettes = []
K_range = range(2, 11)

print("Running K-Means for K = 2 to 10...")
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, km.labels_))
    print(f"  K={k} | Inertia={km.inertia_:.1f} | Silhouette={silhouette_score(X_scaled, km.labels_):.3f}")

# Plot Elbow Curve
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(list(K_range), inertias, marker="o", color="#2563EB", linewidth=2)
axes[0].axvline(x=4, color="#DC2626", linestyle="--", alpha=0.7, label="Optimal K=4")
axes[0].set_title("Elbow Method", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Number of Clusters (K)")
axes[0].set_ylabel("Inertia (WCSS)")
axes[0].legend()

axes[1].plot(list(K_range), silhouettes, marker="s", color="#10B981", linewidth=2)
axes[1].axvline(x=4, color="#DC2626", linestyle="--", alpha=0.7, label="Optimal K=4")
axes[1].set_title("Silhouette Score", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Number of Clusters (K)")
axes[1].set_ylabel("Silhouette Score")
axes[1].legend()

plt.suptitle("Optimal Number of Clusters", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/elbow_curve.png")
plt.close()
print("✅ Saved: elbow_curve.png")

# ── 4. FIT FINAL K-MEANS (K=4) ───────────────────────────────────────────────
OPTIMAL_K = 4
kmeans = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=10)
rfm["Cluster"] = kmeans.fit_predict(X_scaled)

print(f"\nK-Means with K={OPTIMAL_K} complete.")
print(f"Silhouette Score: {silhouette_score(X_scaled, rfm['Cluster']):.3f}")

# ── 5. CLUSTER PROFILING ──────────────────────────────────────────────────────
cluster_profile = rfm.groupby("Cluster").agg(
    Count       = ("CustomerID", "count"),
    Avg_Recency = ("Recency",    "mean"),
    Avg_Freq    = ("Frequency",  "mean"),
    Avg_Monetary= ("Monetary",   "mean"),
    Total_Rev   = ("Monetary",   "sum"),
).round(2)
cluster_profile["Rev_Share_%"] = (
    cluster_profile["Total_Rev"] / cluster_profile["Total_Rev"].sum() * 100
).round(1)
print("\nCluster Profile:")
print(cluster_profile.to_string())

# Map cluster labels based on profile
# (Adjust mapping after reviewing cluster_profile output)
cluster_labels = {
    cluster_profile["Avg_Monetary"].idxmax(): "High Value",
    cluster_profile["Avg_Freq"].idxmax():     "Frequent Buyers",
    cluster_profile["Avg_Recency"].idxmin():  "Recent Buyers",
}
rfm["Cluster_Label"] = rfm["Cluster"].map(
    lambda c: cluster_labels.get(c, "Occasional Buyers")
)

print("\nCluster Label Distribution:")
print(rfm["Cluster_Label"].value_counts())

# ── 6. SCATTER PLOT — Frequency vs Monetary by Cluster ───────────────────────
CMAP = {0: "#1D4ED8", 1: "#DC2626", 2: "#10B981", 3: "#F59E0B"}
fig, ax = plt.subplots(figsize=(9, 6))
for cluster in rfm["Cluster"].unique():
    subset = rfm[rfm["Cluster"] == cluster]
    label = cluster_labels.get(cluster, f"Cluster {cluster}")
    ax.scatter(subset["Frequency"], subset["Monetary"],
               color=CMAP.get(cluster, "#94A3B8"),
               label=label, alpha=0.6, s=25, edgecolors="white", linewidth=0.3)
ax.set_title("K-Means Clusters: Frequency vs Monetary", fontsize=13, fontweight="bold")
ax.set_xlabel("Frequency (# Orders)")
ax.set_ylabel("Monetary Value (£)")
ax.legend(title="Cluster", fontsize=9)
ax.set_xlim(0, rfm["Frequency"].quantile(0.98))
ax.set_ylim(0, rfm["Monetary"].quantile(0.98))
plt.tight_layout()
plt.savefig("outputs/kmeans_clusters.png")
plt.close()
print("✅ Saved: kmeans_clusters.png")

# ── 7. SAVE FINAL OUTPUT ──────────────────────────────────────────────────────
rfm.to_csv("data/rfm_clusters.csv", index=False)
print("\n✅ Final clustered data saved to data/rfm_clusters.csv")
print("\nAll done! Review outputs/ folder for charts.")
