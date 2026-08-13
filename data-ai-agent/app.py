import os
import asyncio
import pandas as pd
import streamlit as st
import agentic_bigquery as abq
from dotenv import load_dotenv

# Load local environment variables (.env)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Conversational Analytics API - Data Agent",
    page_icon="📊",
    layout="wide"
)

# Set custom premium CSS styles (dark layout, nice margins)
st.markdown("""
    <style>
        .stApp {
            background-color: #0b0f19;
            color: #f3f4f6;
        }
        .css-1542z7w {
            background-color: rgba(17, 25, 40, 0.7);
            backdrop-filter: blur(12px);
        }
    </style>
""", unsafe_allow_html=True)

# Main Title & Description (Matching User Workflow Image)
st.title("Conversational Analytics Data Agent 📊")
st.markdown("Build and interact with a data agent powered by **Google Antigravity SDK (ADK)** & **Gemini** to query BigQuery databases in English.")

# Sidebar - Grounding Rules & Schema configuration
st.sidebar.header("Grounding Rules & Database Schema")
st.sidebar.markdown(f"**Target Table:** `{abq.DATASET_METADATA['table_name']}`")
st.sidebar.markdown(f"**Description:** {abq.DATASET_METADATA['description']}")

st.sidebar.subheader("Table Schema Columns:")
for col in abq.DATASET_METADATA['schema']:
    st.sidebar.markdown(f"- **`{col['name']}`** ({col['type']}): *{col['description']}*")

st.sidebar.markdown("---")
st.sidebar.subheader("Example Queries:")
st.sidebar.markdown("- *'Show me the top 5 boy names in Texas in 2021'*")
st.sidebar.markdown("- *'What were the most popular girl names in California in 2020?'*")
st.sidebar.markdown("- *'List top 5 names overall in New York for 2018'*")

# Main Interface: User Prompt Input
user_query = st.text_input("Ask a question about the names database in plain English:", 
                           placeholder="e.g. Show me the top 5 names for baby boys in Texas in 2021")

if st.button("Ask Agent & Analyze", type="primary"):
    if not user_query.strip():
        st.warning("Please enter a query prompt first.")
    else:
        # Reset the global query tracker before run
        abq.LAST_QUERY_RESULT = None
        
        # Verify Gemini API Key is available
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Error: GEMINI_API_KEY environment variable is missing. Please set it in your environment or .env file.")
        else:
            with st.spinner("Agent generating SQL, routing queries, and running data analytics..."):
                try:
                    # Run the agent execution workflow
                    agent = abq.BigQueryDataAgent()
                    summary_response = asyncio.run(agent.run_query(user_query))
                    
                    # Fetch captured results from the tool call
                    result = abq.LAST_QUERY_RESULT
                    
                    if result and result["status"] == "success":
                        st.success("Query executed successfully!")
                        
                        # 1. Show the Generated BigQuery SQL
                        st.subheader("Generated BigQuery SQL")
                        st.code(result["sql_executed"], language="sql")
                        
                        # 2. Show Warning Banner if using Fallback Mock Engine
                        if "warning" in result:
                            st.warning(f"⚠️ {result['warning']}")
                        else:
                            st.info(f"💾 Connected to Live BigQuery database. Source: {result['source']}")
                            
                        # 3. Load results into pandas DataFrame
                        df = pd.DataFrame(result["data"])
                        
                        # 4. Display Data Grid & Visualization Charts
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Query Results Data Table")
                            st.dataframe(df, use_container_width=True)
                            
                        with col2:
                            st.subheader("Visualized Metrics (Bar Chart)")
                            # Dynamically determine the best columns to plot
                            if "name" in df.columns and "number" in df.columns:
                                # Plot popular names chart
                                chart_data = df.set_index("name")[["number"]]
                                st.bar_chart(chart_data)
                            elif len(df.columns) >= 2:
                                # Fallback generic chart mapping first numeric column
                                numeric_cols = df.select_dtypes(include=['number']).columns
                                category_cols = df.select_dtypes(include=['object', 'string']).columns
                                if len(numeric_cols) > 0 and len(category_cols) > 0:
                                    chart_data = df.set_index(category_cols[0])[[numeric_cols[0]]]
                                    st.bar_chart(chart_data)
                                else:
                                    st.info("No numeric columns found to plot chart.")
                            else:
                                st.info("Not enough columns to render chart visualization.")
                                
                        # 5. Display Agent Text Synthesis
                        st.subheader("Agent Summary & Synthesis")
                        st.write(summary_response)
                        
                    else:
                        st.error("Error: The agent was unable to execute the query. Response details:")
                        st.write(summary_response)
                        
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")
