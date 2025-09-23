💰 Financial Data Visualization Dashboard
A full-stack web application for uploading, processing, and visualizing financial data from Excel files. Built with Python Flask backend and modern HTML/CSS/JavaScript frontend.

🎯 Features
📊 Core Functionality

Excel File Upload: Drag-and-drop Excel (.xlsx/.xls) file upload
Data Processing: Automatic parsing and validation of financial data
Database Storage: Secure MySQL storage with user management
Data Visualization: Interactive charts and tables 
Responsive Design: Modern, mobile-friendly interface

🔧 Technical Features

RESTful API: Clean API endpoints for data operations
Error Handling: Comprehensive error handling and user feedback
File Validation: Excel format and data structure validation
Data Sanitization: Input validation and SQL injection prevention
Connection Pooling: Efficient database connection management

🏗️ Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │   MySQL DB      │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │◄──►│ • File Upload   │◄──►│ • Users         │
│ • Chart.js      │    │ • Data Process  │    │ • Financial     │
│ • Axios         │    │ • REST API      │    │   Records       │
└─────────────────┘    └─────────────────┘    └─────────────────┘

🚀 Quick Start
1. Clone the Repository

git clone <repository-url>
cd financial-data-visualization

2. Set Up Python Virtual Environment

python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt