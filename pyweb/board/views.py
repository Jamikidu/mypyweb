from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.forms import QuestionForm, AnswerForm
from board.models import Question, Answer


def index(request):
    return render(request, 'board/index.html')
    # return HttpResponse("웹 메인페이지 입니다.")

# 질문 목록
def question_list(request):
    # question_list = Question.objects.all()
    question_list = Question.objects.order_by('-create_date')    #내림 차순
    # 페이지 처리
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  #검색어

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) | # 내용 검색
            Q(author__username__icontains=kw) |    #질문글쓴이 검색
            Q(answer__author__username__icontains=kw) |    #답변글쓴이 검색
            Q(answer__content__icontains=kw)  # 답변글쓴이 검색
        ).distinct()   # 중복제거

    paginator = Paginator(question_list, 10)    #페이지당 게시글 - 10
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'kw': kw}
    return render(request, 'board/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'board/detail.html', context)

# 질문 등록
@login_required(login_url='common:login')   #로그인 페이지로 이동
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)   #입력된 데이터가 있는 폼
        if form.is_valid(): # 폼이 유효성 검사를 통과했다면!
            question = form.save(commit=False) #가저장
            question.author = request.user  #세션 권한(로그인한) 있는 글쓴이
            question.create_date = timezone.now()   #등록일 생성
            form.save() #실제저장
            return redirect('board:question_list')  #질문 목록 페이지 이동

    else:   # get 방식
        form = QuestionForm()   #폼 객체 생성(빈 폼 생성)
    context = {'form': form}
    return render(request, 'board/question_form.html', context) #get 방식

#답변 등록
@login_required(login_url='common:login')   #로그인 페이지로 이동
def answer_create(request, question_id):
    # 질문이 1개 있어야 답변을 등록할 수 있음
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)    #content만 저장
            answer.author = request.user
            answer.create_date = timezone.now() #답변 등록일
            answer.question = question  #외래키 생성
            form.save()
            return redirect('board:detail', question_id=question.id)    #question.id 주의
    else:
        form = AnswerForm()  #빈 폼 생성
    context = {'question': question, 'form': form}
    return render(request, 'board/detail.html', context)

# 질문 수정
@login_required(login_url='common:login')
def question_modify(request, question_id):
    # 수정을 위해서 질문 1개 가져옴
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save(commit=False) #커밋 아직 안됨
            question.modify_date = timezone.now()   #수정일
            question.author = request.user          #글쓴
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)  #데이터가 이미 있는 폼
    context = {'form': form}
    return render(request, 'board/question_form.html', context)

# 질문 삭제
@login_required(login_url='common:login')   #로그인 안되어 있으면 페이지로 이동시킴
def question_delete(request, question_id):
    # question = Question.objects.get(id=question_id)
    # 모델에서 데이터가 잇으면 가져오고 없으면 404 페이지 오류 처리를 함
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('board:question_list')

# 답변 삭제
@login_required(login_url='common:login')
def answer_delete(reqeust, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect('board:detail', question_id=answer.question.id)