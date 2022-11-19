import streamlit as st
import pandas as pd
import numpy as np
# import plotly_express as px
from PIL import Image
import altair as alt

df = pd.read_csv(r"InteractiveVizApp/Value_Menu_Data_Trans.csv")

colors = {"Arby's": '#d71921', "Burger King": '#185494', "Subway": '#23645d', 
          "McDonalds": '#ffc300', "Taco Bell": '#ec008c', "Wendy's": '#12acec'}


st.set_page_config(page_title='Value Menu Analysis', layout='wide')

with st.container():
	st.title('Stretching Your Dollar & Your Waistband')
	st.subheader('Does the “value” of a value menu change when we decide that we value different things?')

	main_image = Image.open(r"Images\Main_Image.jpg")
	st.image(main_image, caption='Common Sentiment Felt Before the Direct Deposit Hits')

with st.container():
	st.markdown('''While we would all love to be able to dine at the most 
		exquisite restaurants or make every single meal for ourselves every day, 
		sometimes its just not possible-whether it be due to time or budget 
		constraints, we just have to compromise sometimes. Enter the value 
		proposition of fast food franchises: they’re relatively fast, and 
		can be loosely considered to be food (I’m looking at you Burger King 
		and your [“Mac n’ Cheetos"](https://en.wikipedia.org/wiki/Mac_n%27_Cheetos). 
		\n\nWhether I like it or not, I’m the target demographic for fast food 
		companies: I’m also a broke grad student, I very often get hungry 
		at wildly inappropriate times, and I’m a fiend for fast food. 
		Many times, I’ve sat at my desk working only to realize it’s now 
		10PM and I haven’t eaten anything since 11am (What? Is that just me?). 
		Naturally, I think to myself how I can fulfill those cravings but not 
		break the bank. In some instances, this results in me making my way 
		over to the nearest Taco Bell and getting myself a Baja Blast 
		(pronounced *Baah-Jaah*) and a Chalupa (pronounced *Kuh-loop-ah*). 
		But sometimes, I don’t want to spend $7 on just 2 items: enter the 
		coveted value menu. The value menu is meant to be a franchise’s 
		attempt at “…following the value proposition of providing steady 
		quality with decent value pricing that is served quickly and 
		consistently...” , and is, in many cases, made up of the cheapest 
		items on a menu. It is meant to exist as a reduced cost, calorie dense, 
		terrible-for-you-but-so-good food option for those in need of sustenance.
		 After all, it’s called the value menu because it presents some offering
		 of value to the consumer.

\n \nThat’s the narrative from fast food franchises. **The value of the value menu 
is that you get food that you want/need at a cheap price**. 
##### However, is that truly how we define value? Does the **“value”** of a value menu change when we decide that we **value different things**?''')

with st.container():
	st.subheader('Background')

	st.markdown('''I decided to take a subset of some of the most popular fast food 
		franchises shared: Arby’s, Burger King, Subway, McDonalds, Taco Bell, and Wendy’s. 
		We will be using the corresponding box colors to indicate specific franchises moving forward.''') 

	franchises_image = Image.open(r"InteractiveVizApp/Images/Legend.png")
	st.image(franchises_image, caption='The franchises of interest in this analysis.')

	st.markdown('''As such, these will be the 6 main franchises that we focus on in design of our 
		analysis. Overall, 4 chains represent the same domain of food 
		(American burgers and sandwiches): Arby’s, Burger King, McDonalds, and Wendy’s. 
		The argument can be made that Subway (healthy and nutritious) and Taco Bell 
		(if you have a good way of describing Taco Bell’s style, please tell me) 
		represent different market segments that the previous 4. So while I do 
		anticipate there to be some level of overlap across the quantified values 
		across different chains, I hypothesized that there will still be enough 
		meaningful variation to generate impactful insights in this hard-hitting 
		question. 
		For each franchise, I randomly selected 8 items that exist on their value menu 
		and captured their associated franchise, price, item name, cost (in dollars),
		 serving weight (in grams), total calories, calories from fat, total fat content
		  (in grams), saturated fat content (in grams), trans-fats content (in grams), 
		  cholesterol (in mg), sodium (in grams), carbohydrate content (in grams), 
		  fiber content (in grams), sugar content (in grams), and protein content 
		  (in grams). For the purposes of this analysis, I made a few key decisions:

**1.**	I excluded soft drinks or beverages as an eligible menu item since those are the same across different restaurants (except you Baja blast, you’re different). 

**2.**	I priced each item based on how much it cost in the greater Ann Arbor area in October 2022. I found pretty noticeable pricing differences based on geographies, like things typically costing 1.5x more in California. See the below figure for evidence based on the price of a big-mac.''')

	big_mac_image = Image.open(r"InteractiveVizApp/Images/how-much-big-mac-costs.png")
	st.image(big_mac_image, caption='Price of a big-mac across the country. Accessed from Zippia."How Much A Big Mac Costs In Every State" Zippia.com. Sep. 5, 2022')

	st.markdown('''**3.**	I assumed that the serving weight parsed from each nutritional 
		information site constituted the weight of the item received when you actually 
		order, i.e., you’re not getting 2 servings of a big-mac when you go to McDonalds.
		\n\n I didn’t have any pre-configured datasets for this analysis, so I got all data through web-scraping menu options and nutritional information from each of the franchise’s webpage.''')

