from django.db import models

# Create your models here.
class Build( models.Model ):
      name = models.CharField( max_length = 50 )
      revision = models.IntegerField( default = 0 )
      build_date = models.DateField( blank = False )
      complete_flag = models.BooleanField(default = False)
      class Meta:
         unique_together = ( ("name", "revision", "build_date"),)

class Issue( models.Model ):
      file_name = models.CharField( max_length = 1000 )
      description = models.CharField( max_length = 1000 )
      severity = models.IntegerField( default = 0 )
      line = models.IntegerField( default = 0 )
      column = models.IntegerField( default = 0 )
      build = models.ManyToManyField( Build )
      class Meta:
         unique_together = ( ("file_name", "description", "line", "column"),)
