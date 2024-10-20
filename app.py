import streamlit as st
from main import load_data, clean_data, category_distribution, create_category_pies, top_nutrient_foods, create_bar_chart, relation_fat_saturated_fat

st.title("Nutritional Analysis App")

nutrients = load_data("nutrients_csvfile.csv")
nutrients = clean_data(nutrients)

if st.checkbox("Show Raw Data"):
    st.subheader("Nutritional Data")
    st.write(nutrients)

selected_categories = st.multiselect(
    "Select Food Categories to Display",
    options=nutrients['Category'].unique(),
    default=nutrients['Category'].unique()[:3]
)

st.subheader("Category Distribution of Nutritional Metrics")
st.write(
    "The following pie charts illustrate the average distribution of key nutritional metrics across selected food categories. "
    "These metrics include Calories, Protein, Fat, Saturated Fat, Fiber, and Carbohydrates."
)
category_dist = category_distribution(nutrients[nutrients['Category'].isin(selected_categories)])
category_pies = create_category_pies(category_dist)
st.plotly_chart(category_pies)

selected_nutrient = st.selectbox(
    "Select Nutrient to View Top 20 Foods",
    options=['Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs']
)

st.subheader(f"Top 20 {selected_nutrient} Rich Foods")
st.write(
    f"The bar chart below displays the top 20 foods high in {selected_nutrient}. "
    f"These foods can be considered if you are looking to increase your intake of {selected_nutrient.lower()}."
)
top_foods = top_nutrient_foods(nutrients, selected_nutrient)
bar_chart = create_bar_chart(top_foods, 'Food', selected_nutrient, f'Top 20 {selected_nutrient} Rich Foods')
st.plotly_chart(bar_chart)

st.subheader("Explore Relationship Between Fat and Saturated Fat")
fat_range = st.slider(
    "Select Range of Total Fat",
    min_value=0.0,
    max_value=float(nutrients['Fat'].max()),
    value=(0.0, float(nutrients['Fat'].max()))
)

filtered_nutrients = nutrients[(nutrients['Fat'] >= fat_range[0]) & (nutrients['Fat'] <= fat_range[1])]
st.write(
    "The scatter plot below shows the relationship between total Fat and Saturated Fat in various foods "
    "within the selected fat range."
)
fat_relation = relation_fat_saturated_fat(filtered_nutrients)
st.plotly_chart(fat_relation)
