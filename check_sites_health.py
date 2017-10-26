import requests
import whois
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta


def load_urls4check(path):
    with open(path) as urls_file:
        return [row.strip() for row in urls_file]


def is_server_respond_with_200(url):
    try:
        return requests.get(url, timeout=5).status_code == requests.codes.ok
    except requests.exceptions.ConnectTimeout:
        return None


def get_domain_expiration_date(domain_name):
    who_is = whois.whois(domain_name)
    if not who_is:
        return None
    exp_date = who_is["expiration_date"]
    return exp_date[0] if isinstance(exp_date, list) else exp_date


def check_expiration_date(expiration_date):
    return expiration_date - relativedelta(months=1) >= datetime.now()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_with_hosts", help="write path to file with urls for checking")
    file_with_hosts = parser.parse_args().file_with_hosts

    file_names = load_urls4check(file_with_hosts)
    for file_name in file_names:
        is_server_respond_ok = is_server_respond_with_200(file_name)
        if is_server_respond_ok is None:
            print("Site {} not avalible".format(file_name))
            break
        print("Site {} {}responds to requests"
              .format(file_name, '' if is_server_respond_ok else 'not '))

        exp_date = get_domain_expiration_date(file_name)
        print("Its domain name paid for {} than a month"
              .format('more' if check_expiration_date(exp_date) else 'less'))
