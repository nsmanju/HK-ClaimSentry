#include "rule_engine.h"
#include <unordered_set>
#include <algorithm>
#include <cctype>
FlagResult scrutinize_claim(const Claim& claim) {
    std::unordered_set<std::string> public_hospitals = {"QEH","PWH","QMH","PMH","UCH"};
    std::unordered_set<std::string> simple_dx = {"common cold","urti"};
    std::string dx_lower = claim.diagnosis_en;
    std::transform(dx_lower.begin(), dx_lower.end(), dx_lower.begin(), ::tolower);
    if (public_hospitals.count(claim.hospital_code) && simple_dx.count(dx_lower) && claim.amount_hkd > 1200) {
        return {true, "FLAGGED: Public HA " + claim.hospital_code + " cannot bill HKD " + std::to_string((int)claim.amount_hkd) + " for " + claim.diagnosis_en, 0.95};
    }
    if (claim.hko_signal >= 8) {
        if (dx_lower.find("fracture")==std::string::npos && dx_lower.find("emergency")==std::string::npos && dx_lower.find("appendicitis")==std::string::npos) {
            return {true, "FLAGGED: Claim during HKO Signal " + std::to_string(claim.hko_signal) + " - non-emergency travel unlikely", 0.85};
        }
    }
    if (claim.amount_hkd > 9000 && simple_dx.count(dx_lower)) {
        return {true, "FLAGGED: Amount HKD " + std::to_string((int)claim.amount_hkd) + " too high for " + claim.diagnosis_en, 0.75};
    }
    return {false, "OK: Passed C++ rule engine", 0.05};
}
