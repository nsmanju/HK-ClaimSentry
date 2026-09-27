#pragma once
#include <string>
struct Claim {
    std::string hospital_code;
    double amount_hkd = 0;
    int hko_signal = 0;
    std::string diagnosis_en;
};
struct FlagResult {
    bool flagged = false;
    std::string reason;
    double risk_score = 0;
};
FlagResult scrutinize_claim(const Claim& claim);
