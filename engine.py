import logging
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build


EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
SERVICE_ACCOUNT_FILE = ''


logging.basicConfig(filename='error_log.log', level=logging.ERROR)

def start_vocab_app():
  SHEET_ID = ""
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
  credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  service = build('sheets', 'v4', credentials=credentials)
  SHEET_RANGE = ""
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SHEET_ID, range=SHEET_RANGE).execute()
  values = result.get('values', [])
  recipients = dict()
  for item in values[1:]:
    recipients[item[0]] = [thing for thing in item [1:] ]

  for email , features in recipients.items():
    try:
      if (features[-1]).lower() == "no" :
        
        words = read_google_doc(features[0])
        email_body = create_email_body(words)
        send_email(email, email_body)
      
        if features[1] != '.':
          counting_words(words, features[1])

      else:
         continue
      
    except Exception as e:
      logging.error(f"Errore per il destinatario {email}: {e}")
      print(f"Errore con {email}. Passo al destinatario successivo.")
      continue  
  
def counting_words(words, SHEET_ID):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    SHEET_RANGE = ""
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=SHEET_RANGE).execute()
    values = result.get('values', [])
    my_dict = {row[0]: row for row in values[1:]}  

    modified_values = [values[0]]  
    english_terms = list()

    for terms in words:
        english_terms.append(terms[0])
    
    for row in values[1:]:
        if row[0] in english_terms:
            row[1] = str(int(row[1]) + 1)
        modified_values.append(row)

    for word in english_terms:
        if word not in my_dict:
            modified_values.append([word, '1'])

    body = {'values': modified_values}

    result = service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=SHEET_RANGE,
        valueInputOption="RAW",
        body=body
    ).execute()

def read_google_doc(DOCUMENT_ID):
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
    wordstosend = 
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('docs', 'v1', credentials=credentials)

    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    content = doc.get('body').get('content')

    text = ""
    for element in content:
        if 'paragraph' in element:
            elements = element.get('paragraph').get('elements')
            for elem in elements:
                text_run = elem.get('textRun')
                if text_run:
                    text += text_run.get('content')

    lines = text.strip().split('\n')
    term_list = []
    
    for line in lines:
        if '|||' in line:
            term, meaning = line.split('|||')
            term_list.append([term.strip(), meaning.strip()])

    number = min(len(term_list), wordstosend)
    random.shuffle(term_list)
    return random.sample(term_list, number)

def create_email_body(words):
    word_html = "".join(
        f"<div style='text-align: center; margin: 10px 0; font-size: 24px;'><strong>{word_pair[0]} : {word_pair[1]}</strong></div>"
        for word_pair in words
    )

    return f"""
    <html>
    <head>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f9f9f9;
          padding: 20px;
        }}
        h1 {{
          color: #4A90E2;
          text-align: center;
          margin-bottom: 10px;
        }}
        h2 {{
          color: #333;
          text-align: center;
          margin-bottom: 20px;
        }}
        p {{
          font-size: 16px;
          line-height: 1.5;
        }}
        .container {{
          max-width: 600px;
          margin: 0 auto;
          background-color: #fff;
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }}
        .footer {{
          text-align: center;
          margin-top: 20px;
          font-size: 14px;
          color: #888;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Daily Vocabulary</h1>
        <h2>Here are the words for today!</h2>
        {word_html}
        <div class="footer">
          <p>Keep Learning!</p>
          <p style='font-style: italic;'>Mail sent automatically. Please do not respond.</p>
        </div>
      </div>
    </body>
    </html>
    """

def send_email(EMAIL_DESTINATION, email_body):
    msg = MIMEMultipart()
    msg['Subject'] = 'Daily Vocabulary'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_DESTINATION
    msg.attach(MIMEText(email_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f'Email inviata a {EMAIL_DESTINATION}')
    except Exception as e:
        
        logging.error(f"Errore nell'invio dell'email a {EMAIL_DESTINATION}: {e}")
        print(f"Errore nell'invio dell'email a {EMAIL_DESTINATION}: {e}")

