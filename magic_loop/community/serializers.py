from rest_framework import serializers

from .models import Comment, Feedback, Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "author_username",
            "post",
            "content",
            "created_at",
            "is_pinned",
            "likes",
            "dislikes",
        ]


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "content"]


class EvaluateCommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment

    def update(self, instance, validated_data):
        action = self.context.get("action")

        if instance.post.author != self.context["user"]:
            raise serializers.ValidationError(
                "You can only pin comments on your posts."
            )

        if action == "unpin":
            if instance.is_pinned:
                instance.is_pinned = False
            else:
                raise serializers.ValidationError(
                    "Can't unpin comment that has not been pinned."
                )

        elif action == "pin":
            res = Comment.objects.filter(post=instance.post, is_pinned=True)
            if not res.exists():
                instance.is_pinned = True
            else:
                raise serializers.ValidationError(
                    "There already is pinned comment on this post."
                )

        instance.save()
        return instance


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(source="tag", many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "tags",
            "image",
            "likes_count",
            "comment_count",
            "has_pinned_comment",
            "comments",
        ]

    @staticmethod
    def get_comments(obj):
        comments = obj.comments.order_by("-is_pinned", "-created_at")
        return CommentSerializer(comments, many=True, read_only=True).data


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(source="tag", many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "tags",
            "image",
            "comment_count",
            "likes_count",
        ]


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "tag", "image"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["comment"]

    def create(self, validated_data):
        user = self.context.get('user')
        comment = validated_data['comment']
        if self.context.get('action') == 'like':
            action_value = 1
        else:
            action_value = -1

        feedback = Feedback.objects.filter(user=user, comment=comment).first()

        if feedback:
            if feedback.value == action_value:
                feedback.delete()
                return feedback
            else:
                feedback.value = action_value
                feedback.save()
                return feedback
        else:
            return Feedback.objects.create(user=user, comment=comment, value=action_value)
