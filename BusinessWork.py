#!/usr/bin/env python
# encoding: utf-8
"""
@author: 孙超
@license: (C) Copyright 2019-2022, 华泰证券.
@contact: chaochaono1@outlook.com
@file: BusinessWork.py
@time: 2019/5/7 11:13
@desc:
"""
import pdb

QU0TA_NORMAL = -1  # 财务报表指标正常
QUOTA_ATTENTION = 0  # 财务报表指标关注
QUOTA_ATTENTION_SERIOUS = 1  # 财务报表指标重点关注

"""
传参集合
"""
interest_income = 9000  # 利息收入
average_monetary_funds_four_seasons = 1100000  # 前四个季度内平均货币资金
average_monetary_capital_funds_four_seasons = 5000000  # 前四个季度内平均总资产
interest_bearing_liabilities = 500000  # 有息债务
capital_funds = 5000000  # 总资产

qlevel_interest_income_monetary_funds_rate = 0.009  # 利息收入/前四个季度内平均货币基金上限
qlevel_interest_bearing_liabilities_capital_funds_rate = 0.25  # 有息债务/总资产下限


class QuotaBase(object):
    """
    指标基类
    """

    def __init__(self, name: str = None):
        self.name = name
        pass

    def premise(self) -> bool:
        return False

    def compare(self) -> list:
        pass


class QuotaMonetaryFunds(QuotaBase):
    """
    科目：货币资金
    """

    def __init__(
        self,
        name: str = None,
        quota_interest_income: float = 1,
        quota_capital_funds=500000,
        quota_average_monetary_funds_four_seasons: float = 1,
        quota_average_monetary_capital_funds_four_seasons: float = 1,
        quota_interest_bearing_liabilities: float = 1,
        quota_level_interest_income_monetary_funds_rate: float = 0.009,
        quota_level_interest_bearing_liabilities_capital_funds_rate: float = 0.25,
        quota_industry_code: str = "",
        quota_code_exception_industries: list = [],
    ):
        """

        :param name:
        :param quota_interest_income: 利息收入
        :param quota_capital_funds: 总资产
        :param quota_average_monetary_funds_four_seasons: 前四个季度内平均货币资金
        :param quota_average_monetary_capital_funds_four_seasons:  前四个季度内平均总资产
        :param quota_interest_bearing_liabilities: 有息债务
        :param quota_level_interest_income_monetary_funds_rate:  利息收入/前四个季度内平均货币基金上限
        :param quota_level_interest_bearing_liabilities_capital_funds_rate: 有息债务/总资产下限
        :param quota_industry_code: 行业代码入参
        :param quota_code_exception_industries: 排除的行业代码
        """
        self.name = name
        self.capital_funds = quota_capital_funds  # 总资产
        self.interest_income = quota_interest_income  # 利息收入
        self.average_monetary_funds_four_seasons = (
            quota_average_monetary_funds_four_seasons
        )  # 前四个季度内平均货币资金
        self.average_monetary_capital_funds_four_seasons = (
            quota_average_monetary_capital_funds_four_seasons
        )  # 前四个季度内平均总资产
        self.interest_bearing_liabilities = quota_interest_bearing_liabilities  # 有息债务
        self.level_interest_income_monetary_funds_rate = (
            quota_level_interest_income_monetary_funds_rate
        )  # 利息收入/前四个季度内平均货币资金
        self.level_interest_bearing_liabilities_capital_funds_rate = (
            quota_level_interest_bearing_liabilities_capital_funds_rate
        )  # 有息债务/总资产
        self.industry_code = quota_industry_code
        self.code_exception_industry = quota_code_exception_industries

    @property
    def __interest_monetary_funds_rate(self) -> float:
        """
        :return:  利息收入/前四个季度内平均货币资金
        """
        if self.average_monetary_funds_four_seasons == 0:
            raise ZeroDivisionError
        return self.interest_income / self.average_monetary_funds_four_seasons

    @property
    def __interest_bearing_liabilities_capital_funds_rate(self) -> float:
        """
        :return: 有息债务/总资产
        """
        if self.capital_funds == 0:
            raise ZeroDivisionError
        return self.interest_bearing_liabilities / self.capital_funds

    @property
    def __average_monetary_funds_capital_rate(self) -> float:
        """
            前四个季度平均货币资金/前四个季度内平均总货币资产
        :return:
        """
        if self.average_monetary_capital_funds_four_seasons == 0:
            raise ZeroDivisionError
        return (
            self.average_monetary_funds_four_seasons
            / self.average_monetary_capital_funds_four_seasons
        )

    @property
    def __average_monetary_funds_liabilities_rate(self) -> float:
        """
         前四个季度平均货币资金/有息债务
        :return:
        """
        if self.interest_bearing_liabilities == 0:
            raise ZeroDivisionError
        return (
            self.average_monetary_capital_funds_four_seasons
            / self.interest_bearing_liabilities
        )

    def premise(self) -> bool:
        """
        前提判断
        利息收入/前四个季度内平均货币资金 < 0.9%
        :return: True: 前提成立 False：前提不成立
        """
        if (
            self.__interest_monetary_funds_rate
            < self.level_interest_income_monetary_funds_rate
        ):
            return True
        else:
            return False

    def premise_interest_bearing_liabilities_rate(self) -> bool:
        """
        前提判断
        有息债务/总资产是否 >= 下限
        :return: True: 前提成立 False：前提不成立
        """
        if (
            self.__interest_bearing_liabilities_capital_funds_rate
            >= self.level_interest_bearing_liabilities_capital_funds_rate
        ):
            return True
        else:
            return False

    def compare(self) -> list:
        """
        货币资金比对逻辑
        :return:
        """
        result = []
        if self.__interest_monetary_funds_rate:
            dict_premise1 = {"quota": "货币资金1", "attention": QU0TA_NORMAL}
            if (
                self.industry_code not in self.code_exception_industry
                and not self.premise_interest_bearing_liabilities_rate()
            ):
                if 0.2 <= self.__average_monetary_funds_capital_rate < 0.3:
                    dict_premise1["attention"] = QUOTA_ATTENTION
                elif self.__average_monetary_funds_capital_rate >= 0.3:
                    dict_premise1["attention"] = QUOTA_ATTENTION_SERIOUS
            result.append(dict_premise1)

            dict_premise2 = {"quota": "货币资金2", "attention": QU0TA_NORMAL}
            if self.premise_interest_bearing_liabilities_rate():
                if 0.5 <= self.__average_monetary_funds_liabilities_rate < 0.7:
                    dict_premise2["attention"] = QUOTA_ATTENTION
                elif self.__average_monetary_funds_liabilities_rate >= 0.7:
                    dict_premise2["attention"] = QUOTA_ATTENTION_SERIOUS
            result.append(dict_premise2)
        return result


