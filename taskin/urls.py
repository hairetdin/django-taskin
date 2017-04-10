from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from .views import (index_taskin, ProjectViewSet, TaskStatusViewSet,
    TaskViewSet, ProjectMemberViewSet, TaskExecutorViewSet, UserTaskViewSet,
    PeopleViewSet, UserViewSet, TaskCommentViewSet, TaskFileViewSet,
    SessionIdJSONWebToken
    )


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'taskstatuses', TaskStatusViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'members', ProjectMemberViewSet)
router.register(r'taskexecutors', TaskExecutorViewSet)
router.register(r'choicepeople', PeopleViewSet)
router.register(r'people', PeopleViewSet)
router.register(r'choiceusers', UserViewSet)
router.register(r'users', UserViewSet)
router.register(r'taskcomments', TaskCommentViewSet)
router.register(r'taskfiles', TaskFileViewSet)


urlpatterns = [
    url(r'^api/taskin/', include(router.urls)),
    # backend session authentication
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # fronend jwt authentication
    url(r'^api/auth/login/', obtain_jwt_token),
    url(r'^api/auth/token-sessionid/', SessionIdJSONWebToken),
    url(r'^api/auth/verify-token/', verify_jwt_token),
    url(r'^$', index_taskin, name='taskin'),
    url(r'^(?P<path>.*)/$', index_taskin), # for any other request
]
