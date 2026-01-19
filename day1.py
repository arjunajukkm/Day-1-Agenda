import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import datetime
import csv

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="FinBox Onboarding", page_icon="🟦", layout="wide")

# ----------------------------
# 1. LOGGING FUNCTION (User, Date, Time)
# ----------------------------
def log_user_access():
    """
    Logs the user email (if available), date, and time to a CSV file.
    """
    log_file = "login_log.csv"
    
    # Try to get user email from Streamlit experimental headers (works in deployed apps)
    # In local development, this usually returns None.
    try:
        headers = st.context.headers
        user_email = headers.get("X-Shared-Email", "Unknown/Local User")
    except:
        user_email = "Unknown/Local User"

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Create file with header if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "User Email"])

    # Append log entry
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, time_str, user_email])

# Execute Logging
log_user_access()

# ----------------------------
# 2. HELPER: LOAD IMAGES (Logo & Slides)
# ----------------------------
def get_image_base64(file_name_prefix):
    """
    Looks for file_name_prefix.png/jpg/jpeg.
    Returns base64 string.
    """
    for ext in ['.png', '.jpg', '.jpeg']:
        file_name = f"{file_name_prefix}{ext}"
        if os.path.exists(file_name):
            try:
                with open(file_name, "rb") as f:
                    data = f.read()
                    encoded = base64.b64encode(data).decode()
                    return f"data:image/{ext.replace('.', '')};base64,{encoded}"
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
    return None

# Load Custom LOGO
logo_src = get_image_base64("LOGO")
if not logo_src:
    # Fallback if LOGO.png is missing
    logo_src = "https://img.icons8.com/fluency/96/diamond.png" 

# ----------------------------
# 3. AGENDA DATA
# ----------------------------
agenda_items = [
    {"time": "10:00 AM", "duration": "15 Min", "title": "Welcome & Greetings", "desc": "Warm welcome to FinBox by HR Team"},
    {"time": "10:15 AM", "duration": "30 Min", "title": "Introduction to Finbox", "desc": "Company history, milestones, roadmap, and key leadership overview."},
    {"time": "10:45 AM", "duration": "30 Min", "title": "Office Tour", "desc": "Walkthrough of office space, key teams, and amenities."},
    {"time": "11:15 AM", "duration": "15 Min", "title": "Morning Break", "desc": "Short recharge before the deep dive."},
    {"time": "11:30 AM", "duration": "30 Min", "title": "Product Training", "desc": "Brief Intro and walkthrough on the FinBox products."},
    {"time": "12:00 PM", "duration": "90 Min", "title": "IT Setup & Induction", "desc": "Laptop handover, account setup, IT policy orientation."},
    {"time": "01:30 PM", "duration": "90 Min", "title": "Lunch with Buddy", "desc": "Lunch and informal interaction with assigned buddy."},
    {"time": "03:00 PM", "duration": "60 Min", "title": "HR Policies & HRMS", "desc": "Introduction to HR processes, perks, benefits, HRMS navigation."},
    {"time": "04:00 PM", "duration": "30 Min", "title": "Docs & Compliance", "desc": "Complete statutory forms and finalize onboarding documents."},
    {"time": "04:30 PM", "duration": "15 Min", "title": "Evening Break", "desc": "Tea/Coffee break."},
    {"time": "04:45 PM", "duration": "60 Min", "title": "POSH Training", "desc": "Mandatory Prevention of Sexual Harassment awareness session."},
    {"time": "05:45 PM", "duration": "30 Min", "title": "HRBP Connect", "desc": "Discussion with HRBP on role expectations, next steps."},
]

