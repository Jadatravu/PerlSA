from django.shortcuts import render
from SaApp.models import Issue
from SaApp.models import Build
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime

import urllib2
from unidiff import PatchSet

import pysvn

import logging
logger = logging.getLogger(__name__)

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from SaApp.serializers import RestAppSerializer, RestBuildAppSerializer
from rest_framework import permissions

def ssl_server_trust_prompt(trust_dict):
    return True, trust_dict['failures'], True
    #return retcode, accepted_failures, save

def login(*args):
    #name = raw_input("Enter your svn login : ")
    #password = getpass.getpass("Enter your svn password :")
    #return True, name, password, False
    return True, 'sjanardhana', 'Polycom@123', False


def BuildsIndex(request):
    res_str = ''
    build_list = []
    build_id_list = []
    build_objs = Build.objects.filter(complete_flag = True)
    build_dic = {}
    for bu in build_objs:
        build_dic1 = {}
        build_id_list.append(bu.id)
        build_dic1['name'] = bu.name
        build_dic1['revision'] = bu.revision
        build_dic1['issues'] = len(bu.issue_set.all())
        build_dic[bu.id] = build_dic1
        #build_list.append(build_dic)
    build_id_list.sort()    
    return render_to_response(
                      'builds_index.html',
                       {'user':request.user,'message':res_str,'build_list':build_list, 'build_id_list':build_id_list, 'build_dic': build_dic},
                       context_instance=RequestContext(request)
                     )#

def test123(request):
    logger.debug("test")
    logger.error("test")
    logger.info("test")
    logger.warning("test")
    logger.critical("test")
    return render_to_response(
                      'difference_issues.html',
                       {'user':request.user,'message':'','i_fixed':[], 'i_added':[]},
                       context_instance=RequestContext(request)
                     )#

def get_oldfile_line_num(pa, newfile_line_num):
    old_file_range = []
    line_range = []
    count = 0
    for pad in pa:
       logger.debug("step 1 -->")
       logger.debug(newfile_line_num)
       logger.debug(pad.source_start)
       logger.debug(pad.source_length)
       logger.debug(pad.target_start)
       logger.debug(pad.target_length)
       logger.debug(pad.added)
       logger.debug(pad.removed)
       logger.debug(count)
       logger.debug("<--- step 1")
       if newfile_line_num < pad.target_start:
          if count == 0:
             line_range.append(newfile_line_num)
          else:
             source_start = abs( int(pa[count-1].source_start))
             target_start = abs(int(pa[count-1].target_start))
             source_length =abs( int(pa[count-1].source_length))
             target_length = abs( int(pa[count-1].target_length))
             earlier_source_end = int(source_start) + int(source_length)
             earlier_target_end = int(target_start) + int(target_length)
             offset = int(newfile_line_num) - int(earlier_target_end)
             pad_later = int(earlier_source_end) + int(offset)+int(pa[count-1].added) + int(pa[count-1].removed)
             pad_first = int(earlier_source_end) + int(offset)-int(pa[count-1].added) - int(pa[count-1].removed)
             line_range.append(pad_first)
             line_range.append(pad_later)
             pass
          logger.debug("if 1 step 2 -->")
          for lr in line_range:
             logger.debug(lr)
          logger.debug("<--if 1 step 2")
          break
       elif ((int(newfile_line_num) > int(pad.target_start)) and (int(newfile_line_num) < (int(pad.target_start) + int(pad.target_length)))):
                line_range.append(int(pad.source_start) - int(pad.added) -int(pad.removed))
                line_range.append(int(pad.source_start)+int(pad.source_length) + int(pad.added) + int(pad.removed))
                logger.debug("if 2 step 2 -->")
                for lr in line_range:
                   logger.debug(lr)
                logger.debug("<--if 2 step 2")
                break
       else:
           if (int(count)+1) == len(pa):
             source_start = abs( int(pa[count].source_start))
             target_start = abs(int(pa[count].target_start))
             source_length =abs( int(pa[count].source_length))
             target_length = abs( int(pa[count].target_length))
             earlier_source_end = int(source_start) + int(source_length)
             earlier_target_end = int(target_start) + int(target_length)
             offset = int(newfile_line_num) - int(earlier_target_end)
             pad_later = int(earlier_source_end) + int(offset)+int(pa[count].added) + int(pa[count].removed)
             pad_first = int(earlier_source_end) + int(offset)-int(pa[count].added) - int(pa[count].removed)
             line_range.append(pad_first)
             line_range.append(pad_later)
             logger.debug("if 3 step 2 -->")
             for lr in line_range:
                logger.debug(lr)
             logger.debug("<--if 3 step 2")
             break
       count += 1
    return line_range

