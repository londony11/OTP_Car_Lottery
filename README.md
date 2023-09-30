# OTP_Car_Lottery

This script check the OTP Car Lottery page, and notifies you via email about the result.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Manual Execution](#manual-execution)
  - [Automated Execution](#automated-execution)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features
- Web scraping to retrieve lottery numbers from the following:

    [OTP Bank - OTP Gépkocsinyeremény](https://www.otpbank.hu/portal/hu/Megtakaritas/ForintBetetek/Gepkocsinyeremeny)
- Automatic comparison of lottery numbers with your own numbers.
- Email notification when script is executed.

## Requirements
- Python 3.x
- Dependencies (specified in `requirements.txt`)

## Usage
### Manual Execution
1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/londony11/OTP_Car_Lottery.git
   ```
2. Install the required dependencies.
   ```bash
   pip install -r requirements.txt
   ```
3. Modify the configuration in `data_sample.py` to set the recipients of the notification, your email credentials 
(that the script can use to send a mail), and your car lottery numbers. (You can also add a p.s. as well.)

4. Run the script manually:
   ```bash
   python main.py
   ```
### Automated Execution
To automate the script and regularly check for lottery numbers, you can use a task scheduler (e.g., cron on Linux,
Task Scheduler on Windows). Here's how to set it up:
1. Follow steps 1 and 2 from the "Manual Execution" section to clone the repository and install dependencies.
2. Modify the configuration in `data_sample.py` as explained in step 3.
3. Use a task scheduler to run the script at your desired intervals. For example, on Linux, you can open your crontab configuration:
   ```bash
   crontab -e
   ```
4. Add an entry to run the script at your chosen schedule. For example, to run the script every day at 8 AM,
add the following line to your crontab:
   ```bash
   0 8 * * * /usr/bin/python3 /path/to/main.py
   ```
## Configuration
In `data_sample.py`, you can configure the following settings:
- `RECIPIENTS`: List of email addresses you want to send notification
- `MY_EMAIL`: Email address, the script can use for sending emails
- `APP_PASSWORD`: Password for `MY_EMAIL`
- `OTP_BOOK_DATA`: Dictionary for your lottery ticket
  - `owner`: Owner of the ticket
  - `series`: Series of the ticket
  - `number`: Number of the ticket
  - `value`: Value of the ticket
- `POSTSCRIPT`: Postscript for the email message

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow our Contributing Guidelines.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
