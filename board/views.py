from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardWriteForm
from .models import Board
from django.core.paginator import Paginator

def board_list(request):
    pb_boards = Board.objects.filter(board_name='Public').order_by('id')

    paginator = Paginator(pb_boards, 10)
    pagenum = request.GET.get('page')
    pb_boards = paginator.get_page(pagenum)

    context = {
        'pb_boards' : pb_boards,
    }

    return render(request, 'board/board_list.html', context)

def board_write(request):
    if request.method == 'GET':
        write_form = BoardWriteForm()
        context = {
            'forms': write_form,
        }
        return render(request, 'board/board_write.html', context)
    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            board = Board(
                title=write_form.title,
                contents=write_form.contents,
                writer=write_form.writer,
                sentence=write_form.sentence,
            )
            board.save()
            return redirect('/board')
        else:
            context = {
                'forms': write_form,
            }
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/board_write.html', context)

def board_detail(request, pk):
    board = get_object_or_404(Board, id=pk)

    context = {
        'board': board,
    }

    return render(request, 'board/board_detail.html', context)

# user 설정 후 추가 설정 필요
def board_delete(request, pk):
    board = get_object_or_404(Board, id=pk)

    board.delete()
    return redirect('/board')

# user 설정 후 추가 설정 필요
def board_modify(request, pk):
    board = get_object_or_404(Board, id=pk)
    
    context = {
        'board': board,
    }

    if request.method == 'GET':
        write_form = BoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(request, 'board/board_modify.html', context)
    
    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            board.title=write_form.title
            board.contents=write_form.contents
            board.writer=write_form.writer
            board.sentence=write_form.sentence
            
            board.save()
            return redirect('/board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/board_modify.html', context)

