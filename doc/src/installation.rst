import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('user_requests.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            municipality TEXT,
            email TEXT,
            phone TEXT,
            accuracy TEXT,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save the user's request to the database
def save_request_to_db(name, region, municipality, email, phone, accuracy, comments):
    conn = sqlite3.connect('user_requests.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (name, region, municipality, email, phone, accuracy, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, region, municipality, email, phone, accuracy, comments))
    conn.commit()
    conn.close()

# Send the email with the user's request
def send_email(name, region, municipality, email, phone, accuracy, comments):
    from_email = "your_email@example.com"  # Update with your email address
    password = "your_password"             # Update with your email password
    to_email = "oumaimabenhammou1998@gmail.com"

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = "New Request from User"

    # Body of the message
    body = f"""
    User Name: {name}
    Region: {region}
    Municipality: {municipality}
    Email: {email}
    Phone: {phone}
    Accuracy: {accuracy}%
    Additional Comments: {comments}
    """

    message.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.send_message(message)
    server.quit()

# Main function to run the app
def main():
    # Get user input
    name = input("Enter your name: ")
    region = input("Enter your region name: ")
    municipality = input("Enter your municipality name: ")
    email = input("Enter your email address: ")
    phone = input("Enter your phone number: ")
    accuracy = input("Enter the required accuracy (%): ")
    comments = input("Enter any additional comments: ")

    # Save the request and send the email
    save_request_to_db(name, region, municipality, email, phone, accuracy, comments)
    send_email(name, region, municipality, email, phone, accuracy, comments)
    print("The data has been successfully recorded and sent to the specified email.")

# Initialize the database and run the app
initialize_database()
main()
