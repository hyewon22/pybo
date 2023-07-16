from django.db import models
from django.contrib.auth.models import User

# 여기에 모델들 작성하면 되고, 대부분의 모델은 클래스로 만듦.
class Question(models.Model) :  # 모델 상속받음
    subject = models.CharField(max_length=200)  # 질문 제목 (CharField는 글자수 제한 있음)
    content = models.TextField()  # 질문 내용 (TextField는 글자수 제한 없음)
    create_date = models.DateTimeField()  # 질문 작성 일시
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')  # 계정 삭제되면 계정과 연결된 Question 모델 데이터 모두 삭제됨
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self) :
        return self.subject

class Answer(models.Model) :
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 질문 (어떤 질문의 답변인지 알아야 하므로 질문 속성 필요함. 이처럼 어떤 모델이 다른 모델을 속성으로 가질 땐 ForeignKey 사용함. ForeignKey는 다른 모델과의 연결을 의미. on_delete=models.CASCADE는 답변에 연결된 질문이 삭제될 시 답변도 함께 삭제되도록 한 것.)
    content = models.TextField()  # 답변 내용
    create_date = models.DateTimeField()  # 답변 작성 일시
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')  # 계정 삭제되면 계정과 연결된 Question 모델 데이터 모두 삭제됨
    modify_date = models.DateTimeField(null=True, blank=True)  # null 허용, 값 없어도 form.is_valid() 통과됨
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model) :
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
