from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import SBoardLikeUsers, SentenceListComment, WordList
from .models import SentenceList
from .forms import RSentencesWriteForm, SentencesCommentForm
from board.models import Board
from board.forms import PBoardWriteForm, SBoardWriteForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages 


# Create your views here.

def rwordpage(request):
    if request.method == 'GET':
        if request.GET.get('button3')=="3":
            rwordlist = WordList.objects.order_by('?')[:3]
        elif request.GET.get('button4')=="4":
            rwordlist = WordList.objects.order_by('?')[:4]
        elif request.GET.get('button5')=="5":
            rwordlist = WordList.objects.order_by('?')[:5]
        else:
            rwordlist = ''
        form = RSentencesWriteForm()
        context = {
            'forms': form,
            'rwordlist' : rwordlist,
        }
        return render(request, 'rwordpage.html', context)

    elif request.method == 'POST':
        if request.GET.get('button3')=="3":
            rwordlist = WordList.objects.order_by('?')[:3]
        elif request.GET.get('button4')=="4":
            rwordlist = WordList.objects.order_by('?')[:4]
        elif request.GET.get('button5')=="5":
            rwordlist = WordList.objects.order_by('?')[:5]
        else:
            rwordlist = 'click button'

        form = RSentencesWriteForm(request.POST)

        if form.is_valid():
            s = SentenceList()
            s.sentence = form.cleaned_data['sentence']
            s.contents = form.cleaned_data['contents']
            s.writer = request.user
            s.save()
            return redirect('/rboard')
        else:
            context = {
                'forms': form,
                'rwordlist' : rwordlist,
            }
            return render(request, 'rwordpage.html', context)

    
def rwordboard(request):
    rword_setences = SentenceList.objects.filter().order_by('-id')

    paginator = Paginator(rword_setences, 10)
    pagenum = request.GET.get('page')
    rword_setences = paginator.get_page(pagenum)

    context = {
        'rword_setences' : rword_setences,
    }
    return render(request, 'rwordboard.html', context)

#문장 게시판 상세보기
def rword_detail(request, pk):
    sentence = get_object_or_404(SentenceList, id=pk)
    comments = SentenceListComment.objects.filter(Sentence=sentence.id).order_by('created_at')
    if request.GET.get('scbtn')=="1":
        write_form = SBoardWriteForm()
        context = {
            'forms': write_form,
        }
    else:
        write_form = PBoardWriteForm()
    #if request.GET.get('pbbtn')=="1":
        #write_form = PBoardWriteForm()
        #context = {
            #'forms': write_form,
        #}
    comment_form = SentencesCommentForm()

    #조회수 (쿠키 이용)
    cookie_name = 'hit'

    context = {
        'sentence': sentence,
        'forms': write_form,
        'comment_form' : comment_form,
        'comments' : comments
    }

    response = render(request, 'rwordboard_detail.html', context)

    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(pk) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
            sentence.hits += 1
            sentence.save()
            return response
    else:
        response.set_cookie(cookie_name, pk, expires=None)
        sentence.hits += 1
        sentence.save()
        return response

    return render(request, 'rwordboard_detail.html', context)

#댓글 생성
def sen_comments_create(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            sentence = get_object_or_404(SentenceList, pk=pk)
            commentform = SentencesCommentForm(request.POST)
            if commentform.is_valid():
                comment = commentform.save(commit=False)
                comment.Sentence = sentence
                comment.user = request.user
                comment.save()
            return redirect('/' + 'rboard/detail/' + str(pk))
        return redirect('/'+'accounts/login')

#댓글 삭제
def sen_comments_delete(request, Sentence_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(SentenceListComment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('/' + 'rboard/detail/' + str(Sentence_pk))

#좋아요
def likes(request, pk):
    if request.user.is_authenticated:
        sentence = get_object_or_404(SentenceList, id=pk)

        if sentence.like_users.filter(pk=request.user.pk).exists():
            sentence.like_users.remove(request.user)
            return redirect('/' + 'rboard/detail/' + str(pk))
        else:
            sentence.like_users.add(request.user)
            return redirect('/' + 'rboard/detail/' + str(pk))
    else :
        context = {
            'messages' : messages.info(request, '로그인 해주세요.')
        }
        return redirect('/' + 'rboard/detail/' + str(pk), context)