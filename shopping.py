import streamlit as st
import pandas as pd

st.subheader("Create Product")
p1, p2 = st.columns([2, 1])

with p1:
    prod_name = st.text_input("Product name", key="prod_name")

with p2:
    prod_price = st.number_input("Price", min_value=0.0, format="%.2f", key="prod_price")

if st.button("Add Product"):
    ok, msg = admin_create_product(prod_name.strip(), prod_price)
    if ok:
        st.success(msg)
    else:
        st.error(msg)

st.subheader("All Products")
products = list(products_col.find({}, {"_id": 0}))

if products:
    st.dataframe(pd.DataFrame(products))
else:
    st.info("No products yet. Add some above.")

st.subheader("All Orders")
orders = list(orders_col.find({}, {"_id": 0}))

if orders:
    df = pd.DataFrame(orders)
    # convert date for display
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    st.dataframe(df)
else:
    st.info("No orders placed yet.")

# User dashboard
else:
    st.header("Shop — browse products")
    products = list(products_col.find({}, {"_id": 0}))
    if not products:
        st.info("No products available. Ask admin to add products.")
    else:
        df_products = pd.DataFrame(products)
        # show product list with Add-to-cart controls
        for idx, row in df_products.iterrows():
            cols = st.columns([3, 1, 1])
            cols[0].write(f"**{row['name']}**")
            cols[0].write(f"Price: ₹{row['price']:.2f}")
            qty = cols[1].number_input(f"Qty-{idx}", min_value=1, value=1, key=f"qty_{idx}")
            if cols[2].button("Add to cart", key=f"add_{idx}"):
                # add to session cart
                st.session_state.cart.append({
                    "name": row['name'],
                    "price": float(row['price']),
                    "qty": int(qty)
                })
                st.success(f"Added {row['name']} x{qty} to cart")

    st.subheader("Cart")
    if st.session_state.cart:
        cart_df = pd.DataFrame(st.session_state.cart)
        cart_df["subtotal"] = cart_df["price"] * cart_df["qty"]
        st.dataframe(cart_df)
        total = cart_df["subtotal"].sum()
        st.markdown(f"**Total: ₹{total:.2f}**")

        col_buy, col_clear = st.columns(2)

        if col_buy.button("Buy Now"):
            ok, msg = place_order(st.session_state.auth["username"], st.session_state.cart)
            if ok:
                st.session_state.cart = []
                st.success("Order placed successfully 🎉")
            else:
                st.error(msg)

        if col_clear.button("Clear Cart"):
            st.session_state.cart = []
            st.info("Cart cleared")
    else:
        st.info("Your cart is empty")

# If not logged in, show a short intro
else:
    st.write("Welcome — please login from the sidebar. If this is the first run, create an admin from the sidebar.")
