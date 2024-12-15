# Student Portal IPB Log Book Bot

This script automates the process of inputting data into the Student Portal of IPB University for log book entries. It uses Selenium for web automation and allows users to provide configuration and input data through JSON and Excel files.

## Prerequisites

Make sure you have the following installed on your system:

1. **Python** (>=3.8)
2. **Microsoft Edge** (with WebDriver compatible with your browser version)

## Installation

1. Clone the repository or download the script.
2. Install the required Python dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the script, create a `config.json` file in the same directory as the script with the following format:

```json
{
    "EXCEL_FILE": "input.xlsx",
    "SHEET_NAME": "sample",
    "USERNAME": "your_username",
    "PASSWORD": "your_password"
}
```

- `EXCEL_FILE`: Path to the Excel file containing the data.
- `SHEET_NAME`: Name of the sheet in the Excel file.
- `USERNAME`: Your Student Portal username.
- `PASSWORD`: Your Student Portal password.

## Input Data Format

The input Excel file should have columns corresponding to the following fields:

- **date**: The date of the activity.
- **time_start**: Start time of the activity.
- **time_end**: End time of the activity.
- **activity**: Type of activity (Bimbingan, Ujian, Kegiatan).
- **lecturer**: Lecturer’s name (unused for now).
- **mentoring**: Type of mentoring (Hybrid, Offline, Online).
- **location**: Location of the activity.
- **description**: Additional description of the activity.
- **proof**: Proof of the activity (unused for now).

Column headers should be prefixed with `#` followed by the field name (e.g., `#date`, `#time_start`).

## Usage

1. Launch the script by running:

   ```bash
   python main.py
   ```

2. Log in to the Student Portal:
   - The script will open a browser and navigate to the Student Portal login page.
   - Enter your username and password from the `config.json` file automatically.

3. Navigate to the appropriate activity page manually. When ready, press Enter to continue the automation process.

4. The script will process and input all data from the Excel file.

## Notes

- Ensure the Student Portal is accessible before running the script.
- If an error occurs, check the browser logs or console output to debug issues.
- Customize the default values for activity, mentoring type, and other fields directly in the script if needed.

## Dependencies

This script uses the following libraries:

- `pandas`: For reading and processing Excel files.
- `selenium`: For browser automation.
- `time`: For handling delays in the automation process.

To install these dependencies, use the `requirements.txt` provided.

## License

This project is open source and free to use. Modify it as needed for your requirements.