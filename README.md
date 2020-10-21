# oxd

oxd is a CLI for retrieving definitions and synonyms from the [Oxford Dictionaries](https://www.lexico.com/) website (now under the name Lexico). **This is a WIP**. Please let me know if you have any issues or recommendations!

## Installation

oxd is available in the AUR ([Arch User Repository](https://aur.archlinux.org/packages/python-oxd-git/)):

```
$ git clone https://aur.archlinux.org/python-oxd-git.git
$ cd python-oxd-git
$ makepkg -si
```

I plan on refactoring this project and releasing it in the PyPI at some point. For now, if you're not using Arch (or the AUR), you can clone this repo, and set an alias in your `.bashrc`, `.zshrc`, or equivalent:

```
alias oxd="python path/to/oxd.py "
```

## Usage

**Definitions**:

```
$ oxd -d word

DEFINITION OF WORD:

NOUN

| 1  A single distinct meaningful element of speech or writing, used with 
     others (or sometimes alone) to form a sentence and typically shown 
     with a space on either side when written or printed.

+    1.1  A single distinct conceptual unit of language, comprising 
          inflected and variant forms.

+    1.2  Something that someone says or writes; a remark or piece of 
          information.

+    1.3  Speech as distinct from action.

+    1.4  Even the smallest amount of something spoken or written.

+    1.5  A person's account of the truth, especially when it differs from 
          that of another person.

+    1.6  A promise or assurance.

+    1.7  The text or spoken part of a play, opera, or other performed 
          piece; a script.

+    1.8  Angry talk.

+    1.9  A message; news.

+    1.10  A command, password, or motto.

+    1.11  A basic unit of data in a computer, typically 16 or 32 bits long.

TRANSITIVE VERB

| Choose and use particular words in order to say or write (something)

EXCLAMATION

| Used to express agreement.

ORIGIN

Old English, of Germanic origin; related to Dutch woord and German Wort, 
from an Indo-European root shared by Latin verbum ‘word’.

PRONUNCIATION

/wərd/
```

**Synonyms**:

```
$ oxd -s word

SYNONYMS OF WORD:

term, name, expression, designation, locution, turn of phrase, idiom, 
appellation, vocable, remark, comment, statement, utterance, observation, 
pronouncement, declaration, script, text, lyrics, libretto, promise, word 
of honour, assurance, guarantee, undertaking, pledge, vow, oath, bond, 
troth, parole, talk, conversation, chat, tête-à-tête, heart-to-heart, 
one-on-one, one-to-one, head-to-head, discussion, consultation, exchange of 
views, colloquy, confab, powwow, confabulation, news, information, 
communication, intelligence, notice, message, report, communiqué, dispatch, 
bulletin, account, data, facts, info, the low-down, the gen, the dope, the 
poop, tidings, advices, rumour, hearsay, talk, gossip, the grapevine, the 
word on the street, the scuttlebutt, instruction, order, command, signal, 
prompt, cue, tip-off, go-ahead, thumbs up, green light, high sign, command, 
order, decree, edict, mandate, bidding, will, motto, slogan, watchword, 
password, catchword, buzz word, phrase, express, put, couch, frame, set 
forth, formulate, style, say, utter, state
```
