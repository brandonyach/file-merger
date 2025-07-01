# File Merger Tool User Guide

## Introduction

The **File Merger Tool** is a web-based application for combining two data files (CSV or Excel) using exact, fuzzy, or cross merges on one or more columns. Designed for tasks like reconciling inventory, customer records, or project assignments, it offers a user-friendly alternative to complex Excel formulas. Key features include file previews, customizable output by dropping File 2 columns, and secure, no-storage processing.

## Getting Started

### Access the Tool
- Open the web link provided by your team or visit the demo at: [https://file-merger-tool.streamlit.app](https://file-merger-tool.streamlit.app) (contact Brandon Yach for private access).
- Log in with company credentials if prompted.

### Prepare Your Files
- Use CSV or Excel format (`.csv` or `.xlsx`).
- For non-cross merges, ensure files have columns for matching (e.g., `ID`, `First Name`, `Last Name`).
- Example files are in the `data/sample/` directory.

## Using the Tool

### Step 1: Upload Files
1. **File 1**: Click “Upload File 1” to select your first file (e.g., `tasks.csv` with task IDs).
2. **File 2**: Click “Upload File 2” to select your second file (e.g., `staff.csv` with staff details).
3. Confirm loading via success messages (e.g., “Loaded File 1: tasks.csv (3 rows)”).
4. **Previews**: View the first 10 rows of each file below the upload boxes.

### Step 2: Configure the Merge
1. **Choose Merge Type** (left column):
   - **Left**: Keep all File 1 rows, adding matching File 2 data; non-matches get nulls.
   - **Inner**: Keep only rows where File 1 and File 2 match on selected columns.
   - **Outer**: Keep all rows from both files, with nulls for non-matches.
   - **Right**: Keep all File 2 rows, adding matching File 1 data; non-matches get nulls.
   - **Anti**: Keep File 1 rows with no exact match in File 2.
   - **Fuzzy**: Match rows with similar values (e.g., `Alice` ≈ `Alice Brown`).
   - **Fuzzy Anti**: Keep File 1 rows with no similar match in File 2.
   - **Cross**: Combine every File 1 row with every File 2 row (Cartesian product; join columns ignored).
   - **Default**: Left. A description appears for each type.
2. **Select Merge Columns** (if not Cross):
   - **File 1 Columns** (middle column): Choose one or more columns (e.g., `First Name`, `Last Name`).
   - **File 2 Columns** (right column): Choose the same number (e.g., `Given Name`, `Surname`).
   - Columns are paired in order (e.g., `First Name` with `Given Name`).
   - Hidden for cross merge, as columns are not used.
3. **Select File 2 Columns to Drop** (middle column):
   - Choose columns to exclude from File 2 (e.g., `Employee ID`).
   - All other non-merge columns are included by default.
4. **Fuzzy Threshold** (for fuzzy/fuzzy anti merges):
   - Adjust the similarity threshold (50-100, default 90).
   - Higher values require closer matches (e.g., `Alice` ≈ `Alice Brown`).

### Step 3: Merge and Download
1. Click **Merge Files**.
2. **Preview**: View the first 10 rows of the merged data.
3. **Summary**: See match counts (e.g., “Both: 2 rows”, “Left Only: 1 row”).
   - **Both**: Matched rows or cross merge combinations.
   - **Left Only**: File 1 rows without matches.
   - **Right Only**: File 2 rows without matches.
4. **Download**: Save the result as CSV or Excel, named `[File1]_[File2].extension` (e.g., `tasks_staff.csv`).

## Example

**Goal**: Create all possible task-department combinations.

**File 1 (`tasks.csv`)**:
```csv
task_id,project,first_name,last_name
T001,ProjectA,Alice,Brown
T002,ProjectB,Bob,Smith
```

**File 2 (`staff.csv`)**:
```csv
employee_id,given_name,surname,dept
E001,Alice B.,Brown,IT
E002,Bob,Smith,HR
```

**Settings**:
- **Merge Type**: Cross
- **File 2 Columns to Drop**: `employee_id`, `given_name`, `surname`

**Result (`tasks_staff.csv`)**:
```csv
task_id,project,first_name,last_name,dept,_merge
T001,ProjectA,Alice,Brown,IT,Both
T001,ProjectA,Alice,Brown,HR,Both
T002,ProjectB,Bob,Smith,IT,Both
T002,ProjectB,Bob,Smith,HR,Both
```

**Interpretation**: All tasks are paired with all departments.

## Tips
- **File Preparation**: Ensure consistent formats for merge columns.
- **Cross Merge**: No merge columns needed; focus on columns to drop.
- **Fuzzy Matching**: Adjust threshold for stricter or looser matches.
- **Errors**: Check file formats or contact support.
- **Practice**: Use `data/sample/` files to test.

## Support
- **Contact**: Brandon Yach (yachb35@gmail.com).