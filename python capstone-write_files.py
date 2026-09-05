# This script writes sample_data.py and csv_analyzer.py to disk
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── sample_data.py ─────────────────────────────────────────────────────────
sample_data = '''
import csv, random, os
random.seed(42)
REGIONS = ["North","South","East","West","  North ",None,"SOUTH","east"]
CATEGORIES = ["Electronics","Clothing","Food","Books",None,"electronics","FOOD"]
NAMES = ["Alice","Bob","Charlie","Diana","Eve",None,"alice","BOB"]
def generate_sample_csv(filename="sample_sales.csv", n=200):
    rows = []
    for i in range(1, n+1):
        sid   = i if random.random()>0.02 else None
        name  = random.choice(NAMES)
        reg   = random.choice(REGIONS)
        cat   = random.choice(CATEGORIES)
        qty   = random.randint(1,50) if random.random()>0.05 else None
        price = round(random.uniform(5.0,500.0),2) if random.random()>0.05 else None
        date  = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}" if random.random()>0.04 else random.choice(["","N/A","not-a-date"])
        disc  = round(random.uniform(0,0.4),2) if random.random()>0.1 else None
        rows.append([sid,name,reg,cat,qty,price,date,disc])
    for _ in range(10):
        rows.append(random.choice(rows[:50]))
    with open(filename,"w",newline="") as f:
        w = csv.writer(f)
        w.writerow(["sale_id","salesperson","region","category","quantity","unit_price","sale_date","discount"])
        w.writerows(rows)
    print(f"Generated {filename!r} with {len(rows)} rows (includes duplicates and dirty data).")
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_sales.csv")
    generate_sample_csv(out)
'''.strip()

