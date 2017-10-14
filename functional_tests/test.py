# coding:utf8
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(timeout=10)
        # 隐式等待
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])
        return

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        # 判断标题和头部是否都包含 To-Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

        # 输入一个待办事项
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # 输入 "Buy peacock feathers"
        inputbox.send_keys("Buy peacock feathers")

        # 按下回车键 页面刷新
        # 待办事项表格中显示 "1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)

        time.sleep(3)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中还有一个文本框  继续输入待办事项
        inputbox = self.browser.find_element_by_id("id_new_item")
        # 输入 "Use peacock feathers to make a fly"
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        time.sleep(3)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        #
        self.fail("Finish the test!")
        return