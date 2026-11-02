import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import get_cost_analysis

st.set_page_config(page_title='Cost Observability Dashboard', page_icon='📊', layout='wide')
st.title('Cost Observability & ML Optimization')
st.caption('Monthly Cost Monitoring | ML Anomaly Detection')
currency = st.sidebar.selectbox('Currency label', ['CAD', 'USD'])
st.sidebar.caption('Select the currency used by your backend; this does not convert amounts.')
if st.sidebar.button('Refresh Analysis'):
    st.rerun()
try:
    data = get_cost_analysis()
except Exception as exc:
    st.error(f'Backend connection failed: {exc}')
    st.info('Start your FastAPI backend at http://localhost:8000 with GET /cost-analysis.')
    st.stop()

previous = float(data['previous_month_total'])
current = float(data['current_month_total'])
difference = current - previous
percentage = 100 * difference / previous if previous else None
c1, c2, c3, c4 = st.columns(4)
c1.metric('Previous Month', f'{currency} {previous:,.2f}')
c2.metric('Current Month', f'{currency} {current:,.2f}')
c3.metric('Cost Difference', f'{currency} {difference:+,.2f}', delta=f'{percentage:+.1f}%' if percentage is not None else 'N/A', delta_color='inverse')
c4.metric('Estimated Monthly Savings', f"{currency} {float(data.get('estimated_savings', 0)):,.2f}")

st.subheader('Current vs Previous Month')
df = pd.DataFrame(data.get('categories', []))
if df.empty or not {'category', 'previous', 'current'}.issubset(df.columns):
    st.warning('No valid category data returned by the backend.')
    st.stop()
df['previous'] = pd.to_numeric(df['previous'])
df['current'] = pd.to_numeric(df['current'])
df['difference'] = df['current'] - df['previous']
df['change_percent'] = df.apply(lambda row: 100 * row['difference'] / row['previous'] if row['previous'] else None, axis=1)
st.dataframe(df, use_container_width=True)
chart_df = df.melt(id_vars='category', value_vars=['previous', 'current'], var_name='Month', value_name='Cost')
st.plotly_chart(px.bar(chart_df, x='category', y='Cost', color='Month', barmode='group', title='Monthly Cost Comparison'), use_container_width=True)

st.subheader('Why Did Costs Increase?')
increases = df[df['difference'] > 0]
if increases.empty:
    st.success('No category cost increases detected.')
else:
    for _, row in increases.iterrows():
        st.warning(f"{row['category']}: +{currency} {row['difference']:,.2f}")
        reason = row.get('reason', '')
        st.write('Possible reason: ' + (str(reason) if pd.notna(reason) and str(reason).strip() else 'Investigate usage, unit prices, and one-time expenses.'))

st.subheader('ML Anomaly Detection')
anomalies = data.get('anomalies', [])
if anomalies:
    for item in anomalies:
        st.warning(f"{item.get('category', 'Unknown')}: {item.get('message', 'Unusual cost detected')}")
else:
    st.info('No anomalies reported by the backend.')

st.subheader('Cost Optimization Recommendations')
recommendations = data.get('recommendations', [])
if recommendations:
    for rec in recommendations:
        with st.expander(rec.get('category', 'Recommendation')):
            st.write(rec.get('recommendation', 'Review this category.'))
            st.write(f"Estimated savings: {currency} {float(rec.get('estimated_savings', 0)):,.2f}")
else:
    st.info('No recommendations available.')
st.caption('Savings are estimates. ML anomalies do not establish causes. Currency selection changes labels only.')
