from datetime import date
import mysql.connector, smtplib, ssl

def ordinal(num):
    SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix


def age(birthdate):
    # Get today's date object
    today = date.today()

    # A bool that represents if today's day/month precedes the birth day/month
    one_or_zero = ((today.month, today.day) < (birthdate.month, birthdate.day))

    # Calculate the difference in years from the date object's components
    year_difference = today.year - birthdate.year

    # The difference in years is not enough.
    # To get it right, subtract 1 or 0 based on if today precedes the
    # birthdate's month/day.

    # To do this, subtract the 'one_or_zero' boolean
    # from 'year_difference'. (This converts
    # True to 1 and False to 0 under the hood.)
    age = year_difference - one_or_zero

    return age


def run():
    database_connection = mysql.connector.connect(
        host="REDACTED",
        user="REDACTED",
        password="REDACTED",
        database="REDACTED")

    cursor = database_connection.cursor()
    cursor.execute("CALL getTodaysBirthdays()")
    todaysBirthdays = cursor.fetchall()

    port = 465
    fromEmail = "REDACTED"
    emailPassword = "REDACTED"

    context = ssl.create_default_context()

    message = """Subject: Happy Birthday, {0}!

    Hello,

    I wanted to wish you a happy {1} birthday!

    Best wishes
    SENDER"""

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(fromEmail, emailPassword)
        for email, first_name, last_name, birthdate in todaysBirthdays:
            server.sendmail(
                 fromEmail,
                 email,
                 message.format(first_name, ordinal(age(birthdate)))
             )

    database_connection.close()
    cursor.close()


run()
