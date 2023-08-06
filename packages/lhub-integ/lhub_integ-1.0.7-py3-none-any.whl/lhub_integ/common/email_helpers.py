import re
import time
import email.utils
import datetime
from io import StringIO
import csv

from bs4 import BeautifulSoup
from lhub_integ.common import helpers, time_helpers
from lhub_integ.common.input_helpers import safe_strip


def extract_urls(body):
    """
    Parse a plaintext email's message body, and return a sorted list of all unique URLs found

    :param body: plaintext message body
    :return: list of unique URLs
    """

    # In plaintext emails, sometimes URLs are simply placed in the body, but there is also a standard that some mail
    # services support, which is to enclose descriptive text in brackets and links in '<' and '>'
    # Example: [Google] <https://www.google.com/>

    # ToDo: Remove this old entry after vetting the new one
    # urls = re.findall(r'(?<=<)\w+:/{2,}(?:[\w\-]+\.)+\w+\S*?(?=>|\s|$)|(?<!<)\w+:/{2,}(?:[\w\-]+\.)+\w+\S*', body)

    # URL patterns
    url_base_pattern = r'\s*\w+:/{2,}(?:[\w\-]+\.)+\w+\S*?'
    url_patterns = [
        # Capture from body text when a URL is enclosed in '<' and '>' characters
        r'(?<=<){}(?=>|\s|$)'.format(url_base_pattern),

        # Capture from body text when a URL is enclosed in '[' and ']' characters
        r'(?<=\[){}(?=\]|\s|$)'.format(url_base_pattern),

        # Capture when URL appears directly within text but still contains 'xxxx://' prefix
        r'\b(?<!\S)\w+:/{2,}(?:[\w\-]+\.)+\w+\S*?(?=\"|<|\]|\s|$)',

        # Capture when "www.<domain>" appears within text, since Outlook will turn that into a hyperlink
        r'\s(www\.(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]+(?:/\S*)?)',

        # Capture when URL begins with an IP address and is followed by a slash
        r'\s((?:\d{1,3}\.){3}\d{1,3}/\S*)'
    ]

    # Look for URLs in the message body using all defined regex patterns
    urls = []
    for pattern in url_patterns:
        urls.extend([u.strip() for u in re.findall(pattern, body) if u.strip()])

    # If there are any empty values or mailto links, remove those
    urls_non_empty = []
    for u in urls:
        if u and not u.lower().startswith("mailto:") and not u.startswith('#'):
            urls_non_empty.append(u.replace('amp;', '').strip(',.'))

    # Remove duplicates and sort (for user readability)
    urls = sorted(list(set(urls_non_empty)))
    return urls


def extract_urls_from_html(html):
    """
    Parse an HTML email's message body, and return a sorted list of all unique URLs found
    :param html:
    :return: list of unique URLs
    """
    invalid_url_prefixes = ('mailto:', '#', 'tel:')

    def get_urls_from_tags(tags):
        extracted_urls = []
        for tag in tags:
            href = tag.get('href')
            # Sometimes there is an <a> tag without "href" but with a valid URL.
            # In that case, parse the link text w/ regex
            extracted_urls.append(href) if href else extracted_urls.extend(extract_urls(tag.text))
        return extracted_urls

    url_list = []
    soup = BeautifulSoup(html, 'lxml')
    links = soup.findAll('a')
    if links:
        urls = get_urls_from_tags(links)
        for url in urls:
            url = safe_strip(url)
            if url and not url.lower().startswith(invalid_url_prefixes):
                url_list.append(url.replace('amp;', ''))
        url_list = sorted(list(set(url_list)))

    return url_list


def __test_extract_urls_from_html():
    html = """<body><a href="https://logichub.com" /></body>"""
    urls = extract_urls_from_html(html)
    if urls[0] == 'https://logichub.com':
        helpers.print_debug_log("Extract URLs is working fine")
    else:
        helpers.print_debug_log("Extract URLs isn't working properly")


def default_email():
    log = helpers.format_success({})
    log.setdefault('lhub_ts', '%d' % (int(time.time()) * 1000))
    log.setdefault('sender', '')
    log.setdefault('recipients', [])
    log.setdefault('subject', '')
    log.setdefault('body', '')
    log.setdefault('body_text', '')
    log.setdefault('body_html', '')
    # ~Chad: new field to capture the body type (i.e. HTML vs. plaintext)
    log.setdefault('body_type', '')
    log.setdefault('attachments', [])
    log.setdefault('attachment_count', 0)
    log.setdefault('msgid', '')
    log.setdefault('date_received', '')
    log.setdefault('date_sent', '')
    log.setdefault('headers', [])
    log.setdefault('changekey', '')
    log.setdefault('categories', [])
    log.setdefault('urls', [])
    # ~Chad: now that we can pull unread messages too, adding a column for whether or not the message was unread
    log.setdefault('is_read', None)
    return log


def default_send_log(event_dict=None):
    event_dict = event_dict if event_dict else {}
    event_dict.update({
        'date_sent': time_helpers.current_time_string(),
        'recipients': '',
        'cc': '',
        'msg': '',
        'attachments': []
    })
    log = helpers.format_success(event_dict)
    return log


def add_recipients_to_list(recipient_list, existing_recipient_list):
    for mailbox in recipient_list:
        existing_recipient_list.append(mailbox.email_address)
    return existing_recipient_list


def add_recipients_to_list2(recipient_list, existing_recipient_list):
    if recipient_list:
        for mailbox in recipient_list:
            existing_recipient_list.append(mailbox['email'])
        return existing_recipient_list
    else:
        return existing_recipient_list


def parse_date_or_now(v):
    if v is None:
        return datetime.datetime.now()
    tt = email.utils.parsedate_tz(v)
    if tt is None:
        return datetime.datetime.now()
    timestamp = email.utils.mktime_tz(tt)
    date = datetime.datetime.fromtimestamp(timestamp)
    return date


email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)'  # domain
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE)

email_extract_re = re.compile(r"<(([.0-9a-z_+-=]+)@(([0-9a-z-]+\.)+[0-9a-z]{2,9}))>", re.M | re.S | re.I)


def extract_email(s):
    ret = email_extract_re.findall(s)
    if len(ret) < 1:
        p = s.split(" ")
        for e in p:
            e = e.strip()
            if email_re.match(e):
                return e

        return None
    else:
        return ret[0][0]


def parse_recipients(v):
    if v is None:
        return None

    ret = []

    # Sometimes a list is passed, which breaks .replace()
    if isinstance(v, list):
        v = ",".join(v)
    v = v.replace("\n", " ").replace("\r", " ").strip()
    s = StringIO(v)
    c = csv.reader(s)
    try:
        row = c.next()
    except StopIteration:
        return ret

    for entry in row:
        entry = entry.strip()
        if email_re.match(entry):
            e = entry
            entry = ""
        else:
            e = extract_email(entry)
            entry = entry.replace("<%s>" % e, "")
            entry = entry.strip()
            if e and entry.find(e) != -1:
                entry = entry.replace(e, "").strip()

        # If all else has failed
        if entry and e is None:
            e_split = entry.split(" ")
            e = e_split[-1].replace("<", "").replace(">", "")
            entry = " ".join(e_split[:-1])

        ret.append({"name": entry, "email": e})

    return ret
