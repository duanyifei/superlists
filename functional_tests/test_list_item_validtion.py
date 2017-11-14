# coding:utf8
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 打开首页 提交空待办事项

        # 首页刷新 显示错误消息
        # 待办事项不能为空

        # 输入文字 再次提交 没问题

        # 再次提交空待办事项

        # 提示错误消息

        # 输入问题 提交 没问题

        self.fail("write me!")
        return
