#!/usr/bin/python3

from colorama import init as colorama_init, Fore
from html.parser import HTMLParser
import json
import requests
from datetime import datetime
import shelve
import textwrap

colorama_init(autoreset=True)

def quote():
    ''' A module that fetches and print quotes; one per day '''
    curr_date = datetime.now().strftime("%Y-%m-%d")
    quotes_api_link = "http://api.forismatic.com/api/1.0/?"
    quotes_api_options = "method=getQuote&lang="+"en"+"&format=json"
    with shelve.open('show_me_a_quote.db') as quote_db:
        print('{}'.format('\n'))
        if (('curr_date' not in quote_db) or (quote_db['curr_date'] == curr_date)):
            response = requests.get((('{}{}').format(
                quotes_api_link, quotes_api_options)))
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
        print(textwrap.fill(quote_db['quote'], width=80))
        print('{}{}{}'.format('- ', quote_db['author'], '\n'))
