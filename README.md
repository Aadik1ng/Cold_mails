# Internship Inquiry Automation Script

This script automates the process of extracting email addresses and descriptions from a PDF file, generating custom cover letters using the Ollama API, and sending these cover letters along with a resume via email. 

## Prerequisites

1. **Python 3.7+**
2. **Required Python Packages**:
    - `requests`
    - `PyPDF2`
    - `smtplib`
    - `email`

You can install the necessary Python packages using the following command:

\`\`\`sh
pip install requests PyPDF2
\`\`\`

## Configuration

1. **PDF Path**:
    - Update the `pdf_path` variable in the script to point to the PDF file containing email addresses and descriptions.

2. **Resume Path**:
    - Update the `resume_path` variable in the script to point to the PDF file of your resume.

3. **Email Credentials**:
    - Update the `from_email` and `from_password` variables with your email address and password. 
    - If you are using Gmail, ensure that you have enabled "Less secure app access" in your Google account settings or use an App Password.

4. **Ollama API**:
    - Ensure the Ollama API is running locally and accessible at `http://localhost:11434/api/generate`.

## Script Overview

1. **Extract Emails and Descriptions**:
    - The `extract_emails_and_descriptions_from_pdf` function reads the PDF file and extracts email addresses along with their corresponding descriptions.

2. **Generate Cover Letter**:
    - The `generate_cover_letter` function uses the Ollama API to generate a custom cover letter based on the extracted description.

3. **Send Email**:
    - The `send_email` function sends the generated cover letter along with the resume to the extracted email address.

4. **Main Function**:
    - The `main` function orchestrates the extraction, cover letter generation, and email sending process.

## How to Run

1. Ensure all configurations are updated.
2. Run the script using the following command:

\`\`\`sh
python script_name.py
\`\`\`

Replace `script_name.py` with the actual name of the script file.

## Notes

- The script currently stops after sending the first email. If you wish to send emails to all extracted addresses, comment out or remove the `break` statement in the `main` function.
- Ensure your email service provider allows SMTP access and you have the correct credentials.

## Troubleshooting

- **Failed to Generate Cover Letter**: Ensure the Ollama API is running and accessible at the specified endpoint.
- **Failed to Send Email**: Verify your email credentials and ensure SMTP access is enabled for your email account.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.