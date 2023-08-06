=========
Argunizer
=========

Description
-----------

Argunizer is a tool for restructuring an unstructured directory hierarchy into a 
temporal timeline of files in UTC, universal co-ordinated time. By an unstructured 
directory hierarchy I mean the types of directories, which users normally create 
on their desktops, which often encode meaning into the directory names.

Logic
-----

The timeline is contructed out of the last modification
times of all the files in the source directory. Each of the files is then either:
- symlinked under the destination directory (default)
- copied from source to destination directory
- moved from source to destination directory

Layout
^^^^^^

Files are rendered as 
- YYYY/MM/DD/<file>

Note
----

Optionally, it will also be possible to clean up an empty shell of directories, which
has resulted from the move semantics.