def get_oldfile_line_num1(pa, newfile_line_num):
    old_file_range = []
    line_range = []
    count = 0
    for pad in pa:
       if newfile_line_num < pad.target_start:
          if count == 0:
             old_file_range.append(newfile_line_num)
             break
          else:
             source_start = target_start = source_length = target_length = 0
             source_start = abs( int(pa[count-1].source_start))
             target_start = abs(int(pa[count-1].target_start))
             source_length =abs( int(pa[count-1].source_length))
             target_length = abs( int(pa[count-1].target_length))
             logger.debug(">>>")
             logger.debug("-->")
             logger.debug(source_start)
             logger.debug(target_start)
             logger.debug(source_length)
             logger.debug(target_length)
             earlier_source_end = int(source_start) + int(source_length)
             earlier_target_end = int(target_start) + int(target_length)
             offset = int(newfile_line_num) - int(earlier_target_end)
             logger.debug(newfile_line_num)
             logger.debug(earlier_target_end)
             logger.debug(offset)
             logger.debug(pad.added)
             logger.debug(pad.removed)
             logger.debug("<--")
             pad_later = int(earlier_source_end) + int(offset)+int(pad.added) + int(pad.removed)
             pad_first = int(earlier_source_end) + int(offset)-int(pad.added) - int(pad.removed)
             #pad_later = int(earlier_source_end) + int(offset)
             #pad_first = int(earlier_source_end) + int(offset)
             logger.debug(pad_first)
             logger.debug(pad_later)
             line_range=[]
             line_range.append(pad_first)
             line_range.append(pad_later)
             old_file_range = line_range
             logger.debug(len(old_file_range))
             for ofr in line_range:
                 logger.debug( ofr)
             logger.debug("<<<")
             break
          pass
       elif ((int(newfile_line_num) > int(pad.target_start)) and (int(newfile_line_num) < (int(pad.target_start) + int(pad.target_length)))):
            new_file_range = range(int(pad.target_start),(int(pad.target_start)+int(pad.target_length)),1)
            if (new_file_range.__contains__(int(newfile_line_num))):
                #old_file_range.append(int(pad.source_start))
                #old_file_range.append(int(pad.source_start)+int(pad.source_start)+int(pad.source_length))
                line_range.append(int(pad.source_start))
                line_range.append(int(pad.source_start)+int(pad.source_start)+int(pad.source_length))
                break
       else:
           if (int(count)+1) == len(pa):
             source_start = target_start = source_length = target_length = 0
             source_start = abs( int(pa[count-1].source_start))
             target_start = abs(int(pa[count-1].target_start))
             source_length =abs( int(pa[count-1].source_length))
             target_length = abs( int(pa[count-1].target_length))
             earlier_source_end = int(source_start) + int(source_length)
             earlier_target_end = int(target_start) + int(target_length)
             offset = newfile_line_num - earlier_target_end
             logger.debug(">>>")
             logger.debug("-->")
             logger.debug(source_start)
             logger.debug(target_start)
             logger.debug(source_length)
             logger.debug(target_length)
             logger.debug(newfile_line_num)
             logger.debug(earlier_target_end)
             logger.debug(offset)
             logger.debug(pad.added)
             logger.debug(pad.removed)
             logger.debug("<--")
             pad_later = int(earlier_source_end) + int(offset)+int(pad.added) + int(pad.removed)
             pad_first = int(earlier_source_end) + int(offset)-int(pad.added) - int(pad.removed)
             #pad_later = int(earlier_source_end) + int(offset)
             #pad_first = int(earlier_source_end) + int(offset)
             logger.debug(pad_first)
             logger.debug(pad_later)
             line_range=[]
             line_range.append(pad_first)
             line_range.append(pad_later)
             old_file_range = line_range
             logger.debug(len(old_file_range))
             #old_file_range.append(pad_first)
             #old_file_range.append(pad_later)
             #old_file_range = [pad_first,pad_later]
             for ofr in line_range:
                 logger.debug( ofr)
             logger.debug("<<<")
             pass
             break
       count += 1
    logger.debug(">>>")
    for ofr in line_range:
        logger.debug( ofr)
    logger.debug("<<<")
    #return old_file_range
    return line_range

