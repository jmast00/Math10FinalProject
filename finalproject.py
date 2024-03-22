#Final Projecton Streamlit
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import sklearn
from sklearn.linear_model import LinearRegression


st.title('Exploring Top Charts 2010-2019')

st.header('Exploring Data')

st.subheader('Choose an artist to see their top songs')

df = pd.read_csv('top10s.csv',encoding='latin1')  #added encoding argument because certain characters were not being recognized
df['year_datetime'] = pd.to_datetime(df['year'], format='%Y')
    #https://stackoverflow.com/questions/46658232/pandas-convert-column-with-year-integer-to-datetime

    #creaeting a tuple of artists to use in my selectbox
listartists = [x for x in df['artist']]
setartists = set(listartists)
tupleartists = tuple(setartists)

    #defining a function that counts how many times the artist's name appears
    #I want to be able to display which songs each artist has as well
def count(artist):
    return sum(df['artist']==artist)


artist_selection = st.selectbox(
    'Choose an Artist:',
             tupleartists)
    
artistname = np.column_stack([df['artist'].str.contains(f'{artist_selection}', na=False)]) 
df_artistname = df.loc[artistname.any(axis=1)]
artist_array = df_artistname[['title','year']]      
    #https://stackoverflow.com/questions/58351458/how-to-extract-entire-rows-from-pandas-data-frame-if-a-columns-string-value-co

st.write(
    f'{artist_selection} has {count(artist_selection)} songs in top charts'
    )
st.write('Here are their top songs:')
st.table(artist_array.assign(hack='').set_index('hack'))
    #https://github.com/streamlit/streamlit/issues/641

st.header('Now We Graph Our Data')

df_numeric = pd.DataFrame(df.iloc[:,-12:-1])
y_axis = st.selectbox('choose Y axis',list(df_numeric.columns))
x_axis = st.selectbox('choose X axis',list(df_numeric.columns))

st.write('scroll to look around the graph')

interactive_chart = alt.Chart(df).mark_circle().encode(
    x = alt.X(x_axis,scale=alt.Scale(zero=False)),
    y = alt.Y(y_axis,scale=alt.Scale(zero=False)),
    color = alt.Color('top genre',
                      scale=alt.Scale(scheme='dark2'),
                      legend=None), 
    tooltip = ['title','artist','top genre'],   #this should work, but it is not for me
    ).properties(
        title = 'Top Songs From 2010-2019 Interactive'
        ).interactive()
st.write(interactive_chart)

    #graphs for linear regression
chart1 = alt.Chart(df).mark_circle().encode(
    x = alt.X('year_datetime',scale=alt.Scale(zero=False),
              axis=alt.Axis(title='Year')),
    y = alt.Y('pop',axis=alt.Axis(title='Pop')),
    color = alt.Color('year_datetime',scale=alt.Scale(scheme="sinebow"),
                      legend=alt.Legend(title="Year")), 
    tooltip = ['title','artist'],   #same as above, I don't know why it isnt working :(
    ).properties(
        title = 'Poppiness of Top Songs From 2010-2019'
        ).interactive()


st.write(chart1)

st.write("I don't know about you, but I see a positive correlation between"
         " the year and the popiness of the song! It looks like songs get "
         "poppier as the years go on, so I will use"
         " linear regression to plot a line showing this positive correlation")


    #linear regression
st.write("We start by fitting the linear regression. I want to see the"
         "y-intercept and the slope!")

reg = sklearn.linear_model.LinearRegression()
X = np.array(df['year']).reshape(-1,1)
y = np.array(df['pop']).reshape(-1,1)
reg.fit(X,y)
reg_coef = float(reg.coef_)
reg_int = float(reg.intercept_)
    #https://christopherdavisuci.github.io/UCI-Math-10/Week5/Week5-Wednesday.html
    

st.write(f'Our slope turns out to be {reg_coef} and our y intercept is {reg_int}.'
         ' The y-intercept is so negative because our data starts at 2010')  ##I tried to change this by making the values a year, but I dont think that would change it anyways!

x_len = np.arange(2010,2020)
source = pd.DataFrame({
  'x': x_len,
  'f(x)': (reg_coef*x_len)+reg_int
})

st.write('**Interactive Element:**')
color = st.color_picker('Pick A Color for the Line',
                        '#00f900')

linear_regression_chart = alt.Chart(source).mark_line().encode(
    x=alt.X('x',scale=alt.Scale(
        domain=(2010,2019),
        clamp=True)),
    y=alt.Y('f(x)',scale=alt.Scale(
        domain=(0,100),
        clamp=True)),
    color=alt.value(color),
).interactive()     #added interactive() becasue it looks cool but it doesnt add anything to the project, and makes the graph a little funky!
    #https://altair-viz.github.io/gallery/scatter_tooltips.html
    #https://altair-viz.github.io/gallery/simple_line_chart.html
st.write(linear_regression_chart)

st.write('we can see a positive linear regression regarding the songs'
         ' poppiness throughout the years in the following altair chart!')

st.write(linear_regression_chart+chart1)


#added sidebar element for references
st.sidebar.write('**GITHUB REPO**')
st.sidebar.markdown('https://github.com/jmast00/Math10FinalProject')
st.sidebar.write('**REFERENCES**')
st.sidebar.write('datetotime portion https://stackoverflow.com/questions/46658232/pandas-convert-column-with-year-integer-to-datetime')
st.sidebar.write('interactive artist search was based on https://stackoverflow.com/questions/58351458/how-to-extract-entire-rows-from-pandas-data-frame-if-a-columns-string-value-co')
st.sidebar.write('reassigning the labels on the artist table was helped with https://github.com/streamlit/streamlit/issues/641')
st.sidebar.write('a lot of the code was inspired by the class github notes https://christopherdavisuci.github.io/UCI-Math-10/Week5/Week5-Wednesday.html')
st.sidebar.write('the following two links helped with charting and visual elements https://altair-viz.github.io/gallery/scatter_tooltips.html')
st.sidebar.write('https://altair-viz.github.io/gallery/simple_line_chart.html')



