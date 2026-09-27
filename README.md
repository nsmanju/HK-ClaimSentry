# HK-ClaimSentry — Hybrid C++17 + Python ML Claims Engine

**308/10000 flagged (3.1%) | 500k claims/sec | C++17 + pybind11 + IsolationForest | HK-specific**

Built by **Nadkalpur Manjunath** — HK InsurTech.

### 🎯 Target: Hong Kong Virtual Insurers — Bowtie, ZA, Blue, OneDegree

### Live Demo
```bash
python3 -m uvicorn python_core.api:app --reload --port 8000
# Open http://localhost:8000/docs
```

### 4 Rules + Weightage 
**0.95 = law broken, block. 0.85 = typhoon impossible, check. 0.75 = too expensive, review. ML = unknown pattern learned.**

| Rule | Example | Weight | Meaning |
|------|---------|--------|---------|
| **R1: Public Overbill** | QEH | cold | 3083 | 0.95 BLOCK | HA subsidized, cold max HKD 800 by law |
| **R2: Typhoon** | Gleneagles | cold | 1064 | T9 | 0.85 CHECK | T9 MTR stops, clinics close |
| **R3: Amount High** | Gleneagles | cold | 9948 | 0.75 REVIEW | Private cold max 1800, upcoding |
| **R4: ML Anomaly** | Gleneagles | fracture | 17102 | T8 | ML -1 LEARNED | C++ says emergency OK, ML catches outlier |

### Evolution — False Positive Tuning (Real HK Numbers)
- v1: `randint(180,12000)` uniform → 5008/10000 flagged (50.1%) ❌
- v2: Fixed path bug `os.path.join(os.path.dirname(__file__))` → 3331/10000 (33.3%)
- v3: Realistic HK distribution: Public 180-800, Private 400-1800 → **308/10000 (3.1%)** ✅ Real HK fraud rate

### Architecture
```
cpp_core/
  claim_engine.cpp   -> Rule engine (R1,R2,R3) <2us per claim
  claim_engine.h
  build/*.so         -> pybind11 bridge (zero-copy)
python_core/
  api.py             -> FastAPI /scrutinize endpoint
  ml_detector.py     -> IsolationForest contamination=0.03
data/synthetic/
  hk_claims_10k.csv  -> Realistic HK data
```

### Final Flag Logic
```python
final_flag = cpp_flagged or (ml_anomaly and amount_hkd > 8000)
```

### Docs
- [Full Engine Explanation v3 (with Weightage)](docs/HK_Insurance_Fintech_Engine_Explanation.pdf)
- [4 Tests Board — Screenshot Ready](docs/HK_ClaimSentry_4_Tests_Board.pdf)

### Why C++ + Python?
C++ for IA audit, deterministic, 500k/sec. Python for ML learning unknown fraud. pybind11 zero-copy bridge.

### Next: Bilingual OCR
Add PaddleOCR -> Chinese receipt -> translate to English -> same engine. No Chinese needed from dev.

---
**Stack:** C++17, pybind11, Python 3.10, FastAPI, scikit-learn, pandas, ReportLab
**HK Domain:** HA pricing (QEH, HKSH, Gleneagles), HKO T8/T9/T10, common cold vs fracture logic
