import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Pending Smoothie Orders :cup_with_straw:")

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
    editable_df = editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success("You have process the order.")
        except:
            st.write('something went wrong')
else:
    st.success('there are no pending orders')