# ── csv_analyzer.py ─────────────────────────────────────────────────────────
analyzer = r'''#!/usr/bin/env python3
"""
========================================================
  CSV Data Cleaner & Analyzer  |  Python 3.8+
========================================================
Usage:
  python csv_analyzer.py                      # uses sample_sales.csv
  python csv_analyzer.py mydata.csv           # your own CSV
  python csv_analyzer.py mydata.csv --no-plot # skip chart generation
========================================================
"""
import sys, os, argparse, warnings
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOT_AVAILABLE = True
except ImportError:
    PLOT_AVAILABLE = False

DIV = chr(9472) * 70

def section(t):
    print(f"\n{DIV}\n  {t}\n{DIV}")

def sub(t):
    print(f"\n  >> {t}\n  " + "." * 50)

# ── Load ──────────────────────────────────────────────────────────────────────
def load_csv(fp):
    for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(fp, encoding=enc, low_memory=False)
            print(f"  Loaded {fp!r}  ({len(df)} rows x {len(df.columns)} cols) [enc={enc}]")
            return df
        except UnicodeDecodeError:
            continue
    raise ValueError("Cannot decode file with common encodings.")

# ── Profile ───────────────────────────────────────────────────────────────────
def profile_raw(df):
    section("RAW DATA PROFILE")
    tc = df.size
    miss = df.isnull().sum()
    miss_pct = (miss / len(df) * 100).round(2)
    dupes = df.duplicated().sum()
    print(f"\n  Rows          : {len(df)}")
    print(f"  Columns       : {len(df.columns)}")
    print(f"  Total cells   : {tc}")
    print(f"  Duplicate rows: {dupes}")
    print(f"  Missing values: {miss.sum()}  ({miss.sum()/tc*100:.1f}% of cells)")
    sub("Missing Values per Column")
    mdf = pd.DataFrame({"missing": miss, "pct": miss_pct})
    mdf = mdf[mdf["missing"] > 0].sort_values("missing", ascending=False)
    print(mdf.to_string() if not mdf.empty else "  None!")
    sub("Column Data Types")
    print(df.dtypes.to_string())
    sub("Numeric Summary (raw)")
    nc = df.select_dtypes(include="number").columns.tolist()
    print(df[nc].describe().round(2).to_string() if nc else "  No numeric columns.")

# ── Clean ─────────────────────────────────────────────────────────────────────
def clean_dataframe(df):
    section("DATA CLEANING PIPELINE")
    orig = len(df)
    df = df.copy()

    # Step 1 – column names
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
    sub("Step 1 – Normalise column names")
    print(f"  Columns: {list(df.columns)}")

    # Step 2 – strip whitespace
    sc = df.select_dtypes(include="object").columns
    for c in sc:
        df[c] = df[c].str.strip()
    sub("Step 2 – Strip whitespace from strings")
    print(f"  Cleaned {len(sc)} text columns.")

    # Step 3 – title-case
    sub("Step 3 – Standardise text (title-case)")
    for c in sc:
        df[c] = df[c].str.title()
    print(f"  Applied to: {list(sc)}")

    # Step 4 – replace placeholder NA strings
    sub("Step 4 – Replace placeholder strings with NaN")
    na_vals = ["N/A", "NA", "None", "none", "null", "Null", "", "n/a", "NaN", "-"]
    before = df.isnull().sum().sum()
    df.replace(na_vals, np.nan, inplace=True)
    after = df.isnull().sum().sum()
    print(f"  Converted {after - before} placeholder strings -> NaN")

    # Step 5 – remove duplicates
    sub("Step 5 – Remove duplicate rows")
    bd = len(df)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(f"  Removed {bd - len(df)} duplicates  ({bd} -> {len(df)} rows)")

    # Step 6 – coerce numeric
    sub("Step 6 – Coerce numeric columns")
    candidates = ["quantity", "unit_price", "discount", "sale_id",
                  "price", "amount", "qty", "value"]
    coerced = []
    for col in df.columns:
        if col in candidates or df[col].dtype == object:
            try:
                cv = pd.to_numeric(df[col], errors="coerce")
                if cv.notna().sum() > 0.5 * len(df):
                    df[col] = cv
                    coerced.append(col)
            except Exception:
                pass
    print(f"  Coerced to numeric: {coerced}")

    # Step 7 – parse dates
    sub("Step 7 – Parse date columns")
    date_cols = [c for c in df.columns if any(k in c for k in ["date", "time", "dt"])]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            print(f"  {col}: {df[col].notna().sum()} valid, "
                  f"{df[col].isna().sum()} unparseable -> NaT")
        except Exception:
            pass

    # Step 8 – fill numeric NaN with median
    sub("Step 8 – Fill missing numeric values (median strategy)")
    for col in df.select_dtypes(include="number").columns:
        n = df[col].isnull().sum()
        if n > 0:
            m = df[col].median()
            df[col].fillna(m, inplace=True)
            print(f"  {col}: filled {n} NaN -> median {m:.2f}")

    # Step 9 – fill categorical NaN with mode
    sub("Step 9 – Fill missing categorical values (mode strategy)")
    for col in df.select_dtypes(include="object").columns:
        n = df[col].isnull().sum()
        if n > 0:
            mv = df[col].mode(dropna=True)
            if not mv.empty:
                df[col].fillna(mv[0], inplace=True)
                print(f"  {col}: filled {n} NaN -> mode {mv[0]!r}")

    # Step 10 – outlier removal IQR x3
    sub("Step 10 – Outlier removal (IQR x 3 method)")
    bo = len(df)
    mask = pd.Series(False, index=df.index)
    for col in df.select_dtypes(include="number").columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lo = Q1 - 3 * IQR
        hi = Q3 + 3 * IQR
        cm = (df[col] < lo) | (df[col] > hi)
        if cm.sum() > 0:
            print(f"  {col}: {cm.sum()} outliers  bounds=[{lo:.2f}, {hi:.2f}]")
        mask |= cm
    df = df[~mask].reset_index(drop=True)
    print(f"  Removed {bo - len(df)} outlier rows  ({bo} -> {len(df)})")

    # Step 11 – feature engineering
    sub("Step 11 – Derived feature engineering")
    if "unit_price" in df.columns and "quantity" in df.columns:
        df["revenue"] = (df["unit_price"] * df["quantity"]).round(2)
        print("  Added: revenue = unit_price x quantity")
    if "unit_price" in df.columns and "discount" in df.columns:
        df["net_price"] = (df["unit_price"] * (1 - df["discount"])).round(2)
        print("  Added: net_price = unit_price x (1 - discount)")
    if "sale_date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["sale_date"]):
        df["sale_month"] = df["sale_date"].dt.month
        df["sale_quarter"] = df["sale_date"].dt.quarter
        print("  Added: sale_month, sale_quarter")

    print(f"\n  Cleaning complete: {orig} -> {len(df)} rows retained.")
    return df

# ── Analyse ───────────────────────────────────────────────────────────────────
def analyse(df):
    section("STATISTICAL ANALYSIS  (cleaned data)")
    nc = df.select_dtypes(include="number").columns
    if len(nc):
        sub("Descriptive Statistics")
        print(df[nc].describe().round(2).to_string())
    if len(nc) >= 2:
        sub("Correlation Matrix")
        print(df[nc].corr().round(3).to_string())
    for cat in df.select_dtypes(include="object").columns:
        if 1 < df[cat].nunique() <= 20:
            for num in ["revenue", "unit_price", "quantity"]:
                if num in df.columns:
                    sub(f"Mean {num} by {cat}")
                    g = (df.groupby(cat)[num]
                           .agg(["mean", "sum", "count"])
                           .round(2)
                           .sort_values("sum", ascending=False))
                    print(g.to_string())
                    break
    if "revenue" in df.columns:
        sub("Top 5 Revenue Rows")
        print(df.nlargest(5, "revenue").to_string(index=False))
        sub("Bottom 5 Revenue Rows")
        print(df.nsmallest(5, "revenue").to_string(index=False))

# ── Visualise ─────────────────────────────────────────────────────────────────
def visualise(df, out_dir):
    if not PLOT_AVAILABLE:
        print("\n  matplotlib/seaborn not available - skipping charts.")
        return []
    section("VISUALISATIONS")
    sns.set_theme(style="whitegrid", palette="muted")
    saved = []
    nc = df.select_dtypes(include="number").columns.tolist()
    cc = [c for c in df.select_dtypes(include="object").columns
          if 1 < df[c].nunique() <= 20]
    kn = "revenue" if "revenue" in df.columns else (nc[0] if nc else None)

    # 1 – distribution
    if kn:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        sns.histplot(df[kn], kde=True, ax=axes[0], color="steelblue")
        axes[0].set_title(f"Distribution of {kn}")
        sns.boxplot(y=df[kn], ax=axes[1], color="lightcoral")
        axes[1].set_title(f"Boxplot of {kn}")
        fig.suptitle("Key Numeric Distribution", fontsize=13, fontweight="bold")
        plt.tight_layout()
        p = out_dir / "01_distribution.png"
        fig.savefig(p, dpi=120); plt.close(fig)
        saved.append(str(p)); print(f"  Saved: {p.name}")

    # 2 – correlation heatmap
    if len(nc) >= 2:
        fig, ax = plt.subplots(figsize=(min(len(nc)*1.5, 12), min(len(nc)*1.2, 10)))
        sns.heatmap(df[nc].corr(), annot=True, fmt=".2f",
                    cmap="coolwarm", linewidths=0.5, ax=ax)
        ax.set_title("Correlation Heatmap", fontsize=13, fontweight="bold")
        plt.tight_layout()
        p = out_dir / "02_correlation_heatmap.png"
        fig.savefig(p, dpi=120); plt.close(fig)
        saved.append(str(p)); print(f"  Saved: {p.name}")

    # 3 – bar: mean revenue by category
    if cc and "revenue" in df.columns:
        cat = cc[0]
        g = df.groupby(cat)["revenue"].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(max(6, len(g)*1.2), 5))
        sns.barplot(x=g.index, y=g.values, palette="viridis", ax=ax)
        ax.set_title(f"Mean Revenue by {cat.title()}", fontsize=13, fontweight="bold")
        ax.set_xlabel(cat.title()); ax.set_ylabel("Mean Revenue")
        plt.xticks(rotation=30, ha="right"); plt.tight_layout()
        p = out_dir / "03_revenue_by_category.png"
        fig.savefig(p, dpi=120); plt.close(fig)
        saved.append(str(p)); print(f"  Saved: {p.name}")

    # 4 – scatter
    if kn and len(nc) >= 2:
        xc = nc[0] if nc[0] != kn else (nc[1] if len(nc) > 1 else None)
        if xc:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.scatterplot(data=df, x=xc, y=kn,
                            hue=cc[0] if cc else None,
                            alpha=0.6, s=50, ax=ax)
            ax.set_title(f"{xc} vs {kn}", fontsize=13, fontweight="bold")
            plt.tight_layout()
            p = out_dir / "04_scatter.png"
            fig.savefig(p, dpi=120); plt.close(fig)
            saved.append(str(p)); print(f"  Saved: {p.name}")

    # 5 – monthly trend
    if "sale_month" in df.columns and "revenue" in df.columns:
        monthly = df.groupby("sale_month")["revenue"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=monthly, x="sale_month", y="revenue",
                     marker="o", color="teal", linewidth=2, ax=ax)
        ax.set_title("Monthly Total Revenue", fontsize=13, fontweight="bold")
        ax.set_xlabel("Month"); ax.set_ylabel("Total Revenue")
        ax.set_xticks(range(1, 13)); plt.tight_layout()
        p = out_dir / "05_monthly_revenue.png"
        fig.savefig(p, dpi=120); plt.close(fig)
        saved.append(str(p)); print(f"  Saved: {p.name}")

    print(f"\n  {len(saved)} chart(s) saved to: {out_dir}")
    return saved

# ── Export ────────────────────────────────────────────────────────────────────
def export_results(df, out_dir, stem):
    section("EXPORT")
    cc = out_dir / f"{stem}_cleaned.csv"
    df.to_csv(str(cc), index=False)
    print(f"  Cleaned CSV  -> {cc}")
    rt = out_dir / f"{stem}_report.txt"
    nc = df.select_dtypes(include="number").columns
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(rt, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("  CSV ANALYSIS REPORT\n")
        f.write(f"  Generated : {ts}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Rows: {len(df)}   Columns: {len(df.columns)}\n\n")
        f.write("DESCRIPTIVE STATISTICS\n")
        f.write(df[nc].describe().round(2).to_string())
        if len(nc) >= 2:
            f.write("\n\nCORRELATION MATRIX\n")
            f.write(df[nc].corr().round(3).to_string())
    print(f"  Text report  -> {rt}")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="CSV Data Cleaner and Analyzer")
    parser.add_argument("csv_file", nargs="?", default="sample_sales.csv",
                        help="Path to input CSV (default: sample_sales.csv)")
    parser.add_argument("--no-plot", action="store_true",
                        help="Skip chart generation")
    parser.add_argument("--out-dir", default="output",
                        help="Output directory (default: ./output)")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("  CSV DATA CLEANER & ANALYZER")
    print("=" * 70)

    sd = Path(__file__).parent
    cp = Path(args.csv_file) if Path(args.csv_file).is_absolute() else sd / args.csv_file
    od = sd / args.out_dir
    od.mkdir(parents=True, exist_ok=True)

    if not cp.exists():
        print(f"\n  Error: {cp} not found.")
        print("  Run:  python sample_data.py   to generate sample data first.\n")
        sys.exit(1)

    raw = load_csv(str(cp))
    profile_raw(raw)
    clean = clean_dataframe(raw)
    analyse(clean)
    if not args.no_plot:
        visualise(clean, od)
    export_results(clean, od, cp.stem)

    section("DONE")
    print(f"\n  All output saved in: {od}\n")


if __name__ == "__main__":
    main()
'''

with open(os.path.join(BASE, "sample_data.py"), "w", encoding="utf-8") as f:
    f.write(sample_data)
print("Wrote sample_data.py")

with open(os.path.join(BASE, "csv_analyzer.py"), "w", encoding="utf-8") as f:
    f.write(analyzer)
print("Wrote csv_analyzer.py")
