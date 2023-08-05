#!/usr/local/bin/python3
import pandas as pd
import re
from datetime import datetime
import pickle as pkl
from abc import abstractclassmethod

class Asset:
    def __init__(self):
        self.data = pd.DataFrame()

    @staticmethod
    def from_excel(filename, index_col=0):
        self = Asset()
        self.data = pd.read_excel(filename, index_col=index_col)
        return self

    @staticmethod
    def from_buffer(buffer):
        self = Asset()
        self.data = pkl.loads(buffer)
        return self

    def add_record(
        self,
        *,
        date_maturity,
        name_item,
        name_platform,
        name_account,
        yield_annual,
        amount,
        type_asset
    ):
        assert(type(date_maturity) is datetime)
        record_dict = {
            "date_maturity" : [date_maturity],
            "name_item" : [name_item],
            "name_platform" : [name_platform],
            "name_account" : [name_account],
            "yield_annual" : [yield_annual],
            "amount" : [amount],
            "type_asset" : [type_asset],
            "date_update" : [datetime.now()],
            "active" : True
        }
        record = pd.DataFrame(record_dict, index=[self.data.shape[0]])
        self.data = self.data.append(record)
        return self

    @property
    def view(self):
        ret = self.data.copy()
        ret.loc[ret.date_maturity.isnull(), "date_maturity"] = datetime.now()
        return ret

    def save_excel(self, filename, data=None):
        if data is None:
            data = self.data
        data.to_excel(filename)

    @abstractclassmethod
    def get_html(self):
        return None

# vim: ts=4 sw=4 sts=4 expandtab
