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

  DEFINITION(S) OF OPAQUE:

  ADJECTIVE

| 1  Not able to be seen through; not transparent.

     'the windows were opaque with steam'

+    1.1  (especially of language) hard or impossible to understand;
          unfathomable.

          'technical jargon that was opaque to her'

  NOUN

| 1  An opaque thing or substance.

     'And to think that we used to spend the dark winter months hibernating
      our legs away in a cocoon of black opaques!'

+    1.1  A substance for producing opaque areas on negatives.

  ORIGIN

  Late Middle English opake, from Latin opacus ‘darkened’. The current
  spelling (rare before the 19th century) has been influenced by the French
  form.

  PRONUNCIATION

  /oʊˈpeɪk/, /ōˈpāk/

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
