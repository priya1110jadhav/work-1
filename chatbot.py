import streamlit as st
import pandas as pd
import gensql
from database_connector import execute_sql_query
import json
import streamlit.components.v1 as components  # Import Streamlit components
 
# Set the title of the application
st.title("Chatbot Application")
st.write("Ask any question and get an answer:")
 
# Input for user question
user_input = st.text_input("You:")
 
if user_input:
    try:
        # Generate SQL query from user input
        sql_query = gensql.generate_new_trial(user_input)
        st.write("Generated SQL Query:")
        st.code(sql_query, language='sql')
 
        # Execute the SQL query
        st.write("Executing query...")
        column_names, results = execute_sql_query(sql_query)
 
        if not results:
            st.warning("No results found.")
        else:
            # Display the query results in a DataFrame
            df = pd.DataFrame(results, columns=column_names)
            df_unique = df.drop_duplicates()
            st.write("Query Results:")
            st.table(df_unique)
 
            # Convert DataFrame to JSON
            results_json = df_unique.to_json(orient='records')
 
            # Save JSON to a file
            try:
                with open("query_results.json", "w") as f:
                    f.write(results_json)
                st.success("Query results saved to `query_results.json`")
            except Exception as file_error:
                st.error(f"Failed to save query results to a file: {file_error}")
 
            # Embed dendro.html in Streamlit
            try:
                with open("dendro.html", "r") as f:
                    html_content = f.read()
                html_content = html_content.replace("var data =[];", f"var data ={results_json};")
                components.html(html_content, height=500)
            except FileNotFoundError:
                st.error("dendro.html file not found. Ensure the file exists in the application directory.")
            except Exception as html_error:
                st.error(f"Error rendering dendro.html: {html_error}")
 
    except Exception as e:
        st.error(f"An error occurred during execution: {e}")
        st.write("Please verify your input or contact support.")
