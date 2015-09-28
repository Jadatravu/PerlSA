from django.conf.urls import patterns, url

from django.conf.urls import url, include
from rest_framework import routers
from SaApp import views

router = routers.DefaultRouter()
router.register(r'UpdateIssue', views.UpdateIssue, base_name = "issues")
router.register(r'IssueStatus', views.IssueStatus, base_name="issues")
router.register(r'CreateBuild', views.CreateBuild, base_name="builds")
router.register(r'BuildComplete', views.BuildComplete, base_name="builds")

urlpatterns = [
              url(r'^issue_bet_builds/$',views.BuildsIndex1),
              url(r'^new_issue_bet_builds/$',views.BuildsIssueIndex1),
              url(r'^fixed_issue_bet_builds/$',views.BuildsIssueIndex2),
              url(r'^new_issue_bet_builds1/$',views.BuildsIssueIndex3),
              url(r'^test/$',views.test123),
              url(r'^build_index/$',views.BuildsIndex),
              url(r'^', include( router.urls) ),
              url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
