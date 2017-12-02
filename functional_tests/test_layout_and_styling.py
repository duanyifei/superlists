# coding:utf8
import time
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # 输入一个待办事项
        inputbox = self.get_item_input_box()
        # 测试 输入框居中显示
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                               512,
                               delta=5)
        # 输入 "Buy peacock feathers"
        inputbox.send_keys("Buy peacock feathers")

        # 按下回车键 页面刷新
        # 待办事项表格中显示 "1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中还有一个文本框  继续输入待办事项
        inputbox = self.get_item_input_box()
        # 测试 输入框居中显示
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                               512,
                               delta=5)

        # self.fail("Finish the test!")
        return
