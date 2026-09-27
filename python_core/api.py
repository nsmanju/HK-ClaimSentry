from fastapi import FastAPI
from pydantic import BaseModel
import sys
sys.path.append('cpp_core/build')
import claim_engine_cpp

app = FastAPI(title="HK-ClaimSentry v3.1")

class ClaimIn(BaseModel):
    claim_id: str = "CLM99999"
    hospital_code: str = "QEH"
    diagnosis_en: str = "common cold"
    amount_hkd: float = 3083
    hko_signal: int = 0

@app.get("/")
def home():
    return {"engine": "C++ + ML", "rate": "308/10000 (3.1%)", "docs": "/docs"}

@app.post("/scrutinize")
def scrutinize(c: ClaimIn):
    cl = claim_engine_cpp.Claim()
    cl.hospital_code = c.hospital_code
    cl.diagnosis_en = c.diagnosis_en
    cl.amount_hkd = float(c.amount_hkd)
    cl.hko_signal = int(c.hko_signal)
    r = claim_engine_cpp.scrutinize_claim(cl)
    return {"cpp_flagged": bool(r.flagged), "reason": r.reason, "risk_score": r.risk_score, "final_flag": bool(r.flagged or c.amount_hkd>8000)}
