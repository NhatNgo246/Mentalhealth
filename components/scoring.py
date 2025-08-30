from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SubscaleScore:
    raw: int
    adjusted: int
    severity: str
    color: str = "green"
    level_info: Dict = None

@dataclass 
class EnhancedAssessmentResult:
    subscales: Dict[str, SubscaleScore]
    total_score: int
    interpretation: str
    recommendations: Dict
    severity_level: str

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

def score_dass21_enhanced(answers: Dict[int, int], cfg: Dict) -> EnhancedAssessmentResult:
    """Enhanced scoring for DASS-21 with improved Vietnamese interpretation"""
    
    # Calculate subscale scores
    subscale_sums = {"Depression": 0, "Anxiety": 0, "Stress": 0}
    
    for item in cfg["items"]:
        val = answers.get(item["id"], 0)
        subscale_sums[item["subscale"]] += val
    
    # Calculate subscale results with enhanced info
    subscale_results = {}
    scoring_config = cfg["scoring"]["subscales"]
    
    for subscale, raw_score in subscale_sums.items():
        multiplier = scoring_config[subscale]["multiplier"]
        adjusted_score = raw_score * multiplier
        
        # Determine severity level
        severity_levels = scoring_config[subscale]["severity_levels"]
        current_level = "normal"
        level_info = severity_levels["normal"]
        
        for level_name, level_data in severity_levels.items():
            if level_data["min"] <= adjusted_score <= level_data["max"]:
                current_level = level_name
                level_info = level_data
                break
        
        subscale_results[subscale] = SubscaleScore(
            raw=raw_score,
            adjusted=adjusted_score,
            severity=current_level,
            color=level_info["color"],
            level_info=level_info
        )
    
    # Calculate total score
    total_score = sum(result.adjusted for result in subscale_results.values())
    
    # Determine overall interpretation
    total_config = cfg["scoring"]["total_score"]["interpretation"]
    overall_interpretation = "low"
    
    for level_name, level_data in total_config.items():
        if level_data["min"] <= total_score <= level_data["max"]:
            overall_interpretation = level_data["label"]
            break
    
    # Determine highest severity level for recommendations
    severity_order = ["normal", "mild", "moderate", "severe", "extremely_severe"]
    highest_severity = "normal"
    
    for subscale_result in subscale_results.values():
        if subscale_result.severity in severity_order:
            current_index = severity_order.index(subscale_result.severity)
            highest_index = severity_order.index(highest_severity)
            if current_index > highest_index:
                highest_severity = subscale_result.severity
    
    # Get recommendations
    recommendations = cfg["recommendations"].get(highest_severity, cfg["recommendations"]["normal"])
    
    return EnhancedAssessmentResult(
        subscales=subscale_results,
        total_score=total_score,
        interpretation=overall_interpretation,
        recommendations=recommendations,
        severity_level=highest_severity
    )

def score_phq9_enhanced(answers: Dict[int, int], cfg: Dict) -> EnhancedAssessmentResult:
    """Enhanced scoring for PHQ-9 with improved Vietnamese interpretation"""
    
    # Calculate total score
    total_score = sum(answers.get(i, 0) for i in range(1, 10))
    
    # Determine severity level
    severity_levels = cfg["scoring"]["severity_levels"]
    current_level = "minimal"
    level_info = severity_levels["minimal"]
    
    for level_name, level_data in severity_levels.items():
        min_score, max_score = level_data["range"]
        if min_score <= total_score <= max_score:
            current_level = level_name
            level_info = level_data
            break
    
    # Special handling for suicide risk (item 9)
    suicide_risk_score = answers.get(9, 0)
    suicide_risk_assessment = cfg["scoring"]["suicide_risk_assessment"]
    
    # Create a single "Depression" subscale for consistency
    depression_subscale = SubscaleScore(
        raw=total_score,
        adjusted=total_score,
        severity=current_level,
        color=level_info["color"],
        level_info=level_info
    )
    
    subscale_results = {"Depression": depression_subscale}
    
    # Add suicide risk information to the result
    if suicide_risk_score > 0:
        suicide_key = f"item_9_score_{suicide_risk_score}"
        suicide_assessment = suicide_risk_assessment.get(suicide_key, "Cần đánh giá thêm")
        level_info["suicide_risk"] = suicide_assessment
    
    # Get recommendations
    recommendations = cfg["recommendations"].get(current_level, cfg["recommendations"]["minimal"])
    
    # Add emergency contact info if high risk
    if suicide_risk_score >= 2 or total_score >= 15:
        recommendations["emergency_contacts"] = cfg["emergency_contacts"]
        recommendations["urgent_note"] = "⚠️ CẢNH BÁO: Cần can thiệp ngay lập tức!"
    
    return EnhancedAssessmentResult(
        subscales=subscale_results,
        total_score=total_score,
        interpretation=level_info["description"],
        recommendations=recommendations,
        severity_level=current_level
    )

