# ESPN-DataMining
Download NCAA Mens Baskteball Data for years 2012-Current and parse information for statistical purposes.

### Python Programs

The python programs GrabData.py and MakeDataFile.py were created first to data mine the NCAA Data. They are slow. Not only in fetching HTML data, but in opening and parsing the data once it was on the local machine. It took over 12 hours to open parse data and close 17000 files, to make a 380000 line file.

### C++ Programs

Once we saw how slow the Python version was, and how many changes we had to make to get the correct data, we started over in C++ to try and make it faster. The calls to grab the HTML data still take some time, considering over 17000 files are being called and created, but the other files go extremely quicker then the pthon counter part. When timing the latter 3 files (once the data has already been saved) the program ran in under 2 minutes. That means the C++ programs cut down 17000 files, purified the text of 17000 files, and then opened, parsed the data, and closed 17000 while making a 380000 line text file with the data in under 2 minutes. Compared to 12.5 hours, that is 375 times faster. Now I call that efficiency. 

#####Requirements:

Python: Keyring to send emails via python when the shell script crashes

      https://pypi.python.org/pypi/keyring
      
C++: libcurl, multiprotocol file transfer library. To transfer HTTP Files from espn to local computer.

      http://curl.haxx.se/libcurl/
