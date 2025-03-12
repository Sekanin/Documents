from django.db import models
from django.contrib.auth.models import User

class FolderPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=255)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.folder_name}"

    class Meta:
        verbose_name = "Folder Permission"
        verbose_name_plural = "Folder Permissions"