def score_gad7_enhanced(answers: Dict[int, int], cfg: Dict) -> EnhancedAssessmentResult:
    """Enhanced scoring for GAD-7 with improved Vietnamese interpretation"""
    
    # Calculate total score
    total_score = sum(answers.get(i, 0) for i in range(1, 8))
    
    # Determine severity level
    severity_levels = cfg["scoring"]["severity_levels"]
    current_level = "minimal"
    level_info = severity_levels["minimal"]
    
    for level_name, level_data in severity_levels.items():
        min_score, max_score = level_data["range"]
        if min_score <= total_score <= max_score:
            current_level = level_name
            level_info = level_data
            break
    
    # Create a single "Anxiety" subscale for consistency
    anxiety_subscale = SubscaleScore(
        raw=total_score,
        adjusted=total_score,
        severity=current_level,
        color=level_info["color"],
        level_info=level_info
    )
    
    subscale_results = {"Anxiety": anxiety_subscale}
    
    # Get recommendations
    recommendations = cfg["recommendations"].get(current_level, cfg["recommendations"]["minimal"])
    
    # Add emergency contact info if high risk
    if total_score >= 15:
        recommendations["emergency_contacts"] = cfg["emergency_contacts"]
        recommendations["urgent_note"] = "⚠️ CẢNH BÁO: Lo âu nghiêm trọng - Cần hỗ trợ ngay!"
    
    return EnhancedAssessmentResult(
        subscales=subscale_results,
        total_score=total_score,
        interpretation=level_info["description"],
        recommendations=recommendations,
        severity_level=current_level
    )

def score_epds_enhanced(answers: Dict[int, int], cfg: Dict) -> EnhancedAssessmentResult:
    """Enhanced scoring for EPDS with improved Vietnamese interpretation"""
    
    # Calculate total score with special handling for reverse-scored items
    total_score = 0
    
    for item in cfg["items"]:
        item_id = item["id"]
        answer_value = answers.get(item_id, 0)
        
        # Handle reverse scoring for items 1 and 2
        if item.get("reverse_scored", False):
            # For reverse scored items, flip the values
            total_score += (3 - answer_value)
        else:
            total_score += answer_value
    
    # Determine severity level
    severity_levels = cfg["scoring"]["severity_levels"]
    current_level = "no_risk"
    level_info = severity_levels["no_risk"]
    
    for level_name, level_data in severity_levels.items():
        min_score, max_score = level_data["range"]
        if min_score <= total_score <= max_score:
            current_level = level_name
            level_info = level_data
            break
    
    # Special handling for suicide/self-harm risk (item 10)
    suicide_risk_score = answers.get(10, 0)
    suicide_risk_assessment = cfg["scoring"]["suicide_risk_assessment"]
    
    # Create a single "Postnatal Depression" subscale for consistency
    depression_subscale = SubscaleScore(
        raw=total_score,
        adjusted=total_score,
        severity=current_level,
        color=level_info["color"],
        level_info=level_info
    )
    
    subscale_results = {"Postnatal Depression": depression_subscale}
    
    # Add suicide risk information to the result
    if suicide_risk_score > 0:
        suicide_key = f"item_10_score_{suicide_risk_score}"
        suicide_assessment = suicide_risk_assessment.get(suicide_key, "Cần đánh giá thêm")
        level_info["suicide_risk"] = suicide_assessment
    
    # Get recommendations
    recommendations = cfg["recommendations"].get(current_level, cfg["recommendations"]["no_risk"])
    
    # Add emergency contact info if high risk
    if suicide_risk_score >= 2 or total_score >= 12:
        recommendations["emergency_contacts"] = cfg["emergency_contacts"]
        recommendations["urgent_note"] = "⚠️ CẢNH BÁO: Nguy cơ cao - Cần can thiệp ngay lập tức!"
        
    # Add special considerations for postpartum period
    if current_level in ["moderate_risk", "high_risk"]:
        recommendations["special_considerations"] = cfg["special_considerations"]
    
    return EnhancedAssessmentResult(
        subscales=subscale_results,
        total_score=total_score,
        interpretation=level_info["description"],
        recommendations=recommendations,
        severity_level=current_level
    )

