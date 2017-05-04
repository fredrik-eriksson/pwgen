#!/usr/bin/python3

import math
import os
import sys
import subprocess

if sys.version_info[0] < 3:
    import ConfigParser as configparser
else:
    import configparser

if sys.version_info >= (3, 6):
    do_seed = False
    import secrets as random
else:
    do_seed = True
    import random

class DictReadError(Exception):
    pass

class PasswordLengthError(Exception):
    pass

def save_config(target_file, config):
    path = os.path.expanduser(target_file)
    with open(path, 'w') as f:
        config.write(f)

def update_config(
        config=None,

        myspell_dir='/usr/share/hunspell',
        lang='en_US',
        word_min_char=2,
        word_max_char=0,

        words=4,
        capitalize='random',
        separators=',.- _=:',
        trailing_digits=2,
        leading_digits=0,
        special_chars='!?.,:-_$/@',
        trailing_chars=1,
        leading_chars=0,
        passwords=5,
        max_length=0
        ):
    if not config:
        conf = configparser.ConfigParser()
    else:
        conf = config

    def set_if_defined(conf, section, var, val):
        if val is not None:
            conf.set(section, var, str(val))

    if not conf.has_section('dictionary'):
        conf.add_section('dictionary')

    set_if_defined(conf, 'dictionary', 'myspell_dir', myspell_dir)
    set_if_defined(conf, 'dictionary', 'lang', lang)
    set_if_defined(conf, 'dictionary', 'word_min_char', word_min_char)
    set_if_defined(conf, 'dictionary', 'word_max_char', word_max_char)

    if not conf.has_section('passwords'):
        conf.add_section('passwords')
    set_if_defined(conf, 'passwords', 'words', words)
    set_if_defined(conf, 'passwords', 'capitalize', capitalize)
    set_if_defined(conf, 'passwords', 'separators', separators)
    set_if_defined(conf, 'passwords', 'trailing_digits', trailing_digits)
    set_if_defined(conf, 'passwords', 'leading_digits', leading_digits)
    set_if_defined(conf, 'passwords', 'special_chars', special_chars)
    set_if_defined(conf, 'passwords', 'trailing_chars', trailing_chars)
    set_if_defined(conf, 'passwords', 'leading_chars', leading_chars)
    set_if_defined(conf, 'passwords', 'passwords', passwords)
    set_if_defined(conf, 'passwords', 'max_length', max_length)
    return conf

    
def get_config(f_name):
    conf = configparser.ConfigParser()
    conf.read(f_name)
    return conf

def _read_dictionary(conf):
    lang = conf.get('dictionary', 'lang')
    word_min_chars = conf.getint('dictionary', 'word_min_char')
    word_max_chars = conf.getint('dictionary', 'word_max_char')
    dict_file = os.path.join(conf.get('dictionary', 'myspell_dir'), '{}.dic'.format(conf.get('dictionary', 'lang')))
    aff_file = os.path.join(conf.get('dictionary', 'myspell_dir'), '{}.aff'.format(conf.get('dictionary', 'lang')))
    unmunch_bin = conf.get('dictionary', 'unmunch_bin')
    words = set()
    chars = 0
    if os.path.exists(aff_file) and unmunch_bin:
        with open(os.devnull, 'w') as null:
            proc = subprocess.Popen(
                    [ unmunch_bin, dict_file, aff_file ],
                    stdout=subprocess.PIPE,
                    stderr=null
                    )
            out, err = proc.communicate()
        if proc.returncode != 0:
            raise DictReadError('Unmunching dictionaries failed')
        for word in out.splitlines():
            save = word.strip().decode('utf-8')
            if not save:
                continue
            first_char = save[:1]
            last_char = save[-1]
            if first_char in '1234567890,.-:':
                continue
            if last_char in '-':
                continue
            if word_min_chars and len(save) < word_min_chars:
                continue
            if word_max_chars and len(save) > word_max_chars:
                continue
            words.add(save)
            chars += len(save)
    else:
        with open(dict_file, 'r') as f:
            for line in f:
                if not line:
                    continue
                first_char = line[0]
                if first_char in '1234567890,.-:':
                    continue
                word = line.split('/', 1)[0]
                word = word.strip() # remove newlines
                last_char = word[-1]
                if last_char in '-':
                    continue
                if word_min_chars and len(word) < word_min_chars:
                    continue
                if word_max_chars and len(word) > word_max_chars:
                    continue
                words.add(word)
                chars += len(word)
    return {'words': list(words), 'wordlength': int(chars/len(words))}
    

