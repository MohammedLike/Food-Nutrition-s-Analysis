import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data(file_path):
    nutrients = pd.read_csv(file_path)
    return nutrients

def clean_data(nutrients):

    nutrients = nutrients.replace("t", 0)
    nutrients = nutrients.replace("t'", 0)
    nutrients = nutrients.replace(",", "", regex=True)
    nutrients['Protein'] = nutrients['Protein'].replace("-1", "", regex=True)
    nutrients['Fiber'] = nutrients['Fiber'].replace("a", "", regex=True)
    nutrients['Calories'][91] = (8 + 44) / 2


    nutrients['Grams'] = pd.to_numeric(nutrients['Grams'])
    nutrients['Calories'] = pd.to_numeric(nutrients['Calories'])
    nutrients['Protein'] = pd.to_numeric(nutrients['Protein'])
    nutrients['Fat'] = pd.to_numeric(nutrients['Fat'])
    nutrients['Sat.Fat'] = pd.to_numeric(nutrients['Sat.Fat'])
    nutrients['Fiber'] = pd.to_numeric(nutrients['Fiber'])
    nutrients['Carbs'] = pd.to_numeric(nutrients['Carbs'])


    nutrients = nutrients.dropna()


    categories_to_replace = {
        'DrinksAlcohol Beverages': 'Drinks, Alcohol, Beverages',
        'Fats Oils Shortenings': 'Fats, Oils, Shortenings',
        'Fish Seafood': 'Fish, Seafood',
        'Meat Poultry': 'Meat, Poultry',
        'Breads cereals fastfoodgrains': 'Grains',
        'Seeds and Nuts': 'Grains',
        'Desserts sweets': 'Desserts',
        'Jams Jellies': 'Desserts',
        'Fruits A-F': 'Fruits',
        'Fruits G-P': 'Fruits',
        'Fruits R-Z': 'Fruits',
        'Vegetables A-E': 'Vegetables',
        'Vegetables F-P': 'Vegetables',
        'Vegetables R-Z': 'Vegetables'
    }
    nutrients['Category'] = nutrients['Category'].replace(categories_to_replace, regex=True)


    nutrients['Calories'] /= nutrients['Grams']
    nutrients['Protein'] /= nutrients['Grams']
    nutrients['Fat'] /= nutrients['Grams']
    nutrients['Sat.Fat'] /= nutrients['Grams']
    nutrients['Fiber'] /= nutrients['Grams']
    nutrients['Carbs'] /= nutrients['Grams']

    return nutrients

def category_distribution(nutrients):
    numeric_columns = nutrients.select_dtypes(include=['number'])
    category_dist = numeric_columns.groupby(nutrients['Category']).mean()
    return category_dist

def create_category_pies(category_dist):
    fig = make_subplots(rows=2, cols=3, specs=[[{"type": "domain"}] * 3] * 2)

    for i, nutrient in enumerate(['Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs']):
        fig.add_trace(go.Pie(values=category_dist[nutrient].values, title=nutrient,
                             labels=category_dist.index,
                             marker=dict(colors=['#100b', '#f00560'],
                                         line=dict(color='#FFFFFF', width=2.5))),
                      row=i // 3 + 1, col=i % 3 + 1)

    fig.update_layout(title_text="Category Distribution of All Metrics", height=700, width=1000)
    return fig

def top_nutrient_foods(nutrients, nutrient, top_n=20):
    return nutrients.sort_values(by=nutrient, ascending=False).head(top_n)

def create_bar_chart(data, x_col, y_col, title):
    fig = px.bar(data, x=x_col, y=y_col, color=y_col, title=title, template='plotly_white')
    return fig

def relation_fat_saturated_fat(nutrients):
    fig = px.scatter(nutrients, x='Fat', y='Sat.Fat', trendline='lowess', color='Fat',
                     hover_name='Food', template='plotly_white',
                     title='Relation Between Saturated Fat and Fat')
    return fig
