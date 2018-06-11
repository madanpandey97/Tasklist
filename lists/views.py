from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from lists.models import  Todo
from lists.forms import TaskForm


@login_required
def index(request):
    """ Main url function contian list of all task with paginator feature"""

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
    """function of creating task list with task, title task description and task level"""
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
    """ User dashboard, where user can keep track of all the task and who mark the task."""
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
    """ The function for deleting the task only authenticated user can delete their 
        task. No other user can able to delete the task of other user."""
    tasklist = get_object_or_404(Todo, pk=tasklist_id)
    tasklist.delete()
    print(tasklist)
    messages.success(request, "Successfully deleted")
    return redirect('lists:alllist')



@login_required
def task_update(request, id=None):
    """ The function for updating the task title task descripion and the level of task"""
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
    """ The function features can allow other user to mark the task once it is done.Once a task 
    is done the mark button will automatically disabled. user can check on their dashboard who marked it."""
    #obj = Todo.objects.all()
    user = request.user if request.user.is_authenticated else None
    Todo.objects.filter(id=id).update(mark_done=True, answered_by= user)
    return redirect('lists:alllist')


