# coding:utf8
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)
        # 判断标题和头部是否都包含 To-Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

        # 输入一个待办事项
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # 输入 "Buy peacock feathers"
        inputbox.send_keys("Buy peacock feathers")

        # 按下回车键 页面刷新
        # 待办事项表格中显示 "1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)
        # 跳转到新的页面 专属此用户的页面
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中还有一个文本框  继续输入待办事项
        inputbox = self.get_item_input_box()

        # 输入 "Use peacock feathers to make a fly"
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        # todo 卡一下？？？
        time.sleep(5)
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # 测试另一用户无法看到上一用户的信息
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 新用户进行输入
        # 输入一个待办事项
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 测试此页面仅显示 新用户信息
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # self.fail("Finish the test!")
        return