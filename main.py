import requests
import smtplib
from datetime import datetime, timedelta
from data_sample import OTP_BOOK_DATA, RECIPIENTS, POSTSCRIPT, MY_EMAIL, APP_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bs4


def get_data(URL):
    # Get data from OTP website
    response = requests.get(URL)
    website_html = response.text
    soup = bs4.BeautifulSoup(website_html, "html.parser")
    return soup


def check_if_win(soup, OTP_BOOK_DATA):
    actual_date = [item.text for item in soup.find_all(name="h4")][16]
    actual_content = [item.text for item in soup.find_all(name="li", class_="sf-listitem")]
    actual_numbers = actual_content[10:actual_content.index(last_month_hun)]
    actual_series = [item.split()[0] for item in actual_numbers]
    actual_number = [item.split()[1] for item in actual_numbers]
    actual_prize = [item.split()[2:] for item in actual_numbers]

    # Check if we win
    is_win = False
    for number in range(len(actual_numbers)):
        for item in OTP_BOOK_DATA:
            if actual_series[number] == item["sorozat"]:
                if item["sorszám"] in actual_number[number]:
                    is_win = True
                    return f"\nA {item['sorozat']} {item['sorszám']} számú betétkönyv nyert! 🏆\n" \
                               f"Nyertes: {item['tulajdonos']} 🎉\n"

    # If we did not win, only notify certain people
    if not is_win:

        return f"\nEbben a hónapban egyik betétkönyv sem nyert. 😢\n" \
                   f"De a script még működik! 👌"


def send_mail(URL, actual_date, this_year, this_month_hun, actual_sorozatok, actual_sorszam, actual_nyeremeny, actual_numbers):
    # Notify at every event
    RECIPIENTS_ALWAYS_NOTIFY = RECIPIENTS[0:1]
    RECIPIENTS = RECIPIENTS_ALWAYS_NOTIFY

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

    today = datetime.now()
    last_month_date = today - timedelta(30)
    last_month = last_month_date.strftime("%B")
    this_month = today.strftime("%B")
    this_year = today.strftime("%Y")
    last_month_hun = DATETIME_TRANSLATE[last_month]
    this_month_hun = DATETIME_TRANSLATE[this_month]

    # Formulate the email, we would like to send
    message = "Halihó,\n\n"
    message += f"az ebben a hónapban kisorsolt OTP gépjármű nyeremények:\n{URL}\n\n{actual_date}\n"

    # Actual winner numbers
    for number in range(len(actual_numbers)):
        message += f" - {actual_sorozatok[number]} {actual_sorszam[number]} - {' '.join(actual_nyeremeny[number])}\n"

    message += check_if_win(actual_numbers, actual_sorozatok, actual_sorszam)

    message += "\n A következő hónapban ismét jelentkezem!\n\nMinden jót,\nBence OTPbot-ja\n"

    # Postscript
    message += POSTSCRIPT

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


    URL = "https://www.otpbank.hu/portal/hu/Megtakaritas/ForintBetetek/Gepkocsinyeremeny"

    data = get_data(URL)

    check_if_win(data, OTP_BOOK_DATA)

    send_mail()



    actual_date, actual_sorozatok, actual_sorszam, actual_nyeremeny, actual_numbers = get_data(URL)

    return 0


if __name__ == "__main__":
    main()
