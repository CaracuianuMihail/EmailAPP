import smtplib
import imaplib
import poplib
import email
import tkinter as tk
import os
from tkinter import ttk, filedialog, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

EMAIL = "caracuianu.mihail@gmail.com"
PASSWORD = "poad tomm fmti tfbz"

filename = None 

def send_email():
    global filename
    to_email = entry_to.get()
    reply_to = entry_reply_to.get()
    subject = entry_subject.get()
    body = text_body.get("1.0", tk.END)

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    if reply_to:
        msg.add_header('Reply-To', reply_to)
    msg.attach(MIMEText(body, 'plain'))

    if filename:
        with open(filename, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="%s"' % filename.split("/")[-1])
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        messagebox.showinfo("Succes", "Email sent successfully!")
        filename = None
        label_file.config(text="📎 No attachment", foreground="gray")
    except Exception as e:
        messagebox.showerror("Eroare", str(e))

def browse_file():
    global filename
    filename = filedialog.askopenfilename()
    if filename:
        label_file.config(text="📎 " + filename.split("/")[-1], foreground="#2C5F9E")

def save_attachment(part, folder="attachments"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = part.get_filename()
    if filename:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            f.write(part.get_payload(decode=True))
        return filepath
    return None

def fetch_emails_imap():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        typ, data = mail.search(None, "ALL")
        email_list_imap.delete(0, tk.END)
        tree_attachments_imap.delete(*tree_attachments_imap.get_children())
        messages = data[0].split()

        for num in messages[-20:]:
            typ, msg_data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            email_list_imap.insert(0, f"[IMAP] {msg['From']} | {msg['Subject']}")
            
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                filepath = save_attachment(part)
                if filepath:
                    tree_attachments_imap.insert("", 0, values=(msg['Subject'], os.path.basename(filepath)), tags=('clickable',))

        mail.logout()

    except Exception as e:
        messagebox.showerror("Eroare IMAP", str(e))

def fetch_emails_pop3():
    try:
        pop_conn = poplib.POP3_SSL('pop.gmail.com', 995)
        pop_conn.user(EMAIL)
        pop_conn.pass_(PASSWORD)
        status, messages, octets = pop_conn.list()        
        email_list_pop3.delete(0, tk.END)
        tree_attachments_pop3.delete(*tree_attachments_pop3.get_children())
        if not messages:
            messagebox.showinfo("Inbox POP3", "Inbox POP3 is empty.")
            pop_conn.quit()
            return
        for msg_num in messages[-5:]:
            msg_id = msg_num.decode().split()[0]
            response, lines, octets = pop_conn.retr(int(msg_id))
            msg_content = b"\r\n".join(lines).decode()
            msg = email.message_from_string(msg_content)
            
            email_list_pop3.insert(0, f"[POP3] {msg['From']} | {msg['Subject']}")
            
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                filepath = save_attachment(part)
                if filepath:
                    tree_attachments_pop3.insert("", 0, 
                        values=(msg['Subject'], os.path.basename(filepath)), 
                        tags=('clickable',)
                    )

        pop_conn.quit()

    except Exception as e:
        messagebox.showerror("Eroare POP3", str(e))

    except Exception as e:
        messagebox.showerror("Eroare POP3", str(e))

# ---------------------- INTERFACE  ----------------------
root = tk.Tk()
root.title("Laborator #5 - Email Client - ")
root.geometry("1100x800")
root.configure(bg="#F5F6F8")

style = ttk.Style()
style.theme_use("clam")

style.configure(".", font=("Segoe UI", 10), background="#F5F6F8")
style.configure("TNotebook.Tab", padding=(20, 5), font=("Segoe UI", 10, "bold"), background="#E3E6EA", foreground="#2C5F9E")
style.map("TNotebook.Tab", background=[("selected", "#FFFFFF")])

style.configure("TLabel", background="#F5F6F8", foreground="#2D3436")
style.configure("TButton", background="#2C5F9E", foreground="white", borderwidth=0)
style.map("TButton", background=[("active", "#1A4A7E")])

style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#2C5F9E", foreground="white")
style.configure("Treeview", rowheight=28, fieldbackground="#FFFFFF")
style.map("Treeview", background=[("selected", "#E3E6EA")])

style.configure("TEntry", fieldbackground="#FFFFFF", bordercolor="#CCD0D4", lightcolor="#CCD0D4")
style.configure("TLabelframe", background="#F5F6F8", bordercolor="#CCD0D4")

# Notebook
tabs = ttk.Notebook(root)
tab_send = ttk.Frame(tabs)
tab_imap = ttk.Frame(tabs)
tab_pop3 = ttk.Frame(tabs)
tabs.add(tab_send, text='📤 Send Email')
tabs.add(tab_imap, text='📥 Inbox IMAP')
tabs.add(tab_pop3, text='📥 Inbox POP3')
tabs.pack(expand=1, fill="both", padx=15, pady=15)

# ==================== Tab SEND Email ====================
frame_send = ttk.LabelFrame(tab_send, text=" Compose Email ", padding=(20, 15))
frame_send.pack(fill="both", expand=True, padx=15, pady=10)

rows = [
    ("To:", entry_to := ttk.Entry(frame_send, width=65)),
    ("Reply-To:", entry_reply_to := ttk.Entry(frame_send, width=65)),
    ("Subject:", entry_subject := ttk.Entry(frame_send, width=65)),
]

for i, (label_text, widget) in enumerate(rows):
    ttk.Label(frame_send, text=label_text).grid(row=i, column=0, sticky="w", pady=8)
    widget.grid(row=i, column=1, padx=15, pady=8, sticky="ew")

# Mesaj
ttk.Label(frame_send, text="Message:").grid(row=3, column=0, sticky="nw", pady=8)
text_body = tk.Text(frame_send, height=18, wrap="word", font=("Segoe UI", 10), bg="white", padx=10, pady=10)
text_body.grid(row=3, column=1, padx=15, pady=8, sticky="nsew")

# Atașament
attachment_frame = ttk.Frame(frame_send)
attachment_frame.grid(row=4, column=1, sticky="ew", pady=10)
label_file = ttk.Label(attachment_frame, text="📎 No attachment", foreground="#666666")
label_file.pack(side="left", padx=5)

# Butoane
button_frame = ttk.Frame(frame_send)
button_frame.grid(row=5, column=1, sticky="e", pady=15)
ttk.Button(button_frame, text="📁 Choose File", command=browse_file).pack(side="left", padx=8)
ttk.Button(button_frame, text="✈️ Send Email", command=send_email, style="Accent.TButton").pack(side="left", padx=8)

style.configure("Accent.TButton", background="#28A745", foreground="white")
style.map("Accent.TButton", background=[("active", "#218838")])

# ==================== Tab IMAP ====================
frame_imap = ttk.Frame(tab_imap)
frame_imap.pack(fill="both", expand=True, padx=15, pady=10)

# Header
header_imap = ttk.Frame(frame_imap)
header_imap.pack(fill="x", pady=5)
ttk.Button(header_imap, text="🔄 Refresh", command=fetch_emails_imap).pack(side="left", padx=5)

# Listă email-uri
email_list_imap = tk.Listbox(frame_imap, 
    height=14, 
    bg="white", 
    selectbackground="#E3E6EA",
    font=("Segoe UI", 10),
    activestyle="none"
)
email_list_imap.pack(fill="both", expand=True, pady=8)

# Tabel atașamente
tree_attachments_imap = ttk.Treeview(frame_imap, columns=("Subject", "File"), show="headings", height=8)
for col in ("Subject", "File"):
    tree_attachments_imap.heading(col, text=col)
    tree_attachments_imap.column(col, width=300 if col == "Subject" else 400)
tree_attachments_imap.pack(fill="both", expand=True, pady=10)

# ==================== Tab POP3 ====================
frame_pop3 = ttk.Frame(tab_pop3)
frame_pop3.pack(fill="both", expand=True, padx=15, pady=10)

# Structură identică cu IMAP
header_pop3 = ttk.Frame(frame_pop3)
header_pop3.pack(fill="x", pady=5)
ttk.Button(header_pop3, text="🔄 Refresh", command=fetch_emails_pop3).pack(side="left", padx=5)

email_list_pop3 = tk.Listbox(frame_pop3, 
    height=14, 
    bg="white", 
    selectbackground="#E3E6EA",
    font=("Segoe UI", 10),
    activestyle="none"
)
email_list_pop3.pack(fill="both", expand=True, pady=8)

tree_attachments_pop3 = ttk.Treeview(frame_pop3, columns=("Subject", "File"), show="headings", height=8)
for col in ("Subject", "File"):
    tree_attachments_pop3.heading(col, text=col)
    tree_attachments_pop3.column(col, width=300 if col == "File" else 400)
tree_attachments_pop3.pack(fill="both", expand=True, pady=10)

# Layout responsiv
for frame in [frame_send, frame_imap, frame_pop3]:
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(3, weight=1)

root.mainloop()