# China Programmatic Trading Report Validator
## 程序化交易信息报告表验证工具

A validation tool for Shanghai Stock Exchange (SSE) and Shenzhen Stock Exchange (SZSE) programmatic trading reports, supporting both command-line and web-based validation.

## 🌐 Live Demo

**Try the web validator here**: [https://china-programmatic-trading-validator-production.up.railway.app/](https://china-programmatic-trading-validator-production.up.railway.app/)

---

## ⚠️ Disclaimer

**This tool is provided "as is" for informational and educational purposes only.**

- **No Guarantee of Accuracy**: While care has been taken in developing this validator, the author makes no representations or warranties regarding the accuracy, completeness, or reliability of the validation logic.

- **No Affiliation**: This tool is **not affiliated with, endorsed by, or connected to** the Shanghai Stock Exchange, Shenzhen Stock Exchange, Hong Kong Stock Exchange, China Securities Regulatory Commission, or any other regulatory authority or exchange.

- **Not for Compliance Testing**: This tool should **not be relied upon** as a mechanism for testing compliance with China/Hong Kong programmatic trading reporting requirements.

- **Official Testing Required**: Users must engage in official testing with the **Hong Kong Stock Exchange** and relevant regulatory authorities to ensure compliance.

- **No Liability**: The author accepts no liability for any errors, omissions, or consequences arising from the use of this tool.

### For Official Guidance
Please refer to:
- **Hong Kong Stock Exchange (HKEX)**: [Northbound Program Trading Reporting](https://www.hkex.com.hk/Mutual-Market/Stock-Connect/Reference-Materials/Northbound-Program-Trading-Reporting?sc_lang=en)
- Shanghai Stock Exchange (SSE)
- Shenzhen Stock Exchange (SZSE)
- China Securities Regulatory Commission (CSRC)

---

## Features

- **Dual Exchange Support**: Validates reports for both Shanghai (SSE) and Shenzhen (SZSE) exchanges
- **Comprehensive Field Validation**: Shanghai (42 fields), Shenzhen (38 fields)
- **File Naming Validation**: Enforces official HKEX naming standards
- **Bilingual Support**: Chinese and English field names and error messages
- **Multiple Interfaces**: Web-based (Flask) and command-line

---

## File Naming Standards

Files must follow the official HKEX naming convention:

**Shanghai**: `SH_PGTDRPT_<FIRM_ID>_<YYYYMMDD>.xlsx`
**Shenzhen**: `SZ_PGTDRPT_<FIRM_ID>_<YYYYMMDD>.xlsx`

Where:
- **FIRM_ID**: 5-digit broker code with leading zeros (e.g., `09999`)
- **YYYYMMDD**: Submission date, cannot be in future (e.g., `20251205`)

**Examples**:
```
✓ SH_PGTDRPT_09999_20251205.xlsx
✓ SZ_PGTDRPT_12345_20251130.xlsx
✗ SH_PGTDRPT_9999_20251205.xlsx     (Missing leading zero)
✗ SH_PGTDRPT_09999_20301205.xlsx    (Future date)
```

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages**: openpyxl, flask, python-dateutil

---

## Usage

### Command-Line Interface

```bash
python3 ChinaTest.py <path-to-excel-file>
```

**Example**:
```bash
python3 ChinaTest.py SH_PGTDRPT_09999_20251205.xlsx
```

**Exit codes**:
- `0` - Validation passed
- `1` - Validation failed

### Web Interface

Start the web server:

```bash
python3 web_validator.py
```

Or use the startup script:

```bash
./start_web.sh
```

Then open your browser to: `http://127.0.0.1:5000`

**Features**:
- Drag-and-drop file upload
- Real-time validation
- Detailed error reporting with row/column locations
- Field mapping reference tables

---

## Project Structure

```
china-programmatic-trading-validator/
├── .gitignore                      # Git ignore rules
├── ChinaTest.py                    # Core validation logic (command-line)
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── start_web.sh                    # Web server startup script
├── templates/
│   └── index.html                  # Web interface HTML
└── web_validator.py                # Flask web application
```

---

## About This Project

This tool was created as an AI experiment developed using **Claude Sonnet 4.5** by Anthropic. The objective was to extract Chinese specification documents from Shanghai/Shenzhen Stock Exchanges and CSRC, convert them into unified English validation rules, and implement bilingual validation logic.

**Technology Stack**:
- **Python 3.9+**: Core validation logic
- **openpyxl**: Excel file processing
- **Flask**: Web framework
- **HTML/CSS/JavaScript**: Web interface (no external frameworks)

---

**Developed with**: Claude Sonnet 4.5 by Anthropic
**Last Updated**: December 2025
**Version**: 1.0