class QuotaOtherReceivables(QuotaBase):
    """
    科目：其他应收款项
    """

    def __init__(
        self,
        other_receivables: float = 1,
        other_payables: float = 1,
        industry_code: str = "",
        capital_fund=5000,
        code_exception_industry: list = [],
    ):
        self.other_receivables = abs(other_receivables)
        self.other_payables = abs(other_payables)
        self.capital_funds = capital_fund
        self.industry_code = industry_code
        self.code_exception_industry = code_exception_industry

    def premise(self) -> bool:
        """
        前提
        :return:
        """
        return True if (self.other_receivables - self.other_payables) >= 0 else False

    @property
    def __receivables_capital_rate(self) -> float:
        """
        其他应收款/总资产
        :return:
        """
        if self.capital_funds == 0:
            raise ZeroDivisionError
        return self.other_receivables / self.capital_funds

    def compare(self) -> list:
        """
        科目 其他应收款 判定逻辑
        :return:
        """
        result = []
        dict_payables = {"quota": "其他应收款", "attention": QU0TA_NORMAL}
        if self.premise() and self.industry_code not in self.code_exception_industry:
            if 0.15 <= self.__receivables_capital_rate < 0.25:
                dict_payables["attention"] = QUOTA_ATTENTION
            elif self.__receivables_capital_rate >= 0.25:
                dict_payables["attention"] = QUOTA_ATTENTION_SERIOUS
        result.append(dict_payables)
        return result


