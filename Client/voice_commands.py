#-*- coding: utf-8 -*-
#!/usr/bin/env python

# assistant name
ASSISTANT_NAME = 'symbol'

# user commands
STATUS_CMD = 'status'
THX_CMD = 'thank you'
EXIT_CMD = 'exit'
REBOOT_CMD = 'reboot'
SHUTDOWN_CMD = 'shutdown'
TIME_CMD = 'time'
DATE_CMD = 'date'
LOC_CMD = 'location'
ACCOUNT_BALANCE_CMD = 'balance'
LAST_TRANSACTION_CMD = 'last transaction'
LAST_MESSAGE_CMD = 'last message'
TRANSACTION_SEND_CMD = 'send transaction'

# assistant messages
WELCOME_MSG = 'Hi, I am your personal Symbol assistant'
REBOOT_MSG = 'Rebooting system.'
SHUTDOWN_MSG = 'Shutdown system.'
EXIT_MSG = 'Goodbye.' 
COMMAND_MSG = 'How can I help you?'
THX_MSG = "You're welcome."
DONT_UNDERSTAND_MSG = "I don't understand."
SELECT_RECIPIENT_MSG = "Select recipient"
SELECT_AMOUNT_MSG = 'How much XYM do you want to transfer?'
SELECT_MESSAGE_MSG = 'Say your message'
SEND_TRANSACTION_NOT_UNDERSTAND_MSG = 'Sorry, I dont understand. Transaction will not be sent.'
TRANSACTION_NOT_SENDED_MSG = 'No confirmation. Transaction will not be sent. '
TRANSACION_SENDED_MSG = "Transaction sended. I'm waiting for confirmation."

# errors
API_ERROR_MSG = 'API error occured'