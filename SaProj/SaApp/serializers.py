from django.forms import widgets
from rest_framework import serializers
from SaApp.models import Issue
from SaApp.models import Build

class RestAppSerializer(serializers.ModelSerializer):
      """
         This is a serializer class for Issue web api
      """
      class Meta:
           model = Issue
           fields = ('file_name','description','severity','line')

class RestBuildAppSerializer(serializers.ModelSerializer):
      """
         This is a serializer class for Issue web api
      """
      class Meta:
           model = Build
           fields = ('name','revision','build_date','complete_flag')
