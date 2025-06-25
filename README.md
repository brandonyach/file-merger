# File Merger Tool

The File Merger Tool is a Python/Streamlit web application designed to streamline data merging for non-technical users. It enables merging of CSV or Excel files using exact, fuzzy, or cross (Cartesian product) joins on multiple columns, replacing manual Excel workflows with an intuitive interface. Ideal for tasks like reconciling inventory, customer records, or project assignments, the tool offers previews, customizable outputs, and robust security features.

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
- **Testing**: 6 passing unit tests ensure reliability.

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

Access at `http://localhost:8501`.

### Docker Setup
```bash
docker-compose up --build
```

Access at `http://localhost:8501`.

## Usage
1. Upload two CSV or Excel files via the web interface.
2. Select a merge type (e.g., left, fuzzy, cross) from the left column.
3. Choose join columns (if not cross) and File 2 columns to drop.
4. Adjust fuzzy threshold for fuzzy merges (50-100).
5. Click “Merge Files” to preview and download results.

See `docs/user_guide.md` for detailed instructions.

## Testing
Run unit tests to verify merge functionality:
```bash
./scripts/run_tests.sh
```

Expected: 6 tests pass, covering exact, fuzzy, and cross merges.

## Deployment

### Local/Development
Run locally with `streamlit run main.py`.

### Streamlit Community Cloud (Demo)
- Deployed at [Private Link, insert after deployment].
- Access: Contact [Your Name] for private sharing.
- Note: Prototype only; internal deployment recommended for production.

### Production
- **Recommended**: Internal server or cloud (e.g., AWS EC2, Azure App Service).
- **Security**: Integrate SSO (e.g., Azure AD), HTTPS, VPN access.
- **Scale**: Supports 10-20 initial users, scalable.
- See `docs/security_plan.md` for details.

## Documentation
- `docs/user_guide.md`: End-user instructions.
- `docs/security_plan.md`: Security and compliance details.

## Contributing
- Fork the repository and submit pull requests for enhancements.
- Report issues or suggestions to [Your Email].
- Coordinate with IT for production deployment changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
- **Maintainer**: [Your Name] ([Your Email])
- **Support**: Contact [Your Email] or submit issues on GitHub.