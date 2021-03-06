# coding:utf8
import re
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_LIST_ERROR


# Create your tests here.
class HomePageTest(TestCase):
    # maxDiff = None
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve("/")
    #     self.assertEqual(found.func, home_page)
    #     return
    #
    # def test_home_page_return_correct_html(self):
    #     # 令牌不一致 导致无法测试
    #     def del_csrf(text):
    #         """去除 csrftoken 影响"""
    #         text = re.sub("<input[^>]+name=[\'\"]csrfmiddlewaretoken[\'\"][^>]+>", "", text)
    #         return text
    #
    #     request = HttpRequest()
    #     response = home_page(request)
    #     expected_html = render_to_string("home.html", context={'form': ItemForm()}, request=request)
    #     # self.assertEqual(del_csrf(response.content.decode()), del_csrf(expected_html))
    #     self.assertMultiLineEqual(del_csrf(response.content.decode()), del_csrf(expected_html))
    #     return

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        return

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
        return


class ListViewTest(TestCase):
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/%d/' % list_.id,
            data={'text': ''}
        )

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

    def test_for_invalid_input_shows_errors_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
        return

    def test_display_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')
        return

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
        return

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        return

    def test_for_invalid_input_passes_from_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)
        return


class NewListTest(TestCase):
    def test_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        # 测试是否保存入数据库
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        return

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%s/' % new_list.id, 302)
        return

    def test_for_validation_input_renders_home_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        return

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
        return

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context['form'], ItemForm)
        return

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post('/lists/%s/' % correct_list.id,
                         data={'text': 'A new item fro an exists list'}
                         )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item fro an exists list')
        self.assertEqual(new_item.list, correct_list)
        return

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post('/lists/%s/' % correct_list.id,
                                    data={'text': 'A new item fro an exists list'}
                                    )
        self.assertRedirects(response, '/lists/%s/' % correct_list.id)
        return

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%s/' % correct_list.id)
        self.assertEqual(response.context['list'], correct_list)
        return
