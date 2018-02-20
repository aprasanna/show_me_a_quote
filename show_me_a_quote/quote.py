#!/usr/bin/python3

from colorama import init as colorama_init, Fore
from html.parser import HTMLParser
import json
import requests
from datetime import datetime
import shelve
import textwrap

colorama_init(autoreset=True)

CHAR_LIMIT_FOR_QUOTE = 80

curr_date = datetime.now().strftime("%Y-%m-%d")
quotes_api_link = "http://api.forismatic.com/api/1.0/?"
quotes_api_options = "method=getQuote&lang="+"en"+"&format=json"


def print_quote(quote, author):
    ''' Prints a quote with character limit (word wrap supported) '''
    print(textwrap.fill(quote, width=CHAR_LIMIT_FOR_QUOTE))
    print('- {}\n'.format(author))


def fetch_quote():
    ''' Fetches and returns a new quote '''
    return requests.get((('{}{}').format(quotes_api_link, quotes_api_options)))


def check_and_update_db(quote_db):
    ''' Check if db needs to be created or updated and perform an appropriate task '''
    if (('curr_date' not in quote_db) or (quote_db['curr_date'] != curr_date)):
        response = fetch_quote()
        try:
            responseJson = json.loads(response.text.replace('\\', ''))
        except Exception as ex:
            print(Fore.RED + 'Unable to fetch quote! Please try again %r' % ex)
            raise
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
