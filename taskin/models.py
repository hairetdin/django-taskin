# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import signals
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    name = models.CharField(max_length = 250)
    creator = models.ForeignKey(User, related_name="person_creator",
        verbose_name = "Who created")

    def __str__(self):
        return '%s' % (self.name)


class Project(models.Model):
    name = models.CharField(max_length = 100)
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="project_creator",
        verbose_name = "Who created")
    about = models.TextField('About this project', blank=True, null=True)
    members = models.ManyToManyField(
        User,
        related_name='projects_member',
        through='ProjectMember',
        through_fields=('project','user'),
    )

    def __str__(self):
        return '%s' % (self.name)


class TaskStatus(models.Model):
    name = models.CharField(max_length = 25)
    project = models.ForeignKey(Project, related_name='task_statuses')
    order = models.IntegerField(default=10, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '%s' % (self.name)


class ProjectMember(models.Model):
    ADMINISTRATOR = 'AD'
    EXECUTOR = 'EX'
    WATCHER = 'WA'
    PROJECT_RIGHT_CHOICES = (
        (ADMINISTRATOR, 'Administrator'),
        (EXECUTOR, 'Executor'),
        (WATCHER, 'Watcher'),
    )
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    right = models.CharField(max_length=2, choices=PROJECT_RIGHT_CHOICES)

    def __str__(self):
        return '%s %s %s' % (self.project, self.user, self.right)

    def is_project_admin(self):
        if self.right == 'AD':
            return True
        return False

    def is_project_executor(self):
        if self.right == 'EX':
            return True
        return False

    def is_project_watcher(self):
        if self.right == 'WA':
            return True
        return False


class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks',)
    subtask = models.ForeignKey('self', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        related_name="tasks_creator",
        verbose_name = "Who created"
    )
    customer = models.ForeignKey(
        Person,
        related_name='tasks_customer',
        blank=True,
        null=True
    )
    subject = models.CharField(max_length = 100)
    reason = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    date_exec_max = models.DateTimeField(blank=True, null=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(TaskStatus, related_name="tasks",)
    executors = models.ManyToManyField(
        ProjectMember,
        through='TaskExecutor',
        through_fields=('task','executor'),
        related_name='tasks',
    )

    def __str__(self):
        return '%s %s' % (self.date_created, self.subject)


def project_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project/<id>/<filename>
    return 'project/{0}/task/{1}/{2}'.format(
        instance.task.project.id,
        instance.task.id,
        filename
    )


class TaskFile(models.Model):
    task = models.ForeignKey(Task, related_name="taskfiles")
    attachment = models.FileField(upload_to=project_directory_path)
    name = models.CharField(max_length=100, blank=True, null=True) #name is filename without extension
    upload_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='taskfiles_creator')
    size = models.IntegerField(default=0, blank=True, null=True)


class TaskExecutor(models.Model):
    task = models.ForeignKey(Task, related_name="taskexecutors",)
    executor = models.ForeignKey(ProjectMember)
    date_accepted = models.DateTimeField(blank=True, null=True)
    date_closed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s' % (self.task)


class TaskComment(models.Model):
    task = models.ForeignKey('Task', related_name='task_comments')
    creator = models.ForeignKey(User, related_name='task_comments')
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


# There are many executor for task, so
# post_save signal from TaskExecutor to task, when executor closed task
# to check whether the task is closed
def exectask_closed(sender, instance, created, **kwargs):
    task_closed = []
    for executor in instance.task.taskexecutors.all():
        task_closed.append(executor.date_closed)
    if None in task_closed:
        instance.task.date_closed = None
        instance.task.save()
    else:
        instance.task.date_closed = max(task_closed)
        instance.task.save()

signals.post_save.connect(exectask_closed, sender=TaskExecutor)


# when new project created
# post_save signal from Project to create new taskstatuses &
# add project creator to project members
def project_created(sender, instance, created, **kwargs):
    #add creator to members for this project
    if instance.projectmember_set.all().count() == 0:
        new_member = ProjectMember(
            user=instance.creator,
            project=instance,
            right='AD'
        )
        new_member.save()

        #create taskstatuses for this project
        new_taskstatus = TaskStatus(name='New', project=instance, order=1)
        new_taskstatus.save()
        new_taskstatus = TaskStatus(name='In execute', project=instance, order=2)
        new_taskstatus.save()
        new_taskstatus = TaskStatus(name='Completed', project=instance, order=3)
        new_taskstatus.save()

        #create example task
        new_task = Task(
            creator=instance.creator,
            #customer=instance.creator,
            subject='The task example',
            reason='For show this example',
            about='This task created as example',
            project=instance,
            status=new_taskstatus
            )
        new_task.save()

signals.post_save.connect(project_created, sender=Project)


DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", None)
# when new task created
# post_save signal from Task to send email to executor
def task_created(sender, instance, created, **kwargs):
    recipient_list = []
    for executor in instance.executors.all():
        recipient_list.append(executor.user.email)
    send_mail(
        instance.subject,
        instance.about,
        DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

signals.post_save.connect(task_created, sender=Task)
