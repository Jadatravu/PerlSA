#!/usr/bin/env python
import base64
import urllib
import httplib2
import sys
import re

def call_remote(body,url,http,auth,headers):
    response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    #print response
    print content
    pass
#print sys.argv[1]
#print sys.argv[2]
#print sys.argv[3]

http = httplib2.Http()
auth = base64.encodestring( 'user' + ':' + 'password' )
headers = {'Content-type': 'application/x-www-form-urlencoded','Authorization' : 'Basic ' + auth }

"""
create build
curl -X POST -u "user:password" --data "name=FRI_AUG_2015&revision=1234&date_str=\"2015-09-03\"" http://127.0.0.1:8000/CreateBuild/
"""

create_build_body = {'name': sys.argv[2], 'revision': sys.argv[3],'date_str':sys.argv[2]}
create_build_url = 'http://127.0.0.1:9000/CreateBuild/'   
call_remote(create_build_body, create_build_url, http, auth, headers)

"""
open the file
"""

f = open(sys.argv[1])
"""
   read the file line by line
"""
for data in f.readlines():
    data_plus = re.findall("\+(.*)\+",data)   
    """
     parse the line
    """
    dp_lt = re.findall("\^(.*)\^(.*)\^(.*)\^(.*)\^",data_plus[0])
    #print list(dp_lt[0])
    dp_list = list(dp_lt[0])
    print ("line %s, column %s, severity %s, message %s"%(dp_list[0],dp_list[1],dp_list[2],dp_list[3]))
    """
      curl -X POST -u "user:password" --data "file_name=\"one.pl\"&description=\"one two three four\"&severity=0&line=100&column=10&build_name=FRI_AUG_2015&build_revision=1234" http://127.0.0.1:8000/UpdateIssue/ 

    """
    file_n = str(sys.argv[1]).split('/')[-1]
    #print "file_name " + str(file_n)
    update_issue_body = {'file_name': file_n, 'build_revision': sys.argv[3],'build_name':sys.argv[2],'line':dp_list[0],'column':dp_list[1], 'severity':dp_list[2], 'description':dp_list[3]}
    update_issue_url = 'http://127.0.0.1:9000/UpdateIssue/'   
    call_remote(update_issue_body, update_issue_url, http, auth, headers)
""" 
     upload the issue
"""
"""
complete build
curl -X POST -u "user:password" --data "name=FRI_AUG_2015&revision=1234&date_str=\"2015-09-03\"" http://127.0.0.1:8000/BuildComplete/
"""
build_complete_body = {'name': sys.argv[2], 'revision': sys.argv[3],'date_str':sys.argv[2]}
build_complete_url = 'http://127.0.0.1:9000/BuildComplete/'   
call_remote(build_complete_body, build_complete_url, http, auth, headers)



