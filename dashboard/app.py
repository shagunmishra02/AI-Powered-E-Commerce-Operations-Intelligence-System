import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Works both locally (dashboard/ subfolder) and on Streamlit Cloud (repo root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, "")

st.set_page_config(
    page_title="SmartOps Enterprise",
    page_icon="📊",
    layout="wide"
)

# Sidebar

st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart--v1.png",
    width=80
)

st.sidebar.title("SmartOps")

st.sidebar.markdown("""
### AI Product Analytics Platform

Enterprise Decision Support System
"""
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Executive Dashboard",
        "📈 Sales Analytics",
        "📦 Product Analytics",
        "👥 Customer Analytics",
        "📊 Demand Forecast",
        "🚚 Operations",
        "🚨 Risk Monitoring",
        "🤖 AI Reports"
    ]
)

# Load data
@st.cache_data
def load_data():
    master    = pd.read_csv(os.path.join(BASE_DIR, "data", "Processed", "master_data.csv"))
    rfm       = pd.read_csv(os.path.join(BASE_DIR, "data", "Processed", "rfm_segments.csv"))
    forecast  = pd.read_csv(os.path.join(BASE_DIR, "data", "Processed", "demand_forecast.csv"))
    anomalies = pd.read_csv(os.path.join(BASE_DIR, "data", "Processed", "seller_anomalies.csv"))
    return master, rfm, forecast, anomalies

master, rfm, forecast, anomalies = load_data()
master['order_purchase_timestamp'] = pd.to_datetime(master['order_purchase_timestamp'])

# ── PAGE 1: OVERVIEW ──────────────────────────────────
if page == "🏠 Executive Dashboard":

    st.title("📊 Executive Dashboard")
    st.markdown("Enterprise Business Performance Overview")

    # ---------------- KPIs ---------------- #

    total_orders = master['order_id'].nunique()
    total_revenue = master['payment_value'].sum()
    avg_order_value = master['payment_value'].mean()
    delivery_rate = (master['order_status']=="delivered").mean()*100
    active_customers = master['customer_unique_id'].nunique()
    active_sellers = master['seller_id'].nunique()
    anomaly_count = (anomalies['anomaly']==-1).sum()

    forecast_accuracy = 61.5

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "📦 Orders",
        f"{total_orders:,}"
    )

    col2.metric(
        "💰 Revenue",
        f"R${total_revenue:,.0f}"
    )

    col3.metric(
        "🛒 Avg Order Value",
        f"R${avg_order_value:.2f}"
    )

    col4.metric(
        "🚚 Delivery Rate",
        f"{delivery_rate:.1f}%"
    )

    col5,col6,col7,col8 = st.columns(4)

    col5.metric(
        "👥 Customers",
        f"{active_customers:,}"
    )

    col6.metric(
        "🏪 Sellers",
        f"{active_sellers:,}"
    )

    col7.metric(
        "⚠️ Anomalies",
        f"{anomaly_count}"
    )

    col8.metric(
        "📈 Forecast Accuracy",
        f"{forecast_accuracy}%"
    )

    st.divider()

    left,right = st.columns([2,1])

    with left:

        st.subheader("📈 Monthly Order Trend")

        master['order_month'] = master['order_purchase_timestamp'].dt.to_period('M').astype(str)

        monthly = master.groupby('order_month')['order_id'].nunique().reset_index()

        monthly.columns=["Month","Orders"]

        fig = px.bar(
            monthly,
            x="Month",
            y="Orders",
            color="Orders",
            color_continuous_scale="Blues"
        )

        st.plotly_chart(fig,use_container_width=True)

    with right:

        st.subheader("📌 Business Summary")

        st.success("✅ Delivery Rate : {:.1f}%".format(delivery_rate))

        st.info("📈 Forecast Accuracy : 61.5%")

        st.warning("⚠️ Sellers Flagged : {}".format(anomaly_count))

        st.metric(
            "Revenue / Customer",
            f"R${total_revenue/active_customers:.2f}"
        )   

