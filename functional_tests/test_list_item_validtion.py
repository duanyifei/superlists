# coding:utf8
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 打开首页 提交空待办事项
        self.browser.get(self.server_url)
        self.browser.find_element_by_id("id_new_item").send_keys("\n")
        # 首页刷新 显示错误消息
        # 待办事项不能为空
        error = self.browser.find_element_by_css_selector(".has-error")
        self.assertEqual(error.text, "You can't have an empty list item")

        # 输入文字 再次提交 没问题
        self.browser.find_element_by_id("id_new_item").send_keys("Buy milk\n")
        self.check_for_row_in_list_table("1: Buy milk")

        # 再次提交空待办事项
        self.browser.find_element_by_id("id_new_item").send_keys("\n")

        # 提示错误消息
        self.check_for_row_in_list_table("1: Buy milk")
        error = self.browser.find_element_by_css_selector(".has_error")
        self.assertEqual(error.text, "You can't have an empty list item")

        # 输入问题 提交 没问题
        self.browser.find_element_by_id("id_new_item").send_keys("Make tea\n")
        self.check_for_row_in_list_table("1: Buy milk")
        self.check_for_row_in_list_table("2: Make tea")
        return
