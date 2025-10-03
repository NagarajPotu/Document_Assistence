📊 Financial Document Q&A App using Streamlit + Ollama

This is a beginner-friendly Streamlit web app that allows you to upload PDF or Excel financial documents and ask questions about them using a local AI model running with Ollama
.

Everything runs entirely on your computer — no internet-based LLMs (like OpenAI) are required.

🧠 What Does This App Do?

You upload a PDF or Excel file (e.g., a financial report, bank statement, budget sheet)

The app extracts the content from the file

You can then ask questions in plain English, like:

"What was the total revenue in 2022?"

"Which month had the highest expense?"

The app sends this context + your question to a local language model (like LLaMA3) using Ollama

🖥️ Demo Screenshot

(Add a screenshot here if you'd like)

📦 Project Structure
financial-qa-app/
├── app.py             # Main Streamlit app
├── extractor.py       # PDF and Excel data extractors
├── requirements.txt   # Python dependencies
├── .gitignore         # Files to ignore in Git
├── README.md          # You're reading it!

🛠️ Requirements

Before you begin, make sure you have:

✅ A laptop with Windows / macOS / Ubuntu

✅ Python 3.10+ installed

✅ Ollama installed for running the LLM locally

✅ A modern browser (Chrome, Firefox, etc.)

🐍 Step 1: Install Python (if not installed)

🔗 Download Python 3.10+

During installation, check the box that says "Add Python to PATH"

🧠 Step 2: Install Ollama (Local AI Model)

Ollama is a tool that lets you run language models (like LLaMA 3) on your own machine.

🧑‍💻 Download Ollama:

🔗 https://ollama.com/download

Install it for your OS and then open a terminal and run:

ollama run llama3
(This command will download the LLaMA 3 model (~4–5GB). You only need to do this once.)

Keep this terminal open in the background — it starts a local API server at http://localhost:11434.

💻 Step 3: Clone or Download the Project

You can either:

📥 Option A: Download ZIP

Click the green "Code" button on GitHub

Click "Download ZIP"

Extract the ZIP file to a folder

💡 Option B: Use Git (Recommended)
git clone https://github.com/yourusername/financial-qa-app.git
cd financial-qa-app

🧰 Step 4: Set Up Virtual Environment (Optional but Recommended)
# Create a virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

📦 Step 5: Install Required Python Libraries

Make sure you're in the project folder (financial-qa-app) and run:

pip install -r requirements.txt


This installs:

streamlit

requests

pandas

pdfplumber

openpyxl (for reading Excel files)

🚀 Step 6: Run the App

Start your Ollama model in one terminal:

ollama run llama3


Then, in another terminal, run your Streamlit app:

streamlit run app.py


This will open a browser window at:

http://localhost:8501


You can now:

Upload a PDF or Excel file

Ask a question about its contents

Get AI-powered answers instantly — all locally!

🧠 Example Questions to Try

"What is the net profit in this file?"

"Summarize the balance sheet."

"Which department had the highest expenses?"

📁 Supported File Types

.pdf

.xlsx, .xls (Excel)

🛑 Common Issues
Issue	Solution
ModuleNotFoundError	Run pip install -r requirements.txt inside your virtual env
WinError 10061 (Ollama connection)	Make sure ollama run llama3 is running before the app
PDF returns empty text	Some PDFs are scanned images — use OCR or better PDFs
App doesn't open in browser	Manually go to http://localhost:8501 in your browser
🙋 FAQ
🔹 Do I need an internet connection?

Only for the first time when downloading the model via Ollama. After that, it runs fully offline.

🔹 Is it free?

Yes — no API keys, no cloud hosting, everything runs locally.

🔹 Can I deploy this online?

Not with Ollama by default, since it requires a local model. You’d need a server running Ollama for public access.

📜 License

This project is open-source and free to use. Attribution appreciated.

🤝 Contributing

Feel free to fork the project and submit a pull request if you'd like to improve or extend it!

👨‍💻 Made with ❤️ using Streamlit + Ollama
