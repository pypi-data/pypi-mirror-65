pyspell
=======

Description
-----------

This package is intended as a lightweight, efficient, and customizable
spelling corrector. By using the Damerau-Levenshtein distance and a
cached BK tree, the code narrows down possible typos and ranks them
based on their ordering in an dictionary.txt file.

Usage
-----

Checker
~~~~~~~

The Checker class is the root of all of the spellchecking, and should be
used under most circumstances. To load the cached BK tree (or generate a
new one, should the need present itself), call the load method. It takes
two paramters, a wordlist and a pickling location (defaults to
bktree.pickle in the root directory). If there is no cache present at
the given location, it will generate one. ### Methods:

.. code:: python

    Checker.repickle()

This should be called following dictionary modifications not made with
the inbuilt updateDict function. The tree must be recalculated on
change.

.. code:: python

    Checker.load()

Loads the BK tree and sets up the dictionary.

.. code:: python

    Checker.check(word,returnNum,returnType,repeat,forcePrecision)

Checks for a word or list of words. word:list or str returnNum: The
number of arguments to return; 0 is all of the items found within the
tolerance of the tree. 1 will return only the best element of the list,
as defined by the order of the given dictionary. returnType: "pairings",
"rankings", or "words" (default) - Pairings returns an array of each
item and its ranking in the dictionary (in tuple form). I.e:
[(cow,16),(frog,11)] - Rankings returns an array of *just the rankings*
based on the dictionary. - Words returns words in respect to.

repeat: This is primarily a speed saving option. In situations involving
extremely heavy programs or dictionaries, this should be set to False.
It allows the tolerance to increase recursively until at least one match
is found for unknown words. forcePrecision: A manual way to change the
tolerance. The internal mechanism is almost always sufficient, and this
should seldom be changed from its default, False. This method returns a
String, an Array, or None.

.. code:: python

    Checker.updateDict(word,priority,pickle)

Inserts a word,dictionary, or list into a chosen point in the wordlist.
Word can be a dictionary with the keys of the intended words and each
key have a location attribute for where to insert it into the list.
Lists will be inserted in reverse chronological order for priority.
Strings are simply inserted. Priority defines where to put an item in
the dictionary, with -1 (default) being at the very end. (low priority)
Pickle defaults to true, and repickles it after the word(s) is added.
This should be set to false if you intend to call repickle later, after
further modifications.

Example of base code:

.. code:: python

    from pyspell.checker import *
    check=Checker("./pyspell/data/wordlist.txt","./pyspell/data/bktree.pickle"); 
    check.load(); 
    print(check.check("grat")) # --> great 
    print(check.check("diiffficult"))  # ---> difficult

(example.py)
