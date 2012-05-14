I created this project mainly because I take photos extensively for my
photolog and like them to be saved with the timestamp as the filename so that
they can be accessed quickly later.

This script will rename all the files of the supplied type in a specified directory **RECURSIVELY** as the date and time of their creation.

Changelog:

-Added checking for filetype and path
-Made invocation similar to standard command line script invocations
-Added a suffix counter to the filename in case multiple pictures were taken in a second, doesn't skip renaming anymore
-Fixed an issue which caused files to be overwritten if all of them were created
 within the span of a measurable second ( applicable only for DSLR pictures,
 issue doesn't arise in digicams), Skips renaming duplicates instead of overwriting
-FIXED AN ISSUE WHICH CAUSED CORRUPTION OF ALL RENAMED FILES.PLEASE UPDATE YOUR CODE.

**BE EXTREMELY CAREFUL** 
If you want to rename files only in the current directory, make sure you give the path to the child directory.
Consider this enough warning.

I have made this generic for all file types. It will work nicely for any file type
Just enter the file type as the last command line argument. Case is important ( As of now ;) )
Whitespaces have been taken care of

How To :

Just type the following command in the terminal :

python phototime.py --ftype=filetype --path=filepath


Wishlist :

-Make the code independent of case
-Add support for extension using * instead of specifying extension 
