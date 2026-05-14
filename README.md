# Post Naukri Gulf

A Python automation script that fetches job postings from the Jobvite API and posts them to Naukri Gulf automatically.

## Features

- Fetches open job requisitions from Jobvite API
- Filters jobs marked for posting to job boards
- Automatically posts jobs to Naukri Gulf with generated signatures
- Logs results to an Excel file for tracking

## Prerequisites

- Python 3.7+
- Jobvite API access
- Naukri Gulf API credentials

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd post-naukri-gulf
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env` (if provided) or create `.env` file
   - Update the variables with your actual API credentials

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Jobvite API headers
X_JVI_API=your_jobvite_api_key
X_JVI_SC=your_jobvite_sc_key
X_COMPANY_ID=your_company_id

# Jobvite API params
JOB_STATUS=Open
LOC_COUNTRY=United Arab Emirates
START=1
COUNT=500

# Naukri Gulf API keys
SECRET_KEY=your_secret_key
ACCESS_KEY=your_access_key
APP_ID=1
SYSTEM_ID=1
```

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Fetch job requisitions from Jobvite
2. Process each job marked for external posting
3. Generate required signatures
4. Post jobs to Naukri Gulf
5. Log results to `naukri_log.xlsx`

## Logging

Results are logged to `naukri_log.xlsx` with two sheets:
- **Success**: Successfully posted jobs
- **Error**: Failed job postings with error details

Each log entry includes:
- Timestamp
- Job title
- Job ID
- Status
- Response details

## Security

- Never commit the `.env` file to version control
- Keep API keys and secrets secure
- Use environment variables for all sensitive data

## Dependencies

- `requests`: HTTP requests
- `openpyxl`: Excel file handling
- `python-dotenv`: Environment variable loading

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]