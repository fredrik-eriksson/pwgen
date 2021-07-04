# pwgen
Another of those passphrase generators

The functionality is heavily inspired by [HSXKPasswd](https://github.com/bbusschots/hsxkpasswd), but it didn't quite have the functionality I wanted (random capitalization) and I wanted a python module for a possible future uwsgi webapp...

# Why
Because Randall Munroe says so.

![xkcd](https://imgs.xkcd.com/comics/password_strength.png "XKCD")

# Requirements
Python 3 as well as my-/hunspell-dictionaries for the language(s) you want to use.

# What
A password/passphrase generator. See below for some example usage.

```
$ sudo python3 setup.py install

...

$ pwgen --help
usage: pwgen [-h] [--quiet] [--generate-config] [--config-file CONFIG_FILE] [--myspell-dir MYSPELL_DIR] [--encoding ENCODING]
             [--unmunch-bin UNMUNCH_BIN] [--lang LANG] [--word-min-char WORD_MIN_CHAR] [--word-max-char WORD_MAX_CHAR] [--words WORDS]
             [--capitalize {true,false,random}] [--separators SEPARATORS] [--trailing-digits TRAILING_DIGITS]
             [--leading-digits LEADING_DIGITS] [--special-chars SPECIAL_CHARS] [--trailing-chars TRAILING_CHARS]
             [--leading-chars LEADING_CHARS] [--passwords PASSWORDS] [--max-length MAX_LENGTH]

Generate passwords

optional arguments:
  -h, --help            show this help message and exit
  --quiet, -q           Only echo the generated passwords.
  --generate-config, -g
                        Generate configuration file and then exit
  --config-file CONFIG_FILE, -c CONFIG_FILE
                        Configuration file to use
  --myspell-dir MYSPELL_DIR, -i MYSPELL_DIR
                        Directory containing myspell dictionaries
  --encoding ENCODING, -e ENCODING
                        Character encoding of the directory
  --unmunch-bin UNMUNCH_BIN, -u UNMUNCH_BIN
                        Path to my/hunspell unmunch binary
  --lang LANG, -l LANG  Dictionary language to use
  --word-min-char WORD_MIN_CHAR, -m WORD_MIN_CHAR
                        Minimum number of characters in a word
  --word-max-char WORD_MAX_CHAR, -M WORD_MAX_CHAR
                        Maximum number of characters in a word
  --words WORDS, -w WORDS
                        Number of words to use in the passphrase
  --capitalize {true,false,random}, -C {true,false,random}
                        Capitalize the words
  --separators SEPARATORS, -s SEPARATORS
                        Possible characters to use as separators
  --trailing-digits TRAILING_DIGITS, -d TRAILING_DIGITS
                        Number of digits at the end of the passphrase
  --leading-digits LEADING_DIGITS, -D LEADING_DIGITS
                        Number of digits at the start of the passphrase
  --special-chars SPECIAL_CHARS, -S SPECIAL_CHARS
                        Possible characters to use as extra special characters
  --trailing-chars TRAILING_CHARS, -p TRAILING_CHARS
                        Number of special characters to add at the end of the passphrase
  --leading-chars LEADING_CHARS, -P LEADING_CHARS
                        Number of special characters to add at the start of the passphrase
  --passwords PASSWORDS, -n PASSWORDS
                        Number of passwords to generate
  --max-length MAX_LENGTH, -L MAX_LENGTH
                        Maximum length of the generated passwords. Full-knowledge entropy calculation doesn't work when this is set.

$ pwgen -g --myspell-dir /usr/share/hunspell --lang sv_SE
Missing configuration file; generating a new at /home/user/.pwgen.cfg
Updating configuration file at /home/user/.pwgen.cfg

$ pwgen
Generated 5 passwords
Full-knowledge entropy is 82
Blind entropy	Password
========================
171.3           Lämpligen=empirisk=Musikal=Degklump?21
206.32		    Eldgaffel-Stigbygel-Vattenkoppor-ledstång-01
236.84		    Studieform leksaksbil punkinfluenser luftvärdig_09
181.52		    hemnummer:Fyrahundrade:Baku:segertippad!77
227.55		    bärvåg,Workout,Distriktsstyrelse,Förvarstid,89
========================

```
