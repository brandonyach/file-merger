import pandas as pd
import io
from typing import Tuple, Optional, List, Union
from rapidfuzz import process, fuzz

def load_file(file: io.BytesIO) -> pd.DataFrame:
    """Load a CSV or Excel file into a pandas DataFrame."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    return pd.read_excel(file)

def merge_dataframes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    col1: Union[str, List[str]],
    col2: Union[str, List[str]],
    selected_df2_cols: List[str],
    merge_type: str,
    is_csv: bool,
    fuzzy_threshold: float = 90.0
) -> Tuple[bytes, Optional[dict]]:
    """Merge two DataFrames based on specified columns and merge type."""
    # Convert single columns to lists
    col1_list = [col1] if isinstance(col1, str) else col1
    col2_list = [col2] if isinstance(col2, str) else col2

    # Create copies to avoid modifying originals
    df1 = df1.copy()
    df2 = df2.copy()

    if merge_type == 'cross':
        # Cross join (Cartesian product)
        df_merged = df1.assign(key=1).merge(
            df2[selected_df2_cols].assign(key=1),
            on='key',
            how='outer'
        ).drop(columns=['key'])
        df_merged['_merge'] = 'Both'
    else:
        # Validate inputs for non-cross joins
        if len(col1_list) != len(col2_list):
            raise ValueError("Number of join columns must match for File 1 and File 2.")
        if not col1_list or not col2_list:
            raise ValueError("At least one join column must be specified for each file.")
        if not all(col in df1.columns for col in col1_list) or not all(col in df2.columns for col in col2_list):
            raise ValueError("Specified join columns not found in DataFrames.")

        if merge_type in ['fuzzy', 'fuzzy anti']:
            # Fuzzy matching on multiple columns
            matches = []
            # Combine columns into a single string for fuzzy matching
            if len(col2_list) > 1:
                df2_values = df2[col2_list].astype(str).agg(' '.join, axis=1).tolist()
                df1_values = df1[col1_list].astype(str).agg(' '.join, axis=1)
            else:
                df2_values = df2[col2_list[0]].astype(str).tolist()
                df1_values = df1[col1_list[0]].astype(str)

            # Initialize merge column
            df1['_merge'] = 'Left Only'
            df1['_match_index'] = -1

            for idx, val1 in df1_values.items():
                best_match = process.extractOne(val1, df2_values, scorer=fuzz.WRatio)
                if best_match and best_match[1] >= fuzzy_threshold:
                    match_idx = best_match[2]
                    df1.at[idx, '_merge'] = 'Both'
                    df1.at[idx, '_match_index'] = match_idx

            # Merge with df2 based on matches
            df_merged = df1.copy()
            matched_indices = df_merged[df_merged['_match_index'] != -1]['_match_index'].astype(int)
            if not matched_indices.empty:
                matched_data = df2[selected_df2_cols + col2_list].iloc[matched_indices]
                matched_data.index = df_merged[df_merged['_match_index'] != -1].index
                for col in selected_df2_cols + col2_list:
                    df_merged.loc[matched_data.index, col] = matched_data[col]

            # Clean up
            df_merged = df_merged.drop(columns=['_match_index'])

            if merge_type == 'fuzzy anti':
                df_merged = df_merged[df_merged['_merge'] == 'Left Only']
        else:
            # Standard merge (exact matching)
            df2_subset = df2[col2_list + selected_df2_cols].copy() if selected_df2_cols else df2[col2_list].copy()
            df_merged = df1.merge(
                df2_subset,
                left_on=col1_list,
                right_on=col2_list,
                how="left" if merge_type == "anti" else merge_type,
                indicator=True
            )
            df_merged['_merge'] = df_merged['_merge'].map({
                'both': 'Both',
                'left_only': 'Left Only',
                'right_only': 'Right Only'
            })
            if merge_type == "anti":
                df_merged = df_merged[df_merged['_merge'] == 'Left Only']
    
    # Generate merge summary
    merge_summary = df_merged['_merge'].value_counts().to_dict()
    
    # Prepare output for download
    if is_csv:
        output = io.StringIO()
        df_merged.to_csv(output, index=False)
        output.seek(0)
        return output.getvalue().encode('utf-8'), merge_summary
    else:
        output = io.BytesIO()
        df_merged.to_excel(output, index=False)
        output.seek(0)
        return output, merge_summary