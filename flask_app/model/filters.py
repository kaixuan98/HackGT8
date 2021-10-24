import pandas as pd


def transformed_nutrition(data_frame):
    new_df = data_frame.copy()

    # make a new data frame with the nutrition values split up
    new_df['calories'], new_df['total fat (PDV)'], new_df['sugar (PDV)'], new_df['sodium (PDV)'], new_df[
        'protein (PDV)'], new_df['saturated fat (PDV)'], new_df['carbohydrates (PDV)'] = new_df['nutrition'].str.split(
        ',', 6).str

    del new_df['nutrition']  # delete old nutrition column since we split values into their own column
    del new_df['id']  # delete id column since we dont need them

    # clean up calories and carbs so it doesnt have the "[" in the rows
    # plus convert to float
    new_df['calories'] = new_df['calories'].str.replace(r'\D', '').astype(float)
    new_df['carbohydrates (PDV)'] = new_df['carbohydrates (PDV)'].str.replace(r'\D', '').astype(float)

    # change all the nutrition columns into floats instead of string
    # calories and carbs were converted earlier so thats why its not included now

    pd.to_numeric(new_df['total fat (PDV)'])
    pd.to_numeric(new_df['sugar (PDV)'])
    pd.to_numeric(new_df['sodium (PDV)'])
    pd.to_numeric(new_df['protein (PDV)'])
    pd.to_numeric(new_df['saturated fat (PDV)'])

    return new_df


# filters out from list if it contains allergen ingredient
def allergy(allergen, data_frame):
    no_allergen_df = data_frame.copy()

    df_copy = no_allergen_df[~no_allergen_df.ingredients.str.contains(allergen)]

    return df_copy


def nutrition_range(inequality, range_num, nutrition_name, data_frame):
    print(nutrition_name)
    new_df = data_frame.copy()
    if inequality == "less than or equal to":
        index_names = new_df[new_df[nutrition_name] > range_num].index
        new_df.drop(index_names, inplace=True)
    elif inequality == "more than or equal to":
        index_names = new_df[new_df[nutrition_name] < range_num].index
        new_df.drop(index_names, inplace=True)
    else:
        return new_df
    return new_df
