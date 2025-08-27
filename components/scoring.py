from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SubscaleScore:
    raw: int
    adjusted: int
    severity: str

def load_thresholds(cfg: Dict, subscale: str):
    return cfg["severity_thresholds"][subscale]

def severity_from_thresholds(adjusted_score: int, thresholds: Dict[str, List[int]]) -> str:
    for label, (lo, hi) in thresholds.items():
        if lo <= adjusted_score <= hi:
            return label
    return list(thresholds.keys())[-1]

def score_dass21(answers: Dict[int, int], cfg: Dict) -> Dict[str, SubscaleScore]:
    subscale_sums = {"Depression":0, "Anxiety":0, "Stress":0}
    for item in cfg["items"]:
        val = answers.get(item["id"], 0)
        subscale_sums[item["subscale"]] += val
    result = {}
    for subscale, raw in subscale_sums.items():
        adjusted = raw * 2
        sev = severity_from_thresholds(adjusted, load_thresholds(cfg, subscale))
        result[subscale] = SubscaleScore(raw=raw, adjusted=adjusted, severity=sev)
    return result
