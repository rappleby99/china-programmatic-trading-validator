# China Programmatic Trading Report Validator
## 程序化交易信息报告表验证工具

A validation tool for Shanghai Stock Exchange (SSE) and Shenzhen Stock Exchange (SZSE) programmatic trading reports, supporting both command-line and web-based validation.

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

## 🎯 Features

- ✅ **Dual Exchange Support**: Validates reports for both Shanghai (SSE) and Shenzhen (SZSE) exchanges
- ✅ **Comprehensive Field Validation**:
  - Shanghai: 42 fields
  - Shenzhen: 38 fields (includes sequence number)
- ✅ **File Naming Validation**: Enforces official file naming standards
- ✅ **Bilingual Support**: Chinese and English field names, descriptions, and error messages
- ✅ **Multiple Interfaces**:
  - Web-based interface (Flask)
  - Command-line script
- ✅ **Smart Validation**:
  - Required vs conditional fields
  - Enumerated values (with Chinese validation)
  - Multi-value fields with semicolon separation
  - Date format validation
  - Leverage ratio calculations
  - High-frequency trading detection

---

## 📋 File Naming Standards

### Required Format

Files must follow the official HKEX naming convention:

#### Shanghai Stock Exchange (SSE)
```
SH_PGTDRPT_<FIRM_ID>_<YYYYMMDD>.xlsx
```

#### Shenzhen Stock Exchange (SZSE)
```
SZ_PGTDRPT_<FIRM_ID>_<YYYYMMDD>.xlsx
```

### Format Components

| Component | Description | Format | Example |
|-----------|-------------|--------|---------|
| **Exchange Code** | SH (Shanghai) or SZ (Shenzhen) | 2 letters | `SH` or `SZ` |
| **Report Type** | Fixed identifier for programmatic trading | `PGTDRPT` | `PGTDRPT` |
| **FIRM_ID** | 5-digit broker code (with leading zeros) | `\d{5}` | `09999` |
| **Date** | Submission date (cannot be in future) | `YYYYMMDD` | `20251205` |
| **Extension** | Excel file format | `.xlsx` | `.xlsx` |

### Valid Examples
```
✓ SH_PGTDRPT_09999_20251205.xlsx
✓ SZ_PGTDRPT_12345_20251130.xlsx
✓ SH_PGTDRPT_00001_20250101.xlsx
```

