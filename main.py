import requests
import smtplib
import datetime
from bs4 import BeautifulSoup as scrapper


def parse(webpage):
    # parsing the text of the webpage as html
    webpage = scrapper(webpage.text, 'html.parser')

    # we get the date of the last published article
    last_publish_date = str(webpage.select("[class=publishdate]")[0])
    last_publish_date = last_publish_date.split("\n", 2)[1].split(', ', 1)[1]
    last_publish_date = datetime.datetime.strptime(last_publish_date, "%B %d, %Y")

    article = webpage.select("[class=title]")[0]

    # we get the article title and link
    article_title = str(article).split('"')[-2]
    article_link = str(article.select("[href]")).split('"', 2)[1]

    if last_publish_date.date() == datetime.date.today():
        return f'''
        Google AI has published a new article!

        Title: {article_title}
        Link: {article_link}
        '''

    return None


def send_email(message):

    port = 465  # For SSL
    email = 'ppsha100@gmail.com'
    password = 'z2782294'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        try:
            server.sendmail(email, email, message)
            print("Successfully sent email")
        except Exception as e:
            print(e)
            print("Error: unable to send email")


def get_webpage():
    url = 'https://ai.googleblog.com/'
    webpage = requests.get(url)             # we get the url in bytes

    if webpage.status_code == 200:
        message = parse(webpage)
    else:
        message = 'There was some error in getting the webpage'

    if message:
        send_email(message)


get_webpage()
