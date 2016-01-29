# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings
import os.path
from eight_times_eight_project.activities.models import Notification
import urllib, hashlib
from django.utils.html import escape

class Experience(models.Model):

    EDU = "E"
    WORK = "W"
    PROJECT = "P"
    OTHER = "O"

    EXPERIENCE_TYPES = (
        (EDU, '教育经历'),
        (WORK, '工作经历'),
        (PROJECT, '项目经历'),
        (OTHER, '其他经历'),
        )

    UNDERGRADUATE = "U"
    POSTGRADUATE = "P"
    DOCTOR = "D"
    DEGREE_TYPES = (
        (UNDERGRADUATE, '本科'),
        (POSTGRADUATE, '研究生'),
        (DOCTOR, '博士'),
        (OTHER, '其他'),
        )

    _EDU_U_TEMPLATE = u'<l><div class="collapsible-header"><a class="collection-item modal-trigger" href="#modal_edu_{0}"><i class="material-icons small" style="color:#00bfa5">mode_edit</i></a>{1}</div><div class="collapsible-body" style="padding-top:10px;padding-bottom:10px"><small>{2} - {3}<br>{4}<br>{5}</small></div></li><div id="modal_edu_{10}" class="modal modal-fixed-footer modal_edit"><div class="modal-content"><div class="container"><h5 style="color:#7f7f7f;font-weight:300">修改教育经历</h5><div class="row"><form class="col s12" id="edu_1-form"><div class="row center"><div class="input-field col s12"><input id="name" name="name" type="text" class="validate" value="{6}"><label for="name" data-error="wrong">学校</label></div><div class="input-field col s12"><select id="degree" name="degree"><option value="U" selected="selected">本科</option><option value="P">研究生</option><option value="D">博士</option><option value="O">博士后</option></select><label>学历</label></div><div class="input-field col s12"><input id="position" name="position" type="text" class="validate" value="{7}"><label for="position" data-error="wrong">专业</label></div><div class="input-field col s6"><input id="start_date" name="start_date" type="text" class="validate" placeholder="例:2012.9" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1))$" value="{8}"><label for="start_date" data-error="wrong">入学日期</label></div><div class="input-field col s6"><input id="end_date" name="end_date" type="text" class="validate" placeholder="例:2016.6" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1)|至今)$" value="{9}"><label for="end_date" data-error="wrong">毕业日期</label></div></div></form></div></div></div><div class="modal-footer"><a id="#edu_edit_btn_{11}" class="modal-action modal-close waves-effect waves-light btn edit_btn">修改</a> <a id="edu_delete_btn_{12}" class=" modal-action modal-close waves-effect waves-light btn red accent-4 delete_btn">删除</a> <a href="#edu" class="modal-action modal-close waves-effect btn btn-flat black-text">取消</a></div></div>'
    _EDU_P_TEMPLATE = u'<l><div class="collapsible-header"><a class="collection-item modal-trigger" href="#modal_edu_{0}"><i class="material-icons small" style="color:#00bfa5">mode_edit</i></a>{1}</div><div class="collapsible-body" style="padding-top:10px;padding-bottom:10px"><small>{2} - {3}<br>{4}<br>{5}</small></div></li><div id="modal_edu_{10}" class="modal modal-fixed-footer modal_edit"><div class="modal-content"><div class="container"><h5 style="color:#7f7f7f;font-weight:300">修改教育经历</h5><div class="row"><form class="col s12" id="edu_1-form"><div class="row center"><div class="input-field col s12"><input id="name" name="name" type="text" class="validate" value="{6}"><label for="name" data-error="wrong">学校</label></div><div class="input-field col s12"><select id="degree" name="degree"><option value="U">本科</option><option value="P" selected="selected">研究生</option><option value="D">博士</option><option value="O">博士后</option></select><label>学历</label></div><div class="input-field col s12"><input id="position" name="position" type="text" class="validate" value="{7}"><label for="name" data-error="wrong">专业</label></div><div class="input-field col s6"><input id="start_date" name="start_date" type="text" class="validate" placeholder="例:2012.9" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1))$" value="{8}"><label for="start_date" data-error="wrong">入学日期</label></div><div class="input-field col s6"><input id="end_date" name="end_date" type="text" class="validate" placeholder="例:2016.6" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1)|至今)$" value="{9}"><label for="end_date" data-error="wrong">毕业日期</label></div></div></form></div></div></div><div class="modal-footer"><a id="#edu_edit_btn_{11}" class="modal-action modal-close waves-effect waves-light btn edit_btn">修改</a> <a id="edu_delete_btn_{12}" class=" modal-action modal-close waves-effect waves-light btn red accent-4 delete_btn">删除</a><a href="#edu" class="modal-action modal-close waves-effect btn btn-flat black-text">取消</a></div></div>'
    _EDU_D_TEMPLATE = u'<l><div class="collapsible-header"><a class="collection-item modal-trigger" href="#modal_edu_{0}"><i class="material-icons small" style="color:#00bfa5">mode_edit</i></a>{1}</div><div class="collapsible-body" style="padding-top:10px;padding-bottom:10px"><small>{2} - {3}<br>{4}<br>{5}</small></div></li><div id="modal_edu_{10}" class="modal modal-fixed-footer modal_edit"><div class="modal-content"><div class="container"><h5 style="color:#7f7f7f;font-weight:300">修改教育经历</h5><div class="row"><form class="col s12" id="edu_1-form"><div class="row center"><div class="input-field col s12"><input id="name" name="name" type="text" class="validate" value="{6}"><label for="name" data-error="wrong">学校</label></div><div class="input-field col s12"><select id="degree" name="degree"><option value="U">本科</option><option value="P">研究生</option><option value="D" selected="selected">博士</option><option value="O">博士后</option></select><label>学历</label></div><div class="input-field col s12"><input id="position" name="position" type="text" class="validate" value="{7}"><label for="position" data-error="wrong">专业</label></div><div class="input-field col s6"><input id="start_date" name="start_date" type="text" class="validate" placeholder="例:2012.9" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1))$" value="{8}"><label for="start_date" data-error="wrong">入学日期</label></div><div class="input-field col s6"><input id="end_date" name="end_date" type="text" class="validate" placeholder="例:2016.6" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1)|至今)$" value="{9}"><label for="end_date" data-error="wrong">毕业日期</label></div></div></form></div></div></div><div class="modal-footer"><a id="#edu_edit_btn_{11}" class="modal-action modal-close waves-effect waves-light btn edit_btn">修改</a> <a id="edu_delete_btn_{12}" class=" modal-action modal-close waves-effect waves-light btn red accent-4 delete_btn">删除</a><a href="#edu" class="modal-action modal-close waves-effect btn btn-flat black-text">取消</a></div></div>'
    _EDU_O_TEMPLATE = u'<l><div class="collapsible-header"><a class="collection-item modal-trigger" href="#modal_edu_{0}"><i class="material-icons small" style="color:#00bfa5">mode_edit</i></a>{1}</div><div class="collapsible-body" style="padding-top:10px;padding-bottom:10px"><small>{2} - {3}<br>{4}<br>{5}</small></div></li><div id="modal_edu_{10}" class="modal modal-fixed-footer modal_edit"><div class="modal-content"><div class="container"><h5 style="color:#7f7f7f;font-weight:300">修改教育经历</h5><div class="row"><form class="col s12" id="edu_1-form"><div class="row center"><div class="input-field col s12"><input id="name" name="name" type="text" class="validate" value="{6}"><label for="name" data-error="wrong">学校</label></div><div class="input-field col s12"><select id="degree" name="degree"><option value="U">本科</option><option value="P">研究生</option><option value="D">博士</option><option value="O" selected="selected">博士后</option></select><label>学历</label></div><div class="input-field col s12"><input id="position" name="position" type="text" class="validate" value="{7}"><label for="name" data-error="wrong">专业</label></div><div class="input-field col s6"><input id="start_date" name="start_date" type="text" class="validate" placeholder="例:2012.9" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1))$" value="{8}"><label for="start_date" data-error="wrong">入学日期</label></div><div class="input-field col s6"><input id="end_date" name="end_date" type="text" class="validate" placeholder="例:2016.6" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1)|至今)$" value="{9}"><label for="end_date" data-error="wrong">毕业日期</label></div></div></form></div></div></div><div class="modal-footer"><a id="#edu_edit_btn_{11}" class="modal-action modal-close waves-effect waves-light btn edit_btn">修改</a> <a id="edu_delete_btn_{12}" class=" modal-action modal-close waves-effect waves-light btn red accent-4 delete_btn">删除</a><a href="#edu" class="modal-action modal-close waves-effect btn btn-flat black-text">取消</a></div></div>'
    _WORK_TEMPLATE = u'<li><div class="collapsible-header"><a class="collection-item modal-trigger" href="#modal_work_{0}"><i class="material-icons small" style="color:#00bfa5">mode_edit</i></a>{1}</div><div class="collapsible-body" style="text-align:left;padding:20px 30px 20px 30px"><small>{2} - {3}<br>任职于 {4}<br>主要工作：<br>{5}</small></div></li><div id="modal_work_{6}" class="modal modal-fixed-footer"><div class="modal-content"><div class="container"><h5 style="color:#7f7f7f;font-weight:300">修改工作经历</h5><div class="row"><form class="col s12" id="work_form_{7}"><div class="row center"><div class="input-field col s12"><input id="name" name="name" type="text" class="validate" value="{8}"><label for="name" data-error="wrong">公司</label></div><div class="input-field col s12"><input id="position" name="position" type="text" class="validate" value="{9}"><label for="position" data-error="wrong">职位</label></div><div class="input-field col s6"><input id="start_date" name="start_date" type="text" class="validate" placeholder="例:2012.9" value="{10}" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1))$"><label for="start_date" data-error="wrong">入职日期</label></div><div class="input-field col s6"><input id="end_date" name="end_date" type="text" class="validate" placeholder="例:2016.6" value="{11}" pattern="^((19|20)(\d){2}\.(12|11|10|9|8|7|6|5|4|3|2|1)|至今)$"><label for="end_date" data-error="wrong">离职日期</label></div><div class="input-field col s12"><textarea id="description" name="description" class="materialize-textarea">{12}</textarea><label for="description" data-error="wrong">主要工作</label></div></div></form></div></div></div><div class="modal-footer"><a id="work_edit_btn_{13}" class="modal-action modal-close waves-effect waves-light btn edit_btn">修改</a> <a id="work_delete_btn_{14}" class=" modal-action modal-close waves-effect waves-light btn red accent-4 delete_btn">删除</a><a href="#work" class="modal-action modal-close waves-effect btn btn-flat black-text">取消</a></div></div>'
    _PROJECT_TEMPLATE = u'<li><div class="collapsible-header"><a class="collection-item modal-trigger" href="#modal_proj_{0}"><i class="material-icons small" style="color:#00bfa5">mode_edit</i></a>{1}</div><div class="collapsible-body" style="text-align:left;padding:20px 30px 20px 30px"><small>{2}</small></div></li><div id="modal_proj_{3}" class="modal modal-fixed-footer modal_edit"><div class="modal-content"><div class="container"><h5 style="color:#7f7f7f;font-weight:300">修改项目经历</h5><div class="row"><form class="col s12" id="proj_form_{4}"><div class="row center"><div class="input-field col s12"><input id="name" name="name" type="text" class="validate" value="{5}"><label for="project_name" data-error="wrong">项目名称</label></div><div class="input-field col s12"><textarea id="description" name="description" class="materialize-textarea">{6}</textarea><label for="description" data-error="wrong">项目介绍</label></div></div></form></div></div></div><div class="modal-footer"><a id="proj_edit_btn_{7}" class="modal-action modal-close waves-effect waves-light btn edit_btn">修改</a><a id="proj_delete_btn_{8}" class=" modal-action modal-close waves-effect waves-light btn red accent-4 delete_btn">删除</a> <a href="#proj" class="modal-action modal-close waves-effect btn btn-flat black-text">取消</a></div></div>'
    _OTHER_TEMPLATE = u'<li><div class="collapsible-header"><a class="collection-item modal-trigger" href="#modal_other_{0}"><i class="material-icons small" style="color:#00bfa5">mode_edit</i></a>{1}</div><div class="collapsible-body" style="text-align:left;padding:20px 30px 20px 30px"><small>{2}</small></div></li><div id="modal_other_{3}" class="modal modal-fixed-footer modal_edit"><div class="modal-content"><div class="container"><h5 style="color:#7f7f7f;font-weight:300">修改其他经历</h5><div class="row"><form class="col s12" id="other_form_{4}"><div class="row center"><div class="input-field col s12"><input id="name" name="name" type="text" class="validate" value="{5}"><label for="project_name" data-error="wrong">经历名称</label></div><div class="input-field col s12"><textarea id="description" name="description" class="materialize-textarea">{6}</textarea><label for="description" data-error="wrong">经历介绍</label></div></div></form></div></div></div><div class="modal-footer"><a id="other_edit_btn_{7}" class="modal-action modal-close waves-effect waves-light btn edit_btn">修改</a><a id="other_delete_btn_{8}" class=" modal-action modal-close waves-effect waves-light btn red accent-4 delete_btn">删除</a> <a href="#proj" class="modal-action modal-close waves-effect btn btn-flat black-text">取消</a></div></div>'


    user = models.ForeignKey(User, related_name='+')
    experience_type = models.CharField(max_length=1, choices=EXPERIENCE_TYPES)
    name = models.CharField('公司名称,学校名称,项目名称或其他名称', max_length=50)
    position = models.CharField('职位,专业', max_length=50, blank=True)
    degree = models.CharField(max_length=1, choices=DEGREE_TYPES, blank=True)
    description = models.TextField('主要工作,项目介绍或其他介绍', max_length=1000, blank=True)
    start_date = models.CharField('开始时间', max_length=7, blank=True)
    end_date = models.CharField('结束时间', max_length=7, blank=True)


    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'
        ordering = ('-start_date',)

    def __unicode__(self):
        if self.experience_type == self.EDU:
            if self.degree == self.UNDERGRADUATE:
                return self._EDU_U_TEMPLATE.format(
                    self.pk,
                    escape(self.name),
                    escape(self.start_date),
                    escape(self.end_date),
                    escape(self.degree),
                    escape(self.position),
                    escape(self.name),
                    escape(self.position),
                    escape(self.start_date),
                    escape(self.end_date),
                    self.pk,
                    self.pk,
                    self.pk,
                    )
            elif self.degree == self.POSTGRADUATE:
                return self._EDU_P_TEMPLATE.format(
                    self.pk,
                    escape(self.name),
                    escape(self.start_date),
                    escape(self.end_date),
                    escape(self.degree),
                    escape(self.position),
                    escape(self.name),
                    escape(self.position),
                    escape(self.start_date),
                    escape(self.end_date),
                    self.pk,
                    self.pk,
                    self.pk,
                    )
            elif self.degree == self.DOCTOR:
                return self._EDU_D_TEMPLATE.format(
                    self.pk,
                    escape(self.name),
                    escape(self.start_date),
                    escape(self.end_date),
                    escape(self.degree),
                    escape(self.position),
                    escape(self.name),
                    escape(self.position),
                    escape(self.start_date),
                    escape(self.end_date),
                    self.pk,
                    self.pk,
                    self.pk,
                    )
            elif self.degree == self.OTHER:
                return self._EDU_O_TEMPLATE.format(
                    self.pk,
                    escape(self.name),
                    escape(self.start_date),
                    escape(self.end_date),
                    escape(self.degree),
                    escape(self.position),
                    escape(self.name),
                    escape(self.position),
                    escape(self.start_date),
                    escape(self.end_date),
                    self.pk,
                    self.pk,
                    self.pk,
                    )
        elif self.experience_type == self.WORK:
            return self._WORK_TEMPLATE.format(
                    self.pk,
                    escape(self.position),
                    escape(self.start_date),
                    escape(self.end_date),
                    escape(self.name),
                    escape(self.description),
                    self.pk,
                    self.pk,
                    escape(self.name),
                    escape(self.position),
                    escape(self.start_date),
                    escape(self.end_date),
                    escape(self.description),
                    self.pk,
                    self.pk,
                )
        elif self.experience_type == self.PROJECT:
            return self._PROJECT_TEMPLATE.format(
                    self.pk,
                    escape(self.name),
                    escape(self.description),
                    self.pk,
                    self.pk,
                    escape(self.name),
                    escape(self.description),
                    self.pk,
                    self.pk,
                )
        elif self.experience_type == self.OTHER:
            return self._OTHER_TEMPLATE.format(
                    self.pk,
                    escape(self.name),
                    escape(self.description),
                    self.pk,
                    self.pk,
                    escape(self.name),
                    escape(self.description),
                    self.pk,
                    self.pk,
                )
        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url 

    def get_verification_file(self):
        no_file = 'empty'
        try:
            filename = settings.MEDIA_ROOT + '/verification_files/' + self.user.username + '.jpg'
            file_url = settings.MEDIA_URL + 'verification_files/' + self.user.username + '.jpg'
            if os.path.isfile(filename):
                return file_url
            else:
                return no_file
        except Exception, e:
            return no_file