# ----------------------------
# 4. CSS STYLES (Streamlit Container)
# ----------------------------
st.markdown("""
<style>
    :root {
        --fb-blue: #194CFF;
        --fb-dark: #0A0A0A;
    }
    .block-container { 
        padding: 0 !important; 
        max-width: 100% !important; 
    }
    header, footer { display: none !important; }
    .stApp { 
        background-color: var(--fb-dark);
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(25, 76, 255, 0.08), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(25, 76, 255, 0.05), transparent 25%);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 5. GENERATE SLIDES HTML
# ----------------------------
slides_html = ""
for idx, item in enumerate(agenda_items, start=1):
    
    # Load slide image (1.png, 2.png...)
    img_src = get_image_base64(idx)
    if not img_src:
        img_src = "https://img.icons8.com/fluency/240/image-file.png" # Fallback

    slides_html += f"""
    <div class="swiper-slide">
        <div class="glass-card">
            <div class="glow-effect"></div>
            <div class="card-content">
                
                <div class="time-header">
                    {item['time']}
                </div>
                
                <div class="visual-container">
                    <img src="{img_src}" alt="Slide {idx}" />
                </div>

                <div class="text-content">
                    <h3>{item['title']}</h3>
                    <p>{item['desc']}</p>
                    <div class="duration-footer">
                        ⏱ {item['duration']}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

# ----------------------------
# 6. RESPONSIVE HTML COMPONENT
# ----------------------------
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    :root {{
        --fb-blue: #194CFF;
        --fb-dark: #0A0A0A;
        --fb-card-bg: rgba(255, 255, 255, 0.03);
        --fb-border: rgba(255, 255, 255, 0.1);
        --text-main: #FFFFFF;
        --text-muted: #9CA3AF;
    }}

    body {{
        margin: 0; padding: 0;
        font-family: 'Inter', sans-serif;
        background-color: var(--fb-dark);
        color: var(--text-main);
        overflow: hidden;
        height: 100vh; width: 100vw;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }}

    /* --- RESPONSIVE HEADER --- */
    .brand-header {{
        position: absolute; top: 20px; left: 24px; z-index: 50;
        display: flex; align-items: center; gap: 12px;
    }}
    
    .brand-logo-img {{
        height: 32px; /* Default height */
        width: auto;
        object-fit: contain;
    }}

    .header-text {{
        font-size: 14px; 
        color: rgba(255,255,255,0.6); 
        border-left: 1px solid rgba(255,255,255,0.2); 
        padding-left: 12px;
        white-space: nowrap;
    }}

    /* --- SWIPER LAYOUT --- */
    .swiper {{ width: 100%; height: 100%; padding-top: 80px; padding-bottom: 40px; box-sizing: border-box; }}
    
    /* Default Slide (Desktop) */
    .swiper-slide {{
        width: 320px; height: 500px;
        transition: all 0.5s ease;
        opacity: 0.4; transform: scale(0.9);
        filter: blur(2px) grayscale(100%);
    }}

    .swiper-slide-active {{
        opacity: 1; transform: scale(1);
        filter: blur(0) grayscale(0%);
        z-index: 20;
    }}

    /* --- CARD STYLING --- */
    .glass-card {{
        width: 100%; height: 100%; border-radius: 24px;
        position: relative; background: var(--fb-card-bg);
        border: 1px solid var(--fb-border);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        overflow: hidden; transition: all 0.4s ease;
    }}

    .swiper-slide-active .glass-card {{
        border-color: rgba(25, 76, 255, 0.5);
        box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 40px rgba(25, 76, 255, 0.15);
    }}

    .glow-effect {{
        position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle at 50% 50%, rgba(25, 76, 255, 0.15), transparent 60%);
        opacity: 0; transition: opacity 0.5s ease; pointer-events: none;
    }}
    .swiper-slide-active .glow-effect {{ opacity: 1; }}

    .card-content {{
        position: relative; z-index: 2; height: 100%; padding: 24px;
        box-sizing: border-box; display: flex; flex-direction: column;
        justify-content: space-between;
    }}

    /* --- TYPOGRAPHY & CONTENT --- */
    .time-header {{
        text-align: center;
        font-size: 22px; 
        font-weight: 700;
        color: var(--fb-blue);
        margin-bottom: 5px;
    }}

    .visual-container {{
        flex: 1; display: flex; align-items: center; justify-content: center;
        margin: 5px 0; transform: scale(0.9); transition: transform 0.6s ease;
    }}
    .visual-container img {{
        max-width: 90%; max-height: 200px;
        object-fit: contain;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.3));
    }}
    .swiper-slide-active .visual-container {{ transform: scale(1.05); }}

    .text-content {{ text-align: center; }}

    h3 {{ margin: 0 0 8px 0; font-size: 20px; font-weight: 700; color: #fff; line-height: 1.2; }}
    p {{ margin: 0 0 10px 0; font-size: 13px; line-height: 1.4; color: var(--text-muted); }}

    .duration-footer {{
        font-size: 12px;
        color: rgba(255, 255, 255, 0.5);
        font-weight: 600;
        padding-top: 8px;
        border-top: 1px solid rgba(255,255,255,0.1);
        display: inline-block; width: 100%;
    }}

    .swiper-pagination {{ bottom: 15px !important; }}
    .swiper-pagination-bullet {{ background: rgba(255,255,255,0.2); opacity: 1; width: 6px; height: 6px; }}
    .swiper-pagination-bullet-active {{ background: var(--fb-blue); width: 24px; border-radius: 4px; }}

    /* --- MEDIA QUERIES FOR RESPONSIVENESS --- */

    /* Mobile Devices (Portrait) */
    @media (max-width: 480px) {{
        .brand-header {{ top: 15px; left: 15px; gap: 8px; }}
        .brand-logo-img {{ height: 24px; }}
        .header-text {{ font-size: 12px; padding-left: 8px; }}

        .swiper {{ padding-top: 60px; padding-bottom: 40px; }}
        .swiper-slide {{ width: 260px; height: 420px; }} /* Smaller Card */
        
        .card-content {{ padding: 20px; }}
        .time-header {{ font-size: 18px; }}
        h3 {{ font-size: 18px; }}
        p {{ font-size: 12px; }}
        .visual-container img {{ max-height: 150px; }}
    }}

    /* Tablet Devices */
    @media (min-width: 481px) and (max-width: 1024px) {{
        .swiper-slide {{ width: 300px; height: 460px; }}
    }}

  </style>
</head>
<body>

  <div class="brand-header">
    <img src="{logo_src}" class="brand-logo-img" alt="Logo" />
    <div class="header-text">Onboarding Plan</div>
  </div>

  <div class="swiper mySwiper">
    <div class="swiper-wrapper">
      {slides_html}
    </div>
    <div class="swiper-pagination"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
  <script>
    var swiper = new Swiper(".mySwiper", {{
      effect: "coverflow",
      grabCursor: true,
      centeredSlides: true,
      slidesPerView: "auto",
      loop: false,
      speed: 800,
      autoplay: {{
        delay: 3000,
        disableOnInteraction: false,
        stopOnLastSlide: true,
      }},
      coverflowEffect: {{
        rotate: 0,
        stretch: 0,
        depth: 150,
        modifier: 1,
        slideShadows: false,
      }},
      pagination: {{
        el: ".swiper-pagination",
        clickable: true
      }},
    }});
  </script>
</body>
</html>
"""

components.html(html_code, height=800, scrolling=False)