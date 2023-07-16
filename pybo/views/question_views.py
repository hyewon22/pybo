from django.shortcuts import render, get_object_or_404, redirect #  get_object_or_404는 존재하지 않는 페이지 접속 시 오류 대신 404 출력 위해 임포트
from ..models import Question  # Question 모델 데이터를 다뤄야 하므로
from django.utils import timezone
from ..forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login')
def question_create(request) :
    """
    pybo 질문 등록
    """
    if request.method == 'POST' :  # 질문 등록 시 '저장하기' 누르면 /pybo/question/create/가 POST 방식으로 요청받아 데이터 저장됨
        # 입력받은 데이터 저장
        form = QuestionForm(request.POST)  # request.POST는 사용자가 입력한 내용 받아오는 인수. 전달받은 데이터로 폼의 값이 채워지도록 객체 생성
        if form.is_valid() :  # POST 요청으로 받은 form이 유효한가?
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()  # DB에 저장
            return redirect('pybo:index')
    else :  # /pybo/question/create/가 GET 방식으로 요청받아 질문 등록 화면 나타남
        # ex) <a href=""></a> 방식은 get.
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id) :
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author :
        messages.error(request, '수정 권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    
    if request.method == "POST" :
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid() :
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)

    else :
        form = QuestionForm(instance=question)

    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id) :
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author :
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')