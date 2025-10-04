You are an expert software architect. 
Generate the complete backend folder structure for a FastAPI project called “Multi-Agent Fake-News Detection Platform.” 
Do not write any business logic yet — only create clean, well-organized folders, empty Python files with docstrings, and placeholders as needed.

Project Description:
This backend powers a fake-news detection web platform. 
It uses a pre-trained model to generate a reliability score (0–100) for news content, applies threshold-based verdict mapping, and performs LLM-based web evidence searches for uncertain results. 
It also supports feedback collection from users.

Requirements:
- Framework: FastAPI
- Architecture: Modular, scalable, and explainable
- Backend only (no frontend)
- Use this folder structure exactly:

<pre>
backend/
├── main.py
├── config/
│   ├── settings.py
│   └── logger.py
├── routes/
│   ├── detect.py
│   ├── feedback.py
│   └── sources.py
├── core/
│   ├── input_handler.py
│   ├── inference.py
│   ├── verdict_logic.py
│   ├── evidence_agent.py
│   ├── explainability.py
│   └── feedback_manager.py
├── models/
│   ├── detection_models.py
│   ├── feedback_models.py
│   └── evidence_models.py
├── services/
│   ├── ocr_service.py
│   ├── web_scraper.py
│   ├── llm_service.py
│   ├── storage_service.py
│   └── utils.py
├── data/
│   ├── sources/
│   ├── feedback/
│   └── logs/
├── model/
│   ├── model.pkl
│   └── tokenizer/
├── tests/
│   ├── test_detect.py
│   ├── test_feedback.py
│   ├── test_evidence_agent.py
│   └── conftest.py
├── requirements.txt
├── README.md
└── .env
</pre>

Instructions:
1. Generate this folder structure exactly as listed.
2. Each .py file should contain:
   - A short descriptive docstring (1–2 lines) explaining its purpose.
   - An import placeholder (e.g., `from fastapi import APIRouter` if relevant).
3. Do not implement any actual logic or functions yet.
4. Create empty subfolders where specified (like `sources/`, `feedback/`, `logs/`, and `tokenizer/`).
5. Populate README.md with one paragraph describing the backend purpose.
6. Leave requirements.txt empty for now.

Output:
A clean, ready-to-extend FastAPI backend scaffold matching this structure.

