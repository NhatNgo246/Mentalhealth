import json, os

class QuestionnaireManager:
    """Manages all questionnaire operations"""
    
    def __init__(self):
        self.questionnaires = {
            'DASS-21': self.load_dass21_enhanced,
            'PHQ-9': self.load_phq9_enhanced,
            'GAD-7': self.load_gad7_enhanced,
            'EPDS': self.load_epds_enhanced,
            'PSS-10': self.load_pss10_enhanced
        }
    
    def get_questionnaire(self, name):
        """Get questionnaire by name"""
        if name in self.questionnaires:
            return self.questionnaires[name]()
        else:
            raise ValueError(f"Questionnaire {name} not found")
    
    def load_questionnaire(self, name):
        """Alias for get_questionnaire for backward compatibility"""
        return self.get_questionnaire(name)
    
    def load_dass21_enhanced(self):
        return load_dass21_enhanced_vi()
    
    def load_phq9_enhanced(self):
        return load_phq9_enhanced_vi()
    
    def load_gad7_enhanced(self):
        return load_gad7_enhanced_vi()
    
    def load_epds_enhanced(self):
        return load_epds_enhanced_vi()
    
    def load_pss10_enhanced(self):
        return load_pss10_enhanced_vi()
    
    def load_dass21_vi(self):
        return load_dass21_vi()
    
    def load_phq9_vi(self):
        return load_phq9_vi()
    
    def load_gad7_vi(self):
        return load_gad7_vi()
    
    def load_epds_vi(self):
        return load_epds_vi()
    
    def load_pss10_vi(self):
        return load_pss10_vi()

def load_questionnaire(questionnaire_type):
    """Load questionnaire by type - compatibility function"""
    manager = QuestionnaireManager()
    return manager.get_questionnaire(questionnaire_type)

def load_dass21_vi():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "dass21_vi.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_dass21_enhanced_vi():
    """Load enhanced DASS-21 questionnaire with improved Vietnamese context"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "dass21_enhanced_vi.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to original if enhanced not found
        return load_dass21_vi()

def load_phq9_enhanced_vi():
    """Load enhanced PHQ-9 questionnaire with improved Vietnamese context"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "phq9_enhanced_vi.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to original if enhanced not found
        return load_phq9_vi()

def load_phq9_enhanced_vi():
    """Load enhanced PHQ-9 questionnaire with improved Vietnamese context"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "phq9_enhanced_vi.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to original if enhanced not found
        return load_phq9_vi()

def load_phq9_vi():
    """Load original PHQ-9 questionnaire"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "phq9_vi.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_gad7_enhanced_vi():
    """Load enhanced GAD-7 questionnaire with improved Vietnamese context"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "gad7_enhanced_vi.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to original if enhanced not found
        return load_gad7_vi()

def load_gad7_vi():
    """Load original GAD-7 questionnaire"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "gad7_config.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_epds_enhanced_vi():
    """Load enhanced EPDS questionnaire with improved Vietnamese context"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "epds_enhanced_vi.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to original if enhanced not found
        return load_epds_vi()

def load_epds_vi():
    """Load original EPDS questionnaire"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "epds_config.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_pss10_enhanced_vi():
    """Load enhanced PSS-10 questionnaire with improved Vietnamese context"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "pss10_enhanced_vi.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to original if enhanced not found
        return load_pss10_vi()

def load_pss10_vi():
    """Load original PSS-10 questionnaire"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "pss10_config.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
