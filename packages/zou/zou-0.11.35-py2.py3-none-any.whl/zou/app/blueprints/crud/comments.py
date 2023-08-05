from flask_jwt_extended import jwt_required

from zou.app.models.comment import Comment

from zou.app.services import (
    deletion_service,
    notifications_service,
    persons_service,
    tasks_service,
    user_service,
)
from zou.app.utils import permissions

from .base import BaseModelResource, BaseModelsResource


class CommentsResource(BaseModelsResource):
    def __init__(self):
        BaseModelsResource.__init__(self, Comment)


class CommentResource(BaseModelResource):
    def __init__(self):
        BaseModelResource.__init__(self, Comment)

    def post_update(self, instance_dict):
        comment = tasks_service.reset_mentions(instance_dict)
        tasks_service.clear_comment_cache(comment["id"])
        notifications_service.reset_notifications_for_mentions(comment)
        return comment

    def check_read_permissions(self, instance):
        if permissions.has_admin_permissions():
            return True
        else:
            comment = self.get_model_or_404(instance["id"])
            task_id = str(comment.object_id)
            task = tasks_service.get_task(task_id)
            if task is None:
                tasks_service.clear_task_cache(task_id)
                task = tasks_service.get_task(task_id)
            return user_service.check_project_access(task["project_id"])

    def check_update_permissions(self, instance, data):
        if permissions.has_admin_permissions():
            return True
        else:
            comment = self.get_model_or_404(instance["id"])
            current_user = persons_service.get_current_user()
            return current_user["id"] == str(comment.person_id)

    @jwt_required
    def delete(self, instance_id):
        """
        Delete a comment corresponding at given ID.
        """
        comment = tasks_service.get_comment(instance_id)
        task = tasks_service.get_task(comment["object_id"])
        user_service.check_project_access(task["project_id"])
        deletion_service.remove_comment(comment["id"])
        tasks_service.reset_task_data(comment["object_id"])
        tasks_service.clear_comment_cache(comment["id"])
        return "", 204
