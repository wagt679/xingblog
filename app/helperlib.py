# -*- coding: utf-8 -*-

import hashlib
import random
import string
from threading import Thread

def make_salt():
    """
    make a salt for hash password.
    """
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    """
    make stored password string from raw password string.
    """
    if not salt:
        salt=make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    """
    validate password.
    """
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

def send_mail_async(mail, msg):
    def helper(mail, msg):
        mail.send(msg)

    thr = Thread(target=helper, args=[mail, msg])
    thr.start()

if __name__ == "__main__":
    # test code
    h = make_pw_hash('spez', 'hunter2')
    print valid_pw('spez', 'hunter2', h)