def BuildsIssueIndex3(request):
    logger.debug("test")
    logger.debug("test")
    res_str = ""
    issues_added = []
    if request.method == 'GET':
        build1 = request.GET['build1']
        build2 = request.GET['build2']
        build1_objs = Build.objects.filter(name = build1)
        if len(build1_objs) == 0:
            return
        build2_objs = Build.objects.filter(name = build2)
        if len(build2_objs) == 0:
            return
        build1_revision = build1_objs[0].revision
        build2_revision = build2_objs[0].revision
        client = pysvn.Client()
        client.callback_get_login = login
        client.callback_ssl_server_trust_prompt = ssl_server_trust_prompt
        work_path = '/root/PerlSA/02Sep15/lib'
        tmp_path="/tmp/tmp123"
        head = pysvn.Revision(pysvn.opt_revision_kind.number, int(build1_revision))
        end = pysvn.Revision(pysvn.opt_revision_kind.number, int(build2_revision))
        diff_text = client.diff(tmp_path = tmp_path,url_or_path = work_path, revision1=head, revision2=end,recurse=True)
        svn_diff_file = str("/tmp/svn_diff_files/ta_root3_lib_") + str(build1_revision) + str("_") + str(build2_revision) + str(".diff")
        #with open("/tmp/1oct15.diff","w+") as f:
        f = open(svn_diff_file,"w+") 
        f.write(diff_text) 
        f.close()
        issues_build1 = build1_objs[0].issue_set.all()
        issues_build2 = build2_objs[0].issue_set.all()
        new_issue_list = []
        #diff = urllib2.urlopen("file:///tmp/ta_root3_lib_47593_47715.diff")
        svn_diff_file_url = str("file://") + svn_diff_file
        diff = urllib2.urlopen(svn_diff_file_url)
        encoding = diff.headers.getparam('charset')
        patch = PatchSet(diff,encoding=encoding)
        modified_files_list = []
        for pa in patch:
           modified_files_list.append(pa.path.split('/')[-1])
        for msl in modified_files_list:
            logger.debug(msl)
        for ib2 in issues_build2:
          if modified_files_list.__contains__(ib2.file_name.split('^')[-1]):
            #if ib2.file_name.__contains__("Nav.pm"):
            logger.debug("Issue &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            logger.debug("--1")
            logger.debug(ib2.file_name)
            logger.debug(ib2.line)
            logger.debug("--1")
            issue_exists_flag = False
            ib1_objs = build1_objs[0].issue_set.filter(id = ib2.id)
            if (len(ib1_objs) > 0):
                  issue_exists_flag = True
            else:
                if False :
                    issue_exists_flag = True
                else:
                    file_actual_name = ib2.file_name.split('^')[-1]
                    old_file_range = []
                    check_range = []
                    logger.debug(">>>>>>>>>>++++++++++")
                    logger.debug(file_actual_name)
                    for pa in patch:
                        pa_path = str(pa.path).split('/')[-1]
                        #if str(pa_path).__eq__(str(file_actual_name)):
                        #file_actual_name=str("Nav.pm")
                        if str(pa_path).__eq__(str(file_actual_name)):
                           old_file_range = get_oldfile_line_num(pa, int(ib2.line))
                           for ofr in old_file_range:
                               logger.debug(ofr)
                           break
                    logger.debug("++++++++++<<<<<<<<<<<<<<<<<<<<")
                    #check_range = range(int(ib2.line)-10, int(ib2.line)+10, 1)
                    for ofr in old_file_range:
                        logger.debug(ofr)
                    logger.debug(len(old_file_range))
                    if int(len(old_file_range)) > int(1):
                       logger.debug(old_file_range[0])
                       logger.debug(old_file_range[1])
                       check_range = range(old_file_range[0], old_file_range[1], 1)
                    elif len(old_file_range) == 1:
                        check_range.append(old_file_range[0])
                    else:
                        logger.debug("no check range>>>>>>>>>")
                        logger.debug(ib2.file_name)
                        logger.debug(ib2.line)
                        logger.debug("<<<<<<<<<<<no check range")
                        check_range = []
                    #check_range = old_file_range
                    logger.debug("--2")
                    for ch in check_range:
                       logger.debug(ch)
                    logger.debug("--2")
                    if len(check_range) > 1:
                         ib1_objs_check2 = build1_objs[0].issue_set.filter(file_name = ib2.file_name, description = ib2.description, line__in = check_range, column = ib2.column, severity = ib2.severity) 
                         if (len(ib1_objs_check2) > 0):
                            logger.debug("issue exists")
                            issue_exists_flag = True
                    elif len(check_range) == 1:
                         ib1_objs_check2 = build1_objs[0].issue_set.filter(file_name = ib2.file_name, description = ib2.description, line = check_range[0], column = ib2.column, severity = ib2.severity) 
                         if (len(ib1_objs_check2) > 0):
                            logger.debug("issue exists")
                            issue_exists_flag = True
            if issue_exists_flag == False:
               logger.debug("====new issue")
               logger.debug(ib2.line)
               logger.debug(ib2.file_name)
               logger.debug("new issue ====")
               new_issue_list.append(ib2)
            logger.debug("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&Issue")
    return render_to_response(
                      'difference_issues.html',
                       {'user':request.user,'message':res_str,'i_fixed':[], 'i_added':new_issue_list},
                       context_instance=RequestContext(request)
                     )#

def BuildsIssueIndex2(request):
    res_str = ""
    issues_fixed = []
    issues_added = []
    if request.method == 'GET':
        build1 = request.GET['build1']
        build2 = request.GET['build2']
        build1_objs = Build.objects.filter(name = build1)
        if len(build1_objs) == 0:
            return
        build2_objs = Build.objects.filter(name = build2)
        if len(build2_objs) == 0:
            return
        issues_build1 = build1_objs[0].issue_set.all()
        issues_build2 = build2_objs[0].issue_set.all()
        fixed_issue_list = []
        for ib1 in issues_build1:
            fixed_issue_flag = True
            ib2_objs = build2_objs[0].issue_set.filter(id = ib1.id)
            if (len(ib2_objs) > 0):
                  fixed_issue_flag = False
            else:
                if False :
                    fixed_issue_flag = False
                else:
                    check_range = range(int(ib1.line)-10, int(ib1.line)+10, 1)
                    ib2_objs_check2 = build2_objs[0].issue_set.filter(file_name = ib1.file_name, description = ib1.description, line__in = check_range, column = ib1.column, severity = ib1.severity) 
                    if (len(ib2_objs_check2) > 0):
                        fixed_issue_flag = False
                #"""
            if fixed_issue_flag == True:
               fixed_issue_list.append(ib1)
    return render_to_response(
                      'difference_issues.html',
                       {'user':request.user,'message':res_str,'i_fixed':fixed_issue_list, 'i_added':[]},
                       context_instance=RequestContext(request)
                     )#

def BuildsIssueIndex1(request):
    res_str = ""
    issues_fixed = []
    issues_added = []
    if request.method == 'GET':
        build1 = request.GET['build1']
        build2 = request.GET['build2']
        build1_objs = Build.objects.filter(name = build1)
        if len(build1_objs) == 0:
            return
        build2_objs = Build.objects.filter(name = build2)
        if len(build2_objs) == 0:
            return
        issues_build1 = build1_objs[0].issue_set.all()
        issues_build2 = build2_objs[0].issue_set.all()
        new_issue_list = []
        for ib2 in issues_build2:
            issue_exists_flag = False
            ib1_objs = build1_objs[0].issue_set.filter(id = ib2.id)
            if (len(ib1_objs) > 0):
                  issue_exists_flag = True
            else:
                #"""
                #ib1_objs_check1 = build1_objs[0].issue_set.filter(file_name = ib2.file_name, description = ib2.description, line = ib2.line, column = ib2.column, severity = ib2.severity) 
                #if (len(ib1_objs_check1) > 0):
                if False :
                    issue_exists_flag = True
                else:
                    check_range = range(int(ib2.line)-10, int(ib2.line)+10, 1)
                    ib1_objs_check2 = build1_objs[0].issue_set.filter(file_name = ib2.file_name, description = ib2.description, line__in = check_range, column = ib2.column, severity = ib2.severity) 
                    if (len(ib1_objs_check2) > 0):
                        issue_exists_flag = True
                    """
                    #check backward for 10 lines
                    if issue_exists_flag == False:
                        #check forward for 10 lines
                        check_range = range(int(ib2.line)-2, int(ib2.line)-11, -1)
                        ib1_objs_check3 = build1_objs[0].issue_set.filter(file_name = ib2.file_name, description = ib2.description, line__in = check_range, column = ib2.column, severity = ib2.severity) 
                        if (len(ib1_objs_check3) > 0):
                            issue_exists_flag = True
                    """
                #"""
            if issue_exists_flag == False:
               new_issue_list.append(ib2)
    return render_to_response(
                      'difference_issues.html',
                       {'user':request.user,'message':res_str,'i_fixed':[], 'i_added':new_issue_list},
                       context_instance=RequestContext(request)
                     )#

def BuildsIndex1(request):
    res_str = ""
    issues_fixed = []
    issues_added = []
    if request.method == 'GET':
        build1 = request.GET['build1']
        build2 = request.GET['build2']
        build1_objs = Build.objects.filter(name = build1)
        if len(build1_objs) == 0:
            #res_str = str("build %s doesnot exist)%build1 
            return
        build2_objs = Build.objects.filter(name = build2)
        if len(build2_objs) == 0:
            #res_str = str("build %s doesnot exist)%build2 
            return
        issues_build1 = build1_objs[0].issue_set.all()
        issues_build2 = build2_objs[0].issue_set.all()
        issues_build1_list = []
        for iss1 in issues_build1:
            issues_build1_list.append(iss1.id)
        issues_build2_list = []
        for iss2 in issues_build2:
            issues_build2_list.append(iss2.id)
        issues_id_fixed = list(set(issues_build1_list) - set(issues_build2_list))
        issues_id_added = list(set(issues_build2_list) - set(issues_build1_list))
        for i_id_f in issues_id_fixed:
            issues_fixed.append(Issue.objects.get(id = i_id_f))
        for i_id_a in issues_id_added:
            issues_added.append(Issue.objects.get(id = i_id_a))
    return render_to_response(
                      'difference_issues.html',
                       {'user':request.user,'message':res_str,'i_fixed':issues_fixed, 'i_added':issues_added},
                       context_instance=RequestContext(request)
                     )#


class UpdateIssue(viewsets.ModelViewSet):
    cons = []
    file_name = str('')
    issue_desc = str('')

    def g_data(self):
        self.file_name = self.request.GET['file_name']
        self.issue_desc = self.request.GET['description']
        self.line = self.request.GET['line']
        self.column = self.request.GET['column']
        self.severity = self.request.GET['severity']
        self.build_name = self.request.GET['build_name']
        self.build_revision = self.request.GET['build_revision']
        self.cons = Issue.objects.filter(file_name__contains = self.file_name, description__contains = self.issue_desc, line= self.line, column = self.column)
        if ( len(self.cons) == 0 ):
            """ issue not present in the database to be added
            """
            pass 
        else:
            """ issue present in the database to be build added
            """
            pass 

    def get_queryset(self):
        #self.g_data()
        return self.cons

    def create(self,request):
        self.file_name = request.POST['file_name']
        self.issue_desc = request.POST['description']
        self.line = request.POST['line']
        self.column = request.POST['column']
        self.severity = request.POST['severity']
        self.build_name = request.POST['build_name']
        self.build_revision = request.POST['build_revision']
        self.cons = Issue.objects.filter(file_name = self.file_name, description = self.issue_desc, line= self.line, column = self.column)
        if ( len(self.cons) == 0 ):
            """ issue not present in the database to be added
            """
            pass 
            build_objs = Build.objects.filter(name=self.build_name, revision = self.build_revision)
            if len( build_objs ) == 0:
                return HttpResponse("Build Doesnot Exist")
            else:
                issue = Issue(file_name = self.file_name, description = self.issue_desc, severity= self.severity, line = self.line, column = self.column)
                issue.save()
                issue.build.add(build_objs[0])
                return HttpResponse("Issue Added")
        else:
            """ issue present in the database to be build added
            """
            build_objs = Build.objects.filter(name=self.build_name, revision = self.build_revision)
            if len( build_objs ) == 0:
                return HttpResponse("Build Doesnot Exist")
            else:
                self.cons[0].build.add(build_objs[0])
                return HttpResponse("Issue added to the Build")

            pass 
        #return self.cons

    serializer_class = RestAppSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticated,)

