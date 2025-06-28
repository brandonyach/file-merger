import streamlit as st
import pandas as pd
import io
from pathlib import Path
from src.utils.data_processing import load_file, merge_dataframes

def run_app():
    # Set page configuration
    st.set_page_config(page_title="File Merger Tool", layout="wide")
    st.title("File Merger Tool")
    st.markdown("""
    Merge two files (CSV or Excel) by joining on one or more columns or creating a Cartesian product. 
    This tool combines data from any two lists, such as inventories, customer records, or project data. 
    Choose a merge type, including exact matches (left, inner, outer, right, anti), fuzzy matches 
    (fuzzy, fuzzy anti), or a cross merge for all combinations. Select columns from File 2 to drop 
    to customize the output.
    """)

    # File upload section
    st.subheader("Upload Files")
    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("Upload File 1", type=["csv", "xlsx"], key="file1_upload")
    with col2:
        file2 = st.file_uploader("Upload File 2", type=["csv", "xlsx"], key="file2_upload")

    # Initialize session state for dataframes
    if 'df1' not in st.session_state:
        st.session_state.df1 = None
    if 'df2' not in st.session_state:
        st.session_state.df2 = None

    # Process uploaded files
    if file1:
        try:
            st.session_state.df1 = load_file(file1)
            with col1:
                st.success(f"Loaded File 1: {file1.name} ({len(st.session_state.df1)} rows)")
                st.write("File 1 Preview (First 10 Rows)")
                st.dataframe(st.session_state.df1.head(10))
        except Exception as e:
            with col1:
                st.error(f"Error loading File 1: {str(e)}")

    if file2:
        try:
            st.session_state.df2 = load_file(file2)
            with col2:
                st.success(f"Loaded File 2: {file2.name} ({len(st.session_state.df2)} rows)")
                st.write("File 2 Preview (First 10 Rows)")
                st.dataframe(st.session_state.df2.head(10))
        except Exception as e:
            with col2:
                st.error(f"Error loading File 2: {str(e)}")

    # Merge configuration section
    if st.session_state.df1 is not None and st.session_state.df2 is not None:
        
        st.subheader("Configure Merge")
        col5, col3, col4 = st.columns([1, 2, 2])
        
        with col5:
            st.write("Merge Type")
            merge_type = st.selectbox("Select Merge Type", ["left", "inner", "outer", "right", "anti", "fuzzy", "fuzzy anti", "cross"], index=0, key="merge_type_select")
            if merge_type == "left":
                st.info("Left Join: Keep all rows from File 1, adding matching File 2 data; non-matches get null values.")
            elif merge_type == "inner":
                st.info("Inner Join: Keep only rows where File 1 and File 2 match on selected columns.")
            elif merge_type == "outer":
                st.info("Outer Join: Keep all rows from both files, with nulls for non-matching rows.")
            elif merge_type == "right":
                st.info("Right Join: Keep all rows from File 2, adding matching File 1 data; non-matches get null values.")
            elif merge_type == "anti":
                st.info("Anti Join: Keep rows from File 1 with no exact match in File 2 on selected columns.")
            elif merge_type == "fuzzy":
                st.info("Fuzzy Join: Match rows with similar values across selected columns (e.g., ‘Alice’ ≈ ‘Alice Brown’).")
            elif merge_type == "fuzzy anti":
                st.info("Fuzzy Anti-Join: Keep rows from File 1 with no similar match in File 2 on selected columns.")
            elif merge_type == "cross":
                st.info("Cross Join: Combine every row from File 1 with every row from File 2 (Cartesian product). Join columns are ignored.")

        # Join columns selection (hidden for cross merge)
        if merge_type != "cross":
            with col3:
                st.write("File 1 Join Columns")
                col1_list = st.multiselect("Select columns from File 1", st.session_state.df1.columns, key="col1_select")
            with col4:
                st.write("File 2 Join Columns")
                col2_list = st.multiselect("Select columns from File 2", st.session_state.df2.columns, key="col2_select")
        else:
            col1_list, col2_list = [], []

        # File 2 columns to drop
        with col4:
            df2_columns = [col for col in st.session_state.df2.columns if col not in col2_list]
            drop_df2_cols = st.multiselect(
                "Select File 2 Columns to Drop",
                df2_columns,
                default=[],
                key="drop_df2_cols"
            )
            selected_df2_cols = [col for col in df2_columns if col not in drop_df2_cols]
        
        # Fuzzy threshold for fuzzy merges
        if merge_type in ["fuzzy", "fuzzy anti"]:
            fuzzy_threshold = st.slider("Fuzzy Join Threshold", min_value=50.0, max_value=100.0, value=90.0, step=0.1, key="fuzzy_threshold")
            st.caption("Controls how similar values must be to match (0-100). Higher values require closer matches (e.g., ‘Alice’ ≈ ‘Alice Brown’).")
        else:
            fuzzy_threshold = 90.0
        
        # Validate join columns
        if merge_type != "cross" and col1_list and col2_list and len(col1_list) != len(col2_list):
            st.error("Error: Select the same number of join columns for File 1 and File 2.")
            return
        
        # Perform merge when button is clicked
        if st.button("Merge Files", key="merge_button"):
            if merge_type != "cross" and (not col1_list or not col2_list):
                st.error("Error: Please select at least one join column for each file.")
                return
            
            try:
                result, merge_summary = merge_dataframes(
                    st.session_state.df1,
                    st.session_state.df2,
                    col1_list,
                    col2_list,
                    selected_df2_cols,
                    merge_type,
                    file1.name.endswith('.csv'),
                    fuzzy_threshold=fuzzy_threshold
                )
                
                # Convert result to DataFrame for preview
                if file1.name.endswith('.csv'):
                    df_merged = pd.read_csv(io.StringIO(result.decode('utf-8')))
                else:
                    df_merged = pd.read_excel(io.BytesIO(result))
                
                # Generate output file name
                file1_stem = Path(file1.name).stem
                file2_stem = Path(file2.name).stem
                output_filename = f"{file1_stem}_{file2_stem}{'.csv' if file1.name.endswith('.csv') else '.xlsx'}"
                
                # Display preview
                st.subheader("Merged Data Preview")
                if df_merged.empty:
                    st.warning("No records found after merging.")
                else:
                    st.dataframe(df_merged.head(10))
                    st.write(f"Total rows in merged file: {len(df_merged)}")
                
                # Provide download
                st.download_button(
                    label="Download Merged File",
                    data=result,
                    file_name=output_filename,
                    mime="text/csv" if file1.name.endswith('.csv') else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_button"
                )
                
                # Display merge summary
                if merge_summary:
                    st.write("Merge Summary:")
                    for category, count in merge_summary.items():
                        st.write(f"- {category}: {count} rows")
                
            except Exception as e:
                st.error(f"Error during merge: {str(e)}")
    else:
        if file1 or file2:
            st.warning("Please upload both files to proceed with the merge.")