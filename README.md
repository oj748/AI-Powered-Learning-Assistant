# AI-Powered Learning Assistant

## Technology Stack

### Desktop Application

* Python
* PySide6
* Qt WebEngine

### Local AI and Content Processing

* Phi-4-mini-instruct
* llama.cpp / GGUF
* PaddleOCR
* PaddleX
* faster-whisper
* PyMuPDF

### Cloud AI

* Google Gemini API
* Gemini 3.1 Flash-Lite
* Google GenAI Python SDK

### Content Rendering

* HTML
* CSS
* JavaScript
* markdown-it
* MathJax

### Database

* SQLite

## Local and Online Modes

The application provides two AI processing modes.

**Local mode** uses locally running AI models for OCR, audio transcription, summarization, flashcard generation, and quiz generation. Phi-4-mini-instruct is used as the local language model.

**Online mode** uses Gemini 3.1 Flash-Lite through the Gemini API for cloud-based document processing and content generation.

## Local Language Model

The application uses a Q4_K_M GGUF quantization of Microsoft Phi-4-mini-instruct for local content generation.

The GGUF model used by this project is available on Hugging Face:

[`oj748/Phi-4-mini-instruct-Q4_K_M-GGUF`](https://huggingface.co/oj748/Phi-4-mini-instruct-Q4_K_M-GGUF/blob/main/phi4-Q4_K_M.gguf)

The model is not included directly in this repository because of its file size.

## Environment Variables

Create a `.env` file in the project directory and add your Gemini API key:

```env
GEMINI_API_KEY=PASTE_YOUR_API_KEY_HERE
```

The Gemini API key is required only for online AI functionality.

## Model Setup

Downloaded AI model files and model caches are not included in this GitHub repository.

The application uses local model directories under `models/`.

Additional setup instructions for Phi-4-mini-instruct, faster-whisper, and PaddleOCR will be documented as the model initialization workflow is finalized.

## Project Status

The application is currently under development.

The core learning workflow, including transcription, OCR, PDF processing, AI content generation, flashcards, quizzes, persistent storage, and theme support, has been implemented.

## License and Third-Party Components

This project uses several third-party open-source libraries and AI models.

The Phi-4-mini-instruct model was developed by Microsoft. The local GGUF model used by this application is a converted and quantized version of the original model.

Third-party components retain their respective licenses and copyright notices.

A detailed third-party license notice will be added to the repository.

## Author

Ojaswini
