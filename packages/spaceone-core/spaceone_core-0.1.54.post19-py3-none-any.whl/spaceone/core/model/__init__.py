# -*- coding: utf-8 -*-

class BaseModel(object):

    @classmethod
    def connect(cls):
        """ 
        Args:
            None
        Returns:
            None
        """
        raise NotImplementedError('model.connect not implemented!')

    @classmethod
    def create(cls, data):
        """ 
        Args:
            data(dict)
        Returns:
            model_vo(object)
        """
        raise NotImplementedError('model.create not implemented!')

    def update(self, data):
        """ 
        Args:
            data(dict)
        Returns:
            model_vo(object)
        """
        raise NotImplementedError('model.update not implemented!')

    def delete(self):
        """
        Args:
            None
        Returns:
            None
        """
        raise NotImplementedError('model.delete not implemented!')

    def terminate(self):
        """ 
        Args:
            None
        Returns:
            None
        """
        raise NotImplementedError('model.terminate not implemented!')

    @classmethod
    def get(cls, **conditions):
        """ 
        Args:
            conditions(kwargs)
            - key(str) : value(any)
        Returns:
            model_vo(object)
        """
        raise NotImplementedError('model.get not implemented!')

    @classmethod
    def filter(cls, **conditions):
        """ 
        Args:
            conditions(kwargs)
            - key(str) : value(any)
        Returns:
            model_vos(list)
        """
        raise NotImplementedError('model.filter not implemented!')

    def to_dict(self):
        """ 
        Args:
            None
        Returns:
            model_data(dict)
        """
        raise NotImplementedError('model.to_dict not implemented!')

    @classmethod
    def query(cls, **query):
        """
        Args:
            query(kwargs)
                - filter(list)
                [
                    {
                        'key' : 'field(str)', 
                        'value' : 'value(any or list)',
                        'operator' : 'lt | lte | gt | gte | eq | not | exists |
                        contain | not_contain | in | not_in | not_contain_in | match | regex | regex_in'
                    },
                    ...
                ]
                - filter_or(list)
                [
                    {
                        'key' : 'field(str)', 
                        'value' : 'value(any or list)',
                        'operator' : 'lt | lte | gt | gte | eq | not | exists |
                        contain | not_contain | in | not_in | not_contain_in | match | regex | regex_in'
                    },
                    ...
                ]
                - sort(dict)
                {
                  'key' : 'field(str)',
                  'desc' : True | False
                }
                - page(dict)
                {
                    'start': (int),
                    'limit' : (int)
                }
                - distinct(str): 'field'
                - only(list): ['field1', 'field2', '...']
                - exclude(list): ['field1', 'field2', '...']
                - minimal(bool)
                - count_only(bool)

        Returns:
            model_vos(list)
            total_count(int)
        """
        raise NotImplementedError('model.query not implemented!')
