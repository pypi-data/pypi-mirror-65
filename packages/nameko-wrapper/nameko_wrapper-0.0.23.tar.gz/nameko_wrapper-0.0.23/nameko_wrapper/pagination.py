"""
Paginator
"""


class PaginatorBase(object):

    page = 1
    size = 10

    def __call__(self, data, sort=False):
        return self.get_page_info(data)

    @staticmethod
    def get_sort_info(data):
        if data and isinstance(data, dict):
            order = data.get('order')
            if order:
                return SortParser(order).parse()
        return []

    @classmethod
    def get_page_info_from_data(cls, data, sort=False):
        """获取分页信息"""
        if not data:
            page = 0
            size = 0
        else:
            if isinstance(data, dict):
                page = data.get('page', 0)
                size = data.get('size', 0)
            else:
                page = getattr(data, 'page', 0)
                size = getattr(data, 'size', 0)

            # 转换为整数
            try:
                page = int(page)
                size = int(size)
            except Exception as e:
                raise e
            else:
                if page < 0:
                    page = 0

                if size < 0:
                    size = 0

        result = {'page': page, 'size': size}

        if sort:
            order = cls.get_sort_info(data)
            if order:
                result['sort'] = order

        return result

    def get_page_info(self, data, sort=False):
        """获取分页信息将无效分页信息替换为默认信息"""
        info = self.get_page_info_from_data(data, sort=sort)
        if not info['page']:
            info['page'] = self.page

        if not info['size']:
            info['size'] = self.size

        return info

    def get_offset_page_info(self, data, sort=False):
        info = self.get_page_info(data, sort)

        offset = (info['page'] - 1) * info['size']
        return {'offset': offset, 'size': info['size']}

    def get_page_slice(self, data):
        info = self.get_offset_page_info(data)
        return slice(info['offset'], info['offset'] + info['size'])


class DefaultPaginator(PaginatorBase):
    """小型分页"""

    size = 10


class CustomPaginator(PaginatorBase):
    """自定义分页"""

    def __init__(self, size):
        self.size = int(size)

        if self.size <= 0:
            raise ValueError('size must >0')


paginator = DefaultPaginator()


class SortParser(object):
    """排序解析器"""

    def __init__(self, order):
        if not order or not isinstance(order, str):
            raise ValueError(f'Invalid order value {order}, must be str.')

        self.order = order

    def parse(self):
        order_list = self.order.split(',')
        order_list = filter(lambda x: bool(x.strip()), order_list)
        return [item.strip() for item in order_list]


if __name__ == '__main__':
    print(DefaultPaginator().get_page_info(data={'page': '1', 'size': '3', 'order': '-a'}, sort=False))
    print(CustomPaginator('7')({'page': '0', 'size': '3'}))

    s = SortParser(order='a, ,-c')
    print(s.parse())
