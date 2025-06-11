# src/agentic_api/crew.py

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
import os

@CrewBase
class ResearchCrew:
    """A crew that researches a topic and creates a comprehensive report."""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Paths to YAML configuration files with absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agents_config = os.path.join(base_dir, 'config/agents.yaml')
    tasks_config = os.path.join(base_dir, 'config/tasks.yaml')

    @before_kickoff
    def prepare_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare inputs before the crew starts."""
        # You can modify inputs here if needed
        return inputs

    @after_kickoff
    def process_output(self, output):
        """Process output after the crew finishes."""
        # You can modify the output here if needed
        return output

    @agent
    def researcher(self) -> Agent:
        """Create the researcher agent."""
        return Agent(
            config=self.agents_config['researcher'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        """Create the analyst agent."""
        return Agent(
            config=self.agents_config['analyst'],  # type: ignore[index]
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        """Create the research task."""
        return Task(
            config=self.tasks_config['research_task']  # type: ignore[index]
        )

    @task
    def analysis_task(self) -> Task:
        """Create the analysis task."""
        return Task(
            config=self.tasks_config['analysis_task']  # type: ignore[index]
        )

    @crew
    def build(self) -> Crew:
        """Build the crew with the defined agents and tasks."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=Process.sequential
        )