from django.contrib import admin
from .models import *
from django import forms
from django.utils.safestring import mark_safe




from ckeditor_uploader.widgets import CKEditorUploadingWidget 



class MovieAdminForm(forms.ModelForm):
    description = forms.CharField( label='Описание' , widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields ='__all__'




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name' , 'url' , 'id')
    list_display_links=['name']



class ReviewInline1(admin.StackedInline):
    model = Reviews
    extra =1



class ReviewInline2(admin.TabularInline):
    model = Reviews
    extra =1
    readonly_fields =('name' , 'email')


class MovieShotsInline(admin.TabularInline):
    model =MovieShots
    extra=1
    readonly_fields =('get_image',)
    def get_image(self ,obj):
        return mark_safe(f'<img src={obj.image.url} width ="50" height="60"')
    get_image.short_description= 'Изображение'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display =('title' , 'category' , 'url' , 'draft', 'year')
    list_filter=('category__name','title')
    search_fields = ('title' , 'caregory__name')
    inlines = [MovieShotsInline ,ReviewInline1]
    save_on_top =True
    save_as = True
    
    list_editable =('draft',)
    actions =[ 'publish' , 'unpublish']
    form = MovieAdminForm
    readonly_fields =('get_image',)
    # fields =(('actors' , 'directors' , 'genres'), 'title' ,'category' , 'url')
    fieldsets =(
       (
           'Title',{
               'fields':(('title' , 'tagline', 'category' ,'year'),)
           }
       ),
        (
          ' Description',{
               'fields':(('description' , 'poster' , 'get_image'),)
           }
       ),
        (
           'Actors',{
               'classes':('collapse',),
               'fields':(('actors' , 'directors' , 'genres'),)
           }
       ),
        (
           'Options',{
               'fields':(('url' , 'draft'),)
           }
       ),
    )

    def get_image(self ,obj):
        return mark_safe(f'<img src={obj.poster.url} width ="50" height="60"')
    



    def unpublish(self , request, queryset):
        row_update = queryset.update(draft=True)
        if row_update ==1:
            message_bit ="1 запись была обновлена"
        else:
            message_bit=f'{row_update} записи были обновлены'
        self.message_user(request, f"{message_bit}")




    def publish(self , request, queryset):
        row_update = queryset.update(draft=False)
        if row_update ==1:
            message_bit ="1 запись была обновлена"
        else:
            message_bit=f'{row_update} записи были обновлены'
        self.message_user(request,f"{message_bit}")



    get_image.short_description= 'Постер'


    publish.short_description="Опубликовать"
    publish.allоwed_permissions=('change',)

    unpublish.short_description="Снять с публикации"
    unpublish.allоwed_permissions=('change',)



@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display =('name' , 'email' , 'parent' , 'movie' , 'id')
    readonly_fields = ('name' ,'email')
    inlines=[ReviewInline2]
    

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display =('name'  ,  'url')
    list_filter=('name',)
    
    


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display =('title' ,  'movie' ,'get_image' , )
    readonly_fields = ('get_image',)

    def get_image(self ,obj):
        return mark_safe(f'<img src={obj.image.url} width ="50" height="60"')

    get_image.short_description= 'Изображение'
 


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display =('value',)
   


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display =('ip' , 'star' ,  'movie')
  

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display =('name' , 'age' ,'get_image' )
    readonly_fields=('get_image',)
    list_filter=('name',)

    def get_image(self ,obj):
        return mark_safe(f'<img src={obj.image.url} width ="50" height="60"')
    get_image.short_description= 'Изображение'



admin.site.site_title ='KINOTIME'
admin.site.site_header ='KINOTIME'
