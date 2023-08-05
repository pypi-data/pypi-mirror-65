# Max's Utilities

**dateRenamer**<p>
Changes the date in filenames from American to European or vice versa.  Handy to use on checking statements downloaded from your bank.

<b>ImageMetadata</b><p>
Utilities to extract, process and write image file metadata.
It synchronizes captions between the various formats.
The intent is to make the many captions created with Google's defunct Picasa
to be copied into other formats in the photo, so they appear when the
photo is viewed through more modern photo handlers.
There is also a routine to synchronize captions between a .JPG and a .TIFF.
The scanspeeder scanning software will create a JPG, and in a folder underneath it,
a TIFF with the same basename.  When you caption the JPG, you can run Synch_to_TIF
to get the caption copied to the TIF.

<b>myUtilities</b><p>
This is mostly devoted to setting up Python's logger, but also contains an o function, to return an ordinal, e.g. "1st"
a delim function to wrap a variable in delimiters (which is useful when composing SQL strings), etc.

