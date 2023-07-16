from django.shortcuts import render, get_object_or_404, redirect, resolve_url #  get_object_or_404는 존재하지 않는 페이지 접속 시 오류 대신 404 출력 위해 임포트
from ..models import Question, Answer
from django.utils import timezone
from ..forms import AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login')
def answer_create(request, question_id) :  # 인자의 question_id는 urls.py의 'answer/create/<int:question_id>/'에서 question_id를 쓰기 위해 전달하는 것
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST' : 
        form = AnswerForm(request.POST)  # request.POST는 사용자가 입력한 내용 받아오는 인수. 입력 내용 받아와서 아래 절차 밟고 저장.
        if form.is_valid() :
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question_id), answer.id))
    else :  
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id) :
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)  # answer는 Answer 모델 데이터
    if request.user != answer.author :
        messages.error(request, '수정 권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    
    if request.method == "POST" :
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid() :
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()  # 수정일시 저장
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

    else :
        form = AnswerForm(instance=answer)

    context = {'answer' : answer, 'form' : form}
    return render(request, 'pybo/answer_form.html', context)



@login_required(login_url='common:login')
def answer_delete(request, answer_id) :
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author :
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.id)
    answer.delete()
    return redirect('pybo:index')
