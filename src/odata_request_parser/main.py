class OdataSelectParser:
    fields = []

    def add_fields(self, select_fields: list[str]):
        self.fields.extend(select_fields)
        return self

    def parse(self) -> str:
        return ','.join(self.fields)


class OdataFilterParser:
    def parse(self, filter: list, comparator: str = ' and ') -> str:
        parsed_filter_items = []
        for filter_item in filter:
            item, value = self._eval_filter_item(filter_item)
            parsed_filter_items.append(
                self.parse_filter_item(item=item, value=value)
            )
        return comparator.join(parsed_filter_items)

    def parse_filter_item(self, item: str, value: [dict, list]):
        try:
            func = getattr(self, item)
        except:
            raise NotImplementedError(f"The filter operator {item} is not implemented")
        return func(value)

    def _or(self, or_filter: list):
        assert isinstance(or_filter, list)
        return self.parse(or_filter, comparator=' or ')

    def _has(self, filter_value: dict):
        return self._operator(filter_value, operator_str='has')

    def _eq(self, filter_value: dict):
        return self._operator(filter_value, operator_str='eq')

    def _lt(self, filter_value: dict):
        return self._operator(filter_value, operator_str='lt')

    def _le(self, filter_value: dict):
        return self._operator(filter_value, operator_str='le')

    def _gt(self, filter_value: dict):
        return self._operator(filter_value, operator_str='gt')

    def _ge(self, filter_value: dict):
        return self._operator(filter_value, operator_str='ge')

    def _operator(self, filter_item, operator_str: str):
        item, value = self._eval_filter_item(filter_item)
        return f"{item} {operator_str} {value}"

    def _eval_filter_item(self, filter_value):
        assert isinstance(filter_value, dict)
        assert len(filter_value) == 1
        return next(iter(filter_value.items()))