class BuildComplete(viewsets.ModelViewSet):
    def create(self, request):
        self.build_name = self.request.POST['name']
        self.revision = self.request.POST['revision']
        self.date_str = self.request.POST['date_str']
        build_objs = Build.objects.filter(name = self.build_name, revision = self.revision)
        if ( len(build_objs) == 0 ):
            """ build not present in the database to be added
            """
            pass 
            return HttpResponse("Build doesnot exist")
        else:
            """ build present in the database to be build added
            """
            pass 
            build_objs[0].complete_flag = True
            build_objs[0].save()
            return HttpResponse("Build marked as complete")
    serializer_class = RestBuildAppSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticated,)

class CreateBuild(viewsets.ModelViewSet):
    cons = []
    file_name = str('')
    issue_desc = str('')

    def g_data(self):
        self.build_name = self.request.GET['name']
        self.revision = self.request.GET['revision']
        self.date_str = self.request.GET['date_str']
        self.cons = Build.objects.filter(name__contains = self.build_name, revision = self.revision)
        if ( len(self.cons) == 0 ):
            """ build not present in the database to be added
            """
            pass 
        else:
            """ build present in the database to be build added
            """
            pass 
    def create(self, request):
        self.build_name = self.request.POST['name']
        self.revision = self.request.POST['revision']
        self.date_str = self.request.POST['date_str']
        self.cons = Build.objects.filter(name__contains = self.build_name, revision = self.revision)
        if ( len(self.cons) == 0 ):
            """ build not present in the database to be added
            """
            build = Build(name = self.build_name, revision = self.revision, build_date = datetime.datetime.now(), complete_flag = False) 
            build.save()
            pass 
            return HttpResponse("Build created")
        else:
            """ build present in the database to be build added
            """
            pass 
            return HttpResponse("Build already Present in the database")

    def get_queryset(self):
        self.g_data()
        return self.cons

    serializer_class = RestBuildAppSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticated,)

