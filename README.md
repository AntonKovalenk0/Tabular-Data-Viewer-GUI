# Tabular-Data-Viewer-GUI

The task was to build the viewer for the given tabular data.
I ended up making GUI with tkinter library.
Here I'll give some screenshots of the program.
In this project i'm working with: .sas7bdat, .xpt, .xlsx, .csv file extentions.
1) .sas7bdat data example:
![image](https://github.com/user-attachments/assets/b9242cf8-fd76-4cb7-acc6-7269a06a14dd)
2) For .xlsx file, you can switch between different sheets:
![image](https://github.com/user-attachments/assets/055cea8d-a003-4912-a9c5-7b4a28533e56)
3) Inside .csv file raw data was separated by '$':
![image](https://github.com/user-attachments/assets/4ae4a8f7-e941-48fe-9ac4-3961da2b6a6d)
![image](https://github.com/user-attachments/assets/8705744f-bc17-4a87-a3ab-f0bc1d94dc31)
4) En error occured while reading 't.xpt' file:
pyreadstat:
![image](https://github.com/user-attachments/assets/0c79d0e1-2670-4a45-9a55-f7a0ccd31623)
pandas:
ValueError: Header record indicates a CPORT file, which is not readable.

I've tried different methods to read that file but always got an error.
