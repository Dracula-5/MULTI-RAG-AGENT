import os

def search_emails(query):
    hits = []
    for f in os.listdir("data/emails"):
        with open("data/emails/"+f, "r") as file:
            if query.lower() in file.read().lower():
                hits.append(f)
    return ", ".join(hits)
def list_emails():
    return os.listdir("data/emails")
def save_email(filename, content):
    with open("data/emails/"+filename, "w") as file:
        file.write(content)
    return True
def delete_email(filename):
    os.remove("data/emails/"+filename)
    return True
def read_email(filename):
    with open("data/emails/"+filename, "r") as file:
        return file.read()
    return True

def update_email(filename, content):
    with open("data/emails/"+filename, "w") as file:
        file.write(content)
    return True

