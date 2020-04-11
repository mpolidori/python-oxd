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
alias oxd="python path/to/oxd.py"
```

## Examples

Definitions:

```
$ oxd -d opaque

DEFINITION OF OPAQUE:

ADJECTIVE

| 1  Not able to be seen through; not transparent.

+    1.1  (especially of language) hard or impossible to understand.

NOUN

| 1  An opaque thing.

+    1.1  A substance for producing opaque areas on negatives.

ORIGIN

Late Middle English opake, from Latin opacus ‘darkened’. The current 
spelling (rare before the 19th century) has been influenced by the French 
form.

PRONUNCIATION

/ə(ʊ)ˈpeɪk/

```

Synonyms:

```
$ oxd -s opaque

  SYNONYMS OF OPAQUE:

  non-transparent, cloudy, filmy, blurred, smeared, hazy, misty, dirty,
  dingy, muddy, muddied, grimy, smeary, obscure, unclear, dense, uncertain,
  indeterminate, mysterious, puzzling, perplexing, baffling, mystifying,
  confusing, enigmatic, inexplicable, unexplained, concealed, hidden,
  unfathomable, incomprehensible, impenetrable, vague, ambiguous, Delphic,
  indefinite, indistinct, hazy, foggy, nebulous, equivocal, doubtful,
  dubious, oblique, elliptical, oracular, cryptic, deep, abstruse, recondite,
  arcane, esoteric, recherché, as clear as mud

```
