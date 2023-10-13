from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
from .models import Webtoon, User_Webtoon
from .forms import User_WebtoonForm
from collections import Counter
from .secret import gpt_api_key

# import openai
# import csv


# # OpenAI API 인증 정보 설정
# openai.api_key = gpt_api_key



def test(request):
    webtoon_list = User_Webtoon.objects.filter(reviewer=request.user).values('webtoon')
    webtoon_list_genre = Webtoon.objects.filter(id__in=webtoon_list).values('genre')
    all_webtoon_query = Webtoon.objects.all().values('id', 'genre')
    all_webtoon = {item['id']: item['genre'][1:].split('#') for item in all_webtoon_query}
    
    genre = [genre for i in webtoon_list_genre for genre in i['genre'][1:].split('#')]
    most_common_genres = Counter(genre).most_common(3)
    genre = [genre for genre, __ in most_common_genres]
    
    result = find_webtoons_with_genres(all_webtoon, genre)
    result.sort(key=lambda x: x[1], reverse=True)
    
    id_list = [d['webtoon'] for d in webtoon_list]
    
    result = [t for t in result if t[0] not in id_list]
    result = result[:10]
    result = [t[0] for t in result]

    return HttpResponse(result)

def index(request):
    searched = request.GET.get('searched', '')
    page = request.GET.get('page', '1')
    if searched:       
            webtoon_list = Webtoon.objects.filter(
                Q(title__icontains=searched) |
                Q(author__icontains=searched) |
                Q(genre__icontains=searched)).distinct()
    else:
        webtoon_list = Webtoon.objects.all()
    paginator = Paginator(webtoon_list, 12)
    page_obj = paginator.get_page(page)
    context = {'webtoon_list': page_obj, 'searched': searched}
    
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
    searched = request.GET.get('searched', '')
    page = request.GET.get('page', '1')
    if searched:       
            webtoon_list = Webtoon.objects.filter(
                Q(title__icontains=searched) |
                Q(author__icontains=searched) |
                Q(genre__icontains=searched)).distinct()
    else:
        webtoon_list = Webtoon.objects.all()
    paginator = Paginator(webtoon_list, 12)
    page_obj = paginator.get_page(page)
    context = {'webtoon_list': page_obj, 'searched': searched}
    
    return render(request, 'webtoon/webtoon_list.html', context)

@login_required
def aireco(request):
    posible_user = request.user

    # 유저가 본 웹툰
    user_webtoon_list = User_Webtoon.objects.filter(reviewer=posible_user).values('webtoon')
    user_webtoon_list = Webtoon.objects.filter(id__in=user_webtoon_list)

    if user_webtoon_list.count() <= 12:
        page = request.GET.get('page', '1')
        webtoon_list = User_Webtoon.objects.filter(reviewer=request.user).values('webtoon')
        webtoon_list = Webtoon.objects.filter(id__in=webtoon_list)

        paginator = Paginator(webtoon_list, 12)
        page_obj = paginator.get_page(page)
        context = {'webtoon_list': page_obj, 'posible_user': 'false'}

        return render(request, 'webtoon/webtoon_list.html', context)
    
    else:
        page = request.GET.get('page', '1')
        webtoon_list = User_Webtoon.objects.filter(reviewer=request.user).values('webtoon')
        genre_keyword = extract_genre(webtoon_list)
        # Ai 추천 코드
        # webtoon_list = recommendation(webtoon_list)
        result_id = extract_genre(webtoon_list)

        webtoon_list = Webtoon.objects.filter(id__in=result_id)
        paginator = Paginator(webtoon_list, 12)
        page_obj = paginator.get_page(page)
        context = {'webtoon_list': page_obj, 'posible_user': 'true'}

    return render(request, 'webtoon/webtoon_list.html', context)

def extract_genre(webtoon_list):
    
    webtoon_list_genre = Webtoon.objects.filter(id__in=webtoon_list).values('genre')
    all_webtoon_query = Webtoon.objects.all().values('id', 'genre')
    all_webtoon = {item['id']: item['genre'][1:].split('#') for item in all_webtoon_query}
    
    genre = [genre for i in webtoon_list_genre for genre in i['genre'][1:].split('#')]
    most_common_genres = Counter(genre).most_common(3)
    genre = [genre for genre, __ in most_common_genres]
    
    result = find_webtoons_with_genres(all_webtoon, genre)
    result.sort(key=lambda x: x[1], reverse=True)
    
    id_list = [d['webtoon'] for d in webtoon_list]
    
    result = [t for t in result if t[0] not in id_list]
    result = result[:24]
    result = [t[0] for t in result]
    
    return result

def find_webtoons_with_genres(webtoon_data, top_genres):
    matching_webtoons = []
    
    for webtoon_id, genres in webtoon_data.items():
        webtoon_genres = set(genres)
        common_genres = webtoon_genres.intersection(top_genres)
        
        if len(common_genres) >= 3:
            matching_webtoons.append((webtoon_id, 3))
        elif len(common_genres) >= 2:
            matching_webtoons.append((webtoon_id, 2))
        elif len(common_genres) >= 1:
            matching_webtoons.append((webtoon_id, 1))

    return matching_webtoons
### def recommendation(webtoon_list):


# # GPT-3 모델 호출 및 결과 반환 함수
# def generate_chat_response(messages: list, user_input: str) -> str:
#     try:
#         messages.append({"role": "user", "content": f"{user_input}"})
#         completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
#         assistant_content = completion.choices[0].message["content"].strip()
#         messages.append({"role": "assistant", "content": f"{assistant_content}"})
#         return assistant_content
#     except Exception as e:
#         assistant_content = "Error: " + str(e)
#         return assistant_content

# def chat(webtoon_genre: str):

#     # Request Body에서 입력 메시지 추출
#     inputText = f""" 입력하시오 {webtoon_genre}"""

#     # 이전 대화 기록을 저장할 리스트 생성
#     messages = []

#     # GPT-3 모델 호출 및 채팅 응답 생성
#     chat_response = generate_chat_response(messages, inputText)


#     return chat_response

