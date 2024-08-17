from django.test import Client, TestCase
from django.urls import reverse
from accounts.views import User
from store.models import Category, Product

class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(username='admin')
        self.category = Category.objects.create(name='django', slug='django')
        self.product = Product.objects.create(
            category=self.category,
            name='martillo de bronce',
            description='martillo hecho completamente de bronce',
            price='20.00',
            image='django',
            slug='hammerHead',
            is_active=True,
            stock=20
        )

    def test_index_view(self):
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
        response = self.c.get(reverse('product', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/detail.html')
        self.assertContains(response, self.product.name)

    def test_category_list_view(self):
        response = self.c.get(reverse('category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/category.html')
        self.assertContains(response, self.category.name)


class TestURLResponses(TestCase):
    def setUp(self):
        self.c = Client()

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test product detail response status
        """
        response = self.c.get(reverse('product', args=['Hammerhead']))
        self.assertEqual(response.status_code, 200)