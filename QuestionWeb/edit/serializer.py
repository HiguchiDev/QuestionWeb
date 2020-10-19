from rest_framework import serializers # Django Rest Frameworkをインポート
from question.models import Question, TextChoice, Category

class TextChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextChoice # 扱う対象のモデル名を設定する
        fields = '__all__'