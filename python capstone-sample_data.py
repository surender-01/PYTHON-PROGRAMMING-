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