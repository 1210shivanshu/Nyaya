# Nyaya

Nyaya is a Python-based project focused on leveraging AI (via the Groq api) for document intelligence, summarization, and chatbot capabilities.

## Features

- Chatbot integration using Groq api  
- Document Intelligence: Summarization, parsing, and analysis  
- Modular structure for easy extensibility  
- Secure secrets handling via environment variables  
- OCR capabilities with Tesseract integration
- Client-server architecture with Streamlit frontend

## Installation

### Prerequisites

- Python 3.7 or higher
- Tesseract OCR (required for document processing)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ShashankSingh614/Nyaya.git
cd Nyaya
```

### Step 2: Set up Virtual Environment (Recommended)

```bash
python -m venv venv

# On Linux/macOS
source venv/bin/activate  

# On Windows
venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Tesseract OCR

Download and install Tesseract OCR for Windows (64-bit):
- Download `tesseract-ocr-w64-setup-5.5.0.20241111.exe`
- Run the installer and follow the installation instructions
- Ensure Tesseract is added to your system PATH

For other operating systems:
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

## Configuration

### Get Your Groq api Key

1. Visit [Groq Console](https://console.groq.com)
2. Sign up for a free account or log in
3. Navigate to api Keys section
4. Generate a new api key
5. Copy the generated key

### Setup Environment Variables

1. Create a `.env` file in the root directory of the project
2. Add your personal Groq api key:

```env
groq_api_key=your-groq-api-key-goes-here
```
3. Ensure `.env` is listed in `.gitignore` to prevent committing secrets

## Project Structure

```
Nyaya/
│   .env
│   .gitignore
│   README.md
│   requirements.txt
│   step.txt
│   
├───api
│   ├───chatbot
│   │   │   app.py
│   │   │   nyayaFunction.py
│   │   │   requirements.txt
│   │   │   
│   │   └───dataset
│   │           bnsdataset.xlsx
│   │
│   └───documentIntelligence
│           .gitignore
│           app.py
│           documentIntelligence.py
│           nixpacks.tom
│           requirements.txt
│
├───config
├───dataset
│   │   bnsdataset.xlsx
│   │
│   └───fir
│           fir1.pdf
│           fir2.pdf
│           fir3.pdf
│           fir4.pdf
│           fir5.pdf
│           fir6.pdf
│           fir7.pdf
│           fir8.pdf
│
├───logs
│       out_text.txt
│
├───nyaya
│   │   client.py
│   │   documentIntelligence.py
│   │   langTranslator.py
│   │   nyayaFunction.py
│   │   pdfSummarize.py
│   │   pdfUsingOCR.py
│   │   server.py
│   │
│   └───__pycache__
│           langTranslator.cpython-313.pyc
│           nyayaFunction.cpython-313.pyc
│
├───scripts
└───tests
    │   client.py
    │   clientCopy.py
    │   langTranslator.py
    │   nyayaFunction.py
    │   pdfSummarize.py
    │   pdfUsingOCR.py
    │   server.py
    │   sidebarTest.py
    │
    └───__pycache__
            langTranslator.cpython-313.pyc
            nyayaFunction.cpython-313.pyc
```

## Usage

The application uses a client-server architecture. You need to run both the server and client components.

### Running the Server

1. Navigate to the Final directory:
```bash
cd "E:\Shashank Singh\Coding\Nyaya\Final"
```

2. Start the server:
```bash
python server.py
```

### Running the Client

1. Open a new terminal/command prompt
2. Navigate to the Final directory:
```bash
cd "E:\Shashank Singh\Coding\Nyaya\Final"
```

3. Launch the Streamlit client:
```bash
streamlit run client.py
```

The Streamlit interface will open in your default web browser, typically at `http://localhost:8501`.

## Testing

Run the unit tests using:

```bash
python -m unittest discover tests
```

## Dependencies

Key dependencies include:
- Groq api client
- Streamlit (for web interface)
- Tesseract OCR
- Additional packages as specified in `requirements.txt`

## Security Notes

- Never commit your `.env` file or api keys to version control
- If you accidentally expose your Groq api key, rotate it immediately
- Remove any committed secrets from git history

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open-source under the MIT License.

## Contact

- **Author**: Shashank Singh
- **GitHub**: [ShashankSingh614](https://github.com/ShashankSingh614)
- **Email**: singhshashankthakur596@gmail.com

## Troubleshooting

### Common Issues

1. **Tesseract not found**: Ensure Tesseract OCR is properly installed and added to your system PATH
2. **api key errors**: Verify your Groq api key is correctly set in the `.env` file
3. **Port conflicts**: If Streamlit fails to start, ensure port 8501 is available or specify a different port with `streamlit run client.py --server.port 8502`

### Support

For issues and questions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information about the problem
3. Include system information, error messages, and steps to reproduce# Nyaya
