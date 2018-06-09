from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from lists.models import  Todo
from lists.forms import TaskForm


@login_required
def index(request):
    queryset_list = Todo.objects.all() #.order_by("-timestamp")
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset_list, 2)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "taskli": queryset, 
    }
    return render(request, "lists/task_list.html", context)
   


@login_required
def create_task(request):
    all_task_list = Todo.objects.all()
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # create default todolist
            user = request.user if request.user.is_authenticated else None
            task = Todo(
                description=request.POST['description'],
                content= request.POST['content'],
                tesk_medium= request.POST['tesk_medium'],
                creator=user
            )
            task.save()
            return redirect('lists:alllist')
        else:
            return render(request, 'lists/index.html', {'form': form})

    context = {
        'form': form, 
        'taskli':all_task_list
        }
    return render(request, 'lists/create_task.html',context )
   




@login_required
def profile(request):
    tasklist_all = Todo.objects.filter(creator=request.user)
    tasklist_completed = Todo.objects.filter(creator=request.user, mark_done=False)
    print(tasklist_all)
    context={ 
    'tasklist_all':tasklist_all,
    'tasklist_completed':tasklist_completed,
    }


    return render(request, 'lists/profile.html',context )


@login_required
def task_delete(request, tasklist_id):
    tasklist = get_object_or_404(Todo, pk=tasklist_id)
    tasklist.delete()
    print(tasklist)
    messages.success(request, "Successfully deleted")
    return redirect('lists:alllist')



@login_required
def task_update(request, id=None):
    instance = get_object_or_404(Todo, id=id)
    print(instance)
    print(instance)
    form = TaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
       
        return  redirect('lists:alllist')

    context = {
        "desription": instance.description,
        "instance": instance,
        "form":form,
    }
    return render(request, "lists/update_task.html", context)




@login_required
def status_update(request, id=None):
    #obj = Todo.objects.all()
    user = request.user if request.user.is_authenticated else None
    Todo.objects.filter(id=id).update(mark_done=True, answered_by= user)
    return redirect('lists:alllist')




# def todolist(request, todolist_id):
#     all_task_list = Todo.objects.all()
#     print(all_task_list)
#     todolist = get_object_or_404(TodoList, pk=todolist_id)
#     if request.method == 'POST':
#         redirect('lists:add_todo', todolist_id=todolist_id)

#     return render(
#         request, 'lists/todolist.html',
#         {'todolist': todolist, 'form': TaskForm(), 'taskli':all_task_list}
#     )


# def add_todo(request, todolist_id):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             user = request.user if request.user.is_authenticated else None
#             todo = Todo(
#                 description=request.POST['description'],
#                 todolist_id=todolist_id,
#                 creator=user
#             )
#             todo.save()
#             return redirect('lists:todolist', todolist_id=todolist_id)
#         else:
#             return render(request, 'lists/todolist.html', {'form': form})

#     return redirect('lists:index')


# @login_required
# def overview(request):
#     if request.method == 'POST':
#         return redirect('lists:add_todolist')
#     return render(request, 'lists/overview.html', {'form': TodoListForm()})


# def new_todolist(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             # create default todolist
#             user = request.user if request.user.is_authenticated else None
#             todolist = TodoList(creator=user)
#             todolist.save()
#             todo = Todo(
#                 description=request.POST['description'],
#                 todolist_id=todolist.id,
#                 creator=user
#             )
#             todo.save()
#             all_task_list = Todo.objects.all()
#             print(all_task_list)
#             return redirect('lists:todolist', todolist_id=todolist.id)
#         else:
#             return render(request, 'lists/index.html', {'form': form})

#     return redirect('lists:index')


# def add_todolist(request):
#     if request.method == 'POST':
#         form = TodoListForm(request.POST)
#         if form.is_valid():
#             user = request.user if request.user.is_authenticated else None
#             todolist = TodoList(title=request.POST['title'], creator=user)
#             todolist.save()
#             return redirect('lists:todolist', todolist_id=todolist.id)
#         else:
#             return render(request, 'lists/overview.html', {'form': form})

#     return redirect('lists:index')