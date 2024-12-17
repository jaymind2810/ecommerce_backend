from product.models import Product
from product.serializers import ProductAlldataSerializer, ProductSerializer


def getAllProducts(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Products",
            "success": True,
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