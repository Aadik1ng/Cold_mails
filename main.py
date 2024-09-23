import re
import os
import requests  # Ensure you have requests installed
from PyPDF2 import PdfReader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import json
# Path to the PDF file and resume
pdf_path = r'.pdf' #you email Ids 
resume_path = r".pdf"  # Update this with the actual path of resume

# Read the PDF and extract email addresses with their descriptions
def extract_emails_and_descriptions_from_pdf(pdf_path):
    emails_and_descriptions = []
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text()
        if text:  # Ensure text is not None
            lines = text.splitlines()
            for line in lines:
                # Using regex to extract email and description based on expected format
                match = re.search(r'(?P<description>.+?)\s+(?P<email>\w+@\w+\.\w+)', line)
                if match:
                    description = match.group('description').strip()
                    email = match.group('email').strip()
                    emails_and_descriptions.append((email, description))
    return emails_and_descriptions

# Generate cover letter using Ollama API
def generate_cover_letter(email, description):
    prompt = f"Create a custom cover letter for {email.split('@')[0]} based on the following description: {description}. Include my name that is [Name] and currently I am [your description]. I have strong skills in [skills] .Dont mention anything more than this.Include all the tools that are used in industry in the before mentioned applications.{email.split('@')[0]} make sure mention their name from here.DONT PUT ANY TEMPLATES TO FILL IN SUCH AS ""[YOUR NAME]"" etc."
    #use your own prompt
  
    # Prepare the payload with model and prompt
    payload = {
        "model": "mistral", #desire LLM model
        "prompt": prompt
    }
    
    try:
        response = requests.post('http://localhost:11434/api/generate', json=payload, stream=True)
        response.raise_for_status()  # Raises an error for bad responses
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = line.decode('utf-8')
                    json_data = json.loads(data)
                    full_response += json_data.get('response', '')
                    144
                    # Check if the response is complete
                    if json_data.get('done', False):
                        break
                except json.JSONDecodeError:
                    return f'Failed to parse line: {data}'
        
        return full_response or 'Cover letter generation failed.'
    
    except requests.exceptions.HTTPError as http_err:
        return f'Failed to generate cover letter: {http_err}\nResponse content: {response.content.decode()}'
    except requests.exceptions.RequestException as e:
        return f'Failed to generate cover letter: {e}'


# Send email
def send_email(to_email, cover_letter, resume_path):
    from_email = ""  #  email address
    from_password = ""  #  password (You have to paste key here)
    subject = "Inquiry about Internship Opportunity"
    
    # Email setup
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(cover_letter, 'plain'))
    
    # Attach resume
    with open(resume_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(resume_path)}"')
        msg.attach(part)
    
    try:
        # SMTP server setup (example uses Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Main function
def main():
    emails_and_descriptions = extract_emails_and_descriptions_from_pdf(pdf_path)
    
    if emails_and_descriptions:
        for email, description in emails_and_descriptions:
            cover_letter = generate_cover_letter(email, description)
            send_email(email, cover_letter, resume_path)
            # Uncomment the next line if you want to stop after sending one email
            break 
    else:
        print("No email addresses found in the PDF.")

if __name__ == "__main__":
    main()
