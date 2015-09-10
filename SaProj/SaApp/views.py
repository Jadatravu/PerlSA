from django.shortcuts import render
from SaApp.models import Issue
from SaApp.models import Build
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime

import logging
logger = logging.getLogger(__name__)

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from SaApp.serializers import RestAppSerializer, RestBuildAppSerializer
from rest_framework import permissions

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
    pass

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
