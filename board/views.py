import os
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PBoardWriteForm, SBoardWriteForm
from .models import Board
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse

#### 전체 게시판 ####
def board_list(request):
    pb_boards = Board.objects.filter(board_name='Public').order_by('id')
    sc_boards = Board.objects.filter(board_name='Science').order_by('id')

    context = {
        'pb_boards' : pb_boards,
        'sc_boards' : sc_boards,
    }

    return render(request, 'board/board_list.html', context)

#파일 다운로드
def file_download(request):
    path = request.GET['path']
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    binary_file = open(file_path, 'rb')
    response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
    return response

#### 일반인 ####
#게시판 목록
def board_public_list(request):
    pb_boards = Board.objects.filter(board_name='Public').order_by('id')

    paginator = Paginator(pb_boards, 10)
    pagenum = request.GET.get('page')
    pb_boards = paginator.get_page(pagenum)

    context = {
        'pb_boards' : pb_boards,
    }

    return render(request, 'board_public/board_public_list.html', context)

#글 작성하기
def board_public_write(request):
    if request.method == 'GET' or request.method == 'FILES':
        write_form = PBoardWriteForm()
        context = {
            'forms': write_form,
        }
        return render(request, 'board_public/board_public_write.html', context)
    elif request.method == 'POST':
        write_form = PBoardWriteForm(request.POST, request.FILES)

        if write_form.is_valid():
            board = Board(
                title=write_form.title,
                contents=write_form.contents,
                writer=write_form.writer,
                sentence=write_form.sentence,
                image=write_form.image,
                file=write_form.file
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
            return render(request, 'board_public/board_public_write.html', context)

#글 상세보기
def board_public_detail(request, pk):
    board = get_object_or_404(Board, id=pk)

    context = {
        'board': board,
    }

    return render(request, 'board_public/board_public_detail.html', context)

#삭제하기 - user 설정 후 추가 설정 필요
def board_public_delete(request, pk):
    board = get_object_or_404(Board, id=pk)

    board.delete()
    return redirect('/board/public')

#수정하기 - user 설정 후 추가 설정 필요
def board_public_modify(request, pk):
    board = get_object_or_404(Board, id=pk)
    
    context = {
        'board': board,
    }

    if request.method == 'GET' or request.method == 'FILES':
        write_form = PBoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(request, 'board_public/board_public_modify.html', context)
    
    elif request.method == 'POST':
        write_form = PBoardWriteForm(request.POST, request.FILES)

        if write_form.is_valid():
            board.title=write_form.title
            board.contents=write_form.contents
            board.writer=write_form.writer
            board.sentence=write_form.sentence
            board.image=write_form.image
            board.file=write_form.file
            
            board.save()
            return redirect('/board/public')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board_public/board_public_modify.html', context)


#### 과학자 ####
#게시판 목록
def board_science_list(request):
    sc_boards = Board.objects.filter(board_name='Science').order_by('id')

    paginator = Paginator(sc_boards, 10)
    pagenum = request.GET.get('page')
    sc_boards = paginator.get_page(pagenum)

    context = {
        'sc_boards' : sc_boards,
    }

    return render(request, 'board_science/board_science_list.html', context)

#글 작성하기
def board_science_write(request):
    if request.method == 'GET':
        write_form = SBoardWriteForm()
        context = {
            'forms': write_form,
        }
        return render(request, 'board_science/board_science_write.html', context)
    elif request.method == 'POST' or request.method == 'FILES':
        write_form = SBoardWriteForm(request.POST, request.FILES)

        if write_form.is_valid():
            board = Board(
                title=write_form.title,
                contents=write_form.contents,
                writer=write_form.writer,
                sentence=write_form.sentence,
                file=write_form.file,
                board_name="Science"
            )
            board.save()
            return redirect('/board/science')
        else:
            context = {
                'forms': write_form,
            }
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board_science/board_science_write.html', context)

#글 상세보기
def board_science_detail(request, pk):
    board = get_object_or_404(Board, id=pk)

    context = {
        'board': board,
    }

    return render(request, 'board_science/board_science_detail.html', context)

#삭제하기 - user 설정 후 추가 설정 필요
def board_science_delete(request, pk):
    board = get_object_or_404(Board, id=pk)

    board.delete()
    return redirect('/board/science')

#수정하기 - user 설정 후 추가 설정 필요
def board_science_modify(request, pk):
    board = get_object_or_404(Board, id=pk)
    
    context = {
        'board': board,
    }

    if request.method == 'GET' or request.method == 'FILES':
        write_form = SBoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(request, 'board_science/board_science_modify.html', context)
    
    elif request.method == 'POST':
        write_form = SBoardWriteForm(request.POST, request.FILES)

        if write_form.is_valid():
            board.title=write_form.title
            board.contents=write_form.contents
            board.writer=write_form.writer
            board.sentence=write_form.sentence
            board.file=write_form.file
            
            board.save()
            return redirect('/board/science')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board_science/board_science_modify.html', context)
