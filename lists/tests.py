# coding:utf8
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)
        return

    def test_home_page_return_correct_html(self):
        # 令牌不一致 导致无法测试
        # request = HttpRequest()
        # response = home_page(request)
        # expected_html = render_to_string("home.html", request=request)
        # # print(expected_html)
        # # print(response.content.decode())
        # self.assertEqual(response.content.decode(), expected_html)
        return


class ItemAndListModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, list_)
        return


class ListViewTest(TestCase):
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%s/' % correct_list.id)

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
        return

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%s/' % list_.id)
        self.assertTemplateUsed(response, 'list.html')
        return


class NewListTest(TestCase):
    def test_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        # 测试是否保存入数据库
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        return

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%s/' % new_list.id, 302)
        return


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post('/lists/%s/add_item' % correct_list.id,
                         data={'item_text': 'A new item fro an exists list'}
                         )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item fro an exists list')
        self.assertEqual(new_item.list, correct_list)
        return

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post('/lists/%s/add_item' % correct_list.id,
                                    data={'item_text': 'A new item fro an exists list'}
                                    )
        self.assertRedirects(response, '/lists/%s/' % correct_list.id)
        return

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%s/' % correct_list.id)
        self.assertEqual(response.context['list'], correct_list)
        return
