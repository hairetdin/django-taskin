from rest_framework import serializers
#import os
from django.contrib.auth.models import User
from .models import (Project, TaskStatus, Task, ProjectMember, TaskExecutor,
    TaskComment, TaskFile, Person)


class JwtUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username',)


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ('id', 'creator', 'task','attachment','name','upload_date', 'size')
        #read_only_fields = ('name','creator','upload_date', 'size')

    def validate(self, validated_data):
        #validated_data['name'] = os.path.splitext(validated_data['attachment'].name)[0]
        validated_data['name'] = validated_data['attachment'].name
        validated_data['size'] = validated_data['attachment'].size

        return validated_data

    def create(self, validated_data):
        return TaskFile.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    projects_member = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all(), required=False)
    projectmember_set = serializers.PrimaryKeyRelatedField(many=True, queryset=ProjectMember.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name',
                'email', 'is_superuser', 'person',
                'project_creator', 'tasks_creator', 'projects_member',
                'projectmember_set', 'taskfiles_creator',
                )


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ('id', 'task', 'creator', 'text', 'date_created')


class PeopleSerializer(serializers.ModelSerializer):
    tasks_customer = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all(), required=False)
    class Meta:
        model = Person
        fields = ('id', 'user', 'name', 'creator', 'tasks_customer',)


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all(), required=False)
    task_statuses = serializers.PrimaryKeyRelatedField(many=True, queryset=TaskStatus.objects.all(), required=False)
    projectmember_set = serializers.PrimaryKeyRelatedField(many=True, queryset=ProjectMember.objects.all(), required=False)
    class Meta:
        model = Project
        fields = ('id', 'url', 'name', 'date_created', 'creator', 'about', 'members',
            'task_statuses', 'tasks', 'projectmember_set')


class TaskStatusSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all(), required=False)
    class Meta:
        model = TaskStatus
        fields = ('id', 'url', 'name', 'project', 'order', 'tasks')


class ProjectMemberSerializer(serializers.ModelSerializer):
    taskexecutor_set = serializers.PrimaryKeyRelatedField(many=True, queryset=TaskExecutor.objects.all(), required=False)
    class Meta:
        model = ProjectMember
        fields = ('id', 'url', 'user', 'project', 'right', 'taskexecutor_set')


class TaskSerializer(serializers.ModelSerializer):
    #executors = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)
    taskexecutors = serializers.PrimaryKeyRelatedField(many=True, queryset=TaskExecutor.objects.all(), required=False)
    task_comments = serializers.PrimaryKeyRelatedField(many=True, queryset=TaskComment.objects.all(), required=False)
    taskfiles = serializers.PrimaryKeyRelatedField(many=True, queryset=TaskFile.objects.all(), required=False)
    class Meta:
        model = Task
        fields = ('id', 'url', 'subtask', 'date_created', 'creator', 'customer',
            'subject', 'reason', 'about', 'date_exec_max', 'date_closed',
            'project', 'status', 'executors','taskexecutors', 'task_comments',
            'taskfiles')


class TaskExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskExecutor
        fields = ('id', 'url', 'task', 'executor', 'date_accepted', 'date_closed')
