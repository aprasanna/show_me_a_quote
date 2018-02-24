#!/usr/bin/python3

from colorama import init as colorama_init, Fore
from html.parser import HTMLParser
import json
import requests
from datetime import datetime
import shelve
import textwrap
import sys

colorama_init(autoreset=True)

CHAR_LIMIT_FOR_QUOTE = 80

quotes_api_link = "http://api.forismatic.com/api/1.0/?method=getQuote"
quotes_api_options = dict(zip(("lang", "format"), ("en", "json")))


def print_error_and_exit(msg):
    ''' Print error message and exit '''
    print(Fore.RED + msg)
    sys.exit(1)


def print_quote(quote, author):
    ''' Prints a quote with character limit (word wrap supported) '''
    print(textwrap.fill(quote, width=CHAR_LIMIT_FOR_QUOTE))
    print('- {}\n'.format(author))


def fetch_quote():
    ''' Fetches and returns a new quote '''
    try:
        return requests.get(quotes_api_link, params=quotes_api_options)
    except Exception as ex:
        print_error_and_exit('Requests get method failed!')


def check_and_update_db(quote_db):
    ''' Check if db needs to be created or updated and perform an appropriate task '''
    curr_date = datetime.now().strftime("%Y-%m-%d")
    if (('curr_date' not in quote_db) or (quote_db['curr_date'] != curr_date)):
        response = fetch_quote()
        try:
            responseJson = json.loads(response.text.replace('\\', ''))
        except Exception as ex:
            print_error_and_exit("Unable to decode output\n")
        author = responseJson['quoteAuthor']
        quote = responseJson['quoteText']
        if not (author):
            author = 'Unknown'
        quote_db['curr_date'] = curr_date
        quote_db['quote'] = quote
        quote_db['author'] = author


def quote():
    ''' A module that fetches and print quotes; one per day '''
    with shelve.open('show_me_a_quote.db') as quote_db:
        print('\n')
        check_and_update_db(quote_db)
        print_quote(quote_db['quote'], quote_db['author'])
