# oxd

is a CLI for retrieving definitions and synonyms from the [Oxford Dictionaries](https://en.oxforddictionaries.com) website.

## Installation

oxd is available in the AUR (Arch User Repository).

```
$ git clone https://aur.archlinux.org/python-oxd-git.git
$ cd python-oxd-git
$ makepkg -si
```

## Example

Definition:

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
