import sys
from subprocess import check_output

try:
    from unidecode import unidecode
except ImportError:
    print('pip install unidecode')
    sys.exit(1)


class Account(object):
    def __init__(self, email, password, smtp, imap, from_=None):
        self.email = email
        self.password = password
        self.smtp = smtp
        self.imap = imap
        self.from_ = from_

    @property
    def real_password(self):
        return self.get_real_password()

    def get_real_password(self):
        password = check_output(['pass', 'show', self.password])
        return password.rstrip('\n')


class Gmail(Account):
    def __init__(self, **kwargs):
        kwargs.setdefault('imap', 'imap.gmail.com')
        kwargs.setdefault('smtp', 'smtp.gmail.com')
        super(Gmail, self).__init__(**kwargs)


class Airmail(Account):
    def __init__(self, **kwargs):
        kwargs.setdefault('imap', 'mail.cock.li')
        kwargs.setdefault('smtp', 'mail.cock.li')
        super(Airmail, self).__init__(**kwargs)


class Rss(object):
    def __init__(self, prefix, url):
        self.prefix = prefix
        self.url = url


class Reddit(Rss):
    def __init__(self, prefix, subreddits):
        url = 'https://www.reddit.com/r/{}/.rss'.format('+'.join(subreddits))
        super(Reddit, self).__init__(prefix, url=url)

