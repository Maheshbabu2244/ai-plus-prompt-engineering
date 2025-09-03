# 💡 AI Innovation Hub: An Interactive Learning Dashboard

Welcome to the AI Innovation Hub, a comprehensive, hands-on learning platform for mastering the art and science of prompt engineering. Built with Streamlit and powered by leading AI models, this dashboard provides a suite of interactive tools designed to take you from a beginner to an expert. 

## ✨ Features

This dashboard isn't just a set of tools; it's a complete, gamified curriculum. Each module is designed to teach a core concept of prompt engineering in a practical way.

* **🧠 Module 1: Foundations** - An interactive AI explainer bot that adjusts its explanation for different audiences (a child, a college student, an expert).
* **✍️ Module 2: Effective Prompting** - A powerful Prompt Rewriter Tool that takes your basic prompts and suggests expert-level refinements with clear reasoning.
* **🛠️ Module 3: Tools & Models** - A multi-model comparison dashboard to run a single prompt against GPT and Gemini side-by-side.
* **🔗 Module 4: Advanced Techniques** - A prompt chain visualizer that lets you build and execute multi-step AI workflows.
* **🖼️ Module 5: Image Models** - An AI Image Lab to practice prompt-to-image generation (demonstration).
* **🏗️ Module 6: Project Learning** - A mini-studio where you can build and test a real AI application, like an FAQ chatbot grounded in specific context.
* **🛡️ Module 7: Ethics & Bias** - A practical bias detector tool that analyzes text for harmful stereotypes and exclusionary language.
* **💼 My Portfolio** - Automatically saves your best work from the modules into a personal portfolio.
* **🏆 Leaderboard** - Tracks your progress and unlocked badges as you complete challenges.

## 🚀 Tech Stack

* **Framework:** [Streamlit](https://streamlit.io/)
* **AI Orchestration:** [LangChain](https://www.langchain.com/)
* **Large Language Models (LLMs):** [OpenAI GPT-4o](https://openai.com/), [Google Gemini 1.5 Pro](https://deepmind.google/technologies/gemini/)
* **Core Libraries:** Pandas, Requests, Tiktoken
* **UI/UX:** Custom CSS, Lottie for animations

## ⚙️ Setup and Installation

To run this project locally, please follow these steps.

### 1. Clone the Repository
```bash
git clone [https://github.com/Maheshbabu2244/ai-plus-prompt-engineering](https://github.com/Maheshbabu2244/ai-plus-prompt-engineering)
cd ai-plus-prompt-engineering
```

### 2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to keep dependencies isolated.

**Windows:**
```powershell
# Create the environment
python -m venv venv
# Activate the environment
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
# Create the environment
python3 -m venv venv
# Activate the environment
source venv/bin/activate
```

### 3. Install Dependencies
All required libraries are listed in the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys
The application uses API keys for OpenAI and Google.

1.  Create a folder named `.streamlit` in the root of the project.
2.  Inside this folder, create a file named `secrets.toml`.
3.  Add your API keys to this file as shown below:
    ```toml
    # .streamlit/secrets.toml

    OPENAI_API_KEY = "sk-..."
    GOOGLE_API_KEY = "AIzaSy..."
    ```

## ▶️ How to Run
Once the setup is complete, you can launch the application with a single command from your project's root directory.

```bash
streamlit run 🏠_Innovation_Hub.py
```
The application will open automatically in your web browser.

---
Enjoy exploring the world of prompt engineering!
