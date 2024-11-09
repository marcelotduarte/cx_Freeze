import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

# إعداد قاعدة البيانات
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

# حفظ طلب المستخدم في قاعدة البيانات
def save_request_to_db(name, region, municipality, email, phone, accuracy, comments):
    conn = sqlite3.connect('user_requests.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (name, region, municipality, email, phone, accuracy, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, region, municipality, email, phone, accuracy, comments))
    conn.commit()
    conn.close()

# إرسال البريد الإلكتروني
def send_email(name, region, municipality, email, phone, accuracy, comments):
    from_email = "your_email@example.com"  # قم بتحديث بريدك الإلكتروني
    password = "your_password"              # قم بتحديث كلمة المرور الخاصة بك
    to_email = "oumaimabenhammou1998@gmail.com"

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = "طلب جديد من المستخدم"

    # نص الرسالة
    body = f"""
    اسم المستخدم: {name}
    الإقليم: {region}
    الولاية: {municipality}
    البريد الإلكتروني: {email}
    رقم الهاتف: {phone}
    دقة التقييم: {accuracy}%
    ملاحظات إضافية: {comments}
    """

    message.attach(MIMEText(body, 'plain'))

    # إرسال البريد
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.send_message(message)
    server.quit()

# تشغيل التطبيق
def main():
    # إدخال بيانات المستخدم
    name = input("أدخل اسمك: ")
    region = input("أدخل اسم الإقليم: ")
    municipality = input("أدخل اسم الولاية: ")
    email = input("أدخل بريدك الإلكتروني: ")
    phone = input("أدخل رقم الهاتف: ")
    accuracy = input("أدخل درجة الدقة المطلوبة (%): ")
    comments = input("أدخل ملاحظات إضافية: ")

    # حفظ الطلب وإرسال البريد الإلكتروني
    save_request_to_db(name, region, municipality, email, phone, accuracy, comments)
    send_email(name, region, municipality, email, phone, accuracy, comments)
    print("تم تسجيل البيانات وإرسالها بنجاح إلى البريد الإلكتروني المحدد.")

# التهيئة وتشغيل التطبيق
initialize_database()
main()
