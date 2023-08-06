HTRC-Features |Build Status| |PyPI version| |Anaconda-Server Badge|
===================================================================

Tools for working with the `HTRC Extracted Features
dataset <https://sharc.hathitrust.org/features>`__, a dataset of
page-level text features extracted from 13.7 million digitized works.

This library provides a ``FeatureReader`` for parsing files, which are
handled as ``Volume`` objects with collections of ``Page`` objects.
Volumes provide access to metadata (e.g. language), volume-wide feature
information (e.g. token counts), and access to Pages. Pages allow you to
easily parse page-level features, particularly token lists.

This library makes heavy use of `Pandas <pandas.pydata.org>`__,
returning many data representations as DataFrames. This is the leading
way of dealing with structured data in Python, so this library doesn’t
try to reinvent the wheel. Since refactoring around Pandas, the primary
benefit of using the HTRC Feature Reader is performance: reading the
json structures and parsing them is generally faster than custom code.
You also get convenient access to common information, such as
case-folded token counts or part-of-page specific character counts.
Details of the public methods provided by this library can be found in
the `HTRC Feature Reader
docs <http://htrc.github.io/htrc-feature-reader/htrc_features/feature_reader.m.html>`__.

**Table of Contents**: `Installation <#Installation>`__ \|
`Usage <#Usage>`__ \| `Additional Notes <#Additional-Notes>`__

**Links**: `HTRC Feature Reader
Documentation <http://htrc.github.io/htrc-feature-reader/htrc_features/feature_reader.m.html>`__
\| `HTRC Extracted Features
Dataset <https://sharc.hathitrust.org/features>`__

**Citation**: Peter Organisciak and Boris Capitanu, “Text Mining in
Python through the HTRC Feature Reader,” *Programming Historian*, (22
November 2016),
http://programminghistorian.org/lessons/text-mining-with-extracted-features.

Installation
------------

To install,

.. code:: bash

       pip install htrc-feature-reader

That’s it! This library is written for Python 3.0+. For Python
beginners, you’ll need
`pip <https://pip.pypa.io/en/stable/installing/>`__.

Alternately, if you are using
`Anaconda <https://www.continuum.io/downloads>`__, you can install with

.. code:: bash

       conda install -c htrc htrc-feature-reader

The ``conda`` approach is recommended, because it makes sure that some
of the hard-to-install dependencies are properly installed.

Given the nature of data analysis, using iPython with Jupyter notebooks
for preparing your scripts interactively is a recommended convenience.
Most basically, it can be installed with
``pip install ipython[notebook]`` and run with ``ipython notebook`` from
the command line, which starts a session that you can access through
your browser. If this doesn’t work, consult the `iPython
documentation <http://ipython.readthedocs.org/>`__.

Optional: `installing the development
version <#Installing-the-development-version>`__.

.. |Build Status| image:: https://travis-ci.org/htrc/htrc-feature-reader.svg?branch=master
   :target: https://travis-ci.org/htrc/htrc-feature-reader
.. |PyPI version| image:: https://badge.fury.io/py/htrc-feature-reader.svg
   :target: https://badge.fury.io/py/htrc-feature-reader
.. |Anaconda-Server Badge| image:: https://anaconda.org/htrc/htrc-feature-reader/badges/installer/conda.svg
   :target: https://anaconda.org/htrc/htrc-feature-reader

Usage
-----

*Note: for new Python users, a more in-depth lesson is published by
Programming Historian:*\ `Text Mining in Python through the HTRC Feature
Reader <http://programminghistorian.org/lessons/text-mining-with-extracted-features>`__\ *.
That lesson is also the official citation associated the HTRC Feature
Reader library.*

Reading feature files
~~~~~~~~~~~~~~~~~~~~~

The easiest way to start using this library is to use the Volume
interface, which takes a path to an Extracted Features file.

.. code:: ipython3

    from htrc_features import Volume
    vol = Volume('data/ef2-stubby/hvd/34926/hvd.32044093320364.json.bz2')
    vol