class IssueStatus(viewsets.ModelViewSet):
    cons = []
    file_name = str('')
    issue_desc = str('')

    def g_data(self):
        self.file_name = self.request.GET['file_name']
        self.issue_desc = self.request.GET['description']
        self.line = self.request.GET['line']
        self.column = self.request.GET['column']
        self.severity = self.request.GET['severity']
        self.cons = Issue.objects.filter(file_name = self.file_name, description = self.issue_desc, severity = self.severity, line = self.line, column = self.column)
        if ( len(self.cons) == 0 ):
            """ new issue
            """
            pass 
        else:
            """ issue present in the database
            """
            pass 

    def get_queryset(self):
        self.g_data()
        return self.cons

    def create(self,request):
        self.file_name = request.POST['file_name']
        self.issue_desc = request.POST['description']
        self.line = request.POST['line']
        self.column = request.POST['column']
        self.severity = request.POST['severity']
        #return HttpResponse("file _name %s"%(self.file_name))
        #return HttpResponse( str("line :%d, col:%d"%(int(self.line),int(self.column))))
        issue_objs = Issue.objects.filter(file_name = str(self.file_name), description = str(self.issue_desc), line= int(self.line), column = int(self.column), severity = int(self.severity))
        logger.debug(len(issue_objs))
        if ( len(issue_objs) == 0 ):
            return HttpResponse("Issue doesnot Exists[ New Issue ]")
        else:
            return HttpResponse("Issue exists")

    serializer_class = RestAppSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticated,)
