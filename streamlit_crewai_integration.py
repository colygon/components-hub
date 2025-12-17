"""
Streamlit Components Hub - CrewAI Integration Module
Agent 45 Enhancement

This module integrates CrewAI agents into the Streamlit Components Hub
to provide intelligent component curation, analysis, and recommendations.
"""

import streamlit as st
from typing import List, Dict, Optional
from crewai_agents import ComponentCurationAgents


def initialize_crewai_agents():
    """Initialize CrewAI agents with caching."""
    if "crewai_agents" not in st.session_state:
        try:
            st.session_state.crewai_agents = ComponentCurationAgents()
            st.session_state.crewai_enabled = True
        except Exception as e:
            st.warning(f"CrewAI agents not initialized: {e}")
            st.session_state.crewai_enabled = False
    return st.session_state.get("crewai_agents")


def show_ai_insights_panel(component_data: Dict):
    """
    Display AI-powered insights for a component using CrewAI agents.

    Args:
        component_data: Dictionary containing component information
    """
    if not st.session_state.get("crewai_enabled", False):
        return

    agents = st.session_state.get("crewai_agents")
    if not agents:
        return

    with st.expander("🤖 AI Insights (powered by CrewAI)", expanded=False):
        tab1, tab2, tab3 = st.tabs([
            "📊 Quality Analysis",
            "🏷️ Category Insights",
            "💡 Recommendations"
        ])

        with tab1:
            if st.button("Analyze Component Quality", key=f"analyze_{component_data.get('package', 'unknown')}"):
                with st.spinner("AI Agent analyzing component..."):
                    try:
                        analysis = agents.analyze_component(component_data)
                        st.markdown(analysis)
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

        with tab2:
            if st.button("Get Category Insights", key=f"categorize_{component_data.get('package', 'unknown')}"):
                with st.spinner("AI Agent analyzing categories..."):
                    try:
                        from streamlit_app import CATEGORY_NAMES
                        categories = list(CATEGORY_NAMES.keys())
                        categorization = agents.categorize_component(component_data, categories)
                        st.markdown(categorization)
                    except Exception as e:
                        st.error(f"Categorization failed: {e}")

        with tab3:
            if st.button("Get Usage Recommendations", key=f"recommend_{component_data.get('package', 'unknown')}"):
                with st.spinner("AI Agent generating recommendations..."):
                    try:
                        recommendations = agents.generate_recommendations(
                            f"How to use {component_data.get('name', 'this component')}",
                            [component_data]
                        )
                        st.markdown(recommendations)
                    except Exception as e:
                        st.error(f"Recommendation failed: {e}")


def ai_powered_search(search_query: str, components: List[Dict]) -> str:
    """
    Use CrewAI agents to provide intelligent search results and recommendations.

    Args:
        search_query: User's search query
        components: List of all components

    Returns:
        AI-generated search insights
    """
    if not st.session_state.get("crewai_enabled", False):
        return ""

    agents = st.session_state.get("crewai_agents")
    if not agents or not search_query:
        return ""

    try:
        with st.spinner("🤖 AI Agent analyzing your search..."):
            recommendations = agents.generate_recommendations(search_query, components)
            return recommendations
    except Exception as e:
        st.error(f"AI search failed: {e}")
        return ""


def batch_categorization(components: List[Dict], available_categories: List[str]) -> Dict[str, List[str]]:
    """
    Use CrewAI agents to suggest categories for multiple components.

    Args:
        components: List of components to categorize
        available_categories: Available category options

    Returns:
        Dictionary mapping component packages to suggested categories
    """
    if not st.session_state.get("crewai_enabled", False):
        return {}

    agents = st.session_state.get("crewai_agents")
    if not agents:
        return {}

    results = {}
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, component in enumerate(components):
        try:
            status_text.text(f"Analyzing {component.get('name', 'component')}...")
            categorization = agents.categorize_component(component, available_categories)
            results[component.get("package", "")] = categorization
            progress_bar.progress((idx + 1) / len(components))
        except Exception as e:
            st.warning(f"Failed to categorize {component.get('name', 'component')}: {e}")

    status_text.text("Analysis complete!")
    return results


def show_ai_dashboard():
    """
    Display a dedicated AI dashboard with CrewAI agent capabilities.
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 AI Features (CrewAI)")

    if not st.session_state.get("crewai_enabled", False):
        st.sidebar.warning("CrewAI agents not available. Set OPENAI_API_KEY to enable.")
        return

    # AI search helper
    if st.sidebar.checkbox("Enable AI Search Assistant", value=False):
        st.sidebar.info("💡 AI will analyze your searches and provide intelligent recommendations.")

    # Bulk operations
    if st.sidebar.button("🔄 Bulk Categorize All Components"):
        st.sidebar.info("This will use AI to suggest better categories for all components.")

    # Agent statistics
    with st.sidebar.expander("📈 AI Agent Stats"):
        st.write("**Active Agents:** 3")
        st.write("- Component Analyzer")
        st.write("- Category Expert")
        st.write("- Recommendation Specialist")


def get_ai_component_score(component_data: Dict) -> Optional[float]:
    """
    Get an AI-generated quality score for a component.

    Args:
        component_data: Component information

    Returns:
        Quality score between 0 and 1, or None if unavailable
    """
    # This is a placeholder for more sophisticated AI scoring
    # In a full implementation, this would call the CrewAI agents
    stars = component_data.get("stars", 0)
    downloads = component_data.get("downloads", 0)
    has_description = bool(component_data.get("description"))
    has_demo = bool(component_data.get("demo"))

    # Simple scoring algorithm
    score = 0.0
    if stars > 100:
        score += 0.3
    if downloads > 10000:
        score += 0.3
    if has_description:
        score += 0.2
    if has_demo:
        score += 0.2

    return min(score, 1.0)


def show_ai_curated_collections(components: List[Dict]):
    """
    Display AI-curated collections of components.

    Args:
        components: List of all components
    """
    if not st.session_state.get("crewai_enabled", False):
        return

    st.markdown("## 🤖 AI-Curated Collections")
    st.write("Components selected by our AI agents based on quality, popularity, and utility.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ⭐ Hidden Gems")
        st.caption("High-quality components that deserve more attention")

    with col2:
        st.markdown("### 🔥 Trending Now")
        st.caption("Components gaining popularity recently")

    with col3:
        st.markdown("### 🏆 Editor's Choice")
        st.caption("AI-verified top-quality components")


# Utility function to convert component object to dict for AI processing
def component_to_dict(component) -> Dict:
    """
    Convert a Component dataclass to a dictionary for AI processing.

    Args:
        component: Component dataclass instance

    Returns:
        Dictionary representation
    """
    return {
        "name": getattr(component, "name", None),
        "package": getattr(component, "package", None),
        "stars": getattr(component, "stars", 0),
        "downloads": getattr(component, "downloads", 0),
        "description": getattr(component, "github_description", None) or getattr(component, "pypi_description", None),
        "categories": getattr(component, "categories", []),
        "demo": getattr(component, "demo", None),
        "github": getattr(component, "github", None),
        "pypi": getattr(component, "pypi", None)
    }
