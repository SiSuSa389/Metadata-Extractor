H
```markdown
# 🧠 Metadata Extraction API

A production-ready FastAPI-based service that extracts structured metadata (dates, authors, and key terms) from uploaded documents using a combination of **rule-based** and **statistical NLP techniques** (via spaCy). It supports multiple file formats and provides RESTful endpoints for ease of integration.

---

## 🚀 Features

- 🔍 **Extracts metadata**: dates, authors, and domain-specific key terms  
- 📄 **Supports**: `.pdf`, `.docx`, `.txt`, `.md`  
- 🧠 **spaCy-powered NLP** pipeline:  
  - Rule-based matcher for dates and key terms  
  - Named Entity Recognition (NER) for authors, dates, orgs, locations  
- ⚙️ REST API built with **FastAPI**  
- 🧪 Full **testing suite** using PyTest  
- 🐳 **Dockerized** for easy deployment  
- 🧾 JSON output and structured logs  

---

## 🗂️ Project Structure

```

metadata-extraction/
├── app/
│   ├── main.py                # FastAPI application and endpoints
│   ├── models.py              # Pydantic models for input/output
│   ├── extraction/            # Core logic for metadata extraction
│   │   ├── patterns.py
│   │   ├── metadata\_extractor.py
│   │   └── text\_extractor.py
│   └── utils/
│       └── file\_handlers.py   # File validation and output writing
├── data/
│   ├── sample\_documents/      # Sample files for demo
│   └── output/                # JSON output directory
├── logs/                      # App logs
├── tests/                     # Pytest unit and API tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md

````

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/metadata-extraction.git
cd metadata-extraction
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 🧪 Run Locally

### Start the API

```bash
uvicorn app.main:app --reload
```

### API Access

* Base URL: `http://localhost:8000`
* Interactive Docs: `http://localhost:8000/docs`

---

## 🔁 API Endpoints

| Method | Endpoint          | Description           |
| ------ | ----------------- | --------------------- |
| GET    | `/`               | Health check message  |
| GET    | `/health`         | Full health status    |
| POST   | `/extract`        | Upload multiple files |
| POST   | `/extract-single` | Upload a single file  |

---

## 📥 Example Request

### Upload a single file via Python

```python
import requests

with open("sample_research.txt", "rb") as f:
    files = {"file": ("sample_research.txt", f)}
    r = requests.post("http://localhost:8000/extract-single", files=files)
    print(r.json())
```

---

## 🧪 Run Tests

```bash
pytest tests/
```

---

## 🐳 Docker Deployment

### Build & Run

```bash
docker-compose up --build
```

Then open `http://localhost:8000/docs` to test your endpoints.

---

## ✅ Sample Output (JSON)

```json
{
  "file_name": "sample_research.txt",
  "dates": ["March 15, 2024", "January 2024", "February 2024"],
  "authors": ["Dr. John Smith", "Prof. Sarah Johnson"],
  "key_terms": ["machine learning", "natural language processing", "neural network"]
}
```

---

## 📌 Notes

* File size limit: 10 MB
* Only text-based files are supported (PDFs must have extractable text)
* Add more patterns in `patterns.py` to suit specific use cases/domains

---

## 👨‍💻 Author

Built with ❤️ by \[Siddhartha Sahu]
GitHub: \[SiSuSa]
Email: [sidbeingreal@gmail.com](mailto:sidbeingreal@gmail.com)

---

## 📜 License

MIT License


