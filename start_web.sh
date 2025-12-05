#!/bin/bash
# Start the SSE Validator Web Application

echo "======================================================================"
echo "SSE Programmatic Trading Report Validator - Web Interface"
echo "沪股通投资者程序化交易信息报告表验证工具 - 网页版"
echo "======================================================================"
echo ""
echo "Starting web server..."
echo "Open your browser to: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================================================"
echo ""

python3 web_validator.py
