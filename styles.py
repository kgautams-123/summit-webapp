custom_css = """
<style>
    /* Modern Color Palette */
    :root {
        --primary-color: #2B3467;
        --secondary-color: #394867;
        --accent-color: #5C469C;
        --accent-light: #756AB6;
        --success-color: #38A169;
        --warning-color: #EAB308;
        --error-color: #DC2626;
        --background-color: #F8FAFC;
        --text-primary: #1E293B;
        --text-secondary: #64748B;
        --card-background: #FFFFFF;
        --card-shadow: rgba(43, 52, 103, 0.1);
        --gradient-start: #2B3467;
        --gradient-end: #5C469C;
        --transition-speed: 0.3s;
    }

    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, var(--background-color) 0%, #EEF2FF 100%);
    }

    /* Modern Animated Header */
    .header-container {
        background: linear-gradient(45deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px var(--card-shadow);
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 5s infinite;
    }

    @keyframes shine {
        0% { left: -100%; }
        20% { left: 100%; }
        100% { left: 100%; }
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 0.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: var(--text-primary);
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--accent-color) !important;
        color: white !important;
    }

    /* Product grid styling */
    .stSelectbox {
        margin-bottom: 1rem;
    }
    
    .product-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .product-card {
        background: white;
        border-radius: 10px;
        padding: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .product-card img {
        width: 100%;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .product-card p {
        margin: 0;
        font-weight: 600;
        color: var(--text-primary);
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(45deg, var(--accent-color), var(--accent-light)) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(92, 70, 156, 0.2) !important;
    }

    /* Selected Image Container */
    .selected-image-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px var(--card-shadow);
        margin-bottom: 1.5rem;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }

    .sidebar-prompt {
        background: white;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .sidebar-prompt:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Custom Upload Area */
    .upload-container {
        border: 2px dashed var(--accent-light);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: rgba(255,255,255,0.5);
        transition: all 0.3s ease;
    }

    .upload-container:hover {
        border-color: var(--accent-color);
        background: rgba(255,255,255,0.8);
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--accent-color);
        border-radius: 3px;
    }

    /* Download Button */
    .download-button {
        display: inline-block;
        padding: 0.8rem 1.5rem;
        background: linear-gradient(45deg, var(--accent-color), var(--accent-light));
        color: white !important;
        border-radius: 8px;
        text-decoration: none !important;
        font-weight: 600;
        text-align: center;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }

    .download-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(92, 70, 156, 0.2);
    }

    .download-button.linkedin {
        background: linear-gradient(45deg, #0077b5, #00a0dc);
    }

    /* Loading Animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }

    .loading-animation div {
        width: 10px;
        height: 10px;
        margin: 0 5px;
        background-color: var(--accent-color);
        border-radius: 50%;
        animation: bounce 0.5s alternate infinite;
    }

    @keyframes bounce {
        from { transform: translateY(0); }
        to { transform: translateY(-15px); }
    }
</style>
"""
