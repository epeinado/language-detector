LANGUAGE DETECTION
==================


This is a prototype of language detection API based on [ldig](https://github.com/shuyo/ldig).


Usage
-----

1. Extract model directory (if not extracted). Be sure that the extracted folder 
and the files inside it have at least read permission for your user.
    tar xf models/[select model archive]

2. Start server (default port is 8000)
    python lang_detection_api.py [-p port]


API
---

The API has two currently available services.

 * `/detect_language`: receives a text parameter via **POST** and returns the most
probable language for it.
 * `/language_probabilities`: receives a text parameter via **POST** and returns
the probability distribution for each of the supported languages.


Supported Languages
-------------------

id    | lang
:-----|:-------------
ca    |   Catalan
cs    |   Czech
da    |   Dannish
de    |   German
en    |   English
es    |   Spanish
fi    |   Finnish
fr    |   French
hu    |   Hungarian
id    |   Indonesian
it    |   Italian
nl    |   Dutch
no    |   Norwegian
pl    |   Polish
pt    |   Portuguese
ro    |   Romanian
sv    |   Swedish
tr    |   Turkish
vi    |   Vietnamese
