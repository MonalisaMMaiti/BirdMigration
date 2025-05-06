import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
df = pd.read_csv("/Users/Monalisa/Downloads/bird_migration_data.csv")

st.title("🕊️ Bird Migration Visualization Dashboard")
st.markdown("Explore bird migration trends, distances, weather, and success across regions.")

# Section 1: Dataset Overview
st.subheader(" Dataset Overview")
st.write(df.head())

# Section 2: Wind Speed vs Flight Distance
st.subheader(" Wind Speed vs Flight Distance")
fig1 = px.scatter(df, x='Wind_Speed_kmph', y='Flight_Distance_km',
                  color='Migration_Success', size='Flock_Size',
                  hover_data=['Species', 'Region'],
                  title='Wind Speed vs Flight Distance')
st.plotly_chart(fig1)

# Section 3: Species-wise Avg Speed & Distance
st.subheader(" Average Speed vs Flight Distance by Species")
avg_df = df.groupby('Species')[['Average_Speed_kmph', 'Flight_Distance_km']].mean().reset_index()
fig2 = px.scatter(avg_df, x='Flight_Distance_km', y='Average_Speed_kmph', text='Species',
                  title="Species-wise Averages")
st.plotly_chart(fig2)

# Section 4: Correlation Heatmap
st.subheader("Correlation Heatmap")
df['Migration_Success_Encoded'] = df['Migration_Success'].map({'Successful': 1, 'Failed': 0})
corr_df = df[['Wind_Speed_kmph', 'Flight_Distance_km', 'Flock_Size', 'Average_Speed_kmph', 'Migration_Success_Encoded']]
fig3 = px.imshow(corr_df.corr(), text_auto=True, title="Feature Correlation")
st.plotly_chart(fig3)

# Section 5: Pairplot (optional)
st.subheader(" Pairplot (Optional)")
with st.expander("Show Pair Plot"):
    subset = df[['Flight_Distance_km', 'Average_Speed_kmph', 'Wind_Speed_kmph',
                 'Flock_Size', 'Migration_Success_Encoded']].dropna()
    sns_plot = sns.pairplot(subset, diag_kind='kde', plot_kws={'alpha': 0.4})
    st.pyplot(sns_plot)

# Section 6: Weather Conditions Distribution
st.subheader(" Weather Conditions During Migration")
if 'Weather_Condition' in df.columns:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(x='Weather_Condition', data=df, palette='Set2',
                  order=df['Weather_Condition'].value_counts().index)
    ax.set_title('Weather Conditions Frequency')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Section 7: Habitat Type Distribution
st.subheader("Bird Habitat Types")
if 'Habitat' in df.columns:
    fig, ax = plt.subplots(figsize=(8, 4))
    df['Habitat'].value_counts().plot.pie(autopct='%1.1f%%', colors=sns.color_palette('pastel'), ax=ax)
    ax.set_ylabel('')
    ax.set_title('Distribution of Habitats')
    st.pyplot(fig)

# Section 8: Flight Distance by Region
st.subheader(" Flight Distance by Region")
if 'Region' in df.columns:
    fig = px.box(df, x='Region', y='Flight_Distance_km', color='Region',
                 title="Flight Distance Distribution per Region")
    st.plotly_chart(fig)

# Section 9: Migration Reason Count
st.subheader(" Migration Reason Count")
if 'Migration_Reason' in df.columns:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x='Migration_Reason', data=df, palette='husl')
    ax.set_title('Reason for Migration')
    plt.xticks(rotation=0)
    st.pyplot(fig)

# Section 10: Migration Success by Region
st.subheader(" Migration Success by Region")
if 'Region' in df.columns:
    fig = px.histogram(df, x='Region', color='Migration_Success',
                       barmode='group', title='Migration Success Count Across Regions')
    st.plotly_chart(fig)