# ── PAGE 2: DEMAND FORECAST ───────────────────────────
elif page == "📊 Demand Forecast":
    st.title("Module 1 — Demand Forecasting Engine")
    forecast['ds'] = pd.to_datetime(forecast['ds'])

    fig = px.line(forecast, x='ds', y='yhat',
                  title='90-Day Demand Forecast',
                  labels={'ds':'Date','yhat':'Predicted Orders'})
    fig.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'],
                    mode='lines', name='Upper Bound',
                    line=dict(dash='dash', color='lightblue'))
    fig.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'],
                    mode='lines', name='Lower Bound',
                    line=dict(dash='dash', color='lightblue'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Next 30 Days Forecast")
    next30 = forecast.tail(30)[['ds','yhat','yhat_lower','yhat_upper']]
    next30.columns = ['Date','Predicted Orders','Lower','Upper']
    st.dataframe(next30, use_container_width=True)


    # ── SALES ANALYTICS ───────────────────────────────

elif page == "📈 Sales Analytics":

    st.title("📈 Sales Analytics Dashboard")
    st.markdown("Revenue & Sales Performance")

    master['order_month'] = master['order_purchase_timestamp'].dt.to_period('M').astype(str)

    monthly = master.groupby("order_month").agg(
        Revenue=("payment_value","sum"),
        Orders=("order_id","nunique")
    ).reset_index()

    col1,col2 = st.columns(2)

    with col1:

        fig = px.line(
            monthly,
            x="order_month",
            y="Revenue",
            markers=True,
            title="Monthly Revenue"
        )

        st.plotly_chart(fig,use_container_width=True)

    with col2:

        fig = px.bar(
            monthly,
            x="order_month",
            y="Orders",
            color="Orders",
            color_continuous_scale="Blues",
            title="Monthly Orders"
        )

        st.plotly_chart(fig,use_container_width=True)

    st.subheader("Monthly Sales Summary")

    summary = monthly.copy()

    summary.columns=[
        "Month",
        "Revenue (R$)",
        "Orders"
    ]

    st.dataframe(summary,use_container_width=True)


    # ── PAGE : PRODUCT ANALYTICS ───────────────────────────
elif page == "📦 Product Analytics":

    st.title("📦 Product Analytics Dashboard")
    st.markdown("Analyze product and category performance.")

    # ---------------- KPIs ----------------

    total_products = master["product_id"].nunique()
    total_categories = master["product_category_name"].nunique()
    avg_price = master["price"].mean()
    avg_freight = master["freight_value"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📦 Products", f"{total_products:,}")
    c2.metric("🏷 Categories", total_categories)
    c3.metric("💰 Avg Price", f"R${avg_price:.2f}")
    c4.metric("🚚 Avg Freight", f"R${avg_freight:.2f}")

    st.divider()

    # ---------------- Revenue by Category ----------------

    st.subheader("💰 Revenue by Product Category")

    category_revenue = (
        master.groupby("product_category_name")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        category_revenue,
        x="product_category_name",
        y="payment_value",
        color="payment_value",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Orders by Category ----------------

    st.subheader("📦 Best Selling Categories")

    category_orders = (
        master.groupby("product_category_name")["order_id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.pie(
        category_orders,
        values="order_id",
        names="product_category_name",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Product Prices ----------------

    st.subheader("💵 Product Price Distribution")

    fig = px.histogram(
        master,
        x="price",
        nbins=40
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Top Products ----------------

    st.subheader("🏆 Top Products")

    product_table = (
        master.groupby(
            ["product_id", "product_category_name"]
        )
        .agg(
            Orders=("order_id", "count"),
            Revenue=("payment_value", "sum"),
            AvgPrice=("price", "mean")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(20)
        .reset_index()
    )

    st.dataframe(product_table, use_container_width=True)

# ── PAGE 3: CUSTOMER SEGMENTS ─────────────────────────
# ───────────────── CUSTOMER ANALYTICS ─────────────────
elif page == "👥 Customer Analytics":

    st.title("👥 Customer Analytics Dashboard")
    st.markdown("Enterprise Customer Intelligence & Behavioral Analytics")

    # -----------------------------
    # Customer KPIs
    # -----------------------------
    total_customers = master["customer_unique_id"].nunique()

    avg_order_value = master["payment_value"].mean()

    repeat_customers = (
        master.groupby("customer_unique_id")["order_id"]
        .nunique()
        .gt(1)
        .sum()
    )

    churned_customers = int(rfm["Churned"].sum())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("👥 Customers", f"{total_customers:,}")
    c2.metric("💰 Avg Order Value", f"R${avg_order_value:.2f}")
    c3.metric("🔄 Repeat Customers", f"{repeat_customers:,}")
    c4.metric("⚠ Churn Risk", f"{churned_customers:,}")

    st.divider()

    # -----------------------------
    # Customer Segments
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Customer Segments")

        seg = (
            rfm["Segment"]
            .value_counts()
            .reset_index()
        )

        seg.columns = ["Segment", "Customers"]

        fig = px.pie(
            seg,
            names="Segment",
            values="Customers",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Segment Summary")

        summary = (
            rfm.groupby("Segment")
            .agg(
                Customers=("customer_id", "count"),
                Avg_Recency=("Recency", "mean"),
                Avg_Monetary=("Monetary", "mean")
            )
            .round(1)
            .reset_index()
        )

        st.dataframe(summary, use_container_width=True)

    st.divider()

    # -----------------------------
    # Top Customer States
    # -----------------------------
    st.subheader("🌍 Top Customer States")

    state = (
        master.groupby("customer_state")
        .size()
        .reset_index(name="Customers")
        .sort_values("Customers", ascending=False)
    )

    fig = px.bar(
        state,
        x="customer_state",
        y="Customers",
        color="Customers",
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Top Cities
    # -----------------------------
    st.subheader("🏙 Top Customer Cities")

    city = (
        master.groupby("customer_city")
        .size()
        .sort_values(ascending=False)
        .head(15)
        .reset_index(name="Orders")
    )

    fig = px.bar(
        city,
        x="Orders",
        y="customer_city",
        orientation="h",
        color="Orders",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Spending Distribution
    # -----------------------------
    st.subheader("💳 Customer Spending Distribution")

    fig = px.histogram(
        master,
        x="payment_value",
        nbins=40,
        color_discrete_sequence=["royalblue"]
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Highest Spending Customers
    # -----------------------------
    st.subheader("🏆 Top Customers by Revenue")

    top_customers = (
        master.groupby("customer_unique_id")
        .agg(
            Orders=("order_id", "nunique"),
            Revenue=("payment_value", "sum"),
            Avg_Order_Value=("payment_value", "mean")
        )
        .sort_values("Revenue", ascending=False)
        .head(20)
        .reset_index()
    )

    st.dataframe(top_customers, use_container_width=True)


    # ────page4───────────── OPERATIONS DASHBOARD ─────────────────
elif page == "🚚 Operations":

    st.title("🚚 Operations Dashboard")
    st.markdown("Enterprise Operations & Logistics Performance")

    delivered = master[master["order_status"] == "delivered"].copy()

    delivered["order_purchase_timestamp"] = pd.to_datetime(
        delivered["order_purchase_timestamp"]
    )

    delivered["order_delivered_customer_date"] = pd.to_datetime(
        delivered["order_delivered_customer_date"]
    )

    delivered["delivery_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_purchase_timestamp"]
    ).dt.days

    # ---------------- KPIs ----------------

    avg_delivery = delivered["delivery_days"].mean()

    late_orders = (
        delivered["delivery_delay_days"] > 0
    ).sum()

    avg_freight = delivered["freight_value"].mean()

    on_time = (
        (delivered["delivery_delay_days"] <= 0).mean()
        *100
    )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "🚚 Avg Delivery",
        f"{avg_delivery:.1f} Days"
    )

    c2.metric(
        "⚠ Late Deliveries",
        f"{late_orders:,}"
    )

    c3.metric(
        "💰 Avg Freight",
        f"R${avg_freight:.2f}"
    )

    c4.metric(
        "✅ On-Time Delivery",
        f"{on_time:.1f}%"
    )

    st.divider()

    # ---------------- Monthly Delivery ----------------

    st.subheader("Monthly Delivery Trend")

    delivered["Month"] = delivered[
        "order_purchase_timestamp"
    ].dt.to_period("M").astype(str)

    trend = (
        delivered.groupby("Month")
        .agg(
            Orders=("order_id","count"),
            Avg_Delivery=("delivery_days","mean")
        )
        .reset_index()
    )

    fig = px.line(
        trend,
        x="Month",
        y="Avg_Delivery",
        markers=True
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------------- Delivery by State ----------------

    st.subheader("Average Delivery Time by State")

    state = (
        delivered.groupby("customer_state")
        .agg(
            Avg_Delivery=("delivery_days","mean")
        )
        .sort_values(
            "Avg_Delivery",
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        state,
        x="customer_state",
        y="Avg_Delivery",
        color="Avg_Delivery",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------------- Freight ----------------

    st.subheader("Freight Cost Distribution")

    fig = px.histogram(
        delivered,
        x="freight_value",
        nbins=40
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------------- Delivery Delay ----------------

    st.subheader("Delivery Delay Distribution")

    fig = px.histogram(
        delivered,
        x="delivery_delay_days",
        nbins=40
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------------- Sellers ----------------

    st.subheader("Top Sellers by Orders")

    sellers = (
        delivered.groupby("seller_id")
        .agg(
            Orders=("order_id","count"),
            Revenue=("payment_value","sum"),
            Avg_Delivery=("delivery_days","mean")
        )
        .sort_values(
            "Orders",
            ascending=False
        )
        .head(20)
        .reset_index()
    )

    st.dataframe(
        sellers,
        use_container_width=True
    )

# ── PAGE 4: ANOMALY DETECTION ─────────────────────────
# ──────────────── RISK MONITORING ─────────────────

elif page == "🚨 Risk Monitoring":

    st.title("🚨 Risk Monitoring Dashboard")
    st.markdown("Real-Time Operational Risk & Seller Monitoring")

    flagged = anomalies[anomalies["anomaly"] == -1]

    # ---------------- KPIs ----------------

    total_flagged = len(flagged)

    avg_delay = flagged["avg_delay"].mean()

    revenue_at_risk = flagged["total_revenue"].sum()

    avg_orders = flagged["total_orders"].mean()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "🚨 Flagged Sellers",
        f"{total_flagged:,}"
    )

    c2.metric(
        "⏱ Avg Delay",
        f"{avg_delay:.1f} Days"
    )

    c3.metric(
        "💰 Revenue at Risk",
        f"R${revenue_at_risk:,.0f}"
    )

    c4.metric(
        "📦 Avg Orders",
        f"{avg_orders:.0f}"
    )

    st.divider()

    # ---------------- Delay vs Revenue ----------------

    st.subheader("Delay vs Revenue")

    fig = px.scatter(
        flagged,
        x="avg_delay",
        y="total_revenue",
        size="total_orders",
        color="avg_delay",
        hover_data=["seller_id"],
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------------- Highest Delay ----------------

    st.subheader("Highest Delivery Delays")

    top_delay = (
        flagged.sort_values(
            "avg_delay",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        top_delay,
        x="seller_id",
        y="avg_delay",
        color="avg_delay",
        color_continuous_scale="Oranges"
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------------- Revenue at Risk ----------------

    st.subheader("Revenue Exposure")

    top_rev = (
        flagged.sort_values(
            "total_revenue",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        top_rev,
        x="seller_id",
        y="total_revenue",
        color="total_revenue",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------------- Risk Distribution ----------------

    st.subheader("Risk Distribution")

    fig = px.histogram(
        flagged,
        x="avg_delay",
        nbins=30
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------------- Critical Sellers ----------------

    st.subheader("Critical Seller Monitoring")

    table = flagged[
        [
            "seller_id",
            "avg_delay",
            "total_orders",
            "total_revenue"
        ]
    ].sort_values(
        "avg_delay",
        ascending=False
    )

    st.dataframe(
        table,
        use_container_width=True
    )

    st.success(
        f"✅ {total_flagged} sellers are currently flagged for operational review."
    )

# ── PAGE 5: AI REPORTS ────────────────────────────────
# ───────────────── AI REPORTS ─────────────────

elif page == "🤖 AI Reports":

    st.title("🤖 AI Executive Intelligence")
    st.markdown("AI Generated Business Insights & Executive Reporting")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📋 Executive Summary")

        try:
            with open(os.path.join(BASE_DIR, "outputs", "weekly_report.txt")) as f:
                report_content = f.read()

            st.text_area(
                "",
                report_content,
                height=350
            )

        except:

            report_content = ""

            st.warning("Run Module 4 Notebook First")

    with col2:

        st.subheader("📧 Supplier Email Draft")

        try:

            with open(os.path.join(BASE_DIR,"outputs","supplier_email.txt")) as f:

                supplier_content = f.read()

            st.text_area(
                "",
                supplier_content,
                height=350
            )

        except:

            supplier_content=""

            st.warning("Supplier Email Not Found")

    st.divider()

    st.subheader("🧠 AI Business Recommendations")

    st.info("📈 Increase inventory for high demand categories.")

    st.info("🚚 Review logistics partners with frequent delivery delays.")

    st.info("💰 Focus marketing campaigns on high-value customer segments.")

    st.info("🏆 Reward top-performing sellers to improve retention.")

    st.info("⚠ Investigate sellers with abnormal operational behaviour.")

    st.divider()

    st.subheader("📊 Executive KPIs")

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Forecast Accuracy",
        "61.5%"
    )

    c2.metric(
        "Customer Segments",
        rfm["Segment"].nunique()
    )

    c3.metric(
        "Flagged Sellers",
        len(anomalies[anomalies["anomaly"]==-1])
    )

    st.divider()

    st.subheader("📥 Download Reports")

    if report_content:

        st.download_button(
            label="⬇ Download Executive Report",
            data=report_content,
            file_name="Executive_Report.txt",
            mime="text/plain"
        )

    if supplier_content:

        st.download_button(
            label="⬇ Download Supplier Email",
            data=supplier_content,
            file_name="Supplier_Email.txt",
            mime="text/plain"
        )

    st.divider()

    st.subheader("📧 Send Email")

    recipient = st.text_input(
        "Recipient Email"
    )

    if st.button("Send Report"):

        st.success(
            "Email functionality already integrated in Module 4."
        )

    st.divider()

    st.success("✅ SmartOps AI successfully generated business recommendations.")

    # Email section
    st.divider()

st.subheader("📧 Email Executive Report")

recipient = st.text_input(
    "Recipient Email Address",
    placeholder="manager@company.com"
)

col1, col2 = st.columns(2)

with col1:

    if st.button("📨 Send Report"):

        if recipient.strip() == "":
            st.warning("Please enter a recipient email.")

        else:
            try:

                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart

                smtp_server = "smtp-relay.brevo.com"
                port = 587

                login_email = get_secret("BREVO_LOGIN")
                sender_email = get_secret("SENDER_EMAIL")
                sender_password = get_secret("BREVO_SMTP_KEY")

                body = f"""
SMARTOPS ENTERPRISE REPORT

====================================================

EXECUTIVE SUMMARY

{report_content}

====================================================

SUPPLIER EMAIL

{supplier_content}

====================================================

Generated by SmartOps Enterprise
AI Product Analytics Platform
"""

                msg = MIMEMultipart()

                msg["From"] = sender_email
                msg["To"] = recipient
                msg["Subject"] = "SmartOps Enterprise Executive Report"

                msg.attach(MIMEText(body, "plain"))

                with smtplib.SMTP(smtp_server, port) as server:
                    server.starttls()
                    server.login(login_email, sender_password)
                    server.sendmail(
                        sender_email,
                        recipient,
                        msg.as_string()
                    )

                st.success("✅ Report emailed successfully!")

            except Exception as e:

                st.error(f"Email failed: {e}")

with col2:

    st.info("""
### 📌 Email Includes

✅ Executive Summary

✅ Supplier Email Draft

✅ AI Recommendations

✅ Business Insights
""")
    st.divider()

st.info(
    "📌 SmartOps integrates Product Analytics, Customer Analytics, Demand Forecasting, Risk Monitoring and AI-powered Executive Reporting into one enterprise dashboard."
)