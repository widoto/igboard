import os
import re
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PBoardWriteForm, SBoardWriteForm, CommentForm
from .models import Board, BoardLikeUsers, Comment
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count
from django.contrib import messages 

#### 전체 게시판 ####
def board_list(request):
    pb_boards = Board.objects.filter(board_name='Public').order_by('-id')
    sc_boards = Board.objects.filter(board_name='Science').order_by('-id')

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

# 검색
def board_search(request):
    pb_boards = Board.objects.filter(board_name='Public').order_by('-id')
    sc_boards = Board.objects.filter(board_name='Science').order_by('-id')

    q = request.GET.get('q', "")
    search_type = request.GET.get('type', "")

    if q:
        if search_type == "all":
            pb_boards = pb_boards.filter(Q (title__icontains=q)| Q (contents__icontains=q)| Q (writer__icontains=q)| Q (sentence__icontains=q))
            sc_boards = sc_boards.filter(Q (title__icontains=q)| Q (contents__icontains=q)| Q (writer__icontains=q)| Q (sentence__icontains=q))
        elif search_type == "title_contents":
            pb_boards = pb_boards.filter(Q (title__icontains=q)| Q (contents__icontains=q))
            sc_boards = sc_boards.filter(Q (title__icontains=q)| Q (contents__icontains=q))
        elif search_type == "title":
            pb_boards = pb_boards.filter(title__icontains=q)
            sc_boards = sc_boards.filter(title__icontains=q)
        elif search_type == "contents":
            pb_boards = pb_boards.filter(contents__icontains=q)
            sc_boards = sc_boards.filter(contents__icontains=q)
        elif search_type == "writer":
            pb_boards = pb_boards.filter(writer__icontains=q)
            sc_boards = sc_boards.filter(writer__icontains=q)
        elif search_type == "sentence":
            pb_boards = pb_boards.filter(sentence__icontains=q)
            sc_boards = sc_boards.filter(sentence__icontains=q)
        return render(request, 'board/board_search.html', {'pb_boards' : pb_boards,'sc_boards' : sc_boards, 'q' : q})
    
    else:
        return render(request, 'board/board_search.html')

