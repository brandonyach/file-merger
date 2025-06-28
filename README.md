# File Merger Tool

The File Merger Tool is a Python/Streamlit web application designed to streamline data merging for non-technical users. It enables merging of CSV or Excel files using exact, fuzzy, or cross (Cartesian product) joins on multiple columns, replacing manual Excel or spreadsheet workflows with an intuitive interface. 

## Features
- **Flexible Merging**: Supports exact (left, inner, outer, right, anti), fuzzy (fuzzy, fuzzy anti), and cross merges.
- **Multiple Join Columns**: Join on one or more columns (e.g., First Name + Last Name).
- **Fuzzy Matching**: Matches similar values (e.g., ‘Alice’ ≈ ‘Alice Brown’) with adjustable thresholds.
- **Cross Merge**: Generates all possible row combinations (Cartesian product).
- **User-Friendly UI**:
  - Previews first 10 rows of uploaded files.
  - Select merge type first, with clear descriptions for each type.
  - Choose File 2 columns to drop for customized output.
- **Security**: No persistent data storage, ready for SSO and HTTPS integration.

## Installation

### Prerequisites
- Python 3.12+
- Git
- Docker (optional for containerized deployment)

### Local Setup
```bash
git clone https://github.com/your-username/file-merger-tool.git
cd file_merger_tool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
streamlit run main.py
```

## Usage
1. Upload two CSV or Excel files via the web interface.
2. Select a merge type (e.g., left, fuzzy, cross) from the left column.
3. Choose join columns (if not cross) and File 2 columns to drop.
4. Adjust fuzzy threshold for fuzzy merges (50-100).
5. Click “Merge Files” to preview and download results.

See `docs/user_guide.md` for detailed instructions.

## Deployment

### Local/Development
Run locally with `streamlit run main.py`.

### Streamlit Community Cloud 
- Deployed at [Private Link, insert after deployment].
- Note: Prototype only; internal deployment recommended for production.


## Documentation
- `docs/user_guide.md`: End-user instructions.
- `docs/security_plan.md`: Security and compliance details.

## Contributing
- Fork the repository and submit pull requests for enhancements.
- Report issues or suggestions within GitHub Issues.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
- **Maintainer**: Brandon Yach
- **Support**: Submit issues on GitHub.