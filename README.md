# 🧠 GenAICoding

**GenAICoding** is an AI-powered assistant that helps you interact with Jira using natural language. No more digging through menus or learning complicated Jira commands — just type what you need, and the system handles the rest.

Whether you’re assigning tasks, updating issues, or logging progress, GenAICoding makes Jira feel human.

## ✅ What Can GenAICoding Do?

- **Talk to Jira in plain English**  
  Example:  
  *“Create a task to fix the login issue by Monday.”*

- **Create, update, or delete tasks**  
  Automate common Jira actions without needing to remember issue IDs or workflow steps.

- **Send monitoring data to Datadog**  
  Track custom metrics, log events, and monitor service health directly from natural language prompts.

- **Keep your data secure**  
  You provide your own API keys and credentials through a `.env` file, so nothing sensitive is hardcoded.

---

## 🧰 What’s Powering GenAICoding?

You don’t need to worry about the tech, but under the hood, here’s what’s working:

- **OpenAI (ChatGPT)** – Understands what you want  
- **Jira API** – Manages your tasks and projects  
- **Datadog API** – Tracks metrics, service checks, and event logs  
- **LangChain** – Helps the AI tools and APIs work together  
- **Python + dotenv** – Keeps your keys and credentials safe

---

## 🔧 How to Set It Up

You may want help from your technical team, but here’s a simplified setup guide:

### 1. 📥 Download the Project

```bash
git clone https://github.com/your-username/GenAICoding.git
cd GenAICoding
2. 🔐 Configure Your Credentials
Create your .env file:

bash
Copy code
cp .env.example .env
Open the .env file and fill in your keys:

env
Copy code
OPENAI_API_KEY=your-openai-api-key
JIRA_API_TOKEN=your-jira-api-token
JIRA_USERNAME=your-email@example.com
JIRA_INSTANCE_URL=https://yourcompany.atlassian.net
DATADOG_API_KEY=your-datadog-api-key
DATADOG_APP_KEY=your-datadog-app-key
JIRA_PROJECT_KEY=ABC
3. 📦 Install Dependencies
Run this in your terminal:

bash
Copy code
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
4. ▶️ Start Using It
Run the assistant:

bash
Copy code
python main.py "Create a task for the design team to update the mobile app icon."
The AI will interpret your request and perform the action in Jira.

🛠️ Supported Prompts
Here are a few things you can say:

"Create a new bug report for slow checkout flow"

"Update the issue ABC-123 with a new summary"

"Log a Datadog event saying 'Deployed version 2.0' tagged with 'env:prod'"

"Send a service check for 'api.health' with status OK and tag it with 'env:staging'"

❓ Troubleshooting
“Invalid API key” error?
Double-check that your .env file is correctly filled out.

Jira connection failed?
Make sure you're using your Jira email and API token, not your password.

Something else not working?
Try reinstalling dependencies:

bash
Copy code
pip install -r requirements.txt
🤝 Want to Improve It?
If you’re a developer (or working with one), feel free to fork and enhance the project:

bash
Copy code
git checkout -b new-feature
git commit -m "Add cool new thing"
git push origin new-feature
Then open a Pull Request on GitHub to suggest your changes.

📄 License
This project is licensed under the MIT License. You're free to use it, modify it, and share 