### Invalid Examples
```
✗ Shanghai_Report_20251205.xlsx          (Wrong format)
✗ SH_PGTDRPT_9999_20251205.xlsx          (FIRM_ID must be 5 digits)
✗ SH_PGTDRPT_09999_2025-12-05.xlsx       (Date format incorrect)
✗ SH_PGTDRPT_09999_20301205.xlsx         (Date cannot be in future)
✗ SH_PGTDRPT_09999_20251205.xls          (Must be .xlsx)
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages
- `openpyxl` - Excel file reading/writing
- `flask` - Web framework (for web interface)
- `python-dateutil` - Date parsing

---

## 💻 Usage

### Command-Line Interface

#### Basic Validation
```bash
python3 ChinaTest.py <path-to-excel-file>
```

#### Example
```bash
python3 ChinaTest.py SH_PGTDRPT_09999_20251205.xlsx
```

#### Output
The script will:
1. Validate the file naming format
2. Detect the exchange (Shanghai or Shenzhen)
3. Validate all fields according to exchange-specific rules
4. Display errors and warnings
5. Generate a validation report

**Exit codes:**
- `0` - Validation passed (no errors)
- `1` - Validation failed (errors found)

---

### Web Interface

#### Start the Web Server

```bash
python3 web_validator.py
```

Or use the startup script:

```bash
./start_web.sh
```

#### Access the Interface

Open your browser to:
```
http://127.0.0.1:5000
```

#### Features
- Drag-and-drop file upload
- Real-time validation
- Detailed error reporting with row/column locations
- Exchange auto-detection from filename
- Field mapping reference tables (Shanghai & Shenzhen)
- Bilingual field descriptions

---

## 📊 Validation Rules

### Field Types

| Type | Description | Example |
|------|-------------|---------|
| **Text** | Free-form text | Account name, contact info |
| **Number** | Numeric values | Fund size, leverage ratio |
| **Date** | Date in YYYYMMDD format | 20251205 |
| **Enum** | Single selection from list | Report type: 首次/变更/停止使用 |
| **Multi-Enum** | Multiple selections (semicolon-separated) | Fund sources: 自有资金;募集资金 |
| **Multi-Text** | Multiple text values (semicolon-separated) | Software names |

### Required Field Categories

1. **Always Required (必填)**: Must always be filled
2. **Conditional (条件性)**: Required based on other field values
3. **Optional (选填)**: Not required

### Key Validation Rules

#### Report Type (报告类型)
- **首次** (Initial): First report or after termination
- **变更** (Change): Modify existing report
- **停止使用** (Termination): Stop trading

#### Fund Information
- Fund sources must match fund ratio breakdown
- Leverage ratio ≥100 (=100 if no leverage, >100 if leveraged)
- Leveraged funds cannot exceed total fund size

#### High-Frequency Trading
Detected when:
- **Order rate** ≥ 300 orders/second, OR
- **Daily orders** ≥ 20,000 orders/day

If high-frequency:
- Must report server location
- Must upload test report & contingency plan
- Unless exempt (QFII using order-splitting)

#### Multi-Value Fields
- Values separated by `;` (English semicolon)
- No spaces around semicolons
- Example: `自有资金;募集资金;杠杆资金`

#### Strategy Fields
- Main strategy: Only ONE value allowed
- Sub-strategy: Maximum TWO values allowed

---

## 📁 Project Structure

```
ChinaTest/
├── ChinaTest.py                    # Core validation logic (command-line)
├── web_validator.py                # Flask web application
├── start_web.sh                    # Web server startup script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── HFT_Requirements.md             # HFT testing/contingency requirements
├── HFT_Requirements_CSRC_Addendum.md # CSRC-level additional requirements
├── templates/
│   └── index.html                  # Web interface HTML
└── Files/                          # Test files and examples
```

---

## 🔍 Field Specifications

### Shanghai Stock Exchange (SSE) - 42 Fields

1. 联交所参与者名称 (Exchange Participant Name)
2. 经纪商代码 (Broker Code) - **Must be exactly 5 digits**
3. 账户名称 (Account Name)
4. 证件号码 (ID Number)
5. 产品编码 (Product Code) - Optional
6. 券商客户编码 (Client Code/BCAN) - **Unique identifier**
7. 产品管理机构名称 (Product Manager Name)
8. 报告类型 (Report Type) - 首次/变更/停止使用
9. 报告日期 (Report Date) - YYYYMMDD format
10. 是否选取一家联交所参与者集中填报资金信息 (Consolidated Fund Reporting)
... (continues through field 42)

**Key Fields:**
- **Field 32**: 账户最高申报速率 (Max Order Rate) - Triggers HFT requirements
- **Field 33**: 账户单日最高申报笔数 (Max Daily Orders) - Triggers HFT requirements
- **Field 36**: 高频交易系统服务器所在地 (HFT Server Location)
- **Field 41**: 是否上传测试报告及应急方案 (Upload Test Report)
- **Field 42**: 合格境外投资者编码 (QFII Code)

### Shenzhen Stock Exchange (SZSE) - 38 Fields

Similar to Shanghai with these differences:
- **Field 1**: 序号 (Sequence Number) - **Shenzhen-specific**
- Fewer total fields (38 vs 42)
- Some field descriptions differ slightly

Full field specifications available in the web interface under "Field Mapping" tabs.

---

## 🛠️ Development

### About This Project

This tool was created as an AI experiment developed using **Claude Sonnet 4.5** by Anthropic. The primary objective was to:

1. Extract Chinese specification documents from:
   - Shanghai Stock Exchange programmatic trading guidelines
   - Shenzhen Stock Exchange programmatic trading guidelines
   - CSRC regulatory requirements
   - HKEX reporting interface specifications

2. Convert specifications into unified English validation rules

3. Implement bilingual validation logic supporting both Chinese values (as required by exchanges) and English documentation

### Technology Stack

- **Python 3.9+**: Core validation logic
- **openpyxl**: Excel file processing
- **Flask**: Web framework for browser-based validation
- **HTML/CSS/JavaScript**: Web interface (no external frameworks)

### Validation Approach

1. **File naming validation**: Regex pattern matching against official format
2. **Exchange detection**: Auto-detect SSE or SZSE from filename prefix
3. **Field-by-field validation**: Rule-based validation against exchange specifications
4. **Conditional logic**: Smart validation based on field interdependencies
5. **Bilingual error reporting**: Errors show both Chinese and English field names

---

## 📝 Example Validation Output

### Command-Line Output
```
Validating file: SH_PGTDRPT_09999_20251205.xlsx
Exchange detected: SHANGHAI
Firm ID: 09999
Submission Date: 2025-12-05

