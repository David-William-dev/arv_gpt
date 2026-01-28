# ARV-GPT: AI-Powered Heritage Virtual Assistant

ARV-GPT is a full-stack AI chatbot application designed to assist users in exploring heritage locations in Tamil Nadu. It provides multilingual support (English & Tamil), audio responses, and smart query handling using advanced AI models like LLaMA via Groq API. The app integrates Django Rest Framework (DRF) for the backend and Flet for the frontend, with real-time text-to-speech (TTS) features using `flet-audio`. Data is stored in a local SQLite database.

---

## 📌 Features

- 🗣️ **Multilingual Support** – Communicate in English or Tamil with seamless translation using MyMemory API.
- 🧠 **AI Chatbot** – Powered by LLaMA model via Groq API for intelligent and contextual responses.
- 🔐 **Authentication** – User login and signup using Django DRF Token Authentication.
- 🎧 **Real-Time Audio** – TTS integration with Flet for dynamic audio playback.
- 🔄 **Async Response Handling** – Non-blocking communication between frontend and backend.
- 📱 **Cross-Platform Frontend** – Built using Flet for web, desktop, and mobile use.

---

## 🧱 Tech Stack

- **Frontend**: [Flet](https://flet.dev/docs/)
- **Backend**: Django + Django Rest Framework (DRF)
- **Database**: SQLite
- **AI API**: [Groq API](https://console.groq.com/docs/quickstart) using LLaMA-3-8b-Instruct model
- **TTS**: `flet-audio` integration
- **Translation API**: MyMemory Translation API

---

## 🧩 Modules

1. **Authentication** – User sign up, login, and token management.
2. **AI Chat Processing** – Sending user queries to Django backend and handling Groq responses.
3. **Language Toggle** – Switch UI language and AI responses between English and Tamil.
4. **TTS Integration** – Clean markdown and stream audio to the user in real-time.
5. **History & Logging** – Store and display user queries and responses in chat history.
6. **UI/UX** – Custom input field, typing indicator, audio playback button, loading spinner.

---

## 📦 Installation & Run Locally

### 🎡 Frontend

#### step : 1
- To install the dependecy the poetry were used to retrieve the dependecy for the installation of the dependency
- After the installation of the `python-3.10.X` in terminal we have to install the poetry first 
- To install poetry verify docs [Poetry](https://python-poetry.org/docs/)
- After installation of the poetry `poetry install` to install all dependencies in virtual environment in fronted directory.

#### step : 2
- To initialize the flet web use the command
```console
    poetry run flet run --web
```
- To run in android install flet app in mobile from playstore [Flet App](https://flet.dev/docs/getting-started/testing-on-android/)
```console
    poetry run flet run --android
```
### 🐍 Backend

#### step : 1
- To install the dependecy the poetry were used to retrieve the dependecy for the installation of the dependency
- After the installation of the `python-3.10.X` in terminal we have to install the poetry first 
- To install poetry verify docs [Poetry](https://python-poetry.org/docs/)
- After installation of the poetry `poetry install` to install all dependencies in virtual environment in backend directory.

#### step : 2
- To initialize the django web server use the command
```console
    poetry run python manage.py runserver
```
## 📌 Note
- Run both backend and frontend **simultaneously**
- On testing in android make sure the django server device and android mobile are connected in **same network** 