.. raw:: html

    <strong><a href='http://hdl.handle.net/2027/hvd.32044093320364'>The Nautilus.</a></strong> by <em>Delaware Museum of Natural History.</em> (1904, 222 pages) - <code>hvd.32044093320364</code>



The FeatureReader can also download files at read time, by reference to
a HathiTrust volume id. For example, if I want `both of volumes of Pride
and Prejudice <https://catalog.hathitrust.org/Record/100323335>`__, I
can see that the URLs are
babel.hathitrust.org/cgi/pt?id=\ **hvd.32044013656053** and
babel.hathitrust.org/cgi/pt?id=\ **hvd.32044013656061**. In the
FeatureReader, these can be called with the ``ids=[]`` argument, as
follows:

.. code:: ipython3

    for htid in ["hvd.32044013656053", "hvd.32044013656061"]:
        vol = Volume(htid)
        print(vol.title, vol.enumeration_chronology)


.. parsed-literal::

    Pride and prejudice. v.1
    Pride and prejudice. v.2


This downloads the file temporarily, using the HTRC’s web-based download
link
(e.g. https://data.analytics.hathitrust.org/features/get?download-id={{URL}}).
One good pairing with this feature is the `HTRC Python
SDK <https://github.com/htrc/HTRC-PythonSDK>`__\ ’s functionality for
downloading collections.

For example, I have a small collection of knitting-related books at
https://babel.hathitrust.org/cgi/mb?a=listis&c=1174943610. To read the
feature files for those books:

.. code:: ipython3

    from htrc import workset
    volids = workset.load_hathitrust_collection('https://babel.hathitrust.org/cgi/mb?a=listis&c=1174943610')
    FeatureReader(ids=volids).first().title

Remember that for large jobs, it is faster to download your dataset
beforehand, using the ``rsync`` method.

Volume
~~~~~~

A
`Volume <http://htrc.github.io/htrc-feature-reader/htrc_features/feature_reader.m.html#htrc_features.feature_reader.Volume>`__
contains information about the current work and access to the pages of
the work. All the metadata fields from the HTRC JSON file are accessible
as properties of the volume object, including *title*, *language*,
*imprint*, *oclc*, *pubDate*, and *genre*. The main identifier *id* and
*pageCount* are also accessible, and you can find the URL for the Full
View of the text in the HathiTrust Digital Library - if it exists - with
``vol.handle_url``.

.. code:: ipython3

    "Volume {} is a {} page text from {} written in {}. You can doublecheck at {}".format(vol.id, vol.page_count, 
                                                                                          vol.year, vol.language, 
                                                                                          vol.handle_url)




.. parsed-literal::

    'Volume hvd.32044013656061 is a 306 page text from 1903 written in eng. You can doublecheck at http://hdl.handle.net/2027/hvd.32044013656061'



This is the *Extracted Features* dataset, so the features are easily
accessible. To most popular is token counts, which are returned as a
Pandas DataFrame:

.. code:: ipython3

    df = vol.tokenlist()
    df.sample(10)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th>count</th>
        </tr>
        <tr>
          <th>page</th>
          <th>section</th>
          <th>token</th>
          <th>pos</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>201</th>
          <th>body</th>
          <th>abode</th>
          <th>NN</th>
          <td>1</td>
        </tr>
        <tr>
          <th>117</th>
          <th>body</th>
          <th>head</th>
          <th>NN</th>
          <td>1</td>
        </tr>
        <tr>
          <th>126</th>
          <th>body</th>
          <th>for</th>
          <th>IN</th>
          <td>1</td>
        </tr>
        <tr>
          <th>210</th>
          <th>body</th>
          <th>three</th>
          <th>CD</th>
          <td>1</td>
        </tr>
        <tr>
          <th>224</th>
          <th>body</th>
          <th>would</th>
          <th>MD</th>
          <td>1</td>
        </tr>
        <tr>
          <th>89</th>
          <th>body</th>
          <th>The</th>
          <th>DT</th>
          <td>1</td>
        </tr>
        <tr>
          <th>283</th>
          <th>body</th>
          <th>any</th>
          <th>DT</th>
          <td>1</td>
        </tr>
        <tr>
          <th>63</th>
          <th>body</th>
          <th>surprise</th>
          <th>NN</th>
          <td>1</td>
        </tr>
        <tr>
          <th>152</th>
          <th>body</th>
          <th>make</th>
          <th>VB</th>
          <td>1</td>
        </tr>
        <tr>
          <th>170</th>
          <th>body</th>
          <th>I</th>
          <th>PRP</th>
          <td>3</td>
        </tr>
      </tbody>
    </table>
    </div>



Other extracted features are discussed below.

The full included metadata can be seen with ``vol.parser.meta``:

.. code:: ipython3

    vol.parser.meta.keys()




.. parsed-literal::

    dict_keys(['id', 'metadata_schema_version', 'enumeration_chronology', 'type_of_resource', 'title', 'date_created', 'pub_date', 'language', 'access_profile', 'isbn', 'issn', 'lccn', 'oclc', 'page_count', 'feature_schema_version', 'ht_bib_url', 'genre', 'handle_url', 'imprint', 'names', 'source_institution', 'classification', 'issuance', 'bibliographic_format', 'government_document', 'hathitrust_record_number', 'rights_attributes', 'pub_place', 'volume_identifier', 'source_institution_record_number', 'last_update_date'])



These fields are mapped to attributes in ``Volume``, so ``vol.oclc``
will return the oclc field from that metadata. As a convenience,
``Volume.year`` returns the ``pub_date`` information and
``Volume.author`` returns the ``contributor information``.

.. code:: ipython3

    vol.year, vol.author




.. parsed-literal::

    ('1903', ['Austen, Jane 1775-1817 '])



If the minimal metadata included with the extracted feature files is
insufficient, you can fetch HT’s metadata record from the Bib API with
``vol.metadata``. Remember that this calls the HTRC servers for each
volume, so can add considerable overhead. The result is a MARC file,
returned as a `pymarc <https://github.com/edsu/pymarc>`__ record object.
For example, to get the publisher information from field ``260``:

.. code:: ipython3

    vol.metadata['260'].value()




.. parsed-literal::

    'Boston : Little, Brown, 1903.'



*At large-scales, using ``vol.metadata`` is an impolite and inefficient
amount of server pinging; there are better ways to query the API than
one volume at a time. Read about the*\ `HTRC Solr
Proxy <https://wiki.htrc.illinois.edu/display/COM/Solr+Proxy+API+User+Guide>`__\ *.*

Another source of bibliographic metadata is the HathiTrust Bib API. You
can access this information through the URL returned with
``vol.ht_bib_url``:

.. code:: ipython3

    vol.ht_bib_url




.. parsed-literal::

    'http://catalog.hathitrust.org/api/volumes/full/htid/hvd.32044013656061.json'



Volumes also have direct access to volume-wide info of features stored
in pages. For example, you can get a list of words per page through
`Volume.tokens_per_page() <http://htrc.github.io/htrc-feature-reader/htrc_features/feature_reader.m.html#htrc_features.feature_reader.Volume.tokens_per_page>`__.
We’ll discuss these features `below <#Volume-stats-collecting>`__, after
looking first at Pages.

Note that for the most part, the properties of the ``Page`` and
``Volume`` objects aligns with the names in the HTRC Extracted Features
schema, except they are converted to follow `Python naming
conventions <https://google.github.io/styleguide/pyguide.html?showone=Naming#Naming>`__:
converting the ``CamelCase`` of the schema to
``lowercase_with_underscores``. E.g. ``beginLineChars`` from the HTRC
data is accessible as ``Page.begin_line_chars``.

The fun stuff: playing with token counts and character counts
-------------------------------------------------------------

Token counts are returned by ``Volume.tokenlist()`` (or
``Page.tokenlist()``. By default, part-of-speech tagged, case-sensitive
counts are returned for the body.

The token count information is returned as a DataFrame with a MultiIndex
(page, section, token, and part of speech) and one column (count).

.. code:: ipython3

    print(vol.tokenlist()[:3])


.. parsed-literal::

                             count
    page section token  pos       
    1    body    Austen .        1
                 Pride  NNP      1
                 and    CC       1


``Page.tokenlist()`` can be manipulated in various ways. You can
case-fold, for example:

.. code:: ipython3

    tl = vol.tokenlist(case=False)
    tl.sample(5)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th>count</th>
        </tr>
        <tr>
          <th>page</th>
          <th>section</th>
          <th>lowercase</th>
          <th>pos</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>218</th>
          <th>body</th>
          <th>what</th>
          <th>WP</th>
          <td>1</td>
        </tr>
        <tr>
          <th>30</th>
          <th>body</th>
          <th>pemberley</th>
          <th>NNP</th>
          <td>1</td>
        </tr>
        <tr>
          <th>213</th>
          <th>body</th>
          <th>comes</th>
          <th>VBZ</th>
          <td>2</td>
        </tr>
        <tr>
          <th>183</th>
          <th>body</th>
          <th>took</th>
          <th>VBD</th>
          <td>1</td>
        </tr>
        <tr>
          <th>51</th>
          <th>body</th>
          <th>necessary</th>
          <th>JJ</th>
          <td>1</td>
        </tr>
      </tbody>
    </table>
    </div>



Or, you can combine part of speech counts into a single integer.

.. code:: ipython3

    tl = vol.tokenlist(pos=False)
    tl.sample(5)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th></th>
          <th>count</th>
        </tr>
        <tr>
          <th>page</th>
          <th>section</th>
          <th>token</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>264</th>
          <th>body</th>
          <th>family</th>
          <td>2</td>
        </tr>
        <tr>
          <th>47</th>
          <th>body</th>
          <th>journey</th>
          <td>1</td>
        </tr>
        <tr>
          <th>98</th>
          <th>body</th>
          <th>Perhaps</th>
          <td>1</td>
        </tr>
        <tr>
          <th>49</th>
          <th>body</th>
          <th>at</th>
          <td>2</td>
        </tr>
        <tr>
          <th>227</th>
          <th>body</th>
          <th>so</th>
          <td>1</td>
        </tr>
      </tbody>
    </table>
    </div>



Section arguments are valid here: ‘header’, ‘body’, ‘footer’, ‘all’, and
‘group’

.. code:: ipython3

    tl = vol.tokenlist(section="header", case=False, pos=False)
    tl.head(5)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th></th>
          <th>count</th>
        </tr>
        <tr>
          <th>page</th>
          <th>section</th>
          <th>lowercase</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">9</th>
          <th rowspan="5" valign="top">header</th>
          <th>'s</th>
          <td>1</td>
        </tr>
        <tr>
          <th>and</th>
          <td>1</td>
        </tr>
        <tr>
          <th>austen</th>
          <td>1</td>
        </tr>
        <tr>
          <th>jane</th>
          <td>1</td>
        </tr>
        <tr>
          <th>prejudice</th>
          <td>1</td>
        </tr>
      </tbody>
    </table>
    </div>



You can also drop the section index altogether if you’re content with
the default ‘body’.

.. code:: ipython3

    vol.tokenlist(drop_section=True, case=False, pos=False).sample(2)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>count</th>
        </tr>
        <tr>
          <th>page</th>
          <th>lowercase</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>247</th>
          <th>suppose</th>
          <td>1</td>
        </tr>
        <tr>
          <th>76</th>
          <th>would</th>
          <td>2</td>
        </tr>
      </tbody>
    </table>
    </div>



The MultiIndex makes it easy to slice the results, and it is althogether
more memory-efficient. For example, to return just the nouns (``NN``):

.. code:: ipython3

    tl = vol.tokenlist()
    tl.xs('NN', level='pos').head(4)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th></th>
          <th>count</th>
        </tr>
        <tr>
          <th>page</th>
          <th>section</th>
          <th>token</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <th>body</th>
          <th>prejudiceJane</th>
          <td>1</td>
        </tr>
        <tr>
          <th>9</th>
          <th>body</th>
          <th>Volume</th>
          <td>1</td>
        </tr>
        <tr>
          <th>10</th>
          <th>body</th>
          <th>vol</th>
          <td>3</td>
        </tr>
        <tr>
          <th>12</th>
          <th>body</th>
          <th>./■</th>
          <td>1</td>
        </tr>
      </tbody>
    </table>
    </div>



If you are new to Pandas DataFrames, you might find it easier to learn
by converting the index to columns.

.. code:: ipython3

    simpler_tl = df.reset_index()
    simpler_tl[simpler_tl.pos == 'NN']




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>page</th>
          <th>section</th>
          <th>token</th>
          <th>pos</th>
          <th>count</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>3</th>
          <td>1</td>
          <td>body</td>
          <td>prejudiceJane</td>
          <td>NN</td>
          <td>1</td>
        </tr>
        <tr>
          <th>19</th>
          <td>9</td>
          <td>body</td>
          <td>Volume</td>
          <td>NN</td>
          <td>1</td>
        </tr>
        <tr>
          <th>40</th>
          <td>10</td>
          <td>body</td>
          <td>vol</td>
          <td>NN</td>
          <td>3</td>
        </tr>
        <tr>
          <th>51</th>
          <td>12</td>
          <td>body</td>
          <td>./■</td>
          <td>NN</td>
          <td>1</td>
        </tr>
        <tr>
          <th>53</th>
          <td>12</td>
          <td>body</td>
          <td>/</td>
          <td>NN</td>
          <td>1</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>43178</th>
          <td>297</td>
          <td>body</td>
          <td>spite</td>
          <td>NN</td>
          <td>1</td>
        </tr>
        <tr>
          <th>43187</th>
          <td>297</td>
          <td>body</td>
          <td>uncle</td>
          <td>NN</td>
          <td>1</td>
        </tr>
        <tr>
          <th>43191</th>
          <td>297</td>
          <td>body</td>
          <td>warmest</td>
          <td>NN</td>
          <td>1</td>
        </tr>
        <tr>
          <th>43195</th>
          <td>297</td>
          <td>body</td>
          <td>wife</td>
          <td>NN</td>
          <td>1</td>
        </tr>
        <tr>
          <th>43226</th>
          <td>305</td>
          <td>body</td>
          <td>NON-RECEIPT</td>
          <td>NN</td>
          <td>1</td>
        </tr>
      </tbody>
    </table>
    <p>7224 rows × 5 columns</p>
    </div>



If you prefer not to use Pandas, you can always convert the object, with
methods like ``to_dict`` and ``to_csv``).

.. code:: ipython3

    tl[:3].to_csv()




.. parsed-literal::

    'page,section,token,pos,count\n1,body,Austen,.,1\n1,body,Pride,NNP,1\n1,body,and,CC,1\n'



To get just the unique tokens, ``Volume.tokens`` provides them as a set.
Here I select a specific page for brevity and a minimum count, but you
can run the method without arguments.

.. code:: ipython3

    vol.tokens(page_select=21, min_count=5)




.. parsed-literal::

    {'"', ',', '.', 'You', 'been', 'have', 'his', 'in', 'of', 'the', 'you'}



In addition to token lists, you can also access other section features:

.. code:: ipython3

    vol.section_features()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>tokenCount</th>
          <th>lineCount</th>
          <th>emptyLineCount</th>
          <th>capAlphaSeq</th>
          <th>sentenceCount</th>
        </tr>
        <tr>
          <th>page</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <td>4</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
        </tr>
        <tr>
          <th>2</th>
          <td>15</td>
          <td>10</td>
          <td>4</td>
          <td>2</td>
          <td>1</td>
        </tr>
        <tr>
          <th>3</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>302</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>303</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>304</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>305</th>
          <td>49</td>
          <td>11</td>
          <td>2</td>
          <td>3</td>
          <td>3</td>
        </tr>
        <tr>
          <th>306</th>
          <td>2</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
        </tr>
      </tbody>
    </table>
    <p>306 rows × 5 columns</p>
    </div>



Chunking
~~~~~~~~

If you’re working in an instance where you hope to have comparably sized
document units, you can use ‘chunking’ to roll pages into chunks that
aim for a specific length. e.g.

.. code:: ipython3

    by_chunk = vol.tokenlist(chunk=True, chunk_target=10000)
    print(by_chunk.sample(4))
    # Count words per chunk
    by_chunk.groupby(level='chunk').sum()


.. parsed-literal::

                                  count
    chunk section token      pos       
    5     body    husbands   NNS      3
    2     body    frequently RB       3
                  domestic   JJ       3
    3     body    :          :       10




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>count</th>
        </tr>
        <tr>
          <th>chunk</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <td>12453</td>
        </tr>
        <tr>
          <th>2</th>
          <td>9888</td>
        </tr>
        <tr>
          <th>3</th>
          <td>9887</td>
        </tr>
        <tr>
          <th>4</th>
          <td>10129</td>
        </tr>
        <tr>
          <th>5</th>
          <td>10054</td>
        </tr>
        <tr>
          <th>6</th>
          <td>10065</td>
        </tr>
        <tr>
          <th>7</th>
          <td>12327</td>
        </tr>
      </tbody>
    </table>
    </div>



Multiprocessing
~~~~~~~~~~~~~~~

For large jobs, you’ll want to use multiprocessing or multithreading to
speed up your process. This is left up to your preferred method, either
within Python or by spawning multiple scripts from the command line.
Here are two approaches that I like.

Dask
^^^^

Dask offers easy multithreading (shared resources) and multiprocessing
(separate processes) in Python, and is particularly convenient because
it includes a subset of Pandas DataFrames.

Here is a minimal example, that lazily loads token frequencies from a
list of volume IDs, and counts them up by part of speech tag.

.. code:: python

   import dask.dataframe as dd
   from dask import delayed

   def get_tokenlist(vol):
       ''' Load a one volume feature reader, get that volume, and return its tokenlist '''
       return FeatureReader(ids=[volid]).first().tokenlist()

   delayed_dfs = [delayed(get_tokenlist)(volid) for volid in volids]

   # Create a dask
   ddf = (dd.from_delayed(delayed_dfs)
            .reset_index()
            .groupby('pos')[['count']]
            .sum()
         )

   # Run processing
   ddf.compute()

Here is an example of 78 volumes being processed in 24 seconds with 31
threads:

.. figure:: data/dask-progress.png
   :alt: Counting POS in 78 books about knitting

   Counting POS in 78 books about knitting

This example used multithreading. Due to the nature of Python, certain
functions won’t parallelize well. In our case, the part where the JSON
is read from the file and converted to a DataFrame (the light green
parts of the graphic) won’t speed up because Python dicts lock the
Global Interpreter Lock (GIL). However, because Pandas releases the GIL,
nearly everything you do after parsing the JSON will be very quick.

To better understand what happens when ``ddf.compute()``, here is a
graph for 4 volumes:

|image0|

GNU Parallel
^^^^^^^^^^^^

As an alternative to multiprocessing in Python, my preference is to have
simpler Python scripts and to use GNU Parallel on the command line. To
do this, you can set up your Python script to take variable length
arguments of feature file paths, and to print to stdout.

This psuedo-code shows how that you’d use parallel, where the number of
parallel processes is 90% the number of cores, and 50 paths are sent to
the script at a time (if you send too little at a time, the
initialization time of the script can add up).

.. code:: bash

   find feature-files/ -name '*json.bz2' | parallel --eta --jobs 90% -n 50 python your_script.py >output.txt

.. |image0| image:: data/dask-graph.png

Additional Notes
----------------

Installing the development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   git clone https://github.com/htrc/htrc-feature-reader.git
   cd htrc-feature-reader
   python setup.py install

Iterating through the JSON files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to do fast, highly customized processing without
instantiating Volumes, FeatureReader has a convenient generator for
getting the raw JSON as a Python dict: ``fr.jsons()``. This simply does
the file reading, optional decompression, and JSON parsing.

Downloading files within the library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``utils`` includes an Rsyncing utility, ``download_file``. This requires
Rsync to be installed on your system.

**Usage:**

Download one file to the current directory:

::

   utils.download_file(htids='nyp.33433042068894')

Download multiple files to the current directory:

::

   ids = ['nyp.33433042068894', 'nyp.33433074943592', 'nyp.33433074943600']
   utils.download_file(htids=ids)

Download file to ``/tmp``:

::

   utils.download_file(htids='nyp.33433042068894', outdir='/tmp')

Download file to current directory, keeping pairtree directory
structure, i.e.
``./nyp/pairtree_root/33/43/30/42/06/88/94/33433042068894/nyp.33433042068894.json.bz2``:

``utils.download_file(htids='nyp.33433042068894', keep_dirs=True)``

Getting the Rsync URL
~~~~~~~~~~~~~~~~~~~~~

If you have a HathiTrust Volume ID and want to be able to download the
features for a specific book, ``hrtc_features.utils`` contains an
`id_to_rsync <http://htrc.github.io/htrc-feature-reader/htrc_features/utils.m.html#htrc_features.utils.id_to_rsync>`__
function. This uses the `pairtree <http://pythonhosted.org/Pairtree/>`__
library but has a fallback written with that library is not installed,
since it isn’t compatible with Python 3.

.. code:: ipython3

    from htrc_features import utils
    utils.id_to_rsync('miun.adx6300.0001.001')




.. parsed-literal::

    'miun/pairtree_root/ad/x6/30/0,/00/01/,0/01/adx6300,0001,001/miun.adx6300,0001,001.json.bz2'



See the `ID to Rsync notebook <examples/ID_to_Rsync_Link.ipynb>`__ for
more information on this format and on Rsyncing lists of urls.

There is also a command line utility installed with the HTRC Feature
Reader:

.. code:: bash

   $ htid2rsync miun.adx6300.0001.001
   miun/pairtree_root/ad/x6/30/0,/00/01/,0/01/adx6300,0001,001/miun.adx6300,0001,001.json.bz2

Advanced Features
~~~~~~~~~~~~~~~~~

In the beta Extracted Features release, schema 2.0, a few features were
separated out to an advanced files. However, *this designation is no
longer present starting with schema 3.0*, meaning information like
``beginLineChars``, ``endLineChars``, and ``capAlphaSeq`` are always
available:

.. code:: ipython3

    # What is the longest sequence of capital letter on each page?
    vol.cap_alpha_seqs()[:10]




.. parsed-literal::

    [0, 1, 0, 0, 0, 0, 0, 0, 4, 1]



.. code:: ipython3

    end_line_chars = vol.end_line_chars()
    print(end_line_chars.head())


.. parsed-literal::

                             count
    page section place char       
    2    body    end   -         1
                       :         1
                       I         1
                       f         1
                       t         1


.. code:: ipython3

    # Find pages that have lines ending with "!"
    idx = pd.IndexSlice
    print(end_line_chars.loc[idx[:,:,:,'!'],].head())


.. parsed-literal::

                             count
    page section place char       
    45   body    end   !         1
    75   body    end   !         1
    77   body    end   !         1
    91   body    end   !         1
    92   body    end   !         1


Testing
~~~~~~~

This library is meant to be compatible with Python 3.2+ and Python 2.7+.
Tests are written for py.test and can be run with ``setup.py test``, or
directly with ``python -m py.test -v``.

If you find a bug, leave an issue on the issue tracker, or contact Peter
Organisciak at ``organisciak+htrc@gmail.com``.
