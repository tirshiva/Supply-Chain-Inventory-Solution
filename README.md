# Smart Inventory Scanner

An intelligent inventory management system that uses OCR technology to automatically update inventory records from bill images.

## Features

- OCR-based bill processing
- Automatic inventory updates
- User authentication and authorization
- Real-time inventory tracking
- Bill history and search
- Low stock alerts
- Business analytics dashboard

## Tech Stack

- Backend: Python with FastAPI
- Frontend: React with Material-UI
- Database: SQLite (development) / PostgreSQL (production)
- OCR: Tesseract
- Authentication: JWT

## Quick Start

For detailed setup and running instructions, please refer to [RUNNING.md](RUNNING.md).

### Basic Setup

1. Clone the repository
2. Create and activate virtual environment
3. Run setup script: `python setup.py`
4. Start the application: `python main.py --mode development`

## Project Structure

```
smart-inventory-scanner/
├── app/                    # Backend application
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── frontend/              # React frontend
│   ├── public/           # Static files
│   └── src/              # Source code
├── tests/                 # Test files
├── main.py               # Application entry point
├── setup.py              # Setup script
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## API Documentation

Once the application is running, visit:
- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For detailed running instructions and troubleshooting, please refer to [RUNNING.md](RUNNING.md).