# -*- coding: utf-8 -*-


import numpy as np

from openfisca_core.model_api import *
from openfisca_survey_manager.statshelpers import mark_weighted_percentiles


from ppdland.entities import *


class salary(Variable):
    value_type = float
    entity = Individu
    label = "Salary"
    definition_period = YEAR


class potential_salary(Variable):
    value_type = float
    entity = Individu
    label = "Potential salary"
    definition_period = YEAR


class pension(Variable):
    value_type = float
    entity = Individu
    label = "Pension"
    definition_period = YEAR


class income_tax(Variable):
    value_type = float
    entity = Individu
    label = "Income tax"
    definition_period = YEAR

    def formula(individu, period, parameters):
        salary = individu('salary', period)
        pension = individu('pension', period)
        return compute_income_tax(salary, pension, period, parameters)


# class minimum_income(Variable):
#     value_type = float
#     entity = Individu
#     definition_period = YEAR

#     def formula(individu, period, parameters):
#         salary = individu('salary', period)
#         pension = individu('pension', period)
#         minimum_income = parameters(period).minimum_income
#         return max_((minimum_income - salary - pension), 0)


class disposable_income(Variable):
    definition_period = YEAR
    label = "Disposable income"
    entity = Individu
    value_type = float

    def formula(individu, period):
        salary = individu('salary', period)
        pension = individu('pension', period)
        income_tax = individu('income_tax', period)
        return salary + pension - income_tax


class decile(Variable):
    value_type = int
    entity = Individu
    label = "Disposable income decile"
    definition_period = YEAR

    def formula(individu, period):
        disposable_income = individu('disposable_income', period)
        labels = np.arange(1, 11)
        weights = 1.0 * np.ones(shape = len(disposable_income))
        decile, _ = mark_weighted_percentiles(
            disposable_income,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile


def compute_income_tax(salary, pension, period, parameters):
    salary_tax_base_deduction = min_(0.1 * salary, 100)  # 10% tax_base_deduction limitded to 100
    taxable_salary = salary - salary_tax_base_deduction
    pension_tax_base_deduction = min_(pension * 0.1, 200) * (pension > 0)  # 10% tax_base_deduction to 200
    taxable_pension = pension - pension_tax_base_deduction
    taxable_income = max_(0, taxable_salary + taxable_pension)
    tax_scale = parameters(period).tax_scale
    return tax_scale.calc(taxable_income)
