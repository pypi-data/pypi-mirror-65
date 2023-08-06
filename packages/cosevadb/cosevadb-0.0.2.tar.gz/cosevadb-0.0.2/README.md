Python module to handle csv files as tables of SQL RDBMS.
We can pass SQL queries to parse and retreive data from csv files

### Usage
```
import cosevadb
cosevadb.query("select name,age from data/passengers.csv,data/header.csv where native='USA'")
```
#### Return type
```
[sqlcode,'<success/error message>',[result/empty]]

On error  >>> SQLCode=-1, empty result list
On success>>> SQLCode=0
```
#### Reserved words
SELECT

FROM

WHERE

### Operators supported
Arithmatic operators : +, -, *, /, %

Comparison operators : >, <, >=, <=, =, !=

Logical operators : &,|

### Operator precedence (in order from high to low)
'%'

'/'

'*'

'+'

'-'

'<','<='

'>','>='

'!'

'='

'&'

'|'

### File formats
Comma seperated value(.csv) files.

### Instructions
* String values should be within '<string>'
* A file with headers(Comma separated) should be passed along with csv data file
* As of now only select operations implemented
* Comparison operator '=' is used instead of '=='
* Expression evaluation will use BODMAS and have individual operator precedence unlike python or java. i.e., '9-7+1' will result '1'

### Licence
MIT Licence. Contributions are welcome

![](screenshot.png)
