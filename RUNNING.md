# Running Smart Inventory Scanner

This guide provides step-by-step instructions for running the Smart Inventory Scanner application, both for first-time setup and subsequent runs.

## First-Time Setup

1. **Prerequisites**
   - Python 3.8 or higher
   - Node.js 14 or higher
   - Tesseract OCR installed:
     - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
     - Linux: `sudo apt-get install tesseract-ocr`
     - Mac: `brew install tesseract`

2. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/smart-inventory-scanner.git
   cd smart-inventory-scanner
   ```

3. **Create and Activate Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

4. **Run Setup Script**
   ```bash
   python setup.py
   ```
   This will:
   - Install all required Python packages
   - Install frontend dependencies
   - Set up the database
   - Create an admin user
   - Configure the application

5. **Start the Application**
   ```bash
   python main.py --mode development
   ```

6. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

7. **Login Credentials**
   - Email: admin@example.com
   - Password: admin123
   - **Important**: Change these credentials after first login!

## Running After Setup

1. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

2. **Start the Application**
   ```bash
   python main.py --mode development
   ```

## Troubleshooting

### Common Issues and Solutions

1. **Port Already in Use**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F

   # Linux/Mac
   lsof -i :8000
   kill -9 <PID>
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   cd frontend
   npm install
   cd ..
   ```

3. **Database Issues**
   ```bash
   # Remove existing database
   rm inventory.db
   # Reinitialize database
   python -m app.db_init
   ```

4. **Frontend Build Issues**
   ```bash
   cd frontend
   npm run build
   cd ..
   ```

### Development Mode Options

```bash
# Custom host and ports
python main.py --mode development --host 127.0.0.1 --backend-port 8000 --frontend-port 3000

# Production mode
python main.py --mode production
```

## Stopping the Application

1. Press `Ctrl+C` in the terminal where the application is running
2. Wait for both frontend and backend servers to stop
3. Deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Database Management

### SQLite (Development)
- Database file: `inventory.db`
- Backup: Simply copy the database file
- Reset: Delete the file and run `python -m app.db_init`

### PostgreSQL (Production)
1. Install PostgreSQL
2. Create database and user
3. Update `.env` file with connection string
4. Run database initialization

## Security Notes

1. Change default admin credentials
2. Use strong passwords
3. Keep your `.env` file secure
4. Regularly backup your database
5. Update dependencies regularly

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review the error messages
3. Check the application logs
4. Create an issue on GitHub 