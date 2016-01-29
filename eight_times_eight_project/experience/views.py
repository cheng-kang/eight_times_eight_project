# -*- coding: UTF-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from eight_times_eight_project.auth_new.forms import SignUpForm,SignUpProfileForm
from django.contrib.auth.models import User
from eight_times_eight_project.auth_new.models import Profile
from django.core import serializers

from django.contrib.auth.decorators import login_required
from eight_times_eight_project.decorators import ajax_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from eight_times_eight_project.experience.models import Experience

@login_required
@ajax_required
def new_experience(request):
    user = request.user
    type = request.POST['type']
    name = request.POST.get('name', '')
    position = request.POST.get('position', '')
    degree = request.POST.get('degree', '')
    description = request.POST.get('description', '')
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')

    #此处需不需要加上try?以防止插入出错
    experience = Experience(user=user, experience_type=type, name=name, position=position, degree=degree, description=description, start_date=start_date, end_date=end_date)
    experience.save()

    result = "{'experience_type': '"+type+"','name': '"+name+"', 'position': '"+position+"', 'degree':'"+degree+"', 'description': '"+description+"', 'start_date': '"+start_date+"', 'end_date': '"+end_date+"', 'status': 'done'}"

    return HttpResponse(experience)

@login_required
@ajax_required
def edit_experience(request):

    user = request.user
    experience_id = request.POST['experience_id']

    name = request.POST.get('name', '')
    position = request.POST.get('position', '')
    degree = request.POST.get('degree', '')
    description = request.POST.get('description', '')
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')

    experience = Experience.objects.get(pk=experience_id, user=user)
    if experience:
        experience.name = name
        experience.position = position
        experience.degree = degree
        experience.description = description
        experience.start_date = start_date
        experience.end_date = end_date
        experience.save()

        return HttpResponse(experience)
    else:
        return HttpResponseForbidden()


@login_required
@ajax_required
def delete_experience(request):
    try:
        user = request.user
        experience_id = request.POST['experience_id']

        experience = Experience.get(pk=experience_id, user=user)
        if experience:
            experience.delete()

            return HttpResponse("deleted")
        else:
            return HttpResponseForbidden()
    except Exception, e:
        return HttpResponseBadRequest()
