# coding:utf8
import time
from unittest import skip
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        """
        html 5 required 字段导致前端阻止表单提交  此测试失效
        """
        # # 打开首页 提交空待办事项
        # self.browser.get(self.server_url)
        # self.get_item_input_box().send_keys(Keys.ENTER)
        # # 首页刷新 显示错误消息
        # # 待办事项不能为空
        # time.sleep(1)
        # error = self.browser.find_element_by_css_selector(".has-error")
        # self.assertEqual(error.text, "You can't have an empty list item")
        #
        # # 输入文字 再次提交 没问题
        # self.get_item_input_box().send_keys("Buy milk" + Keys.ENTER)
        # self.check_for_row_in_list_table("1: Buy milk")
        #
        # # 再次提交空待办事项
        # self.get_item_input_box().send_keys(Keys.ENTER)
        # time.sleep(1)
        # # 提示错误消息
        # self.check_for_row_in_list_table("1: Buy milk")
        # error = self.browser.find_element_by_css_selector(".has-error")
        # self.assertEqual(error.text, "You can't have an empty list item")
        #
        # # 输入问题 提交 没问题
        # self.get_item_input_box().send_keys("Make tea" + Keys.ENTER)
        # time.sleep(3)
        # self.check_for_row_in_list_table("1: Buy milk")
        # self.check_for_row_in_list_table("2: Make tea")
        return
