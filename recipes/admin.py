from django.contrib import admin
from .models import Tag, Recipe, RecipeIngredient

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')



class RecipeIngredientlnline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientlnline, )
    list_display = ('id', 'author', 'title', 'is_active')
    search_fields = ('title', )
    list_filter = ('is_active', 'tags')
    # date_hierarchy = 'created_date'
    filter_horizontal = ('tags', )
    autocomplete_fields = ('author', )


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_author', 'recipe', 'title', 'unit', )
    # date_hierarchy = 'created_date'
    autocomplete_fields = ('recipe', )
    list_filter = ('unit', )
    search_fields = ('title', )

    def get_author(self, obj):
        return obj.recipe.author


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