with st.container():
	st.subheader('Analysis')

	st.markdown('''The first question that I sought to answer is central to the 
		overall motivations of this paper: what are the different ways that we can 
		define value?  Naturally, I initially defined value very simply: *how much of it do I get?* 
		With respect to fast food items, I thought about *how much do I get* in 
		2 different ways: 
*	How much do I get **in terms of weight** for a given item
*	How much do I get **in terms of calories** for a given item
 ''')

	st.markdown('''I believed these to be a good baseline for understanding value, as they're typically
	what consumers associated with value, and they represent the directives behind corporate strategy on
	developing value menus. **Note:** For `weight` of an item, it's measured in grams. We went ahead and also applied normalization techniques to both the weight and calories values
	for each fast food item. This was done to reduce the impact of outliers, but still retain relative distances between values. **The scatter plots of the weight and calories vs. cost can be seen below:** ''')

	add_selectbox = st.multiselect(
    'Select Franchise(s) to display',
    ("Arby's", 'Burger King', 'Subway', 'McDonalds', 'Taco Bell', "Wendy's"))

    # st.markdown(add_selectbox)

	brush = alt.selection(type='interval', resolve='global')

	if len(add_selectbox) == 0:
		dfs = df
	else:
		dfs = df[df['Franchise'].isin(add_selectbox)]

	base = alt.Chart(dfs).mark_point(filled=True).encode(
	    y=alt.Y('Cost_Dollars', title='Cost ($)'),
	    color=alt.condition(brush, 'Franchise:N', alt.value('lightgray'), scale=alt.Scale(domain=list(colors.keys()),
	            range=list(colors.values())))
	).add_selection(
	    brush
	).properties(
	    width=550,
	    height=550
	)

	(base.encode(x=alt.X('Calories_Normalized_Min_Max', title='Normalized Calories'), tooltip=['Menu_Item', 'Calories_Normalized_Min_Max', 'Cost_Dollars']).add_selection(alt.selection_single()) | base.encode(x=alt.X('Serving_Weight_G_Normalized_Min_Max', title='Normalized Serving Weight (grams)'), tooltip=['Menu_Item', 'Serving_Weight_G_Normalized_Min_Max', 'Cost_Dollars']).add_selection(alt.selection_single()) )

	st.markdown('''From here, we see that it is difficult to identify any particular trends in the franchise's scoring. This means that we should add in additional features in our visualizations
	to try to determine value on. ''')

