# FastAPI Live Proof — 2026-09-27

Engine: C++17 .so 408K + pybind11 + IsolationForest

Test 1 — R1 Public Overbill:
curl -X POST http://localhost:8000/scrutinize -d '{"hospital_code":"QEH","diagnosis_en":"common cold","amount_hkd":3083,"hko_signal":0}'
→ {"cpp_flagged":true,"reason":"FLAGGED: Public HA QEH cannot bill HKD 3083 for common cold","risk_score":0.95,"final_flag":true} ✅

Build: cmake .. && make → claim_engine_cpp.cpython-312-x86_64-linux-gnu.so 408K
Run: python3 -m uvicorn python_core.api:app --reload --port 8000
Docs: http://localhost:8000/docs

Weightage: 0.95=law broken block, 0.85=typhoon check, 0.75=review, ML=learned
