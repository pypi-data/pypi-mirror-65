from elasticsearch_dsl import Q

from nameko_wrapper.exceptions import ParameterException
from nameko_wrapper.pagination import paginator
from nameko_wrapper.elasticsearch import ESSearch

from marshmallow import Schema


class PayloadHandler(object):
    """Payload Handler"""

    def __init__(self, origin, schema=None, *, id_field="id"):
        """
        :param origin: 上传数据 格式：{'token': '', 'data': {}}
        :param schema: 校检表单
        :param id_field: 指定id所在字段属性名称
        """

        self.origin = origin
        self._id = None
        self._id_field = id_field

        self.raw_data = self.origin.get("data", {})
        if self.raw_data is None:
            self.raw_data = {}

        if not isinstance(self.raw_data, dict):
            raise ParameterException(msg="不支持的上传参数类型")

        # Validate Schema
        self._id = self.raw_data.get(id_field)  # 提取ID
        if schema and issubclass(schema, Schema):
            data = schema().load(data=self.raw_data, many=False)
        else:
            data = self.raw_data

        self.data = data

    def get_payload_id(self, many=False):
        """获取payload中的id值"""

        if not self._id:
            raise ParameterException(msg="id参数不存在")

        if type(self._id) not in [list, str, int]:
            raise ParameterException(msg="不支持的id类型")

        if many and not isinstance(self._id, list):
            return [self._id]
        elif not many and isinstance(self._id, list):
            if len(self._id) == 1:
                return self._id[0]
            else:
                raise ParameterException(msg="获取到多个id")

        return self._id

    def get_page_info(self, sort=False):
        """获取payload分页信息"""

        return paginator.get_page_info(self.raw_data, sort=sort)

    def get_page_list(self, model, query=None, schema=None, *, sort=True, to_dict=False):
        """获取分页列表"""

        page_info = self.get_page_info(sort=sort)

        if query is None:
            query = Q()
        
        search = self.model.search().query(query)[paginator.get_page_slice(page_info)]
        if sort and 'sort' in page_info and page_info['sort']:
            search = search.sort(page_info['sort'])
        
        if to_dict:
            return ESSearch(search, schema=schema, many=True).result
        else:
            return [i for i in search]
        
    def get_instance(self, model, *, raise_exception=True):
        """获取实例"""

        id_value = self.get_payload_id()

        doc = model.get_document_by_id(
            document_id=id_value, raise_exception=raise_exception
        )
        return doc

    def create_instance(self, model, *, data=None, return_result=False):
        """创建实例

        :param model: 模型
        :param data: 处理后的data
        :param return_result: 返回结果
        """

        data = self.data if data is None else data

        doc = model(**data)
        doc.save()

        if return_result:
            result = data.copy()
            result["id"] = doc.meta.id
            return {"data": result, "code": 201}

        return doc

    def modify_instance(
        self, model, *, data=None, raise_exception=True, return_result=False
    ):
        """修改实例"""

        id_value = self.get_payload_id()
        if not isinstance(id_value, (str, int)):
            raise ParameterException(msg="无效的id参数类型")

        doc = model.get_document_by_id(
            document_id=id_value, raise_exception=raise_exception
        )

        data = self.data if data is None else data
        payload = data.copy()
        payload.pop(self._id_field, None)
        doc.update(**payload)

        if return_result:
            payload[self._id_field] = id_value
            return {"data": payload, "code": 200}

        return doc

    def delete_instance(
        self, model, *, raise_exception=True, return_result=False, many=False
    ):
        """删除实例"""

        if many and isinstance(self._id, list):
            query = Q("ids", **{"values": self._id})
            search = model.search().query(query)
            search.delete()
        elif isinstance(self._id, str) or isinstance(self._id, int):
            doc = model.get_document_by_id(
                document_id=self._id, raise_exception=raise_exception
            )
            doc.delete()

            if not return_result:
                return doc
        else:
            raise ParameterException(msg="无效的id类型")

        if return_result:
            return {"data": {"id": self._id}, "code": 204}

        return