with st.container():

		st.markdown('''The first thing that I did was attempt to develop a standard of evaluating how well a given fast food item does in 
			adherence to the macronutrient content described in the CDC guidelines. To do this, I found the ratio of each macronutrient for 
			each menu item, and then found the cartesian distance between each menu item’s ratios and the prescribed ratios of 0.5 : 0.35 : 0.15. Doing so gives us the following 
			distribution:''')

		base_3 = alt.Chart(df).mark_bar(stroke='black').encode(
	    alt.X("Distance_From_Macros:Q", bin=True, title='Macronutrient Adherence Score'),
	    alt.Y('count()'),
	    color=alt.Color('Franchise:N', scale=alt.Scale(domain=list(colors.keys()),
	            range=list(colors.values())))).properties(
	    width=550,
	    height=550)
		base_3

		st.markdown('''Again, these values were determined by finding the euclidian distance between a vector representation of the menu item's macronutrient ratios and the vector representation
		of the ratios specified by the CDC. While this was a relatively good first step proxy for determining how good a food item was at hitting macronutrient targets, I wanted to see if I could do better. 
		Borrowing from the ‘DD’ index, I sought to develop my own indexing methodology. To do this, I instead sought to find the absolute residuals between the recommended daily 
		macronutrient intakes for men and women aged 19-50 and the macronutrient data for each menu item. The CDC states that it is recommended that a person consumes roughly 75g of 
		protein, 300g of carbs, and 60g of fats a day to it their macronutrient goals, with only about 27g of fats allowed from saturated fats. To develop our new methodology, we will 
		divide each daily recommended intake by 3 (to represent 3 meals a day) and multiply by the weight corresponding to the prescribed ratio.''')
		st.markdown('''**This is a bit confusing, so lets break it down.** Carbs will be the indexing weight, meaning it gets a weight of 1/0.5 = `2`, proteins the next important with a weight of 1/0.35 = `2.85`, and finally fats with a weight of 1/0.15 `6.66`.
			We can then plot these visualizations to understand how they change the distribution of menu items when scored on this proxy for health.''')


		add_selectbox_3 = st.multiselect(
		'Select Franchise(s) to display',
		("Arby's", 'Burger King', 'Subway', 'McDonalds', 'Taco Bell', "Wendy's"), key=3)

		# st.markdown(add_selectbox)

		brush_3 = alt.selection(type='interval', resolve='global')

		if len(add_selectbox_3) == 0:
			dfs = df
		else:
			dfs = df[df['Franchise'].isin(add_selectbox_3)]

		base_3 = alt.Chart(dfs).mark_point(filled=True).encode(
		    y=alt.Y('Cost_Dollars', title='Cost ($)'),
		    color=alt.condition(brush_3, 'Franchise:N', alt.value('lightgray'), scale=alt.Scale(domain=list(colors.keys()),
		            range=list(colors.values())))
		).add_selection(
		    brush_3
		).properties(
		    width=550,
		    height=550
		)

		(base_3.encode(x=alt.X('Distance_From_Macros', title='Macronutrient Adherence Score'), tooltip=['Menu_Item', 'Distance_From_Macros', 'Cost_Dollars']).add_selection(alt.selection_single()) 
		| base_3.encode(x=alt.X('Distance_From_Macros_Revised_Normalized_Min_Max', title='Macronutrient Adherence Score Revised & Normalized'), tooltip=['Menu_Item', 'Distance_From_Macros_Revised_Normalized_Min_Max', 'Cost_Dollars']).add_selection(alt.selection_single()) )


		st.markdown(''' And now from here we see that…nothing is immediately visible. While this might be initially disheartening, it brings up a valuable point. 
			I can find value in every single franchise depending on what I value in that moment in time. In actuality, value doesn’t exist in a single variable – 
			it is multifaceted and ultimately a linear combination of all of these factors described above. As such, I came to a final stage for the learning 
			objective of how the user will be able to select how to define value. I created an aggregated score that is a linear combination of each menu items 
			MinMax normalized serving weight, number of calories, and revised metric for distance to macronutrient goals. The user will, eventually, be able to 
			define their own weights for these dimensions and aggregate accordingly. Therefore, the user will be able to define value how they see fit in that moment
			and time. For me personally, I defined value as 50% distance to macro goals, 35% calories, and 15% portion size.''')
		st.subheader('Please update the values below to show how your aggregate score would change')
		
		calories_target = st.text_input('Percent Target Calories', '0.35')
		weight_target = st.text_input('Percent Target Weight ', '0.15')
		macro_target = st.text_input('Percent Target Macronutrient Content', '0.5')

		df['Agg_Score_2'] = df.apply(lambda x: (float(calories_target)*x['Calories_Normalized_Min_Max']) + (float(weight_target)*x['Serving_Weight_G_Normalized_Min_Max']) + (float(macro_target)*x['Distance_From_Macros_Revised_Normalized_Min_Max_Modified']), axis=1)

		add_selectbox_2 = st.multiselect(
	    'Select Franchise(s) to display',
	    ("Arby's", 'Burger King', 'Subway', 'McDonalds', 'Taco Bell', "Wendy's"), key=2)

		brush_2 = alt.selection(type='interval', resolve='global')

		if len(add_selectbox_2) == 0:
			dfs = df
		else:
			dfs = df[df['Franchise'].isin(add_selectbox_2)]

		base_2 = alt.Chart(dfs).mark_point(filled=True).encode(
		    y=alt.Y('Cost_Dollars', title='Cost ($)'),
		    color=alt.condition(brush_2, 'Franchise:N', alt.value('lightgray'), scale=alt.Scale(domain=list(colors.keys()),
		            range=list(colors.values()))),
		    tooltip=['Menu_Item', 'Agg_Score', 'Cost_Dollars']
		).add_selection(
		    brush_2
		).properties(
		    width=550,
		    height=550
		).add_selection(alt.selection_single())


		hist = alt.Chart(dfs).mark_bar().encode(
		    x='count()',
		    y='Franchise',
		    color=alt.Color('Franchise:N', scale=alt.Scale(domain=list(colors.keys()),
            range=list(colors.values())))
		).transform_filter(
		    brush_2
		).properties(
		    width=1100,
		)

		if float(calories_target) + float(weight_target) + float(macro_target) != 1.0:

			st.error('Error: Values do not add up to 1.0', icon=None)
			(base_2.encode(x=alt.X('Agg_Score', title='Aggregate Score'), tooltip=['Menu_Item', 'Agg_Score', 'Cost_Dollars']).add_selection(alt.selection_single()))

		elif float(calories_target) + float(weight_target) + float(macro_target) == 1.0:
			((base_2.encode(x=alt.X('Agg_Score', title='Aggregate Score'), tooltip=['Menu_Item', 'Agg_Score', 'Cost_Dollars']).add_selection(alt.selection_single()) 
			| base_2.encode(x=alt.X('Agg_Score_2', title='Aggregate Score Updated'), tooltip=['Menu_Item', 'Agg_Score_2', 'Cost_Dollars']).add_selection(alt.selection_single())) & hist)
		# 	| base_2.encode(x=alt.X('Agg_Score', title='Aggregate Score'), tooltip=['Menu_Item', 'Agg_Score', 'Cost_Dollars']).add_selection(alt.selection_single()))

		st.markdown('''From here, the aggregation of how a particular franchise will do for the things I value leads to some pretty clear clustering. For example, 
			I see that Subway will be on the more expensive side, but will generally give me middling performance on my evaluation of value. Unsurprisingly, 
			Taco Bell would be my clear choice here. It has decently high aggregated scores, while also being low-cost – exactly what I care about!''')
		# df_value_menu_data['Agg_Score'] = df_value_menu_data.apply(lambda x: (0.35*x['Calories_Normalized_Min_Max']) + (0.15*x['Serving_Weight_G_Normalized_Min_Max']) + (0.5*x['Distance_From_Macros_Revised_Normalized_Min_Max_Modified']), axis=1)

with st.container():

	boxplot = ((alt.Chart(df).mark_boxplot().encode(
	x=alt.X('Franchise:N', axis=alt.Axis(labelAngle=-45)),
	y='Trans_Fat_G:Q',
	color=alt.Color('Franchise:N', scale=alt.Scale(domain=list(colors.keys()),
	    range=list(colors.values())))
	).properties(width=550)

	+
	alt.Chart(df).mark_rule(color='red').encode(

	alt.Y('mean(Trans_Fat_G):Q', 
	  axis=alt.Axis(title = '')))
	)
	|

	(alt.Chart(df).mark_boxplot().encode(
	x=alt.X('Franchise:N', axis=alt.Axis(labelAngle=-45)),
	y='Chol_mG:Q',
	color=alt.Color('Franchise:N', scale=alt.Scale(domain=list(colors.keys()),
	    range=list(colors.values())))
	).properties(width=500)

	+
	alt.Chart(df).mark_rule(color='red').encode(
	alt.Y('mean(Trans_Fat_G):Q', 
	  axis=alt.Axis(title = '')))
	)).configure_axis(
	labelFontSize=15,
	titleFontSize=15
	)

	boxplot
