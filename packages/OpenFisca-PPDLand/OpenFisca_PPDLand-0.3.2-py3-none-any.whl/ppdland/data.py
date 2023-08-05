# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd


def create_input_dataframe():
    """
    Create input dataframe with variable salary and pension
    """
    # Almost 15 millions people
    # Around 1.5 million household
    np.random.seed(216)
    number_of_households = 1.5e6
    household_weight = 50
    minimum_salary = 70
    size = int(number_of_households / household_weight)
    # print("Size of the sample: {}".format(size))
    # We choose a mean salary of 5e6 CFA with a log normal ditribution
    # We choose a mean pension of 2.5e6 CFA
    mean_salary = 3.5e3
    median_salary = .4 * mean_salary
    pension_salary_ratio = .9
    mean_pension = pension_salary_ratio * mean_salary
    median_pension = .9 * mean_pension
    is_retired = np.random.binomial(1, .2, size = size)
    # mean_salary = exp(mu + sigma ** 2 / 2)
    # median_salary = exp(mu)
    potential_wage_earner = np.logical_not(is_retired)
    mu = np.log(median_salary)
    sigma = np.sqrt(2 * np.log(mean_salary / median_salary))
    potential_salary = (
        potential_wage_earner
        * np.random.lognormal(mean = mu, sigma = sigma, size = int(size))
        )
    potential_salary = potential_wage_earner * np.maximum(minimum_salary, potential_salary)
    is_employed = potential_wage_earner * np.random.binomial(1, .9, size = size)
    salary = is_employed * potential_salary
    mu = np.log(median_pension)
    sigma = np.sqrt(2 * np.log(mean_pension / median_pension))
    pension = (
        is_retired
        * np.random.lognormal(mean = mu, sigma = sigma, size = int(size))
        )
    return pd.DataFrame({
        'pension': pension,
        'potential_salary': potential_salary,
        'salary': salary,
        })
