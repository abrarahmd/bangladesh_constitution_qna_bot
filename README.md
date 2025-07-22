# Constitution QnA Bot

A question-answering bot for the Bangladesh Constitution using LLMs and vector search.

---

## 🚀 Quick Start

### 1. Clone the Repository

```sh
git clone https://github.com/abrarahmd/bangladesh_constitution_qna_bot.git
cd your-repo-name
```

### 2. Install Python Dependencies

```sh
pip install -r requirements.txt
```

---

## 🔑 API Setup

### Use Groq (Recommended for Most Users)

1. **Get a Groq API Key:**  
   Sign up at [https://console.groq.com/](https://console.groq.com/) and copy your API key.

2. **Create a `.env` file in your project root:**
   ```
   GROQ_API_KEY=sk-...your_groq_key_here...
   ```

---

---

## ⚡️ Running the App

```sh
python src/app.py
```

- When prompted, type your question and press Enter.
- Type `exit` to quit.

---

## 📝 Notes

- **.env file:** Never share your `.env` or API keys publicly.

---

## 📂 Project Structure

```
src/
  app.py
  config.py
  chunker.py
  embedder.py
  pdf_parser.py
  rag_pipeline.py
  vector_store.py
data/
  raw_pdfs/
  vector_store/
requirements.txt
.env (not included in git)
```

---

## 🤝 Contributing

Pull requests and issues are welcome!
Contact If you have any questions, suggestions, or feedback, please feel free to contact me at [abrargroad2000@gmail.com].

---

## 📄 License

[MIT](LICENSE)
