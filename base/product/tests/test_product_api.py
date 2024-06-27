from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import Product, Category, Shop, Seller
from address.models import ShopAddress, Country, City
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics')
        country = Country.objects.create(name="Russia", continent="Europe")
        city = City.objects.create(name="Moscow", timezone="GTC+3", country=country, display_name="Moscow, Russia")
        self.shop = Shop.objects.create(
            name='Tech Store', 
            description='A store that sells tech products', 
            rate=4.5, 
            address=ShopAddress.objects.create(country=country, city=city,
                                               street="Arbat", building_number=1,
                                               entrance_number=1, apartment_number=1)
        )
        self.user = User.objects.create_user(phone="+79999999999", username='seller1', password='pass')
        self.seller = Seller.objects.create(user=self.user, shop=self.shop)
        
        self.shop_2 = Shop.objects.create(
            name='Tech Store 2.0', 
            description='A store that sells tech products 2.0', 
            rate=4.5, 
            address=ShopAddress.objects.create(country=country, city=city,
                                               street="Arbat", building_number=1,
                                               entrance_number=1, apartment_number=1)
        )

        self.user_2 = User.objects.create_user(phone="+78888888888", username='seller2', password='pass')
        self.seller_2 = Seller.objects.create(user=self.user_2, shop=self.shop_2)
        
        self.product_data = {
            'name': 'Iphone 11',
            'category': self.category.id,
            'quantity': 10,
            'description': 'An Apple smartphone',
            'discount': '0.10',
            'price': '30000.00',
            'status': 'IN STOCK',
            'rate': '4.00',
            'seller': self.seller.pk
        }
        
    def login(self):
        url = reverse("auth:login")
        
        login_data = {
            "phone": self.user.phone,
            "password": "pass"
        }
        
        response = self.client.post(url, data=login_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        # Login
        self.login()
        
        url = reverse('product:product-list')
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # POST
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.last().name, 'Iphone 11')

    def test_update_product(self):
        # Login
        self.login()

        product = Product.objects.create(
            name='Iphone 11', 
            category=self.category, 
            quantity=10, 
            description='An Apple smartphone', 
            discount=0.1, 
            price=30000.00, 
            status='IN STOCK', 
            rate=4.00, 
            seller=self.seller
        )
        url = reverse('product:product-detail', kwargs={'pk': product.pk})
        update_data = {
            'name': 'Iphone 12',
            'category': self.category.id,
            'quantity': 15,
            'description': 'An updated Apple smartphone',
            'discount': '0.15',
            'price': '35000.00',
            'status': 'IN STOCK',
            'rate': '4.5',
            'seller': self.seller_2.pk
        }
        
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        product.refresh_from_db()
        
        self.assertEqual(Product.objects.get(id=product.id).name, 'Iphone 12')
        self.assertEqual(product.shop.first(), self.seller_2.shop)

    def test_get_product(self):
        # Login
        self.login()
        
        product = Product.objects.create(
            name='Iphone 11', 
            category=self.category, 
            quantity=10, 
            description='An Apple smartphone', 
            discount=0.1, 
            price=30000.00, 
            status='IN STOCK', 
            rate=4.00, 
            seller=self.seller
        )
        url = reverse('product:product-detail', kwargs={'pk': product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Iphone 11')

    def test_delete_product(self):
        # Login
        self.login()
        
        product = Product.objects.create(
            name='Iphone 11', 
            category=self.category, 
            quantity=10, 
            description='An Apple smartphone', 
            discount=0.1, 
            price=30000.00, 
            status='IN STOCK', 
            rate=4.00, 
            seller=self.seller
        )
        url = reverse('product:product-detail', kwargs={'pk': product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
