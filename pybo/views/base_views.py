from django.shortcuts import render, get_object_or_404, redirect #  get_object_or_404는 존재하지 않는 페이지 접속 시 오류 대신 404 출력 위해 임포트
from ..models import Question  # Question 모델 데이터를 다뤄야 하므로
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count


def index(request) :  # request는 장고에 의해 자동으로 전달되는 HTTP 요청 객체
    """
    pybo 목록 출력
    """

    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지는 1로 기본값 설정
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬 기준

    # 정렬
    if so == 'recommend' :
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular' :
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_voter', '-create_date')
    else :  # recent
        question_list = Question.objects.order_by('-create_date')
        

    #조회
    if kw :
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여줌
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj, 'page' : page, 'kw' : kw}  # 요청된 페이지?
    return render(request, 'pybo/question_list.html', context)  # render함수는 context에 있는 Question 모델 데이터 question_list를 pybo/question_list.html 파일에 적용해서 HTML코드로 변환함. request는 response하기 위해 받는 필수 인자. 장고에서는 pybo/question_list.html 이런 파일을 템플릿이라고 부름. 템플릿은 장고의 태그를 추가로 사용할 수 있는 HTML파일이라 생각하면 됨.

def detail(request, question_id) :
    """
    pybo 내용 출력
    """
    # question = Question.objects.get(id=question_id) 이 코드 말고 존재하지 않는 페이지 접속하면 오류 대신 404 페이지 출력하게 하기 위해서 아래 코드로.
    question = get_object_or_404(Question, pk=question_id) # pk(기본키)에 해당하는 건 없으면 오류 대신 404 출력.
    context = {'question' : question} # context는 딕셔너리 형태로.
    return render(request, 'pybo/question_detail.html', context) # context는 pybo/question_detail.html에 전달됨.