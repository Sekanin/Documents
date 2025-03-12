import os
from django import template

register = template.Library()

FILE_TYPES = {
    '.pdf': 'pdf',
    '.png': 'image',
    '.jpg': 'image',
    '.jpeg': 'image',
    '.gif': 'image',
    '.doc': 'document',
    '.docx': 'document',
    '.xls': 'spreadsheet',
    '.xlsx': 'spreadsheet',
    '.txt': 'text',
    '.zip': 'archive',
    '.rar': 'archive',
    '.mp3': 'audio',
    '.mp4': 'video',
    '.mkv': 'video',
}

@register.filter
def get_file_type(item_name):
    if not item_name:
        return 'unknown'

    extension = os.path.splitext(item_name)[1].lower()

    return FILE_TYPES.get(extension, 'file')
