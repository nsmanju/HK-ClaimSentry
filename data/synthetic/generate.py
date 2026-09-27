import csv, random, os
hospitals = ["QEH","PWH","QMH","HKSH","CUHKMC","Gleneagles"]
def realistic_amount(hospital, dx):
    public = ["QEH","PWH","QMH"]
    if dx in ["common cold","urti"]:
        return random.randint(180, 800) if hospital in public else random.randint(400, 1800)
    if dx == "gastroenteritis":
        return random.randint(500, 1500) if hospital in public else random.randint(1200, 3500)
    if dx == "fracture":
        return random.randint(2000, 6000) if hospital in public else random.randint(8000, 20000)
    return random.randint(5000, 20000)
dx_list = ["common cold","urti","gastroenteritis","fracture","emergency appendicitis"]

# Always write to this folder, no matter where you run from
out_path = os.path.join(os.path.dirname(__file__), "hk_claims_10k.csv")
with open(out_path,'w', newline='') as f:
    w=csv.writer(f)
    w.writerow(["claim_id","hospital_code","diagnosis_en","amount_hkd","hko_signal"])
    for i in range(10000):
        hosp = random.choice(hospitals)
        d = random.choice(dx_list)
        amt = realistic_amount(hosp, d)
        sig = random.choices([0,8,9,10], weights=[96,2,1,1])[0]
        w.writerow([f"CLM{i:05d}", hosp, d, amt, sig])
print(f"Generated REALISTIC {out_path}")
