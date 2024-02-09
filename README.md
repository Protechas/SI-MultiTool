SIMultitool.exe is a Python code that will analyze all PDFs in a folder (and the folders inside) that you select within the GUI to determine whether or not it has BLUE and/or YELLOW highlights. Once this is done, it will then make a copy of the documents that include only the pages with highlights that will be saved to a location of your choice. While doing this, the program will also compress the new file to make sure attachments are sent without error, while keeping the quality of the original PDF and without corrupting any documents. 

 

Update: 

New file name is SI MultiTool.py 

This update now includes the 4 following functional buttons within the GUI: 

1. "Compress" Compresses PDFs within the folder selected and presents an output with any files that could not be compressed. 

2. "Copy Yellow Highlights" This will copy all pages from PDFs within the folder that have yellow highlights. 

3. "Copy Blue Highlights" This will copy all pages from PDFs within the folder that have blue highlights. 

4. "Copy Y/B Highlights" This function will copy all highlighted pages from PDFs withing the folder that have yellow and/or blue highlights. 

 

If a PDF has more than one page that has the selected color, they will all be merged into one copied PDF. File compression will still be ran while keeping file quality. 

All copied PDFs will have the same name as the original file aside from the ending. At the end of each copied name will be one of the following: 

 

1. _Blue 

2. _Yellow 

3. _YB 

 

When using the "Compress" option, all files above 1400kb are put into their own folders with the same name. They are then split into parts and labeled as, part-1, part-2 etc. 

 

There are parts of the code that have been implemented in order to make additions and/or modifications as necessary. 

 

Conclusion: 

Pilot test successful 

No opportunities based on the functions we're looking for at this time 
