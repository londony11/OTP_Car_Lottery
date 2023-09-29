import requests
import smtplib
from datetime import datetime, timedelta
from data_sample import OTP_BOOK_DATA, RECIPIENTS, POSTSCRIPT, MY_EMAIL, APP_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bs4

URL = "https://www.otpbank.hu/portal/hu/Megtakaritas/ForintBetetek/Gepkocsinyeremeny"
DATETIME_TRANSLATE = {
    "January": "Január",
    "February": "Február",
    "March": "Március",
    "April": "Április",
    "May": "Márjus",
    "June": "Június",
    "July": "Július",
    "August": "Augusztus",
    "September": "Szeptember",
    "October": "Október",
    "November": "November",
    "December": "December",
}


def get_data(URL):
    # Get data from OTP website
    response = requests.get(URL)
    website_html = response.text
    soup = bs4.BeautifulSoup(website_html, "html.parser")
    return soup


def check_if_win(soup, OTP_BOOK_DATA, POSTSCRIPT, DATETIME_TRANSLATE, URL):
    # get relevant dates
    today = datetime.now()
    last_month_date = today - timedelta(30)
    last_month = last_month_date.strftime("%B")
    last_month_hun = DATETIME_TRANSLATE[last_month]

    # get data from HTML
    actual_date = [item.text for item in soup.find_all(name="h4")][16]
    actual_content = [item.text for item in soup.find_all(name="li", class_="sf-listitem")]
    actual_numbers = actual_content[10:actual_content.index(last_month_hun)]
    actual_series = [item.split()[0] for item in actual_numbers]
    actual_number = [item.split()[1] for item in actual_numbers]
    actual_prize = [item.split()[2:] for item in actual_numbers]

    # compose message (Hungarian)
    message = "Halihó,\n\n"
    message += f"az ebben a hónapban kisorsolt OTP gépjármű nyeremények:\n{URL}\n\n{actual_date}\n"
    # Actual winner numbers
    for number in range(len(actual_numbers)):
        message += f" - {actual_series[number]} {actual_number[number]} - {' '.join(actual_prize[number])}\n"
    # changing part based on result
    is_win = False
    for number in range(len(actual_numbers)):
        for item in OTP_BOOK_DATA:
            if actual_series[number] == item["series"]:
                if item["number"] in actual_number[number]:
                    is_win = True
                    message += f"\nA {item['series']} {item['number']} számú betétkönyv nyert! 🏆\n" \
                               f"Nyertes: {item['owner']} 🎉\n"
    if not is_win:
        message += f"\nEbben a hónapban egyik betétkönyv sem nyert. 😢\n" \
                   f"De a script még működik! 👌"

    # closing part
    message += "\n A következő hónapban ismét jelentkezem!\n\nMinden jót,\nBence OTPbot-ja\n"
    # add ps
    message += POSTSCRIPT
    return message


def send_mail(message, RECIPIENTS, MY_EMAIL, APP_PASSWORD, DATETIME_TRANSLATE):
    today = datetime.now()
    this_month = today.strftime("%B")
    this_year = today.strftime("%Y")
    this_month_hun = DATETIME_TRANSLATE[this_month]

    # Send mail
    msg = MIMEMultipart()
    msg["From"] = MY_EMAIL
    msg["To"] = RECIPIENTS
    msg["Subject"] = f"OTP gépjárműnyeremény sorsolás - {this_year} {this_month_hun}"
    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=APP_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=RECIPIENTS,
            msg=msg.as_string(),
        )


def main():
    data = get_data(URL)
    message = check_if_win(data, OTP_BOOK_DATA, POSTSCRIPT, DATETIME_TRANSLATE, URL)
    send_mail(message, RECIPIENTS, MY_EMAIL, APP_PASSWORD, DATETIME_TRANSLATE)


if __name__ == "__main__":
    main()