class QuotaBusinessReputation(QuotaBase):
    """
    科目：商誉
    """

    def __init__(
        self,
        reputation: float = 100.0,
        capital_fund: float = 1000,
        industry_code="",
        code_exception_industry=[],
    ):
        """

        :param reputation: 商誉
        :param capital_fund: 总资产
        """
        self.reputation = reputation
        self.capital_fund = capital_fund
        self.industry_code = industry_code
        self.code_exception_industry = code_exception_industry

    def premise(self) -> bool:
        return True

    def compare(self) -> list:
        result = []
        dict_reputation = {"quota": "商誉", "attention": QU0TA_NORMAL}
        if self.capital_fund == 0:
            raise ZeroDivisionError
        if 0.15 < self.reputation / self.capital_fund < 0.2:
            dict_reputation["attention"] = QUOTA_ATTENTION
        elif self.reputation / self.capital_fund >= 0.2:
            dict_reputation["attention"] = QUOTA_ATTENTION_SERIOUS
        result.append(dict_reputation)
        return result


class QuotaImmaterialAssets(QuotaBase):
    def __init__(
        self,
        immaterial_assets: float = 100.0,
        capital_fund: float = 1000,
        industry_code="",
        code_exception_industry=[],
    ):
        """

        :param immaterial_assets: 无形资产
        :param capital_fund:  总资产
        :param industry_code: 行业代码
        :param code_exception_industry: 不适用的行业代码数组
        """
        self.immaterial_assets = immaterial_assets
        self.capital_fund = capital_fund
        self.industry_code = industry_code
        self.code_exception_industry = code_exception_industry

    @property
    def __immaterial_asset_rate(self) -> float:
        if self.capital_fund == 0:
            raise ZeroDivisionError
        return self.immaterial_assets / self.capital_fund

    def premise(self) -> bool:
        return True

    def compare(self) -> list:
        result = []
        dict_material = {"quota": "无形资产", "attention": QU0TA_NORMAL}
        if 0.15 <= self.__immaterial_asset_rate < 0.2:
            dict_material["attention"] = QUOTA_ATTENTION
        elif self.__immaterial_asset_rate >= 0.2:
            dict_material["attention"] = QUOTA_ATTENTION_SERIOUS
        result.append(dict_material)
        return result


class QuotaConstructionInProgress(QuotaBase):
    """
    科目： 在建工程
    """

    def __init__(
        self,
        constructions: float = 100,
        capital_fund: float = 1000,
        industry_code: str = "",
        code_exception_industry: list = [],
    ):
        """

        :param constructions: 在建工程
        :param capital_fund: 总资产
        :param industry_code:  行业代码
        :param code_exception_industry:
        """
        self.constructions = constructions
        self.capital_fund = capital_fund
        self.industry_code = industry_code
        self.code_exception_industry = code_exception_industry

    def premise(self) -> bool:
        return True

    @property
    def __construction_rate(self) -> float:
        if self.capital_fund == 0:
            raise ZeroDivisionError
        return self.constructions / self.capital_fund

    def compare(self) -> list:
        """
        对比逻辑
        :return:
        """
        result = []
        dict_material = {"quota": "在建工程", "attention": QU0TA_NORMAL}
        if 0.2 <= self.__construction_rate < 0.3:
            dict_material["attention"] = QUOTA_ATTENTION
        elif self.__construction_rate >= 0.3:
            dict_material["attention"] = QUOTA_ATTENTION_SERIOUS
        result.append(dict_material)
        return result


# class QuotaGrossProfitRate(QuotaBase):
#     def __init__(self,
#         gross_profit_rate: float=0.1,
#         industory
#         industry_code:str="",
#         code_exception_industry:list=[]):
#         self.gross_profit_rate = gross_profit_rate


def main():
    # 其他应收款项
    receivable = QuotaOtherReceivables(
        other_receivables=10000, other_payables=8000, capital_fund=20000
    )
    print(receivable.compare())
    # 商誉
    reputation = QuotaBusinessReputation(reputation=1000, capital_fund=2000)
    print(reputation.compare())
    # 无形资产
    immaterial = QuotaImmaterialAssets(immaterial_assets=1000, capital_fund=2000)
    print(immaterial.compare())

    # 在建工程
    construction = QuotaConstructionInProgress(constructions=2000, capital_fund=3000)
    print(construction.compare())

    # 货币资金
    monetary_funds = QuotaMonetaryFunds(
        quota_interest_income=1000,
        quota_capital_funds=50000,
        quota_average_monetary_funds_four_seasons=30000,
        quota_average_monetary_capital_funds_four_seasons=40000,
        quota_interest_bearing_liabilities=20000,
    )
    print(monetary_funds.compare())


if __name__ == "__main__":
    main()
