"""
SSE Programmatic Trading Report Web Validator
Flask web application for validating Excel files
"""
from flask import Flask, render_template, request, jsonify
import tempfile
import os
from pathlib import Path
from ChinaTest import SSEValidator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate_file():
    """Validate uploaded Excel file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Only Excel files (.xlsx) are supported'}), 400

    # Create temporary file (automatically deleted after use)
    with tempfile.NamedTemporaryFile(delete=True, suffix='.xlsx') as tmp_file:
        try:
            # Save uploaded file to temporary location
            file.save(tmp_file.name)

            # Validate the file (pass original filename for exchange detection)
            validator = SSEValidator()
            is_valid, errors = validator.validate_file(tmp_file.name, original_filename=file.filename)

            # Generate report
            report = validator.generate_report()

            # Prepare response with structured data
            response = {
                'is_valid': is_valid,
                'report': report,
                'exchange_type': validator.exchange_type,  # Include detected exchange type
                'firm_id': validator.firm_id,  # Include broker code from filename
                'submission_date': validator.submission_date.strftime('%Y%m%d') if validator.submission_date else None,
                'summary': {
                    'total_rows': len(validator.row_results),
                    'valid_rows': len([r for r in validator.row_results if r.is_valid]),
                    'invalid_rows': len([r for r in validator.row_results if not r.is_valid]),
                    'total_errors': len([e for e in validator.errors if e.severity.value == 'ERROR']),
                    'total_warnings': len([e for e in validator.errors if e.severity.value == 'WARNING'])
                },
                'row_results': [
                    {
                        'row_num': r.row_num,
                        'account_name': r.account_name,
                        'client_code': r.client_code,
                        'is_valid': r.is_valid,
                        'error_count': r.error_count,
                        'warning_count': r.warning_count
                    }
                    for r in validator.row_results
                ],
                'errors': [
                    {
                        'row_num': e.row_num,
                        'field_name_cn': e.field_name_cn,
                        'field_name_en': e.field_name_en,
                        'field_col': e.field_col,
                        'message': e.message,
                        'value': e.field_value,
                        'severity': e.severity.value,
                        'account_name': e.account_name,
                        'client_code': e.client_code
                    }
                    for e in validator.errors
                ]
            }

            return jsonify(response)

        except Exception as e:
            return jsonify({'error': f'Validation error: {str(e)}'}), 500

        # Temporary file is automatically deleted when exiting the 'with' block
        # No uploaded data is saved to disk

@app.route('/download-template')
def download_template():
    """Information about downloading the template"""
    return jsonify({
        'message': 'Please download the template from the official SSE website',
        'template_file': 'SSETemplate.xlsx'
    })

if __name__ == '__main__':
    # Run in debug mode for development
    # For production, use a proper WSGI server like gunicorn
    app.run(debug=True, host='127.0.0.1', port=5000)
