# EmailAPP
EmailAPP using IMAP, POP3 and SMTP.
A Python application for managing emails via SMTP, IMAP, and POP3 protocols, with a modern graphical interface.

## Project Structure
The project consists of two main files:  
`main.py` - The client application source code  

## Requirements ⚙️
- Python 3.7+  
- Python modules:  
`tkinter, smtplib, imaplib, poplib, email`

## Installation 🛠️
Clone the repository

#Configuration ⚡
1. Enable access for less secure apps in your Google account:
Visit Security Settings
Turn on "Allow less secure apps"

2.  Update authentication credentials in the code:
`
EMAIL = "your_email@gmail.com"  # Replace with your email
PASSWORD = "app_specific_password"  # Use an app-specific password
`

## Usage 🖥️
Send Email ✉️
Select the 📤 Send Email tab.
Fill in the fields:
To: Recipient's email address
Reply-To (optional): Reply address
Subject: Email subject
Write your message in the large text box.

For attachments:
Click 📁 Choose File
Select the desired file
Click ✈️ Send Email to send.
Check Inbox 📥

For IMAP:
Select the 📥 Inbox IMAP tab.
Click 🔄 Refresh to load messages.
The latest 20 emails will appear in the list.
Attachments are displayed in the table below.

For POP3:
Select the 📥 Inbox POP3 tab.
Click 🔄 Refresh to update.
If no emails exist, you will see "Inbox POP3 is empty".
The latest 5 emails with attachments appear in the table.

## Attachment Management 📎
Received files are automatically saved in the attachments folder.
File locations are shown in the File column of the tables.

## Limitations 🚧
Works only with Gmail accounts.
Emails are displayed in plain text format only.
Limited to 5 emails for POP3 and 20 for IMAP.
Does not support sending to multiple recipients.

#👨💻 Author
Name: Caracuianu Mihail
Group: TI-221
Technical University of Moldova
Lab #5 – Network Programming
