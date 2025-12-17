"""
CrewAI Agents for Streamlit Components Hub
Agent 45 - Component Curation System
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import List, Dict, Optional
import os


class ComponentCurationAgents:
    """
    Three specialized agents for curating and analyzing Streamlit components:
    1. Component Analyzer - Analyzes component quality, features, and documentation
    2. Category Expert - Categorizes components and identifies missing categories
    3. Recommendation Specialist - Generates recommendations and rankings
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the agents with OpenAI API key."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=self.api_key
        )

    def create_component_analyzer(self) -> Agent:
        """
        Agent 1: Component Analyzer
        Analyzes component quality, features, and documentation.
        """
        return Agent(
            role="Component Quality Analyst",
            goal="Analyze Streamlit components for quality, features, and documentation completeness",
            backstory="""You are an expert in evaluating software components with years of
            experience in the Streamlit ecosystem. You have a keen eye for identifying
            well-maintained, documented, and useful components. You analyze GitHub stars,
            download statistics, code quality, and documentation to assess component value.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def create_category_expert(self) -> Agent:
        """
        Agent 2: Category Expert
        Categorizes components and identifies missing categories.
        """
        return Agent(
            role="Component Categorization Expert",
            goal="Accurately categorize Streamlit components and identify missing or miscategorized items",
            backstory="""You are a taxonomy expert specializing in organizing software
            components. You understand the nuances between different component types like
            widgets, charts, dataframes, navigation tools, and integrations. You ensure
            components are properly tagged and discoverable by users looking for specific
            functionality.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def create_recommendation_specialist(self) -> Agent:
        """
        Agent 3: Recommendation Specialist
        Generates recommendations and rankings based on analysis.
        """
        return Agent(
            role="Component Recommendation Specialist",
            goal="Generate personalized component recommendations and create quality rankings",
            backstory="""You are a recommendation systems expert who understands user needs
            and matches them with the best Streamlit components. You consider factors like
            popularity, maintenance status, ease of use, and specific use cases to provide
            tailored suggestions. You help users discover hidden gems and avoid deprecated
            or low-quality components.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def analyze_component(self, component_data: Dict) -> str:
        """
        Analyze a single component using the Component Analyzer agent.

        Args:
            component_data: Dictionary containing component information

        Returns:
            Analysis report string
        """
        analyzer = self.create_component_analyzer()

        task = Task(
            description=f"""Analyze this Streamlit component and provide a detailed assessment:

            Component Name: {component_data.get('name', 'Unknown')}
            Package: {component_data.get('package', 'Unknown')}
            GitHub Stars: {component_data.get('stars', 0)}
            Downloads: {component_data.get('downloads', 0)}
            Description: {component_data.get('description', 'No description')}
            Categories: {component_data.get('categories', [])}

            Provide assessment on:
            1. Component quality and maintenance
            2. Documentation completeness
            3. Community adoption
            4. Potential use cases
            5. Strengths and weaknesses
            """,
            agent=analyzer,
            expected_output="A comprehensive analysis report with quality metrics and recommendations"
        )

        crew = Crew(
            agents=[analyzer],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def categorize_component(self, component_data: Dict, available_categories: List[str]) -> str:
        """
        Categorize a component using the Category Expert agent.

        Args:
            component_data: Dictionary containing component information
            available_categories: List of available category options

        Returns:
            Categorization report with suggested categories
        """
        expert = self.create_category_expert()

        task = Task(
            description=f"""Categorize this Streamlit component accurately:

            Component Name: {component_data.get('name', 'Unknown')}
            Package: {component_data.get('package', 'Unknown')}
            Description: {component_data.get('description', 'No description')}
            Current Categories: {component_data.get('categories', [])}

            Available Categories: {', '.join(available_categories)}

            Provide:
            1. Recommended primary category
            2. Secondary categories (if applicable)
            3. Justification for each category
            4. Flag if current categorization is incorrect
            5. Suggest new categories if none fit perfectly
            """,
            agent=expert,
            expected_output="Categorization recommendations with justifications"
        )

        crew = Crew(
            agents=[expert],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def generate_recommendations(self, user_query: str, components_list: List[Dict]) -> str:
        """
        Generate component recommendations using the Recommendation Specialist.

        Args:
            user_query: User's search query or requirements
            components_list: List of available components

        Returns:
            Recommendation report
        """
        specialist = self.create_recommendation_specialist()

        # Prepare component summary
        components_summary = "\n".join([
            f"- {c.get('name', 'Unknown')}: {c.get('description', 'No description')[:100]}... "
            f"(Stars: {c.get('stars', 0)}, Downloads: {c.get('downloads', 0)})"
            for c in components_list[:50]  # Limit to top 50 for context
        ])

        task = Task(
            description=f"""Generate personalized Streamlit component recommendations:

            User Query: {user_query}

            Available Components:
            {components_summary}

            Provide:
            1. Top 5 recommended components with explanations
            2. Why each component matches the user's needs
            3. Alternative options to consider
            4. Warning about any deprecated or low-quality components
            5. Suggested combination of components if applicable
            """,
            agent=specialist,
            expected_output="Personalized component recommendations with detailed justifications"
        )

        crew = Crew(
            agents=[specialist],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def collaborative_analysis(self, component_data: Dict, available_categories: List[str]) -> Dict[str, str]:
        """
        Run all three agents collaboratively to analyze a component.

        Args:
            component_data: Dictionary containing component information
            available_categories: List of available categories

        Returns:
            Dictionary with results from all three agents
        """
        analyzer = self.create_component_analyzer()
        expert = self.create_category_expert()
        specialist = self.create_recommendation_specialist()

        # Task 1: Analyze component quality
        analysis_task = Task(
            description=f"""Analyze this Streamlit component:

            Component: {component_data.get('name', 'Unknown')}
            Package: {component_data.get('package', 'Unknown')}
            Stars: {component_data.get('stars', 0)}
            Downloads: {component_data.get('downloads', 0)}
            Description: {component_data.get('description', 'No description')}

            Provide quality assessment and key features.
            """,
            agent=analyzer,
            expected_output="Quality assessment report"
        )

        # Task 2: Categorize the component
        categorization_task = Task(
            description=f"""Based on the analysis, categorize this component:

            Component: {component_data.get('name', 'Unknown')}
            Available Categories: {', '.join(available_categories)}

            Provide accurate categorization.
            """,
            agent=expert,
            expected_output="Categorization recommendations"
        )

        # Task 3: Generate usage recommendations
        recommendation_task = Task(
            description=f"""Based on the analysis and categorization, recommend:

            Component: {component_data.get('name', 'Unknown')}

            1. Best use cases
            2. Target audience
            3. Integration tips
            """,
            agent=specialist,
            expected_output="Usage recommendations and best practices"
        )

        # Create crew with all agents working together
        crew = Crew(
            agents=[analyzer, expert, specialist],
            tasks=[analysis_task, categorization_task, recommendation_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        return {
            "analysis": str(result),
            "status": "completed"
        }


def demo_crewai_agents():
    """
    Demo function to showcase the CrewAI agents in action.
    """
    # Example component data
    example_component = {
        "name": "AgGrid",
        "package": "streamlit-aggrid",
        "stars": 1500,
        "downloads": 50000,
        "description": "A Streamlit component to display interactive dataframes using AG Grid",
        "categories": ["dataframe"]
    }

    # Initialize agents
    agents = ComponentCurationAgents()

    # Example 1: Analyze a component
    print("=" * 80)
    print("AGENT 1: COMPONENT ANALYZER")
    print("=" * 80)
    analysis = agents.analyze_component(example_component)
    print(analysis)
    print("\n")

    # Example 2: Categorize a component
    print("=" * 80)
    print("AGENT 2: CATEGORY EXPERT")
    print("=" * 80)
    categories = ["widgets", "charts", "dataframe", "image", "text", "maps"]
    categorization = agents.categorize_component(example_component, categories)
    print(categorization)
    print("\n")

    # Example 3: Generate recommendations
    print("=" * 80)
    print("AGENT 3: RECOMMENDATION SPECIALIST")
    print("=" * 80)
    components = [example_component]
    recommendations = agents.generate_recommendations(
        "I need a component to display interactive tables with sorting and filtering",
        components
    )
    print(recommendations)


if __name__ == "__main__":
    # Run demo if executed directly
    print("CrewAI Component Curation Agents - Demo")
    print("Make sure OPENAI_API_KEY is set in your environment")
    demo_crewai_agents()
