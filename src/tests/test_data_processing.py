import pytest
import pandas as pd
from src.utils.data_processing import merge_dataframes
import io

def test_merge_dataframes_anti_join():
    df1 = pd.DataFrame({
        'id': ['T001', 'T002', 'T003'],
        'name': ['Alice Brown', 'Bob Smith', 'Charlie']
    })
    df2 = pd.DataFrame({
        'employee_id': ['E001', 'E002'],
        'name': ['Alice Brown', 'Bob Smith'],
        'dept': ['IT', 'HR']
    })
    
    result, summary = merge_dataframes(
        df1, df2, ['name'], ['name'], ['dept'], 'anti', True
    )
    result_df = pd.read_csv(io.StringIO(result.decode('utf-8')))
    
    assert len(result_df) == 1
    assert result_df['name'].iloc[0] == 'Charlie'
    assert summary.get('Left Only', 0) == 1

def test_merge_dataframes_left_join():
    df1 = pd.DataFrame({
        'id': ['T001', 'T002'],
        'name': ['Alice Brown', 'Bob Smith']
    })
    df2 = pd.DataFrame({
        'employee_id': ['E001'],
        'name': ['Alice Brown'],
        'dept': ['IT']
    })
    
    result, summary = merge_dataframes(
        df1, df2, ['name'], ['name'], ['dept'], 'left', True
    )
    result_df = pd.read_csv(io.StringIO(result.decode('utf-8')))
    
    assert len(result_df) == 2
    assert summary.get('Both', 0) == 1
    assert summary.get('Left Only', 0) == 1

def test_merge_dataframes_fuzzy_join():
    df1 = pd.DataFrame({
        'id': ['T001', 'T002', 'T003'],
        'name': ['Alice', 'Bob', 'Charlie']
    })
    df2 = pd.DataFrame({
        'employee_id': ['E001', 'E002'],
        'name': ['Alice Brown', 'Bob Smith'],
        'dept': ['IT', 'HR']
    })
    
    result, summary = merge_dataframes(
        df1, df2, ['name'], ['name'], ['dept'], 'fuzzy', True, fuzzy_threshold=80.0
    )
    result_df = pd.read_csv(io.StringIO(result.decode('utf-8')))
    
    assert len(result_df) == 3
    assert summary.get('Both', 0) >= 2
    assert result_df[result_df['name'] == 'Charlie']['_merge'].iloc[0] == 'Left Only'

def test_merge_dataframes_fuzzy_anti_join():
    df1 = pd.DataFrame({
        'id': ['T001', 'T002', 'T003'],
        'name': ['Alice', 'Bob', 'Charlie']
    })
    df2 = pd.DataFrame({
        'employee_id': ['E001', 'E002'],
        'name': ['Alice Brown', 'Bob Smith'],
        'dept': ['IT', 'HR']
    })
    
    result, summary = merge_dataframes(
        df1, df2, ['name'], ['name'], ['dept'], 'fuzzy anti', True, fuzzy_threshold=80.0
    )
    result_df = pd.read_csv(io.StringIO(result.decode('utf-8')))
    
    assert len(result_df) == 1
    assert result_df['name'].iloc[0] == 'Charlie'
    assert summary.get('Left Only', 0) == 1

def test_merge_dataframes_multi_column_join():
    df1 = pd.DataFrame({
        'id': ['T001', 'T002', 'T003'],
        'first_name': ['Alice', 'Bob', 'Charlie'],
        'last_name': ['Brown', 'Smith', 'Wilson']
    })
    df2 = pd.DataFrame({
        'employee_id': ['E001', 'E002'],
        'given_name': ['Alice B.', 'Bob'],
        'surname': ['Brown', 'Smith'],
        'dept': ['IT', 'HR']
    })
    
    result, summary = merge_dataframes(
        df1, df2, ['first_name', 'last_name'], ['given_name', 'surname'], ['dept'], 'fuzzy', True, fuzzy_threshold=80.0
    )
    result_df = pd.read_csv(io.StringIO(result.decode('utf-8')))
    
    assert len(result_df) == 3
    assert summary.get('Both', 0) >= 2
    assert result_df[result_df['first_name'] == 'Charlie']['_merge'].iloc[0] == 'Left Only'

def test_merge_dataframes_cross():
    df1 = pd.DataFrame({
        'id': ['T001', 'T002'],
        'name': ['Alice', 'Bob']
    })
    df2 = pd.DataFrame({
        'employee_id': ['E001'],
        'dept': ['IT']
    })
    
    result, summary = merge_dataframes(
        df1, df2, [], [], ['dept'], 'cross', True
    )
    result_df = pd.read_csv(io.StringIO(result.decode('utf-8')))
    
    assert len(result_df) == 2  # 2 * 1
    assert result_df['dept'].tolist() == ['IT', 'IT']
    assert summary.get('Both', 0) == 2