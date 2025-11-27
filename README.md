# A-Data-Driven-Look-into-Class-Division
A Data-Driven Look into Class Division: From Degrees to Demographics


External libraries:
pandas 
numpy
seaborn
matplotlib
sklearn
scipy.stats 
re
pathlib

These can be installed using the command pip install pandas numpy seaborn matplotlib scikit-learn scipy

Files required: analysis.py, cen_cleaning.py, combine_cleaned.py and all the CSV included.


Instructions:


---step 1
There are a total of 24 csv files available gotten from Statistcs Canada. These files are not the cleaned version. In order to clean them you must first run cen_cleaning.py. You can run the script by either clicking the play button or typing in the command python cen_cleaning.py. The file must be in the same directory as you are in. Running this file will create 24 new cleaned files. "clean" will be somewhere in the filename.

Note*: The cleaned datasets were not provided in order to keep things organized, if you wish to see the full analysis you must clean the given csv files first. 

Note*: Do not the change the file names provided, otherwise the cleaning script won't recognize them and won't run. 

Note*: Do not change the file names that the script creates, otherwise the next script won't run.

---step 2 
After cleaning, you can run the script combine_cleaned.py by either clicking the play button or typing python combine_cleaned.py into your terminal. This will create a new combined dataset called censusdatajoint.csv which has all the data we need for our analysis. 

Note*: Do not change the file name that the script creates, otherwise the next script won't run.

---step3
After combining the data, you can run analysis.py by either clicking on the play button in you IDE or typing in the command python analysis.py
This script will create several visuals and output some results from the tests that were performed. 

Note*: If you are on mac or for whatever reason python filename.py command to run does not work for you, you can try python3 filename.py. If that doesn't work either just cick the play button. 

Note*: The analysis report is also available as a pdf file.




