
# 🧠 Metadata Extraction API

A FastAPI-based NLP service to extract metadata like dates, authors, and key terms from documents using **spaCy**. Supports `.pdf`, `.docx`, `.txt`, and `.md` formats. Includes REST API endpoints, Docker support, and a test suite.

---

## 🚀 Features

- Extracts metadata: **dates**, **authors**, **key terms**
- Supports multiple formats: `.pdf`, `.docx`, `.txt`, `.md`
- Uses **spaCy** for NER and rule-based pattern matching
- REST API built with **FastAPI**
- Dockerized for easy deployment
- Includes unit and API tests

---

## 🗂️ Project Structure

```
metadata-extraction/
├── app/
│   ├── main.py                # FastAPI endpoints
│   ├── models.py              # Pydantic I/O schemas
│   ├── extraction/            # NLP logic
│   └── utils/                 # File handling
├── data/                      # Sample docs and output
├── logs/                      # App logs
├── tests/                     # PyTest suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SiSuSa/metadata-extraction.git
cd metadata-extraction
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

Open docs at: `http://localhost:8000/docs`

---

## 📤 API Endpoints

| Method | Endpoint          | Description           |
|--------|-------------------|-----------------------|
| GET    | `/`               | Basic health check    |
| GET    | `/health`         | Service diagnostics   |
| POST   | `/extract`        | Upload multiple files |
| POST   | `/extract-single` | Upload one file       |

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🐳 Docker Setup

```bash
docker-compose up --build
```

---

## ✅ Sample Output

```json
{
  "file_name": "sample_research.txt",
  "dates": ["March 15, 2024"],
  "authors": ["Dr. John Smith"],
  "key_terms": ["machine learning", "NLP", "neural networks"]
}
```

---

## 👨‍💻 Author

Built with ❤️ by **Siddhartha Sahu**  
GitHub: [SiSuSa](https://github.com/SiSuSa)  
Email: [sidbeingreal@gmail.com](mailto:sidbeingreal@gmail.com)

---

## 📜 License

MIT License
