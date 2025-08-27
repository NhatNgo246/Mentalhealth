# Mental Health Support App - Logo Integration

## 📝 Logo Usage Guide

### Logo Files
- **Main Logo**: `assets/logo.png` - Primary logo file for the application
- **Source**: Copied from `/workspaces/Mentalhealth/logo.png`

### Implementation

#### 1. Page Configuration
```python
st.set_page_config(
    page_title="Mental Health Support App",
    page_icon="assets/logo.png",  # Logo as browser tab icon
    layout="wide"
)
```

#### 2. Display Logo Function
```python
from components.ui import display_logo

# Centered logo with custom width
display_logo(width=150, centered=True)

# Left-aligned logo
display_logo(width=80, centered=False)
```

#### 3. Usage Examples

**Hero Section (Main Page):**
```python
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    display_logo(width=150, centered=True)
```

**Header (All Pages):**
```python
def app_header():
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        display_logo(width=80, centered=False)
```

### Features
- ✅ **Fallback Support**: Automatically shows 🧠 emoji if logo fails to load
- ✅ **Responsive**: Adjustable width parameter
- ✅ **Consistent**: Same styling across all pages
- ✅ **Error Handling**: Graceful degradation if logo file missing

### Logo Placement
1. **Browser Tab**: Page icon in browser tab
2. **App Header**: Small logo in header section
3. **Hero Section**: Large centered logo on main page
4. **Page Headers**: Consistent logo across all pages

### Styling Notes
- Logo width is adjustable via `width` parameter
- Centered placement uses column layout for responsiveness
- Fallback emoji scales with width (`width//20` rem)
- No background or borders - transparent PNG recommended

### Maintenance
- Update logo: Replace `assets/logo.png` 
- Modify size: Adjust `width` parameter in function calls
- Change fallback: Update emoji in `display_logo()` function
