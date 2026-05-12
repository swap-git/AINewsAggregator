import os
import yaml
from datetime import date, timedelta
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv

load_dotenv()

# 1. Setup API Keys
# Please update your OPENAI_API_KEY with a valid key (should start with 'sk-')
openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# 2. Initialize Tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# 3. Agents
# Load YAML files
BASE_DIR = Path(__file__).resolve().parent.parent
agents_config_path = BASE_DIR / "config" / "agents.yaml"
tasks_config_path = BASE_DIR / "config" / "tasks.yaml"

with agents_config_path.open('r', encoding='utf-8') as f:
    agents_config = yaml.safe_load(f)
with tasks_config_path.open('r', encoding='utf-8') as f:
    tasks_config = yaml.safe_load(f)

researcher = Agent(config=agents_config['global_ai_researcher'], tools=[search_tool, scrape_tool],
    verbose=True)
analyst = Agent(config=agents_config['tech_product_analyst'], verbose=True)


# 4. Tasks
task1 = Task(config=tasks_config['gather_news_task'], agent=researcher)
task2 = Task(config=tasks_config['briefing_task'], agent=analyst, context=[task1], output_file="daily_ai_briefing.md"
)

# 5. The Crew
daily_ai_crew = Crew(
    agents=[researcher, analyst],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

# 6. Kickoff the process
if __name__ == "__main__":
    print("Starting Daily AI News Gathering...")
    end = date.today()
    start = end - timedelta(days=2)
    result = daily_ai_crew.kickoff(
        inputs={
            "topic": "Global AI news",
            "current_date": end.isoformat(),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        }
    )
    print("\n--- DAILY BRIEFING COMPLETE ---\n")
    print(result)
