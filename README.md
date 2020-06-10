# ssc_project
## Overview
web automation, web crawler, and xml file generator to support SSCC website revamp.
<br>
Only "kb_xml.py" is used for KB migration. The program generates xml file that matches file 
format as specified in <a>https://kb.wisc.edu/kbAdmin/index.php?group_id=400&t=Documents&mi=19</a>. 
<br>
"map_tool.py" is used to map links in migrated document to link to the
other migrated documents instead of original documents.

December 2019 ~ June 2020
## Prerequisites
the program requires python/python3 and following packages
### "kb_xml.py" & "web_crawl.py"
```
pip3 install bs4
pip3 install pandas
```
### "web_automation.py"
```
pip3 install selenium
pip3 install pandas
```

### "map_tool"
```bash
pip3 install bs4
pip3 install pandas
pip3 install PyQt5
```

## Run
### "kb_xml.py"
```
python3 kb_xml.py
```
The program will prompt:<br>
```from what index to start:``` write down integer value that indicates index within "links_pub.csv".
<br>
```how many links to batch:``` write down integer value that indicates the number of links in a batch
<br>
```batch id:``` write down string value that indicates batch id. The program will later record
batch id in Batch section of "links_pub.csv" file. 
<br>
<br>
example usage:

```from what index to start: 10 ``` 
<br>
```how many links to batch: 20``` 
<br>
```batch id: test.xml```
<br>
links from index 10 to 29 (20 files [10, 11, ... ,28, 29]) will be converted into "xml_files/test.xml" file.
Also, for debugging purpose, there will be log created in "log.txt" file that shows success/fail of conversion.


### "map_tool.py"
```bash
python3 map_tool.py
```
[![YouTube Thumbnail](http://i3.ytimg.com/vi/aovVOvcyinc/maxresdefault.jpg)](https://www.youtube.com/watch?v=aovVOvcyinc)

