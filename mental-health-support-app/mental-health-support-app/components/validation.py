"""
Validation Rules cho Mental Health Support Application
Đảm bảo tính chính xác và an toàn của ứng dụng trong production
"""

from typing import Dict, List, Any, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MentalHealthAppValidator:
    """Validator chuyên biệt cho ứng dụng sức khỏe tâm lý"""
    
    def __init__(self):
        self.required_subscales = ["Depression", "Anxiety", "Stress"]
        self.expected_item_count = 21
        self.expected_options_count = 4
        self.valid_option_values = [0, 1, 2, 3]
        
    def validate_questionnaire_config(self, cfg: Dict) -> bool:
        """Validate cấu hình questionnaire"""
        errors = []
        
        # Kiểm tra các field bắt buộc
        required_fields = ["items", "options", "severity_thresholds"]
        for field in required_fields:
            if field not in cfg:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            logger.error(f"Config validation failed: {errors}")
            return False
            
        # Validate items
        if not self._validate_items(cfg["items"], errors):
            logger.error(f"Items validation failed: {errors}")
            return False
            
        # Validate options
        if not self._validate_options(cfg["options"], errors):
            logger.error(f"Options validation failed: {errors}")
            return False
            
        # Validate severity thresholds
        if not self._validate_severity_thresholds(cfg["severity_thresholds"], errors):
            logger.error(f"Severity thresholds validation failed: {errors}")
            return False
            
        logger.info("✅ Questionnaire configuration is valid")
        return True
    
    def _validate_items(self, items: List[Dict], errors: List[str]) -> bool:
        """Validate danh sách câu hỏi"""
        if len(items) != self.expected_item_count:
            errors.append(f"Expected {self.expected_item_count} items, got {len(items)}")
            return False
            
        item_ids = []
        subscale_counts = {s: 0 for s in self.required_subscales}
        
        for i, item in enumerate(items):
            # Kiểm tra required fields
            required_item_fields = ["id", "text", "subscale"]
            for field in required_item_fields:
                if field not in item:
                    errors.append(f"Item {i}: missing field '{field}'")
                    
            # Kiểm tra unique ID
            if "id" in item:
                if item["id"] in item_ids:
                    errors.append(f"Duplicate item ID: {item['id']}")
                item_ids.append(item["id"])
                
            # Kiểm tra valid subscale
            if "subscale" in item:
                if item["subscale"] not in self.required_subscales:
                    errors.append(f"Invalid subscale: {item['subscale']}")
                else:
                    subscale_counts[item["subscale"]] += 1
                    
        # Kiểm tra distribution across subscales (DASS-21: 7 per subscale)
        for subscale, count in subscale_counts.items():
            if count != 7:
                errors.append(f"Subscale {subscale}: expected 7 items, got {count}")
                
        return len(errors) == 0
    
    def _validate_options(self, options: List[Dict], errors: List[str]) -> bool:
        """Validate các tùy chọn trả lời"""
        if len(options) != self.expected_options_count:
            errors.append(f"Expected {self.expected_options_count} options, got {len(options)}")
            return False
            
        values = []
        for i, option in enumerate(options):
            if "value" not in option:
                errors.append(f"Option {i}: missing 'value' field")
            if "label" not in option:
                errors.append(f"Option {i}: missing 'label' field")
                
            if "value" in option:
                values.append(option["value"])
                
        if sorted(values) != self.valid_option_values:
            errors.append(f"Invalid option values: expected {self.valid_option_values}, got {sorted(values)}")
            
        return len(errors) == 0
    
    def _validate_severity_thresholds(self, thresholds: Dict, errors: List[str]) -> bool:
        """Validate ngưỡng phân loại mức độ nghiêm trọng"""
        expected_levels = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
        
        for subscale in self.required_subscales:
            if subscale not in thresholds:
                errors.append(f"Missing severity thresholds for {subscale}")
                continue
                
            subscale_thresholds = thresholds[subscale]
            
            # Kiểm tra tất cả levels có đủ không
            for level in expected_levels:
                if level not in subscale_thresholds:
                    errors.append(f"{subscale}: missing {level} threshold")
                    continue
                    
                threshold = subscale_thresholds[level]
                if not isinstance(threshold, list) or len(threshold) != 2:
                    errors.append(f"{subscale}.{level}: threshold must be [min, max]")
                    continue
                    
                if threshold[0] > threshold[1]:
                    errors.append(f"{subscale}.{level}: min > max in threshold")
                    
            # Kiểm tra thresholds không overlap
            if not self._validate_threshold_ranges(subscale_thresholds, errors, subscale):
                continue
                
        return len(errors) == 0
    
    def _validate_threshold_ranges(self, thresholds: Dict, errors: List[str], subscale: str) -> bool:
        """Validate các range thresholds không overlap"""
        levels = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
        ranges = []
        
        for level in levels:
            if level in thresholds:
                ranges.append((thresholds[level][0], thresholds[level][1], level))
        
        # Sort by start value
        ranges.sort(key=lambda x: x[0])
        
        # Check for gaps or overlaps
        for i in range(len(ranges) - 1):
            current_end = ranges[i][1]
            next_start = ranges[i + 1][0]
            
            if current_end + 1 != next_start:
                errors.append(f"{subscale}: gap or overlap between {ranges[i][2]} and {ranges[i+1][2]}")
                return False
                
        return True
    
    def validate_user_answers(self, answers: Dict[int, int], cfg: Dict) -> bool:
        """Validate câu trả lời của người dùng"""
        errors = []
        
        # Kiểm tra số lượng câu trả lời
        expected_count = len(cfg["items"])
        if len(answers) != expected_count:
            errors.append(f"Expected {expected_count} answers, got {len(answers)}")
            
        # Kiểm tra tất cả item IDs có trong answers
        item_ids = {item["id"] for item in cfg["items"]}
        for item_id in item_ids:
            if item_id not in answers:
                errors.append(f"Missing answer for item {item_id}")
                
        # Kiểm tra giá trị answers hợp lệ
        for item_id, answer in answers.items():
            if answer not in self.valid_option_values:
                errors.append(f"Invalid answer value for item {item_id}: {answer}")
                
        if errors:
            logger.error(f"Answer validation failed: {errors}")
            return False
            
        logger.info("✅ User answers are valid")
        return True
    
    def validate_computed_scores(self, scores: Dict, cfg: Dict) -> bool:
        """Validate điểm số được tính toán"""
        errors = []
        
        # Kiểm tra tất cả subscales có scores
        for subscale in self.required_subscales:
            if subscale not in scores:
                errors.append(f"Missing score for {subscale}")
                continue
                
            score_obj = scores[subscale]
            
            # Kiểm tra có đủ attributes
            required_attrs = ["raw", "adjusted", "severity"]
            for attr in required_attrs:
                if not hasattr(score_obj, attr):
                    errors.append(f"{subscale}: missing {attr} attribute")
                    
            # Kiểm tra logic adjusted = raw * 2
            if hasattr(score_obj, "raw") and hasattr(score_obj, "adjusted"):
                if score_obj.adjusted != score_obj.raw * 2:
                    errors.append(f"{subscale}: adjusted score calculation error")
                    
            # Kiểm tra severity hợp lệ
            if hasattr(score_obj, "severity"):
                valid_severities = list(cfg["severity_thresholds"][subscale].keys())
                if score_obj.severity not in valid_severities:
                    errors.append(f"{subscale}: invalid severity '{score_obj.severity}'")
                    
        if errors:
            logger.error(f"Score validation failed: {errors}")
            return False
            
        logger.info("✅ Computed scores are valid")
        return True

# Global validator instance
validator = MentalHealthAppValidator()

def validate_app_state(cfg: Dict, answers: Optional[Dict] = None, scores: Optional[Dict] = None) -> bool:
    """Validate toàn bộ state của ứng dụng"""
    logger.info("🔍 Starting comprehensive app state validation...")
    
    # Validate config
    if not validator.validate_questionnaire_config(cfg):
        return False
        
    # Validate answers if provided
    if answers is not None:
        if not validator.validate_user_answers(answers, cfg):
            return False
            
    # Validate scores if provided  
    if scores is not None:
        if not validator.validate_computed_scores(scores, cfg):
            return False
            
    logger.info("🎉 All validations passed - App state is SAFE")
    return True