def generate_passwords(conf):

    nr_of_words = conf.getint('passwords', 'words')
    nr_of_ld = conf.getint('passwords', 'leading_digits')
    nr_of_td = conf.getint('passwords', 'trailing_digits')
    nr_of_lc = conf.getint('passwords', 'leading_chars')
    nr_of_tc = conf.getint('passwords', 'trailing_chars')
    special_chars = conf.get('passwords', 'special_chars')
    separators = conf.get('passwords', 'separators')
    capitalize = conf.get('passwords', 'capitalize')
    max_len = conf.getint('passwords', 'max_length')

    if do_seed:
        random.seed()
    res = {}
    dict_data = _read_dictionary(conf)

    words = dict_data['words']
    word_length = dict_data['wordlength']
    approx_pwd_length = nr_of_words*word_length+nr_of_ld+nr_of_td+nr_of_lc+nr_of_tc+nr_of_words-1
    if max_len and approx_pwd_length > max_len:
        raise PasswordLengthError(
                "Password would be ~{} charactes long but max_len is {}; "\
                "please adjust max_lenght, words and/or the "\
                "trailing/leading settings.".format(
                    approx_pwd_length, 
                    max_len)
        )

    capitalize_entropy = 1
    if capitalize == 'random':
        capitalize_entropy = 2
    # seen entropy is calculated from the password rules.
    # At the moment setting max_length breaks this calculation as not all
    # combinations of words are possible.
    if max_len:
        seen_entropy = False
    else:
        seen_entropy = math.log(
                len(words)**nr_of_words *\
                len(separators) *\
                10**nr_of_ld *\
                10**nr_of_td *\
                len(special_chars)**nr_of_lc *\
                len(special_chars)**nr_of_tc *\
                capitalize_entropy
                , 2)

    while len(res) < conf.getint('passwords', 'passwords'):
        separator = random.choice(separators)
        my_words = []
        
        for i in range(nr_of_words):
            word = random.choice(words)
            if capitalize == 'random':
                if random.choice((True, False)):
                    word = word.capitalize()
            elif capitalize == 'true':
                word = word.capitalize()
            my_words.append(word)

        base_pwd = separator.join(my_words)
        leading_digits = ''.join(random.choice('1234567890') for i in range(nr_of_ld))
        trailing_digits = ''.join(random.choice('1234567890') for i in range(nr_of_td))
        leading_chars = ''.join(random.choice(special_chars) for i in range(nr_of_lc)) 
        trailing_chars = ''.join(random.choice(special_chars) for i in range(nr_of_tc)) 
        if leading_digits or leading_chars:
            base_pwd = "{}{}".format(separator, base_pwd)
        if trailing_digits or trailing_chars:
            base_pwd = "{}{}".format(base_pwd, separator)
        pwd = '{lc}{ld}{base}{td}{tc}'.format(
                lc=leading_chars,
                ld=leading_digits,
                base=base_pwd,
                td=trailing_digits,
                tc=trailing_chars)
        # blind entropy is calculated only by the number of unique characters
        # and password length
        blind_entropy = math.log(len(''.join(set(pwd)))**len(pwd), 2)

        if max_len and len(pwd) > max_len:
            continue
        res[pwd] = { 
                'length': len(pwd), 
                'entropy': blind_entropy,
                }
    return (res, seen_entropy)
