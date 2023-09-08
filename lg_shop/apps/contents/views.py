from django.shortcuts import render, redirect, reverse
from django.views import View

from .utlis import get_categories
from .models import ContentCategory, Content


class GoIndexView(View):
    def get(self, request):
        return redirect(reverse("contents:index"))


class IndexView(View):
    def get(self, request, *args, **kwargs):
        categories = get_categories()
        # print("categories", categories)

        # 查询是所有的广告类别
        context_categories = ContentCategory.objects.all()
        # print(context_categories)
        contents = {}

        for context_category in context_categories:
            contents[context_category.key] = Content.objects.filter(category_id=context_category.id,
                                                                    status=True).all().order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, "index.html", context)
