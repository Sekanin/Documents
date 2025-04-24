import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FolderPermission

BASE_FOLDER_PATH = getattr(settings, 'BASE_FOLDER_PATH', 'C:/Users/SEKAN/Desktop/docs')
DEFAULT_ICON_PATH = '/static/myapp/images/default.jpg'


def home(request):
    return render(request, "home/index.html")


@login_required
def open_folder(request):
    user_permissions = FolderPermission.objects.filter(user=request.user)
    allowed_folders = [perm.folder_name for perm in user_permissions if perm.can_view]
    folders = [folder for folder in os.listdir(BASE_FOLDER_PATH) if folder in allowed_folders]

    return render(request, 'myapp/folders_list.html', {'folders': folders})

def list_folder_contents(folder_path):
    folder_contents = []
    allowed_file_types = {'.pdf'}

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            subfolder_contents = list_folder_contents(item_path)
            folder_contents.append({
                'name': item,
                'type': 'folder',
                'contents': subfolder_contents
            })

        elif any(item.endswith(ext) for ext in allowed_file_types):
            jpg_name = item[:-4] + '.jpg'
            jpg_path = os.path.join(folder_path, jpg_name)

            if os.path.exists(jpg_path):
                icon_path = os.path.join(settings.STATIC_URL, 'myapp/images', jpg_name)
            else:
                icon_path = DEFAULT_ICON_PATH

            folder_contents.append({
                'name': item,
                'type': 'file',
                'icon': icon_path
            })

    return folder_contents

@login_required
def folder_view(request, folder_name):
    folder_path = os.path.join(BASE_FOLDER_PATH, folder_name)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        folder_contents = list_folder_contents(folder_path)
        return render(request, 'myapp/folder_contents.html', {
            'folder_contents': folder_contents,
            'folder_name': folder_name,
        })
    else:
        return HttpResponse('Folder not found', status=404)

@login_required
def dynamic_subfolder_view(request, folder_name, subfolder_names):
    try:
        folder_path = os.path.join(BASE_FOLDER_PATH, folder_name, subfolder_names)
        print(f"Folder root : {folder_path}")

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            folder_contents = list_folder_contents(folder_path)
            context = {
                'folder_contents': folder_contents,
                'folder_name': folder_name,
                'subfolder_names': subfolder_names,
            }
            return render(request, 'myapp/subfolder_contents.html', context)
        else:
            print(f"Folder not found : {folder_path}")
            return HttpResponse('Folder not found', status=404)
    except Exception as e:
        print(f"Error : {e}")
        return HttpResponse('Internal Server Error', status=500)

def handle_file_response(file_path, file_name):
    with open(file_path, 'rb') as file:
        if file_name.endswith('.pdf'):
            response = HttpResponse(file.read(), content_type='application/pdf')
        elif file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            response = HttpResponse(file.read(), content_type='image/jpeg')
        else:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'inline; filename={file_name}'
        return response

def open_files(request, folder_name, file_name):
    file_path = os.path.join(BASE_FOLDER_PATH, folder_name, file_name)
    if os.path.exists(file_path):
        return handle_file_response(file_path, file_name)
    else:
        raise Http404('File not found')

def open_file(request, folder_name, subfolder_names, file_name):
    file_path = os.path.join(BASE_FOLDER_PATH, folder_name, subfolder_names, file_name)
    if os.path.exists(file_path):
        return handle_file_response(file_path, file_name)
    else:
        raise Http404('File not found')
