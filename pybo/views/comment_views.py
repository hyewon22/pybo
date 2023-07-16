from django.shortcuts import render, get_object_or_404, redirect, resolve_url #  get_object_or_404는 존재하지 않는 페이지 접속 시 오류 대신 404 출력 위해 임포트
from ..models import Question, Answer, Comment  # Question 모델 데이터를 다뤄야 하므로
from django.utils import timezone
from ..forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login')
def comment_create_question(request, question_id) :
    """
    pybo 질문 댓글 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else :
        form = CommentForm()
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)
    

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id) :
    """
    pybo 질문 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author :
        messages.error(request, '댓글 수정 권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    
    if request.method == "POST" :
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))  # pybo:detail의 <int:question_id>에서 question_id는 comment.question.id가 됨
    else :
        form = CommentForm(instance=comment)
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)
    

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id) :
    """
    pybo 질문 댓글 삭제
    """    
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author :
        messages.error(request, '댓글 삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)  # comment.question.id는 해당 Comment 모델 데이터의 question 속성의 id를 의미
    else :
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)



@login_required(login_url='common:login')
def comment_create_answer(request, answer_id) :
    """
    pybo 답변 댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else :
        form = CommentForm()
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)
    

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id) :
    """
    pybo 답변 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author :
        messages.error(request, '댓글 수정 권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    
    if request.method == "POST" :
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else :
        form = CommentForm(instance=comment)
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)
        


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id) :
    """
    pybo 답변 댓글 삭제
    """    
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author :
        messages.error(request, '댓글 삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else :
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)