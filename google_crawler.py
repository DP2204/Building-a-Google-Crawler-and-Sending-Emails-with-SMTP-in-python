# -*- coding: utf-8 -*-
"""HackVeda_Task-1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iajswf8Vz3uZhRVXzlDscT453Xce1MsA
"""

import pandas as pd  # Library for data manipulation and analysis
import requests      # Library to handle HTTP requests
import json          # Library to handle JSON data
import smtplib       # Library to handle email sending
from datetime import date , timedelta
from email.mime.multipart import MIMEMultipart  # For creating email messages
from email.mime.text import MIMEText            # For adding text content to emails
from email.mime.base import MIMEBase            # For adding attachments to emails
from email import encoders                      # For encoding email attachments
import re                                       # Library for regular expression operations

# Function to sanitize the filename by replacing non-alphanumeric characters with underscores
def sanitize_filename(keyword):
    return re.sub(r'\W+', '_', keyword)

# Function to perform the search and send the email
def smtp(keyword, to_email):

    # Define global variables to store questions and links
    question_list = []
    question_link = []

    # Store the original keyword for resetting later
    sanitized_keyword = sanitize_filename(keyword)  # Sanitize the keyword for filename

    # Define the list of sites to search
    site_list = ["quora.com"]
    for site in site_list:
        keyword = keyword + " site:" + site  # Append site restriction to the keyword

        # Construct the Google Custom Search API URL
        google_url = "https://www.googleapis.com/customsearch/v1?key= AIzaSyC220148BBm9m6uki2xQQCVBbeZnsDhmlI&cx=10292279b748d46e3"
        google_url = google_url + "&q=" + keyword  # Append the search query to the URL

        # Send a network request to Google
        res = requests.get(google_url)
        json_res = json.loads(res.text)  # Load the response as JSON

        try:
            # Loop through each item in the response
            for item in json_res["items"]:
                title = item["title"]
                link = item["link"]
                title = title.replace(" - Quora", "")  # Clean up the title
                question_list.append(title)  # Add title to question list
                question_link.append(link)  # Add link to link list
        except Exception as e:
            print("Exception", e)


    # Create a DataFrame with questions and links
    question_dict = {"Questions": question_list, "Links": question_link}
    df = pd.DataFrame(data=question_dict)

    # Convert links to clickable hyperlinks
    df['Links'] = df['Links'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    # Save DataFrame to HTML file with the sanitized keyword as the filename
    html_output = df.to_html(escape=False)
    html_filename = f"{sanitized_keyword}.html"
    with open(html_filename, "w") as file:
        file.write(html_output)

    # Email details
    from_email = 'dp809307@gmail.com'
    from_password = 'jlgg ddvq cahv zsuc '
    subject = keyword + " Questions and Links"
    body = 'Your requested search result ' + keyword + ' file is present in the attachment.'

    # Create a multipart email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Attach the HTML file
    with open(html_filename, 'rb') as attachment:                                       # Open the HTML file in binary read mode
        part = MIMEBase('application', 'octet-stream')                                  # Create a MIMEBase object for the attachment
        part.set_payload(attachment.read())                                             # Read the content of the file and set it as the payload
        encoders.encode_base64(part)                                                    # Encode the payload using base64 encoding
        part.add_header('Content-Disposition', f"attachment; filename={html_filename}") # Add a header to indicate the attachment
        msg.attach(part)                                                                # Attach the MIMEBase object to the email message

    # Send the email via Google's SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)                                     # Connect to Google's SMTP server
        server.starttls()                                                                # Start TLS for security
        server.login(from_email, from_password)                                          # Log in to the email account
        text = msg.as_string()                                                           # Convert the message to a string
        server.sendmail(from_email, to_email, text)                                      # Send the email
        print(f'Your search result has been mailed to you successfully.')
    except Exception as e:
        print(f'Failed to send email. Error: {e}')
    finally:
        server.quit()  # Close the connection to the SMTP server

# Example usage
if __name__ == "__main__":
    # Take input from the user
    search_query = input("Enter the keyword to search for: ")
    reci_email = input("Enter the email address: ")

    # Perform the search and send the email
    smtp(search_query, reci_email)