def score_pss10_enhanced(answers: Dict[int, int], cfg: Dict) -> EnhancedAssessmentResult:
    """Enhanced scoring for PSS-10 with improved Vietnamese interpretation"""
    
    # Calculate total score with reverse scoring
    total_score = 0
    reverse_items = cfg["scoring"]["reverse_scoring"]["items"]
    
    for item in cfg["items"]:
        item_id = item["id"]
        answer_value = answers.get(item_id, 0)
        
        # Handle reverse scoring for specific items
        if item_id in reverse_items:
            # For reverse scored items: 4 - original_score
            total_score += (4 - answer_value)
        else:
            total_score += answer_value
    
    # Determine severity level
    severity_levels = cfg["scoring"]["severity_levels"]
    current_level = "low"
    level_info = severity_levels["low"]
    
    for level_name, level_data in severity_levels.items():
        min_score, max_score = level_data["range"]
        if min_score <= total_score <= max_score:
            current_level = level_name
            level_info = level_data
            break
    
    # Create a single "Perceived Stress" subscale for consistency
    stress_subscale = SubscaleScore(
        raw=total_score,
        adjusted=total_score,
        severity=current_level,
        color=level_info["color"],
        level_info=level_info
    )
    
    subscale_results = {"Perceived Stress": stress_subscale}
    
    # Get recommendations
    recommendations = cfg["recommendations"].get(current_level, cfg["recommendations"]["low"])
    
    # Add stress management techniques
    recommendations["stress_techniques"] = cfg["stress_management_techniques"]
    
    # Add emergency contact info if high stress
    if total_score >= 30:
        recommendations["emergency_contacts"] = cfg["emergency_contacts"]
        recommendations["urgent_note"] = "⚠️ CẢNH BÁO: Căng thẳng nghiêm trọng - Cần hỗ trợ ngay!"
    
    return EnhancedAssessmentResult(
        subscales=subscale_results,
        total_score=total_score,
        interpretation=level_info["description"],
        recommendations=recommendations,
        severity_level=current_level
    )

def calculate_scores(questionnaire_type, responses):
    """
    Main scoring function - compatibility wrapper for all questionnaire types
    
    Args:
        questionnaire_type: String indicating questionnaire type
        responses: List of response values
        
    Returns:
        Dict with scoring results including total_score, severity, interpretation
    """
    
    # Convert responses to dict format if it's a list
    if isinstance(responses, list):
        answers = {i+1: val for i, val in enumerate(responses)}
    else:
        answers = responses
    
    # Mock configuration for basic scoring
    # In production, this should load from actual config files
    
    if questionnaire_type.upper() == "PHQ-9":
        total_score = sum(answers.values()) if isinstance(answers, dict) else sum(responses)
        
        if total_score <= 4:
            severity = "Minimal"
            interpretation = "Ít có dấu hiệu trầm cảm"
        elif total_score <= 9:
            severity = "Mild"
            interpretation = "Trầm cảm nhẹ"
        elif total_score <= 14:
            severity = "Moderate"
            interpretation = "Trầm cảm vừa"
        elif total_score <= 19:
            severity = "Moderately severe"
            interpretation = "Trầm cảm khá nặng"
        else:
            severity = "Severe"
            interpretation = "Trầm cảm nặng"
            
    elif questionnaire_type.upper() == "GAD-7":
        total_score = sum(answers.values()) if isinstance(answers, dict) else sum(responses)
        
        if total_score <= 4:
            severity = "Minimal"
            interpretation = "Ít có dấu hiệu lo âu"
        elif total_score <= 9:
            severity = "Mild"
            interpretation = "Lo âu nhẹ"
        elif total_score <= 14:
            severity = "Moderate"
            interpretation = "Lo âu vừa"
        else:
            severity = "Severe"
            interpretation = "Lo âu nặng"
            
    elif questionnaire_type.upper() == "DASS-21":
        total_score = sum(answers.values()) if isinstance(answers, dict) else sum(responses)
        adjusted_score = total_score * 2
        
        if adjusted_score <= 9:
            severity = "Normal"
            interpretation = "Trạng thái bình thường"
        elif adjusted_score <= 13:
            severity = "Mild"
            interpretation = "Mức độ nhẹ"
        elif adjusted_score <= 20:
            severity = "Moderate"
            interpretation = "Mức độ vừa"
        elif adjusted_score <= 27:
            severity = "Severe"
            interpretation = "Mức độ nặng"
        else:
            severity = "Extremely severe"
            interpretation = "Mức độ rất nặng"
            
    elif questionnaire_type.upper() == "PSS-10":
        total_score = sum(answers.values()) if isinstance(answers, dict) else sum(responses)
        
        if total_score <= 13:
            severity = "Low"
            interpretation = "Mức căng thẳng thấp"
        elif total_score <= 26:
            severity = "Moderate"
            interpretation = "Mức căng thẳng vừa"
        else:
            severity = "High"
            interpretation = "Mức căng thẳng cao"
            
    elif questionnaire_type.upper() == "EPDS":
        total_score = sum(answers.values()) if isinstance(answers, dict) else sum(responses)
        
        if total_score <= 9:
            severity = "Low risk"
            interpretation = "Nguy cơ thấp"
        elif total_score <= 12:
            severity = "Moderate risk"
            interpretation = "Nguy cơ vừa"
        else:
            severity = "High risk"
            interpretation = "Nguy cơ cao"
    else:
        # Default scoring
        total_score = sum(answers.values()) if isinstance(answers, dict) else sum(responses)
        severity = "Unknown"
        interpretation = f"Điểm tổng: {total_score}"
    
    return {
        "total_score": total_score,
        "severity": severity,
        "interpretation": interpretation,
        "questionnaire_type": questionnaire_type,
        "recommendations": {
            "immediate": "Tham khảo ý kiến chuyên gia nếu cần" if severity in ["Severe", "High", "High risk"] else "Tiếp tục theo dõi tình trạng",
            "followup": "Đánh giá lại sau 2-4 tuần"
        }
    }

