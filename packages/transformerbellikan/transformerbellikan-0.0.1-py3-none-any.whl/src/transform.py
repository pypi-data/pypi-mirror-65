import numpy as np
import pandas as pd


def convert_cat_col1(catcol):
    job = {
        'admin.': 'admin.',
        'blue-collar': 'blue-collar',
        'entrepreneur': 'entrepreneur',
        'housemaid': 'other',
        'management': 'management',
        'retired': 'retired',
        'self-employed': 'other',
        'services': 'services',
        'student': 'student',
        'technician': 'technician',
        'unemployed': 'other',
        'unknown': 'other'
    }

    marital = {
        'married': 'married',
        'single': 'single',
        'divorced': 'divorced',
        'unknown': 'single'
    }

    education = {
        'basic.4y': 'basic.4y',
        'high.school': 'high.school',
        'basic.6y': 'basic.6y',
        'basic.9y': 'basic.9y',
        'professional.course': 'professional.course',
        'other': 'other',
        'university.degree': 'university.degree',
        'unknown': 'other',
        'illiterate': 'other'
    }

    housing = {
        'no': 'no',
        'yes': 'yes',
        'unknown': 'no'
    }

    loan = {
        'no': 'no',
        'yes': 'yes',
        'unknown': 'no'
    }

    return (
        catcol
            .assign(job=lambda df: df['job'].replace(job),
                    marital=lambda df: df['marital'].replace(marital),
                    education=lambda df: df['education'].replace(education),
                    housing=lambda df: df['housing'].replace(housing),
                    loan=lambda df: df['loan'].replace(loan))
    )


def convert_cat_col2(catcol):
    y = {
        'yes': 1,
        'no': 0
    }

    contact = {
        'telephone': 1,
        'cellular': 0
    }

    housing = {
        'yes': 1,
        'no': 0
    }

    loan = {
        'yes': 1,
        'no': 0
    }

    return (
        catcol
            .assign(y=lambda df: df['y'].replace(y),
                    contact=lambda df: df['contact'].replace(contact),
                    housing=lambda df: df['housing'].replace(housing),
                    loan=lambda df: df['loan'].replace(loan))
    )


def convert_cat_col3(catcol):
    months = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }

    days = {
        'mon': 1,
        'tue': 2,
        'wed': 3,
        'thu': 4,
        'fri': 5,
        'sat': 6,
        'sun': 7
    }

    catcol1 = (
        catcol
            .assign(month1=lambda df: df['month'].replace(months),
                    day_of_week1=lambda df: df['day_of_week'].replace(days))
    )
    catcol1['day_of_week1'] = pd.to_numeric(catcol1['day_of_week1'])
    catcol1['day_of_week1' + '_sin'] = np.sin(2 * np.pi * catcol1['day_of_week1'] / 7)
    catcol1['month1' + '_cos'] = np.cos(2 * np.pi * catcol1['month1'] / 12)

    return catcol1


def log_transformation(numcol):
    return (
        numcol
            .assign(log_duration=lambda df: (df['duration'] + 1).transform(np.log))
            .assign(log_campaign=lambda df: (df['campaign'] + 1).transform(np.log))
    )


def transform(input_data):
    num_col = input_data.select_dtypes(include=['int', 'float'])
    cat_col = input_data.select_dtypes(include='object')

    # Preparation of categorical variables
    cat_col = convert_cat_col1(cat_col)
    cat_col = convert_cat_col2(cat_col)
    cat_col = convert_cat_col3(cat_col)

    # Preparation of numerical variables
    num_col = log_transformation(num_col)

    # Merge all variables into the final dataset
    return (
        pd.concat([num_col, cat_col], axis=1)
            .drop(
            ['default', 'month', 'day_of_week', 'duration', 'campaign', 'month1', 'day_of_week1'], axis=1)
    )

# if __name__ == '__main__':
#     data = (
#         pd.read_csv('bank-additional-full.csv', delimiter=";")
#             .rename(columns=str.lower)
#     )
#     data = transform(data)
#     return (data)
