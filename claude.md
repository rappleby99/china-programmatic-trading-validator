# Claude Context: China Programmatic Trading Report Validator

## Project Overview

Validation tool for Shanghai (SSE) and Shenzhen (SZSE) Stock Exchange programmatic trading reports. Validates Excel files against official Chinese specifications with bilingual error reporting.

**Live Demo**: https://china-programmatic-trading-validator-production.up.railway.app/

## Key Files

- **ChinaTest.py** - Core validation engine with all field rules
- **web_validator.py** - Flask web application wrapper
- **templates/index.html** - Single-page web interface with field reference tables
- **requirements.txt** - Python dependencies (openpyxl, Flask, gunicorn)
- **Procfile** - Railway deployment configuration

## Architecture

### File Naming Enforcement
- Pattern: `(SH|SZ)_PGTDRPT_(\d{5})_(\d{8})\.xlsx`
- Auto-detects exchange (Shanghai vs Shenzhen) from filename prefix
- Validates broker code (5 digits) and submission date (not future)

### Validation Logic
- **Shanghai**: 42 fields (lines 227-582 in ChinaTest.py)
- **Shenzhen**: 38 fields (lines 585-909 in ChinaTest.py)
- Field types: Text, Number, Date, Enum, Multi-Enum, Multi-Text
- Conditional requirements based on report type ('首次', '变更', '停止使用')
- Smart validation: fund ratios, leverage calculations, HFT detection

### Important Patterns
- All enumerated values use **Chinese characters** (e.g., '首次', '是', '自有资金')
- Conditional logic in **English** (e.g., `"Required if report_type in ['Initial','Update']"`)
- Bilingual error messages: `field_name_cn` + `field_name_en`
- Multi-value fields use semicolon separator (e.g., '自有资金;募集资金')

## Field Specifications

Field definitions contain:
- `num`: Field number/position
- `cn`: Chinese field name
- `en`: English field name
- `descCn`: Chinese description (exact from specifications)
- `descEn`: English translation
- `type`: Text/Number/Date/Enum/Multi-Enum/Multi-Text
- `len`: Max length
- `req`: "必填" (Required), "条件性" (Conditional), "选填" (Optional)
- `cond`: JavaScript-style conditional logic
- `values`: Enumerated options (if applicable)

## High-Frequency Trading (HFT) Rules

Triggered when:
- Order rate ≥ 300 orders/second, OR
- Daily orders ≥ 20,000 orders/day

Requirements:
- Server location (field 36)
- Test report upload (field 41)
- Exemption: QFII with order-splitting only

## Deployment

- **Local**: `python3 web_validator.py` → http://127.0.0.1:5000
- **Production**: Railway with gunicorn via Procfile
- **Branch Protection**: Enabled on `main` (no force-push, no deletion)

## Development Notes

1. **Specification Sources**: Chinese PDFs/DOCXs from SSE, SZSE, CSRC, HKEX
2. **Created With**: Claude Sonnet 4.5 (AI experiment)
3. **No External JS Frameworks**: Vanilla JavaScript in index.html
4. **Security**: temp files auto-deleted, no data persistence
5. **Disclaimers**: Present in ChinaTest.py header, index.html footer, README.md

## Common Tasks

**Add new field validation**: Update field definitions in ChinaTest.py (lines 227+ for Shanghai, 585+ for Shenzhen)

**Modify conditional logic**: Update `cond` property in field definition using English logic

**Update web UI field tables**: Modify JavaScript arrays in index.html (lines 1237-1317 for Shanghai, 1320-1439 for Shenzhen)

**Change file naming pattern**: Update regex in `detect_exchange()` method (ChinaTest.py line 146)
