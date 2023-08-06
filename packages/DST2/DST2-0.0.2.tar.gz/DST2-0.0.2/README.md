
### The New DST QA Library (DST2)
DST2 is the new QA library that addresses issues like ease of use,dynamic reporting and error management.
The new library has only one function called "perform_qa" that does most of the check for the deliverables(similar pandas dataframes).
Functionalities
* Dynamic Error Management
* Flexible Reporting
* Search Operations
* Shorter Notebook Codes
* More..

### Installation and Importation
Installation of DST2 package can be made via pip as shown below.


```python
#pip install DST2
```


```python
#For iimporting the QA library
import DST2.QA as q
import pandas as pd
```

The package is built on top of pandas thus making it easier to compare dataframes


```python
dfOld = pd.read_excel('dataset/august.xlsx',sheet_name='Results') #change file names to something more intuitive like old.xlsx
dfNew = pd.read_excel('dataset/october_1.xlsx',sheet_name='Results')#change file names to something more intuitive like new.xlsx
```

#### Starting a QA process
When initiating a new QA process, you will hae to provide the following
* Name of the Excel report
* The previous and new deliverable via pandas
* The index column (a column name or a list of columns)


```python
#Initiate a QA process
qa = q.QA_Report("Report 1",dfOld,dfNew,'Company ID')
```


```python
#Create Reports
qa.create_report()
```


```python
#Let's create another report specifying parameters
```


```python
#Start a Report
qa2 = q.QA_Report("Report 2",dfOld,dfNew,'Company ID')
```

#### Perform QA 
This is the core of the QA process where you decide to:
* Perform column or score comparisons
* Set deltas
* Search columns for QA
* Perform QA on all columns


```python
#Perform QA on Columns comparisons
spec_cols = ['Highest Controversy Level-Answer Category','Does the company meet your screening criteria?'] #fields in both files
qa2.perform_qa(columns=spec_cols)
```


```python
#Perform QA on Score changes with default delta = 5
cols = ['Total ESG Score','Percentile']
qa2.perform_qa(columns=cols,type='score', delta=5) #default is 5 anyways
```


```python
#Create Reports
qa2.create_report()
```

#### Recap!
We have used 3 parameters with the perform_qa function which are

* choosing an index that identifies each row uniquely - 'Company ID' 
* columns -- To specify the columns to perform QA on
* type -- To specify if it is a column or score comparison and by default it performs a column comparison
* delta -- By default it is set to 5 and it is used when we perform a score comparison to define a threshold.


```python
#Start a Report
qa3 = q.QA_Report("Report 3",dfOld,dfNew,'Company ID')
```

### More on parameters
We have used 3 more parameters with the perform_qa function which are
* all_cols -- To perform QA on all columns and it is set to False by default
* keywords -- To search for some keywords in field names eligible for QA
* takeout_keywords -- To search for some keywords in field names NOT eligible for QA
* In this last example we have added the type score because we are performing score changes


```python
qa3.perform_qa(all_cols=True,takeout_keywords=['score','percentile'])
```


```python
qa3.perform_qa(keywords=['score','percentile'],takeout_keywords='overall',type='score', delta=10)
```


```python
qa3.create_report()
```
