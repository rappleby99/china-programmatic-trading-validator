# SSE Programmatic Trading Report Web Validator

Modern web interface for validating SSE (Shanghai Stock Exchange) programmatic trading reports.

## Features

- 🌐 **Modern Web Interface** - Clean, responsive design
- 🔒 **Secure** - Files processed in memory, NOT saved to disk
- ⚡ **Fast** - Instant validation results
- 📊 **Detailed Reports** - Summary statistics and error details
- 🎯 **User-Friendly** - Drag-and-drop file upload
- ⚠️ **Security Warnings** - Clear disclaimers about test-only usage

## Security Features

1. **No Data Persistence**: Uploaded files are processed using Python's `tempfile.NamedTemporaryFile` with `delete=True`, ensuring automatic deletion
2. **Memory Processing**: Files are validated in memory and immediately discarded
3. **File Size Limit**: Maximum 16MB upload size
4. **Format Validation**: Only `.xlsx` files accepted
5. **Clear Warnings**: Prominent security notices on the UI

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have the validation script:
   - `chinatest.py` must be in the same directory as `web_validator.py`

## Running the Web Application

### Development Mode

```bash
python web_validator.py
```

Then open your browser to: `http://127.0.0.1:5000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_validator:app
```

## Usage

1. Open the web interface in your browser
2. Read the security warnings
3. Upload an Excel file (`.xlsx`)
   - Click to browse OR drag-and-drop
4. Click "Validate File"
5. View results:
   - Summary statistics
   - Row-by-row validation status
   - Detailed error messages
   - Full text report

## Command-Line Alternative

For batch processing or integration, use the standalone script:

```bash
python chinatest.py your_file.xlsx
```

## File Structure

```
ChinaTest/
├── chinatest.py           # Core validation engine (standalone)
├── web_validator.py       # Flask web application
├── templates/
│   └── index.html        # Web interface
├── requirements.txt       # Python dependencies
├── SSETemplate.xlsx       # Official SSE template
└── README_WEB.md         # This file
```

## Security Notice

**⚠️ IMPORTANT:**
- This tool is for **TESTING PURPOSES ONLY**
- **DO NOT** upload files containing real client data
- **DO NOT** use in production with sensitive information
- Use sanitized or test data only
- Uploaded files are automatically deleted after validation

## Technical Details

### Backend (Flask)

- **Framework**: Flask 3.0.0
- **File Handling**: `tempfile.NamedTemporaryFile` with auto-delete
- **Validation**: Imports from `chinatest.py`
- **API Endpoint**: `/validate` (POST)
- **Response**: JSON with structured validation results

### Frontend (HTML/CSS/JavaScript)

- **Design**: Modern gradient design with responsive layout
- **Upload**: Drag-and-drop + click-to-browse
- **Real-time**: AJAX file upload and validation
- **Display**: Color-coded results with icons
- **Mobile**: Responsive design for all devices

### Validation Features

All validations from the standalone script:
- ✓ Field length validation
- ✓ Required field validation
- ✓ Conditional requirements
- ✓ Enumerated values
- ✓ Multi-value fields
- ✓ Format validation (dates, codes, numbers)
- ✓ Business rules (leverage, ratios, high-frequency)
- ✓ Report date future validation
- ✓ QFII code conditional requirement
- ✓ Futures account multi-value support

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

## Troubleshooting

**Port already in use:**
```bash
python web_validator.py
# Change port in web_validator.py: app.run(port=5001)
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**File upload fails:**
- Check file size (max 16MB)
- Ensure file is `.xlsx` format
- Check browser console for errors

## License

For internal testing use only.
