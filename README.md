# Template ML Project

A comprehensive Python project framework for machine learning research and experimentation. This project provides a structured template for building, training, and evaluating machine learning models with integrated logging, configuration management, and data handling utilities.

## Overview

**Template ML Project** is designed as a scalable foundation for machine learning experimentation and model development. It combines modern ML libraries (PyTorch, scikit-learn, LightGBM) with financial data tools (yfinance, pandas-datareader) and time-series analysis capabilities (statsmodels, pandas-ta).

**Version:** 0.1.0  
**Python:** ≥3.13

## Features

- **Modular Architecture**: Organized directory structure for datasets, models, training logic, and utilities
- **Integrated Logging**: Centralized logging configuration with JSON templates
- **Project Scaffolding**: Automated project structure builder via YAML configuration
- **ML Ready**: Pre-configured with PyTorch, scikit-learn, and LightGBM
- **Financial Data**: Built-in support for yfinance and pandas-datareader
- **Time Series Analysis**: Statsmodels and pandas-ta for advanced analysis
- **Testing Framework**: Pre-configured test directory for unit tests

## Project Structure

```
template_ml_project/
├── src/                          # Main source code
│   ├── __init__.py
│   ├── models/                   # Model implementations
│   │   └── __init__.py
│   ├── dataset/                  # Data loading and preprocessing
│   │   └── __init__.py
│   ├── train/                    # Training scripts and logic
│   │   └── __init__.py
│   └── utils/                    # Utility functions and helpers
│       └── __init__.py
├── data/                         # Data files (raw, processed)
├── configs/                      # Configuration files
│   └── logging/                  # Logging configuration (generated)
├── resources/                    # Static resources
├── logs/                         # Application logs (generated)
├── test/                         # Unit tests
│   └── __init__.py
├── main.py                       # Entry point
├── project_builder.py            # Project structure generator
├── project_structure.yaml        # Structure definition
├── pyproject.toml                # Project metadata and dependencies
└── README.md                     # This file
```

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   cd forecast_lab
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```
   Or with uv:
   ```bash
   uv sync
   ```

### Initialize Project Structure

The project includes a builder to generate the directory structure from a YAML configuration:

```bash
python project_builder.py project_structure.yaml
```

This will:
- Create all directories defined in `project_structure.yaml`
- Generate placeholder files
- Set up logging configuration at `configs/logging/logging_config.json`

### Running the Application

```bash
python main.py
```

## Key Components

### `project_builder.py`

Automated project scaffolding tool that reads a YAML specification and generates the complete directory structure.

**Key Functions:**
- `read_yaml_file(file_path)` - Load and parse YAML configuration
- `create_directory(directory_path)` - Create directories with parent path creation
- `create_empty_file(file_path)` - Create placeholder files
- `setup_logging(log_file_path, root_log_level)` - Generate logging configuration
- `main(file_path)` - Orchestrate the build process

**Example Usage:**
```python
from project_builder import main
main("project_structure.yaml")
```

### `project_structure.yaml`

YAML-based configuration file defining:
- Project metadata (name, version, description)
- Directory hierarchy with file/folder types
- Logging configuration (level, log file path)

**Structure:**
```yaml
project:
  name: "template-ml-project"
  version: "0.1.0"
  description: "Your project description"

directories:
  - name: src
    type: directory
    children:
      - name: models
        type: directory
      - name: __init__.py
        type: file

logging:
  root_log_level: INFO
  log_file_path: logs/forecast-lab.log
```

## Dependencies

### Core Data Science & ML
- **PyTorch** (≥2.9.1) - Deep learning framework
- **scikit-learn** (≥1.8.0) - Classical ML algorithms
- **LightGBM** (≥4.6.0) - Gradient boosting
- **NumPy** (≥2.2.6) - Numerical computing
- **Pandas** (≥2.3.3) - Data manipulation
- **SciPy** (≥1.16.3) - Scientific computing

### Time Series & Financial Data
- **Statsmodels** (≥0.14.6) - Statistical modeling
- **pandas-ta** (≥0.4.71b0) - Technical analysis
- **yfinance** (≥0.2.66) - Yahoo Finance data
- **pandas-datareader** (≥0.10.0) - Web data reading

### Visualization & NLP
- **Matplotlib** (≥3.10.7) - Plotting
- **Seaborn** (≥0.13.2) - Statistical visualization
- **Transformers** (≥4.57.3) - HuggingFace NLP models

### Development
- **Ruff** (≥0.14.8) - Fast Python linter

## Development Workflow

### Running Tests

```bash
python -m pytest test/
```

### Code Quality

Check code with Ruff:
```bash
ruff check src/ test/
ruff format src/ test/
```

### Logging

Configure logging via `configs/logging/logging_config.json` (auto-generated). The default configuration uses:
- Log Level: INFO
- Log File: `logs/template-ml-project.log`

## Configuration

All project configuration is defined in `project_structure.yaml`. To modify:

1. Edit `project_structure.yaml`
2. Run `python project_builder.py project_structure.yaml`
3. Adjust application code as needed

## Common Tasks

### Adding a New Module

1. Create a new directory under `src/`
2. Add `__init__.py` to make it a package
3. Implement your module
4. Update imports in `main.py` or other modules

### Working with Data

- Place raw data files in `data/`
- Use `src/dataset/` for data loading and preprocessing utilities
- Store processed data in `data/processed/` (create as needed)

### Model Development

- Implement model classes in `src/models/`
- Create training scripts in `src/train/`
- Use `src/utils/` for shared utilities (data pipelines, metrics, etc.)

## Troubleshooting

### Project Structure Not Created

Ensure:
- `project_structure.yaml` exists and is valid YAML
- Parent directories are created before files
- Proper read/write permissions in the target directory

### Import Errors

- Verify all `__init__.py` files are present in package directories
- Check `PYTHONPATH` includes the project root
- Install the project in development mode: `pip install -e .`

### Logging Configuration Issues

- Verify `configs/logging/` directory exists
- Check `logging_config_template.json` is present
- Ensure `logs/` directory exists or will be created

## Contributing

1. Create a feature branch
2. Make changes following PEP 8 (enforced by Ruff)
3. Write tests in `test/`
4. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or issues, please open an issue on the repository.