# Basic scoring functions for backward compatibility
def score_phq9(answers: Dict) -> Dict:
    """Basic PHQ-9 scoring function"""
    total_score = sum(answers.values()) if isinstance(answers, dict) else 0
    
    if total_score < 5:
        severity = "Minimal"
        interpretation = "Triệu chứng trầm cảm tối thiểu"
    elif total_score < 10:
        severity = "Mild"
        interpretation = "Triệu chứng trầm cảm nhẹ"
    elif total_score < 15:
        severity = "Moderate"
        interpretation = "Triệu chứng trầm cảm vừa phải"
    elif total_score < 20:
        severity = "Moderately severe"
        interpretation = "Triệu chứng trầm cảm khá nặng"
    else:
        severity = "Severe"
        interpretation = "Triệu chứng trầm cảm nặng"
    
    return {
        "total_score": total_score,
        "severity": severity,
        "interpretation": interpretation
    }

def score_gad7(answers: Dict) -> Dict:
    """Basic GAD-7 scoring function"""
    total_score = sum(answers.values()) if isinstance(answers, dict) else 0
    
    if total_score < 5:
        severity = "Minimal"
        interpretation = "Lo âu tối thiểu"
    elif total_score < 10:
        severity = "Mild"
        interpretation = "Lo âu nhẹ"
    elif total_score < 15:
        severity = "Moderate"
        interpretation = "Lo âu vừa phải"
    else:
        severity = "Severe"
        interpretation = "Lo âu nặng"
    
    return {
        "total_score": total_score,
        "severity": severity,
        "interpretation": interpretation
    }

def score_dass21(answers: Dict) -> Dict:
    """Basic DASS-21 scoring function"""
    # DASS-21 subscale items
    depression_items = [3, 5, 10, 13, 16, 17, 21]
    anxiety_items = [2, 4, 7, 9, 15, 19, 20]
    stress_items = [1, 6, 8, 11, 12, 14, 18]
    
    # Calculate subscale scores
    depression_score = sum(answers.get(f'q{i}', 0) for i in depression_items) * 2
    anxiety_score = sum(answers.get(f'q{i}', 0) for i in anxiety_items) * 2
    stress_score = sum(answers.get(f'q{i}', 0) for i in stress_items) * 2
    total_score = depression_score + anxiety_score + stress_score
    
    # Determine severity levels
    def get_severity(score, thresholds):
        if score < thresholds[0]:
            return "Normal"
        elif score < thresholds[1]:
            return "Mild"
        elif score < thresholds[2]:
            return "Moderate"
        elif score < thresholds[3]:
            return "Severe"
        else:
            return "Extremely severe"
    
    # DASS-21 severity thresholds
    depression_severity = get_severity(depression_score, [10, 14, 21, 28])
    anxiety_severity = get_severity(anxiety_score, [8, 10, 15, 20])
    stress_severity = get_severity(stress_score, [15, 19, 26, 34])
    
    return {
        "total_score": total_score,
        "depression_score": depression_score,
        "anxiety_score": anxiety_score,
        "stress_score": stress_score,
        "depression_severity": depression_severity,
        "anxiety_severity": anxiety_severity,
        "stress_severity": stress_severity
    }
