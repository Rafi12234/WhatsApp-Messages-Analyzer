import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
# Set page config for better appearance
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Main app styling */
    .main > div {
        padding: 2rem 1rem;
    }

    /* Custom sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Sidebar title styling */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #ff6b6b;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        color: white;
        text-align: center;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: white;
    }

    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        color: rgba(255,255,255,0.9);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        font-size: 1.5rem;
        margin: 2rem 0 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
    }

    /* Card containers */
    .analysis-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #f0f2f6;
    }

    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Title styling */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin: 2rem 0;
    }

    /* Sidebar styling */
    .css-1d391kg .css-1oe5cao {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Custom alert boxes */
    .info-box {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Main title with emoji
st.markdown('<h1 class="main-title">💬 WhatsApp Chat Analyzer</h1>', unsafe_allow_html=True)

# Sidebar with enhanced styling
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 2rem;">
    <h2 style="color: white; margin: 0;">📊 Analysis Dashboard</h2>
    <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">Upload your WhatsApp chat export</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=['txt'],
    help="Export your WhatsApp chat as a .txt file"
)

if uploaded_file is not None:
    # File processing
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(data)

    # User selection
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "🔍 Show analysis for:",
        user_list,
        help="Select a specific user or 'Overall' for group analysis"
    )

    # Enhanced analysis button
    if st.sidebar.button("🚀 Show Analysis"):

        # Fetch statistics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # Top Statistics Section with enhanced cards
        st.markdown('<div class="section-header">📈 Key Statistics</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Messages</div>
                <div class="metric-value">{num_messages:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #2d5f5f 0%, #8b4d63 100%);">
                <div class="metric-label">Total Words</div>
                <div class="metric-value">{words:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #2d5f5f 0%, #8b4d63 100%);">
                <div class="metric-label">Media Shared</div>
                <div class="metric-value">{num_media_messages:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #ffecd2 0%, #5d4e75 100%);">
                <div class="metric-label">Links Shared</div>
                <div class="metric-value">{num_links:,}</div>
            </div>
            """, unsafe_allow_html=True)

        # Busiest Users Section (only for Overall)
        if selected_user == 'Overall':
            st.markdown('<div class="section-header">👑 Most Active Users</div>', unsafe_allow_html=True)

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns([2, 1])

            with col1:

                fig, ax = plt.subplots(figsize=(10, 6))

                # Enhanced bar chart with gradient colors
                bars = ax.bar(x.index, x.values,
                              color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'])

                # Styling the plot
                ax.set_facecolor('#f8f9fa')
                fig.patch.set_facecolor('white')
                plt.xticks(rotation=45, ha='right')
                plt.title('Message Count by User', fontsize=16, fontweight='bold', pad=20)
                plt.xlabel('Users', fontsize=12, fontweight='500')
                plt.ylabel('Number of Messages', fontsize=12, fontweight='500')

                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontweight='bold')

                plt.tight_layout()
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:

                st.subheader("📊 Percentage Breakdown")
                st.dataframe(new_df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Word Cloud Section
        st.markdown('<div class="section-header">☁️ Word Cloud</div>', unsafe_allow_html=True)


        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        fig.patch.set_facecolor('white')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # Most Common Words Section
        st.markdown('<div class="section-header">🔤 Most Frequent Words</div>', unsafe_allow_html=True)


        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 8))

        bars = ax.barh(most_common_df[0], most_common_df[1],
                       color=plt.cm.viridis(range(len(most_common_df))))

        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        plt.title('Most Common Words', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Frequency', fontsize=12, fontweight='500')

        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height() / 2.,
                    f'{int(width)}',
                    ha='left', va='center', fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # Timeline Analysis Section
        st.markdown('<div class="section-header">📅 Timeline Analysis</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("📈 Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(timeline['time'], timeline['message'],
                    color='#4ecdc4', linewidth=3, marker='o', markersize=6)
            ax.fill_between(timeline['time'], timeline['message'],
                            alpha=0.3, color='#4ecdc4')

            ax.set_facecolor('#f8f9fa')
            fig.patch.set_facecolor('white')
            plt.xticks(rotation=45, ha='right')
            plt.title('Messages Over Months', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:

            st.subheader("📊 Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(daily_timeline['only_date'], daily_timeline['message'],
                    color='#ff6b6b', linewidth=2, alpha=0.8)

            ax.set_facecolor('#f8f9fa')
            fig.patch.set_facecolor('white')
            plt.xticks(rotation=45, ha='right')
            plt.title('Daily Message Count', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # Activity Map Section
        st.markdown('<div class="section-header">🗓️ Activity Patterns</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("📅 Most Active Days")
            busy_day = helper.week_activity_map(selected_user, df)

            fig, ax = plt.subplots(figsize=(8, 6))
            bars = ax.bar(busy_day.index, busy_day.values,
                          color=['#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3',
                                 '#ff9f43', '#10ac84', '#ee5253'])

            ax.set_facecolor('#f8f9fa')
            fig.patch.set_facecolor('white')
            plt.xticks(rotation=45)
            plt.title('Activity by Day of Week', fontweight='bold')

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:

            st.subheader("📆 Most Active Months")
            busy_month = helper.month_activity_map(selected_user, df)

            fig, ax = plt.subplots(figsize=(8, 6))
            bars = ax.bar(busy_month.index, busy_month.values,
                          color=plt.cm.Set3(range(len(busy_month))))

            ax.set_facecolor('#f8f9fa')
            fig.patch.set_facecolor('white')
            plt.xticks(rotation=45)
            plt.title('Activity by Month', fontweight='bold')

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # Activity Heatmap Section
        st.markdown('<div class="section-header">🔥 Activity Heatmap</div>', unsafe_allow_html=True)


        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 8))

        sns.heatmap(user_heatmap,
                    cmap='YlOrRd',
                    annot=True,
                    fmt='.0f',
                    cbar_kws={'label': 'Number of Messages'},
                    ax=ax)

        plt.title('Activity Heatmap: Day vs Time Period',
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Time Period', fontsize=12, fontweight='500')
        plt.ylabel('Day of Week', fontsize=12, fontweight='500')

        fig.patch.set_facecolor('white')
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Welcome message when no file is uploaded
    st.markdown("""
    <div class="info-box">
        <h3>👋 Welcome to WhatsApp Chat Analyzer!</h3>
        <p>Please upload your WhatsApp chat export file (.txt) using the sidebar to begin analysis.</p>
        <br>
        <p><strong>How to export WhatsApp chat:</strong></p>
        <p>1. Open WhatsApp on your phone</p>
        <p>2. Go to the chat you want to analyze</p>
        <p>3. Tap on chat settings (three dots)</p>
        <p>4. Select "Export chat" → "Without media"</p>
        <p>5. Save the .txt file and upload it here</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature showcase
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 3rem 0;">
        <div class="analysis-card">
            <h3 style="color: #667eea;">📊 Comprehensive Analytics</h3>
            <p>Get detailed insights into message patterns, user activity, and communication trends.</p>
        </div>
        <div class="analysis-card">
            <h3 style="color: #667eea;">☁️ Word Cloud Visualization</h3>
            <p>Discover the most frequently used words in your conversations with beautiful word clouds.</p>
        </div>
        <div class="analysis-card">
            <h3 style="color: #667eea;">📅 Timeline Analysis</h3>
            <p>Track your messaging patterns over time with interactive timeline charts.</p>
        </div>
        <div class="analysis-card">
            <h3 style="color: #667eea;">🔥 Activity Heatmaps</h3>
            <p>Visualize when you're most active with detailed heatmap analysis.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
