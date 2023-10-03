from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
from .models import Webtoon, User_Webtoon
from .forms import User_WebtoonForm

import csv

def test(request):
    # path = '/Users/jangmingyu/django/webtoon_recommendation_2/webtoon_com_3.csv'
    # file = open(path)
    # reader = csv.reader(file)
    # list1 = []
    # for n,row in enumerate(reader):
    #     if n == 0:
    #         continue
    #     list1.append(Webtoon(
    #         title=row[0], 
    #         author=row[1], 
    #         rating=float(row[2]), 
    #         image=row[3], 
    #         webtoon_url=row[4], 
    #         genre=row[5],
    #         week=row[6],))
    # Webtoon.objects.bulk_create(list1)
    return HttpResponse('test')

def index(request):
    page = request.GET.get('page', '1')
    webtoon_list = Webtoon.objects.all()
    paginator = Paginator(webtoon_list, 12)
    page_obj = paginator.get_page(page)
    context = {'webtoon_list': page_obj}

    return render(request, 'webtoon/webtoon_list.html', context)

def week(request, webtoon_week):
    page = request.GET.get('page', '1')
    if webtoon_week == 'all':
        webtoon_list = Webtoon.objects.all()
    else:
        webtoon_list = Webtoon.objects.filter(
            Q(week__icontains=webtoon_week)
        )
        
    paginator = Paginator(webtoon_list, 12)
    page_obj = paginator.get_page(page)
    context = {'webtoon_list': page_obj}
    return render(request, 'webtoon/webtoon_list.html', context)

def detail(request, webtoon_id):
    form = User_WebtoonForm()
    webtoon = get_object_or_404(Webtoon,pk=webtoon_id)
    if request.user.is_authenticated == True:
        webtoon_reivew = User_Webtoon.objects.filter(reviewer=request.user, webtoon=webtoon)
        context = { 'webtoon': webtoon , 'form': form, 'webtoon_review': webtoon_reivew.first()}
    else:
        context = { 'webtoon': webtoon }
    return render(request, 'webtoon/webtoon_detail.html', context)

@login_required
def review(request, webtoon_id):
    webtoon = get_object_or_404(Webtoon,pk=webtoon_id)
    if request.method == "POST":
        form = User_WebtoonForm(request.POST)
        if form.is_valid():
            user_webtoon = form.save(commit=False)
            user_webtoon.reviewer = request.user
            user_webtoon.webtoon = webtoon
            user_webtoon.save()
            return redirect('webtoon:detail', webtoon_id=webtoon.id)
    else:
        form = User_WebtoonForm()
        
    context = { 'webtoon': webtoon , 'form': form}
    return render(request, 'webtoon/webtoon_detail.html', context)

def review_update(request, webtoon_id):
    webtoon_user = get_object_or_404(User_Webtoon, reviewer=request.user, webtoon=webtoon_id)
    if request.method == "POST":
        form = User_WebtoonForm(request.POST, instance=webtoon_user)
        if form.is_valid():
            user_webtoon = form.save(commit=False)
            user_webtoon.reviewer = request.user
            user_webtoon.webtoon = webtoon_user.webtoon
            user_webtoon.save()
            return redirect('webtoon:detail', webtoon_id=webtoon_user.webtoon.id)
    else:
        form = User_WebtoonForm(instance=webtoon_user)
         
    context = { 'webtoon': webtoon_user.webtoon , 'form': form}
    return render(request, 'webtoon/webtoon_detail.html', context)

@login_required
def mypage(request):
    page = request.GET.get('page', '1')
    webtoon_list = User_Webtoon.objects.filter(reviewer=request.user).values('webtoon')
    webtoon_list = Webtoon.objects.filter(id__in=webtoon_list)
    paginator = Paginator(webtoon_list, 12)
    page_obj = paginator.get_page(page)
    context = {'webtoon_list': page_obj}

    return render(request, 'webtoon/webtoon_list.html', context)

def search(request):
    page = request.GET.get('page', '1')
    if request.method == 'POST':
            searched = request.POST['searched']        
            webtoon_list = Webtoon.objects.filter(
                Q(title__icontains=searched) |
                Q(author__icontains=searched) |
                Q(genre__icontains=searched)).distinct()
    else:
        webtoon_list = Webtoon.objects.last()
    paginator = Paginator(webtoon_list, 12)
    page_obj = paginator.get_page(page)
    context = {'webtoon_list': page_obj}
    
    return render(request, 'webtoon/webtoon_list.html', context)
# def detail(request, webtoon_id):
#     webtoon = get_object_or_404(Webtoon,pk=webtoon_id)
#     context = { 'webtoon': webtoon }

#     return render(request, 'pybo/question_detail.html', context)