#### 일반인 ####
#게시판 목록
def board_public_list(request):
    sort = request.GET.get('sort','')

    if sort == 'likes':
        pb_boards = Board.objects.filter(board_name='Public').annotate(like_count=Count('like_users')).order_by('-like_count', '-write_dttm')
    else:
        pb_boards = Board.objects.filter(board_name='Public').order_by('-id')

    paginator = Paginator(pb_boards, 10)
    pagenum = request.GET.get('page')
    pb_boards = paginator.get_page(pagenum)

    context = {
        'pb_boards' : pb_boards,
        'sort':sort,
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
                writer=request.user,
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
    comments = Comment.objects.filter(board=board.id).order_by('created_at')
    # 좋아요 수 띄우기
    like = BoardLikeUsers.objects.filter(board = board.id).annotate(Count('user'))
    like_num = like.count()
    #댓글
    comment_form = CommentForm()

    context = {
        'board': board,
        'like_num' : like_num,
        'comment_form' : comment_form,
        'comments' : comments
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
        file_change_check = request.POST.get('fileChange', False)
        file_check = request.POST.get('file-clear', False)
        image_change_check = request.POST.get('imageChange', False)
        image_check = request.POST.get('image-clear', False)

        if file_check or file_change_check:
            os.remove(os.path.join(settings.MEDIA_ROOT, board.file.path))
            board.file = ''
        if image_check or image_change_check:
            os.remove(os.path.join(settings.MEDIA_ROOT, board.image.path))
            board.image = ''

        write_form = PBoardWriteForm(request.POST, request.FILES)

        if write_form.is_valid():
            board.title=write_form.title
            board.contents=write_form.contents
            board.writer=write_form.writer
            board.sentence=write_form.sentence
            if write_form.image:
                board.image=write_form.image
            if write_form.file:
                board.file=write_form.file
            
            board.save()
            return redirect('/board/public')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board_public/board_public_modify.html', context)

# 검색
def board_public_search(request):
    boards = Board.objects.filter(board_name='Public').order_by('-id')

    q = request.GET.get('q', '')
    search_type = request.GET.get('type', '')

    if q:
        if search_type == "all":
            boards = boards.filter(Q (title__icontains=q)| Q (contents__icontains=q)| Q (writer__icontains=q)| Q (sentence__icontains=q))
        elif search_type == "title_contents":
            boards = boards.filter(Q (title__icontains=q)| Q (contents__icontains=q))
        elif search_type == "title":
            boards = boards.filter(title__icontains=q)
        elif search_type == "contents":
            boards = boards.filter(contents__icontains=q)
        elif search_type == "writer":
            boards = boards.filter(writer__icontains=q)
        elif search_type == "sentence":
            boards = boards.filter(sentence__icontains=q)
        paginator = Paginator(boards, 10)
        pagenum = request.GET.get('page')
        boards = paginator.get_page(pagenum)

        context = {
            'boards' : boards,
            'q' : q,
            'type' : search_type
        }

        return render(request, 'board_public/board_public_search.html', context)
    
    else:
        return render(request, 'board_public/board_public_search.html')

#좋아요
def likes(request, pk):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, id=pk)

        if board.like_users.filter(pk=request.user.pk).exists():
            board.like_users.remove(request.user)
            return redirect('/' + 'board/public/detail/' + str(pk))
        else:
            board.like_users.add(request.user)
            return redirect('/' + 'board/public/detail/' + str(pk))
    else :
        context = {
            'messages' : messages.info(request, '로그인 해주세요.')
        }
        return redirect('/' + 'board/public/detail/' + str(pk), context)

#일반인_댓글 생성
def comments_create(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            board = get_object_or_404(Board, pk=pk)
            commentform = CommentForm(request.POST)
            if commentform.is_valid():
                comment = commentform.save(commit=False)
                comment.board = board
                comment.user = request.user
                comment.save()
            return redirect('/' + 'board/public/detail/' + str(pk))
        return redirect('/'+'accounts/login')

#일반인_댓글 삭제
def comments_delete(request, board_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('/' + 'board/public/detail/' + str(board_pk))

#### 과학자 ####
#게시판 목록
def board_science_list(request):
    sort = request.GET.get('sort','')
    if sort == 'likes':
        sc_boards = Board.objects.filter(board_name='Science').annotate(like_count=Count('like_users')).order_by('-like_count', '-write_dttm')
    else:
        sc_boards = Board.objects.filter(board_name='Science').order_by('-id')

    paginator = Paginator(sc_boards, 10)
    pagenum = request.GET.get('page')
    sc_boards = paginator.get_page(pagenum)

    context = {
        'sc_boards' : sc_boards,
        'sort' : sort
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
                writer=request.user,
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
    # 좋아요 수 띄우기
    like = BoardLikeUsers.objects.filter(board = board.id).annotate(Count('user'))
    like_num=like.count()

    context = {
        'board': board,
        'like_num' : like_num,
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
        file_change_check = request.POST.get('fileChange', False)
        file_check = request.POST.get('file-clear', False)

        if file_check or file_change_check:
            os.remove(os.path.join(settings.MEDIA_ROOT, board.file.path))
            board.file = ''

        write_form = SBoardWriteForm(request.POST, request.FILES)

        if write_form.is_valid():
            board.title=write_form.title
            board.contents=write_form.contents
            board.writer=write_form.writer
            board.sentence=write_form.sentence
            if write_form.file:
                board.file=write_form.file
            
            board.save()
            return redirect('/board/science')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board_science/board_science_modify.html', context)

# 검색
def board_science_search(request):
    boards = Board.objects.filter(board_name='Science').order_by('-id')

    q = request.GET.get('q', '')
    search_type = request.GET.get('type', '')

    if q:
        if search_type == "all":
            boards = boards.filter(Q (title__icontains=q)| Q (contents__icontains=q)| Q (writer__icontains=q)| Q (sentence__icontains=q))
        elif search_type == "title_contents":
            boards = boards.filter(Q (title__icontains=q)| Q (contents__icontains=q))
        elif search_type == "title":
            boards = boards.filter(title__icontains=q)
        elif search_type == "contents":
            boards = boards.filter(contents__icontains=q)
        elif search_type == "writer":
            boards = boards.filter(writer__icontains=q)
        elif search_type == "sentence":
            boards = boards.filter(sentence__icontains=q)
        paginator = Paginator(boards, 10)
        pagenum = request.GET.get('page')
        boards = paginator.get_page(pagenum)

        context = {
            'boards' : boards,
            'q' : q,
            'type' : search_type
        }
        return render(request, 'board_science/board_science_search.html', context)
    
    else:
        return render(request, 'board_science/board_science_search.html')

#좋아요
def board_science_likes(request, pk):
    #if request.user.is_authenticated:
    board = get_object_or_404(Board, id=pk)

    if board.like_users.filter(pk=request.user.pk).exists():
        board.like_users.remove(request.user)
        return redirect('/' + 'board/science/detail/' + str(pk))
    else:
        board.like_users.add(request.user)
        return redirect('/' + 'board/science/detail/' + str(pk))
        #return redirect('board/board_detail/' + str(pk))

    #return redirect('#로그인')