=== Validation Results ===

[ERROR] Row 2, Column 8 '报告类型' (report_type): Invalid value for report_type. Must be one of: 首次, 变更, 停止使用 (value: 'Initial')
[WARNING] Row 2, Column 11 '账户资金规模（人民币，万元）' (fund_size): Fund size should be numeric with max 2 decimals (value: '1000.123')

=== Summary ===
Total Rows: 5
Valid Rows: 4
Invalid Rows: 1
Total Errors: 1
Total Warnings: 1

Validation FAILED
```

### Web Interface Output
- Visual display with error highlighting
- Row-by-row validation status
- Filterable error list
- Field mapping reference tables
- Downloadable validation report

---

## ❓ Common Issues

### Issue: "Invalid filename format"
**Solution**: Ensure filename follows exact pattern: `SH_PGTDRPT_09999_20251205.xlsx`

### Issue: "Invalid value for report_type. Must be one of: 首次, 变更, 停止使用"
**Solution**: Use Chinese characters for enumerated values, not English translations

### Issue: "Broker code must be exactly 5 characters"
**Solution**: Ensure broker code has leading zeros (e.g., `09999` not `9999`)

### Issue: "Submission date cannot be in the future"
**Solution**: Use today's date or earlier in the filename

### Issue: "Fund sources must match fund ratio breakdown"
**Solution**: Ensure all sources in field 12 have corresponding percentages in field 14

### Issue: "Leveraged funds cannot exceed total fund size"
**Solution**: Field 15 (leveraged funds) must be ≤ Field 11 (total fund size)

---

## 📚 Additional Documentation

- **HFT_Requirements.md**: Comprehensive guide to high-frequency trading test report and contingency plan requirements
- **HFT_Requirements_CSRC_Addendum.md**: Additional CSRC-level requirements for testing and emergency response

---

## 🤝 Contributing

This is an experimental project created for educational purposes. While contributions are welcome, please note:

- This tool is not officially maintained by any regulatory authority
- Changes should align with official HKEX/SSE/SZSE specifications
- All validation logic must support both Chinese and English documentation
- Test any changes against official specification documents

---

## 📄 License

This project is provided as-is for educational and informational purposes only. See disclaimer above.

---

## 🔗 Official Resources

- **HKEX Northbound Program Trading**: https://www.hkex.com.hk/Mutual-Market/Stock-Connect/Reference-Materials/Northbound-Program-Trading-Reporting?sc_lang=en
- **Shanghai Stock Exchange**: http://www.sse.com.cn
- **Shenzhen Stock Exchange**: http://www.szse.cn
- **China Securities Regulatory Commission**: http://www.csrc.gov.cn

---

**Developed with**: Claude Sonnet 4.5 by Anthropic
**Last Updated**: December 2025
**Version**: 1.0
