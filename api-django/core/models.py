from django.db import models

# Create your models here.
class Video(models.Model):
  title = models.CharField(max_length=100, unique=True, verbose_name='Title')
  description = models.TextField(verbose_name='Description')
  thumbnail = models.ImageField(upload_to='thumbnails/', verbose_name='Thumbnail')
  slug = models.SlugField(unique=True)
  published_at = models.DateTimeField(verbose_name='Published At', null=True, editable=False)
  is_published = models.BooleanField(default=False, verbose_name='Is Published')
  num_likes = models.IntegerField(default=0, verbose_name='Likes', editable=False)
  num_views = models.IntegerField(default=0, verbose_name='Views', editable=False)
  tags = models.ManyToManyField('Tag', verbose_name='Tags', related_name='videos')

  def get_video_status_display(self):
    if not hasattr(self, 'video_media'):
      return 'Pending'
    return self.video_media.get_status_display()

  class Meta:
    verbose_name = 'Video'
    verbose_name_plural = 'Videos'

  def __str__(self):
    return self.title

class VideoMedia(models.Model):
  class Status(models.TextChoices):
    UPLOADED_STARTED = 'UPLOADED_STARTED', 'Uploaded Started'
    PROCESS_STARTED = 'PROCESSING_STARTED', 'Process Started'
    PROCESS_FINISHED = 'PROCESSING_FINISHED', 'Process Finished'
    PROCESS_ERROR = 'PROCESSING_ERROR', 'Process Error'
  
  video_path = models.CharField(max_length=255, verbose_name='Video')
  status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED_STARTED, verbose_name='Status')
  video = models.OneToOneField('Video', on_delete=models.PROTECT, verbose_name='Video', related_name='video_media')

  def get_status_display(self):
    return VideoMedia.Status(self.status).label
  
  class Media:
    verbose_name = 'Media'
    verbose_name_plural = 'Media'

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True, verbose_name='Name')

  class Meta:
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'

  def __str__(self):
    return self.name