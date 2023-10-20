#######
BCP47Py
#######

Provides standardized tags that is used to identify:

* Scripts
* Languages
* Ext Language
* Regions
* Grandfathered
* Redundant


.. warning::
   Following BCP47 extensions are not implemented:

   * **Extension T (Transformed Content)**: Extension T is described in the informational RFC 6497. It allows a language
     tag to include information on how the tagged data was transliterated, transcribed, or otherwise transformed. For
     example, the tag en-t-jp could be used for content in English that was translated from the original Japanese.
     Additional substrings could indicate that the translation was done mechanically, or in accordance with a
     published standard.
   * **Extension U (Unicode Locale)**: Extension U is described in the informational RFC 6067. It allows a wide variety of
     locale attributes found in the Common Locale Data Repository (CLDR) to be embedded in language tags. These attributes
     include country subdivisions, calendar and time zone data, collation order, currency, number system, and keyboard
     identification.