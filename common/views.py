from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
# from common.forms import UserForm
from .forms import UserForm

def signup(request) :
    '''
    회원가입
    '''
    if request.method == "POST" :  # 리퀘스트 방식이 POST라면
        form = UserForm(request.POST)  # request.POST의 내용을 form에 담아서
        if form.is_valid() :  # form의 내용이 유효한지 확인하고
            form.save()  # 유효하다면 저장 (이 단계에서 데이터베이스에 form 필드 저장됨)
            username = form.cleaned_data.get('username')
    else :
        form = UserForm()  # 리퀘스트 방식이 GET이라면 입력할 수 있도록 빈 폼만 보여짐
    return render(request, 'common/signup.html', {'form' : form})            


