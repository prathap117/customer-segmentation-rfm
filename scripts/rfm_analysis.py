"""
RFM Analysis & Customer Segmentation
Author: Yaradoni Prathapa
Dataset: UCI Online Retail Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 150
os.makedirs("outputs", exist_ok=True)

# ── 1. LOAD & CLEAN DATA ──────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv("data/online_retail.csv", encoding="ISO-8859-1")

# Clean
df.dropna(subset=["CustomerID"], inplace=True)
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
df.drop_duplicates(inplace=True)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
df["TotalRevenue"] = df["Quantity"] * df["UnitPrice"]

print(f"Cleaned data shape: {df.shape}")

# ── 2. COMPUTE RFM METRICS ────────────────────────────────────────────────────
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
print(f"Snapshot date (reference): {snapshot_date.date()}")

rfm = df.groupby("CustomerID").agg(
    Recency   = ("InvoiceDate",   lambda x: (snapshot_date - x.max()).days),
    Frequency = ("InvoiceNo",     "nunique"),
    Monetary  = ("TotalRevenue",  "sum")
).reset_index()

rfm["Monetary"] = rfm["Monetary"].round(2)
print(f"\nRFM table shape: {rfm.shape}")
print(rfm.describe().round(2))

# ── 3. RFM SCORING (1–5 quintiles) ───────────────────────────────────────────
# Recency: lower days = higher score (inverted)
rfm["R_Score"] = pd.qcut(rfm["Recency"],   q=5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"),  q=5, labels=[1, 2, 3, 4, 5]).astype(int)

rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
rfm["RFM_Total"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

print(f"\nRFM Scores assigned. Sample:\n{rfm.head()}")

# ── 4. SEGMENT LABELLING ──────────────────────────────────────────────────────
def assign_segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3:
        return "Loyal Customers"
    elif r >= 4 and f <= 2:
        return "Potential Loyalists"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2 and m <= 2:
        return "Lost Customers"
    else:
        return "Need Attention"

rfm["Segment"] = rfm.apply(assign_segment, axis=1)

print("\nSegment Distribution:")
print(rfm["Segment"].value_counts())

# ── 5. SAVE RFM DATA ──────────────────────────────────────────────────────────
rfm.to_csv("data/rfm_scores.csv", index=False)
print("\nRFM scores saved to data/rfm_scores.csv")

# ── 6. VISUALIZATIONS ─────────────────────────────────────────────────────────

# Chart 1 — Distribution of R, F, M
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, col, color, label in zip(
    axes,
    ["Recency", "Frequency", "Monetary"],
    ["#3B82F6", "#10B981", "#F59E0B"],
    ["Days Since Last Purchase", "Number of Orders", "Total Spend (£)"]
):
    ax.hist(rfm[col], bins=30, color=color, edgecolor="white", alpha=0.85)
    ax.set_title(col, fontsize=12, fontweight="bold")
    ax.set_xlabel(label, fontsize=9)
    ax.set_ylabel("Customer Count", fontsize=9)
plt.suptitle("RFM Metric Distributions", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("outputs/rfm_distribution.png", bbox_inches="tight")
plt.close()
print("✅ Saved: rfm_distribution.png")

# Chart 2 — Customer Count by Segment
seg_counts = rfm["Segment"].value_counts().reset_index()
seg_counts.columns = ["Segment", "Count"]

COLORS = {
    "Champions": "#1D4ED8",
    "Loyal Customers": "#059669",
    "Potential Loyalists": "#7C3AED",
    "At Risk": "#DC2626",
    "Lost Customers": "#6B7280",
    "Need Attention": "#D97706",
}
colors = [COLORS.get(s, "#94A3B8") for s in seg_counts["Segment"]]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(seg_counts["Segment"], seg_counts["Count"], color=colors, edgecolor="white")
for bar in bars:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
            str(int(bar.get_height())), ha="center", fontsize=9, fontweight="bold")
ax.set_title("Customer Count by Segment", fontsize=14, fontweight="bold")
ax.set_ylabel("Number of Customers")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("outputs/customer_segments_bar.png")
plt.close()
print("✅ Saved: customer_segments_bar.png")

# Chart 3 — Frequency vs Monetary scatter, coloured by segment
fig, ax = plt.subplots(figsize=(10, 6))
for seg, color in COLORS.items():
    subset = rfm[rfm["Segment"] == seg]
    ax.scatter(subset["Frequency"], subset["Monetary"],
               label=seg, color=color, alpha=0.6, s=30, edgecolors="white", linewidth=0.3)
ax.set_title("Frequency vs Monetary Value by Segment", fontsize=14, fontweight="bold")
ax.set_xlabel("Frequency (# Orders)")
ax.set_ylabel("Monetary Value (£)")
ax.legend(title="Segment", fontsize=8, title_fontsize=9, loc="upper right")
ax.set_xlim(0, rfm["Frequency"].quantile(0.98))
ax.set_ylim(0, rfm["Monetary"].quantile(0.98))
plt.tight_layout()
plt.savefig("outputs/rfm_scatter.png")
plt.close()
print("✅ Saved: rfm_scatter.png")

# Chart 4 — Segment Heatmap (avg RFM by segment)
seg_avg = rfm.groupby("Segment")[["R_Score", "F_Score", "M_Score"]].mean().round(2)
seg_avg.columns = ["Avg Recency Score", "Avg Frequency Score", "Avg Monetary Score"]

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(seg_avg, annot=True, fmt=".2f", cmap="Blues",
            linewidths=0.5, ax=ax, annot_kws={"size": 10})
ax.set_title("Average RFM Scores by Customer Segment", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/segment_heatmap.png")
plt.close()
print("✅ Saved: segment_heatmap.png")

# ── 7. BUSINESS SUMMARY ───────────────────────────────────────────────────────
print("\n========== SEGMENT BUSINESS SUMMARY ==========")
summary = rfm.groupby("Segment").agg(
    Customers     = ("CustomerID", "count"),
    Avg_Recency   = ("Recency",    "mean"),
    Avg_Frequency = ("Frequency",  "mean"),
    Avg_Monetary  = ("Monetary",   "mean"),
    Total_Revenue = ("Monetary",   "sum"),
).round(2)
summary["Revenue_Share_%"] = (summary["Total_Revenue"] / summary["Total_Revenue"].sum() * 100).round(1)
print(summary.sort_values("Total_Revenue", ascending=False).to_string())
print("===============================================")
