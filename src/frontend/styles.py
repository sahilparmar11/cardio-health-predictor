
def load_css():
    return """
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        /* Container Padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* --- Custom Stat Card --- */
        .stat-card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #E8F5E9;
            text-align: center;
            transition: transform 0.2s;
        }
        .stat-card:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 15px rgba(46, 125, 50, 0.1);
            border-color: #66BB6A;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2E7D32;
        }
        .stat-label {
            font-size: 0.9rem;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stat-icon {
            font-size: 1.5rem;
            margin-bottom: 10px;
            color: #4CAF50;
        }

        /* --- Hide System UI Elements --- */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;} 
        [data-testid="stToolbar"] {visibility: hidden !important;} 
        .stDeployButton {display: none !important;}

        /* --- Hero Section --- */
        .hero-box {
            background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%);
            border-radius: 20px;
            padding: 40px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 10px 20px rgba(46, 125, 50, 0.2);
            text-align: center;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            font-weight: 300;
            opacity: 0.9;
        }

        /* --- Global Card Style --- */
        [data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"], .stCard {
            background-color: white; /* Force white card on light green background */
            border-radius: 20px !important;
            padding: 2rem !important;
            box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1); /* Subtle Green Shadow */
            border: 1px solid rgba(46, 125, 50, 0.1) !important;
            transition: all 0.3s ease;
        }
        
        /* Adjust card background if in dark mode (Automatic fallback or keep white? User wanted White/Green) 
           Let's stick to the config.toml variables where possible, but here we force a 'Card' look.
           If we use var(--secondary-background-color) it might represent the sidebar color.
           Let's try using white with valid text color.
        */
        
        /* Hover Effect for Cards */
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(46, 125, 50, 0.2);
            border-color: #81C784 !important;
        }

        /* --- Header Styles --- */
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1B5E20; /* Dark Green - High Contrast */
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Sub-headers section specific */
        .dashboard-header { border-bottom: 3px solid #4CAF50; display: inline-block; }
        .assessment-header { border-bottom: 3px solid #2E7D32; display: inline-block; }
        .analytics-header { border-bottom: 3px solid #00838F; display: inline-block; } # Teal for analytics

        /* --- KPI/Stat Card Style --- */
        div.css-1r6slb0.e1tzin5v2, [data-testid="stMetric"] { 
            background-color: white;
            border: 1px solid #E8F5E9;
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            color: #2E7D32;
        }

        /* --- Divider --- */
        hr {
            border-color: #C8E6C9; /* Light Green divider */
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
        
        /* --- Inputs --- */
        /* Target input borders to be Green */
        .stTextInput input, .stNumberInput input, .stSelectbox > div > div {
            border-radius: 10px;
            border: 1px solid #A5D6A7;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox > div > div:focus {
            border-color: #2E7D32;
            box-shadow: 0 0 0 1px #2E7D32;
        }

        /* --- Buttons --- */
        .stButton > button {
            border-radius: 30px;
            font-weight: 600;
            padding: 12px 30px;
            border: none;
            transition: 0.3s;
            background-color: #2E7D32; /* Flat Green */
            color: white !important;
            box-shadow: 0 4px 6px rgba(46, 125, 50, 0.3);
        }
        
        .stButton > button:hover {
            background-color: #1B5E20; /* Darker Green on Hover */
            transform: scale(1.02);
            box-shadow: 0 6px 12px rgba(46, 125, 50, 0.4);
        }

    </style>
    """
