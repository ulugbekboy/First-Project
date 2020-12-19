from django.views.generic.base import View 
from django.views.generic import ListView , DetailView
from .models import *
from django.shortcuts import render , redirect
from .forms import *
from django.db.models import Q
from django.http import JsonResponse


# class MoviesView(View):
#     def get (self ,request):
#         movies = Movie.objects.all()
#         return render(request , 'movies.html' , {'movies_list': movies})


class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear ,ListView):
    
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name= 'movies.html'
    paginate_by =3

    def get_context_data(self,*args , **kwargs):
        context = super().get_context_data(*args , **kwargs)
        context["categories"] = Category.objects.all().order_by('-id')
        context['movies'] = Movie.objects.order_by("id")[:3]
        return context
  

    
   


# class MovieDetailView(View):
#     def get(self, request , pk):
#         movie = Movie.objects.get(id=pk)
#         return render(request , 'moviedetail.html' , {'movie': movie})


class MovieDetailView(GenreYear ,DetailView):
    model = Movie
    slug_field = 'url'
    template_name= 'moviedetail.html'

    def get_context_data(self,*args , **kwargs):
        context = super().get_context_data(*args , **kwargs)
        context["categories"] = Category.objects.all()
        context['movies'] = Movie.objects.order_by("id")[:3]
        context['star_form'] = RatingForm()
        return context


class AddReview(View):
    def post(self , request , pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form =form.save(commit=False)
            if request.POST.get('parent' , None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear ,DetailView):
    model = Actor
    template_name='actors.html'
    slug_field='name'


class FilterMoviesView(GenreYear ,ListView):
    
    template_name ='movies.html'
    paginate_by =3
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset
    
    def get_context_data(self,*args , **kwargs):
        context = super().get_context_data(*args , **kwargs)
        context["categories"] = Category.objects.all()
        context['movies'] = Movie.objects.order_by("id")[:3]
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


    

class JsonFilterMoviesView(ListView):
    
    template_name ='movies.html'
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)

    def get_context_data(self,*args , **kwargs):
        context = super().get_context_data(*args , **kwargs)
        context["categories"] = Category.objects.all()
        context['movies'] = Movie.objects.order_by("id")[:3]
        return context


class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class SearchView(ListView):
    
    template_name= 'movies.html'
    paginate_by = 3
    slug_field = 'url'
    queryset = Movie.objects.filter(draft=False)

    def get_queryset(self):
        queryset = Movie.objects.filter(
        Q(year__in=self.request.GET.getlist("year")) |
        Q(genres__in=self.request.GET.getlist("genre"))
    ).distinct()
        return queryset


    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context = super().get_context_data(*args , **kwargs)
        context["categories"] = Category.objects.all()
        context['movies'] = Movie.objects.order_by("-id")[:3]
        return context

       