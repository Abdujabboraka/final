from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from pyexpat.errors import messages
from django.contrib import messages
from .models import Product, Category, Image, Review, Comments
from django.core.paginator import Paginator

# Create your views here.

def homepage(request):
    if request.method == 'POST':
        # Handling the review form submission
        rate = request.POST.get('rate')
        content = request.POST.get('content')
        author = request.user
        address = request.POST.get('address')
        author_photo = request.POST.get('author_photo')

        # Create a new review
        Review.objects.create(rate=rate, content=content, author=author, address=address, author_photo=author_photo)
        messages.success(request, "sizning Sharxingiz saqlandi Raxmat 😊 !")
        return redirect('homepage')  # Redirect to avoid resubmission on page refresh

    categories = Category.objects.all()[6:22].annotate(product_count=Count('product'))
    products = Product.objects.all()
    reviews = Review.objects.all()
    total = Product.objects.count()

    paginator = Paginator(products, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'reviews': reviews,
        'total': total,

    }

    return render(request, 'index.html', context)


def select_by_category(request, category_id):
    products = Product.objects.filter(category=category_id)
    # [6:22] BU DEGANI SABBAII SHUKI SUB KATEGORIYALARGA 3 TA QOSHIB MAN BOSHQATDAN QOSHMASLIK UCHUN ! :)
    categories = Category.objects.all()[6:22].annotate(product_count=Count('product'))
    reviews = Review.objects.all()
    total = Product.objects.count()
    context = {
        'products': products,
        'categories': categories,
        'reviews': reviews,
        'total': total
    }

    return render(request, 'index.html', context)


def search(request):
    query = request.GET.get('query', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        products = Product.objects.none()
    categories = Category.objects.all()[6:22].annotate(product_count=Count('product'))
    reviews = Review.objects.all()
    total = Product.objects.count()
    context = {
        'query': query,
        'products': products,
        'categories': categories,
        'reviews': reviews,
        'total': total
    }
    return render(request, 'index.html', context)


def detail(request, pk):
    product = Product.objects.get(id=pk)
    related = Product.objects.exclude(id=pk)[:5]
    comments = Comments.objects.filter(product=product)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comments.objects.create(user=request.user, product=product, content=content)
        return redirect('detail', pk=pk)

    context = {
        'product': product,
        'related': related,
        'comments': comments
    }
    return render(request, 'ShopApp/detail.html', context)

