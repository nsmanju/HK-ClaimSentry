import pandas as pd, sys, os
sys.path.append('cpp_core/build')
sys.path.append('/home/nadkalpur/HK.Insurance.Fintech/cpp_core/build')
import claim_engine_cpp
from sklearn.ensemble import IsolationForest

df = pd.read_csv('data/synthetic/hk_claims_10k.csv')
print(f"Loaded {len(df)} HK claims")

def get_cpp_score(row):
    c = claim_engine_cpp.Claim()
    c.hospital_code = row['hospital_code']
    c.amount_hkd = float(row['amount_hkd'])
    c.hko_signal = int(row['hko_signal'])
    c.diagnosis_en = row['diagnosis_en']
    r = claim_engine_cpp.scrutinize_claim(c)
    return r.risk_score, int(r.flagged)

df[['cpp_score','cpp_flagged']] = df.apply(lambda r: pd.Series(get_cpp_score(r)), axis=1)

# ML only 3% anomaly now, not 5%
X = df[['amount_hkd','hko_signal','cpp_score']]
iso = IsolationForest(contamination=0.03, random_state=42)
df['ml_anomaly'] = iso.fit_predict(X)

# Final flag = C++ flagged OR (ML anomaly AND high amount)
df['final_flag'] = (df['cpp_flagged']==1) | ((df['ml_anomaly']==-1) & (df['amount_hkd']>8000))

print("\n--- Combined C++ + ML Results ---")
print(df[df['final_flag']==1].head(10).to_string(index=False))
print(f"\nTotal Flagged: {df['final_flag'].sum()} / {len(df)} ({df['final_flag'].mean()*100:.1f}%)")
df[df['final_flag']==1].to_csv('data/synthetic/flagged_claims.csv', index=False)
print("\nSaved flagged_claims.csv")
