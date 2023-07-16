from django import forms
from pybo.models import Question, Answer, Comment

'''
Form (일반 폼) : 직접 필드 정의, 위젯 설정이 필요
Model Form (모델 폼) : 모델과 필드를 지정하면 모델폼이 자동으로 폼 필드를 생성
'''

class QuestionForm(forms.ModelForm) :  # 질문 등록 위한 폼 클래스 (모델폼)
    class Meta :
        model = Question  # Question 모델과 연결된 폼 (모델폼 객체 저장 시 연결된 모델의 데이터를 저장 가능)
        fields = ['subject', 'content']  # 질문 등록창에서 subject, content만 보여지며 폼으로 질문 데이터 저장 시 Question 모델의 subject, content가 입력값대로 저장됨. create_date값은 저장되지 않아서 이건 views.question_create에서 따로 저장해줌.
        labels = {
            'subject' : '제목',
            'content' : '내용'
        }

class AnswerForm(forms.ModelForm) :
    class Meta :
        model = Answer
        fields = ['content']  # 이 fields는 Answer모델에 있는 속성들이어야만 함. 답변 등록창에서 content만 보여짐.
        labels = {
            'content' : '답변 내용'
        }

class CommentForm(forms.ModelForm) :
    class Meta :
        model = Comment
        fields = ['content']
        labels = {
            'content' : '댓글 내용'
        }