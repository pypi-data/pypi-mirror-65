# Toolbox
Package containing functions frequently used by me in other scripts
## How to install:
You can fork the rep or use pip:
 ``` python
 pip install gab_toolbox
 ```
## List of tools:

Here I will list and briefly describe the functions contained.

### valid_title:

Function used to check and eventually modify strings used for saving file names in case they contain not accepted symbols. 
```python
valid_title(title,[char])
```
The function checks if the string or array of strings specified in **title** is valid and returns the string/s with the invalid character/s replaced with a valid character set **= '_'** by [default]. If you want to change the substituting character  just change the **[char]** entry.

### import_file:
Function used to import files as an array. Every new line is a new entry of the array.

```python
importtxt(file)
```
In **file** you must specify the name and extension of the file you want to import and, if the file is not located in the working directory, you must add the full file path.

### write_file:
Function used to write text files from arrays. Every array entry will be written in a separeted line.

```python
write(array,file)
```

+ In **array** you must write the target array that needs to be exported. 
+ In **file** you must specify the name and extension. The full path name must be specified if you don't want the file in the working directory. 

### dic2arr:

Function used to convert dictionaries to a 2D array. Every entry corrisponds to a dict entry.

```python
dic2arr(dictionary,[order],[sort],[rev])
```
+ The first argument accepts the **dictionary** variable and it's the only obligatory argument. 
+ The **[order]** argument controls how the array is filled; for **order=0** [default] the resulting array will follow the dict order [key, value], for **order=1** the opposite.
+ The **[sort] and [rev]** arguments control the order of the array; for **sort = 1** the array will be sorted following an ascending order of the first value and then the second value of each array, for **rev = 1** the sorting order will be discending. By default **sort=0 and rev=0**.

### arr2dic(array,[sort],[rev])
Function used to convert 2D arrays in dictionaries. The array needs to be formatted as **[[*key*,*value*],...]** and every array will corrispond to a dict entry.

```python
arr2dic(array,[sort],[rev],[overwrite])
```
+ The first argument accepts the **array** variable and it's the only obligatory argument. 
+ The **[sort] and [rev]** argument control the order of the dictionary; for **sort = 1** the dictionary will be sorted following an ascending order of the first value of each array, for rev = 1 the sorting order will be discending. By [default] **sort=0 and rev=0**.
+ The **[overwrite]** argument gives the possibility to merge multiple *values* under the same *key*; for **overwrite=0** [default] the values will be merged while for **overwrite=1** it will only save the last *value* corresponding to the *key*.

