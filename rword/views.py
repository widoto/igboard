from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import WordList
from .models import SentenceList
from .forms import RSentencesWriteForm
from board.models import Board
from board.forms import PBoardWriteForm
from django.core.paginator import Paginator


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
            # s.writer = request.user "SentenceList.writer" must be a "User" instance.
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
    if request.method == 'GET' or request.method == 'FILES':
        rwordboard = get_object_or_404(SentenceList, id=pk)
        write_form = PBoardWriteForm()

        context = {
            'rwordboard': rwordboard,
            'forms': write_form,
        }
        return render(request, 'rwordboard_detail.html', context)
    elif request.method == 'POST':
        write_form = PBoardWriteForm(request.POST, request.FILES)

        if write_form.is_valid():
            board = Board(
                title=write_form.title,
                contents=write_form.contents,
                writer=request.user,
                sentence=write_form.sentence,
                image=write_form.image,
                #file=write_form.file
            )
            board.save()
            return redirect('/board/public')
        else:
            context = {
                'forms': write_form,
            }
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'rwordboard_detail.html', context)