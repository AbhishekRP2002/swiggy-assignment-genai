import streamlit as st
from src.agent import PersonalAssistant
import time
import os

st.set_page_config(
    page_title="Swiggy Personal Assistant", page_icon="🎯", layout="wide"
)

st.markdown(
    """
<style>
    .main {
        padding: 2rem;
    }
    .output-container {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    .intent-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .entity-item {
        background-color: #e1e5eb;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
    }
    .follow-up {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
    }
    .search-result {
        border-left: 3px solid #4CAF50;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    .example-card {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🎯 Personal Assistant")
st.markdown("""
This personal assistant analyzes user queries and:
1. Categorizes them into intent categories (dining, travel, gifting, cab booking, or other)
2. Extracts relevant entities from the query
3. Provides follow-up questions for missing information
4. Performs web searches for non-standard queries
""")

api_key = st.text_input(
    "OpenAI API Key", type="password", help="Enter your OpenAI API key"
)
st.caption("Your API key is not stored and is only used for this session.")

if "selected_example" not in st.session_state:
    st.session_state.selected_example = ""

st.subheader("Example Queries")
example_queries = [
    "I need a table for two tonight at a restaurant with a sunset-view",
    "Book me a flight to Paris next month for a week",
    "I need a gift for my mom's birthday under $100",
    "Get me a cab from the airport to downtown tomorrow morning",
    "What's the latest news about artificial intelligence?",
]

for i, example in enumerate(example_queries):
    if st.button(f"Example {i+1}: {example}", key=f"example_{i}"):
        st.session_state.selected_example = example

user_query = st.text_input(
    "Enter your query",
    value=st.session_state.selected_example,
    placeholder="E.g., I need a table for two tonight for my anniversary.",
)

if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY")


if st.button("Generate Response") and user_query and api_key:
    with st.spinner("Analyzing your query..."):
        try:
            assistant = PersonalAssistant(api_key=api_key)
            start_time = time.time()
            response = assistant.process_query(user_query)
            processing_time = time.time() - start_time

            st.success(f"Analysis completed in {processing_time:.2f} seconds")
            tab1, tab2 = st.tabs(["Formatted View", "JSON View"])

            with tab1:
                # intent category
                intent = response.get("intent_category", "unknown")
                intent_color = {
                    "dining": "#4CAF50",
                    "travel": "#2196F3",
                    "gifting": "#FF9800",
                    "cab booking": "#9C27B0",
                    "other": "#607D8B",
                }.get(intent, "#607D8B")

                st.markdown(
                    f"""
                <div style="margin-bottom: 1rem;">
                    <span style="background-color: {intent_color}; color: white; padding: 0.3rem 0.6rem; border-radius: 1rem; font-size: 0.8rem;">
                        {intent.upper()}
                    </span>
                    <span style="margin-left: 1rem; color: #666;">
                        Confidence: {response.get("confidence_score", 0):.2f}
                    </span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Display entities
                if response.get("entities"):
                    st.markdown("##### Extracted Entities")
                    for key, value in response.get("entities", {}).items():
                        st.markdown(
                            f"""
                        <div class="entity-item">
                            <strong>{key}:</strong> {value}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No entities were extracted from this query.")

                # show follow-up questions
                if response.get("follow_up_questions"):
                    st.markdown("##### Suggested Follow-up Questions")
                    for question in response.get("follow_up_questions", []):
                        st.markdown(
                            f"""
                        <div class="follow-up">
                            {question}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                # show web search results if available
                if response.get("Web Search_results"):
                    st.markdown("##### Web Search Results")
                    for result in response.get("Web Search_results", []):
                        st.markdown(
                            f"""
                        <div class="search-result">
                            <a href="{result.get('link', '#')}" target="_blank"><strong>{result.get('title', 'No title')}</strong></a>
                            <p>{result.get('snippet', 'No snippet available')}</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

            with tab2:
                # Display raw JSON
                st.json(response)

        except Exception as e:
            st.error(f"Error processing your request: {str(e)}")
