import json

from django.http import HttpResponse

from app.note.model import Note, Tag
from app.user.model import auth_service, User

from django.core import serializers


def post_note(request, ):
    auth_service.check_auth(request)
    json_data = json.loads(request.body)
    title, content = [json_data.get(it) for it in ["title", "content"]]
    note = Note(title=title, content=content, user=User.objects.get(id=request.session['user']["id"]))
    # TODO handle errors properly

    note.save()
    return HttpResponse(json.dumps(dict(title=title, content=content, id=note.id)), status=201)


def edit_note(request, id):
    auth_service.check_auth(request)
    json_data = json.loads(request.body)
    title, content = [json_data.get(it) for it in ["title", "content"]]
    note = Note.objects.get(id=id)

    if not note:
        return HttpResponse(status=404)

    note.title = title
    note.content = content
    # TODO optimistic lock
    note.save()
    return HttpResponse(json.dumps(dict(title=title, content=content, id=note.id)), status=200)


def add_tag(request, id, ):
    auth_service.check_auth(request)
    tag_name = json.loads(request.body)['tag_name']
    # TODO handle errors properly
    note = Note.objects.get(id=id, user__id=request.session['user']["id"])
    try:
        tag = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist:
        tag = Tag(name=tag_name)
        tag.save()

    # TODO handle errors properly
    note.tags.add(tag)
    note.save()
    return HttpResponse(status=200)


def by_tag(request, tag_name):
    notes = Note.objects.filter(tags__name__in=[tag_name], user__id=request.session['user']["id"])
    # TODO handle error properly
    return HttpResponse(serializers.serialize('json', notes), status=200)


def delete_note(request, ):
    auth_service.check_auth(request)
    note = Note.objects.filter(id=id, user__id=request.session['user']["id"])
    # TODO handle error properly
    note.delete()
    # TODO optimistic lock
    return HttpResponse(status=200)
