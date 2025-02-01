from math import ceil
from product.models import Product, Category
from product.serializers import ProductAlldataSerializer, ProductSerializer, CategorySerializer
from django.db.models import Q


def getAllProducts(request):
    try:        
        # Sorting
        order = request.GET.get('sort', 'create_date')

        # Filtering by categories
        categories = request.GET.getlist('categories[]', [])
        if categories:
            products = Product.objects.filter(category_id__name__in=categories).order_by(order)
        else:
            products = Product.objects.all().order_by(order)

        # Search query
        search_query = request.GET.get('q', '')
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

            
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        total_count = products.count()

        start = (page - 1) * page_size
        end = start + page_size

        paginated_products = products[start:end]

        serializer = ProductSerializer(paginated_products, many=True)

        # Determine if there's more data
        has_more = end < total_count
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Products",
            "success": True,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": ceil(total_count / page_size),
                "has_more": has_more,
            }
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def createProduct(request):
    try: 
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Product Created Successfully.",
                "success": True,
            }
        else:
            return {
                "data": serializer.errors,
                "status": 400,
                "message": "Something went wrong..!!",
                "success": True,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def getProductDetail(request, pk):
    try: 
        product = Product.objects.get(pk=pk)
        if product:
            serializer = ProductAlldataSerializer(product)
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Product Created Successfully.",
                "success": True,
            }
        else :
            return {
                "data": {},
                "status": 400,
                "message": "Product not found.",
                "success": True,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def updateProduct(request, pk):
    try: 
        product = Product.objects.get(pk=pk)
        if product:
            serializer = ProductAlldataSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {
                    "data": serializer.data,
                    "status": 200,
                    "message": "Product Updated Successfully.",
                    "success": True,
                }
            else:
                return {
                    "data": serializer.errors,
                    "status": 400,
                    "message": "Something went wrong..!!",
                    "success": True,
                }
        else:
            return {
                "data": {},
                "status": 400,
                "message": "Product not found.",
                "success": True,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def deleteProduct(request, pk):
    try: 
        product = Product.objects.get(pk=pk)
        if product:
            product.delete()
            return {
                "data": {},
                "status": 200,
                "message": "Product Deleted Successfully.",
                "success": True,
            }
        else:
            return {
                "data": {},
                "status": 400,
                "message": "Product not found.",
                "success": True,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def getAllTrendingProducts(request):
    try:
        products = Product.objects.filter(visibility='Public', publish_status='Published').order_by("?")[:4]
        serializer = ProductSerializer(products, many=True)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Trending Products",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def getAllRelatedProducts(request):
    try:
        products = Product.objects.filter(visibility='Public', publish_status='Published').order_by("?")[:4]
        serializer = ProductSerializer(products, many=True)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Trending Products",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def getAllCategories(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Categories",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

