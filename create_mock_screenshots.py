import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size):
    # Standard Windows Malgun Gothic font path
    font_path = "C:\\Windows\\Fonts\\malgun.ttf"
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()

def create_overview():
    width, height = 1000, 650
    # Background slate color
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Soft background radial glow simulation (draw circular layers)
    for r in range(500, 0, -20):
        alpha = int((1 - r/500) * 20)
        draw.ellipse([50-r/10, 50-r/10, 50+r/10, 50+r/10], fill=(139, 92, 246, alpha))
        draw.ellipse([900-r/10, 600-r/10, 900+r/10, 600+r/10], fill=(16, 185, 129, alpha))
        
    # Main Header border & active light
    draw.rectangle([20, 20, 980, 80], fill=(30, 41, 59, 180), outline=(255, 255, 255, 20), width=1)
    draw.ellipse([45, 45, 57, 57], fill=(34, 197, 94, 255)) # Green glow active dot
    draw.text((70, 39), "Cenciel AI Brand-Ops OS", font=get_font(20), fill=(255, 255, 255, 255))
    draw.text((800, 43), "Cenciel AI Active  ●", font=get_font(14), fill=(34, 197, 94, 255))
    
    # Pipe main diagram panel
    draw.rectangle([50, 150, 950, 550], fill=(30, 41, 59, 100), outline=(255, 255, 255, 10), width=1)
    
    draw.text((100, 190), "Cenciel AI Pipeline Overview", font=get_font(24), fill=(255, 255, 255, 255))
    draw.text((100, 230), "단 한 번의 입력으로 화장품 브랜드 마케팅 자료를 속성으로 작문합니다.", font=get_font(14), fill=(148, 163, 184, 255))
    
    # Intertwined steps
    steps = [
        ("Step 1. Market Radar", "시장 경쟁 리포트 및 트렌드 성분 분석", (100, 300, 320, 460), (139, 92, 246)),
        ("Step 2. VOC Insights", "소비자 정량 평점 및 성성 불편 탐지", (380, 300, 600, 460), (16, 185, 129)),
        ("Step 3. Copywriter", "멀티 채널 카드뉴스 및 포스팅 구성", (660, 300, 880, 460), (139, 92, 246))
    ]
    
    for title, desc, coords, color in steps:
        draw.rectangle(list(coords), fill=(30, 41, 59, 200), outline=color + (150,), width=2)
        draw.text((coords[0] + 20, coords[1] + 25), title, font=get_font(16), fill=(255,255,255,255))
        # Word wrap desc
        draw.text((coords[0] + 20, coords[1] + 70), desc[:11], font=get_font(12), fill=(148, 163, 184, 255))
        draw.text((coords[0] + 20, coords[1] + 95), desc[11:], font=get_font(12), fill=(148, 163, 184, 255))
        
    os.makedirs("static/images", exist_ok=True)
    img.save("static/images/01_overview.png")

def create_step1():
    width, height = 1000, 650
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Header bar
    draw.rectangle([20, 20, 980, 80], fill=(30, 41, 59, 180), outline=(255, 255, 255, 20), width=1)
    draw.text((70, 39), "Step 1. Market Radar (시장 트렌드 분석)", font=get_font(20), fill=(255, 255, 255, 255))
    
    # Left Input column
    draw.rectangle([50, 120, 400, 580], fill=(30, 41, 59, 100), outline=(255, 255, 255, 10), width=1)
    draw.text((80, 160), "1단계 시장 입력", font=get_font(18), fill=(255, 255, 255, 255))
    draw.rectangle([80, 220, 370, 270], fill=(15, 23, 42, 255), outline=(139, 92, 246, 120), width=1)
    draw.text((100, 232), "비비크림", font=get_font(15), fill=(255, 255, 255, 255))
    
    # Search Button
    draw.rectangle([80, 300, 370, 350], fill=(139, 92, 246, 255), outline=None)
    draw.text((140, 312), "시장 레이더 가동하기", font=get_font(15), fill=(255, 255, 255, 255))
    
    # Right Results column
    draw.rectangle([430, 120, 950, 580], fill=(30, 41, 59, 180), outline=(255, 255, 255, 10), width=1)
    draw.text((470, 160), "비비크림 트렌드 분석 보고서", font=get_font(20), fill=(167, 139, 250, 255))
    
    # Tag list box
    draw.text((470, 210), "✔ 주요 트렌드 연계 키워드:", font=get_font(14), fill=(255, 255, 255, 255))
    tags = ["비비크림 추천", "재생 비비", "커버력 좋은 비비", "톤업 크림", "EWG 그린등급"]
    x_off = 470
    for tag in tags:
        draw.rectangle([x_off, 245, x_off + len(tag)*13 + 12, 275], fill=(139, 92, 246, 60), outline=(139, 92, 246, 120))
        draw.text((x_off + 6, 250), tag, font=get_font(12), fill=(186, 230, 253, 255))
        x_off += len(tag)*13 + 22
        
    # Competitor USP List
    draw.text((470, 310), "✔ 경쟁사 핵심 마케팅 강점(USP) 요약:", font=get_font(14), fill=(255, 255, 255, 255))
    usps = [
        ("피부과 처방 성분", "병풀 정량 추출물과 판테놀 함유로 메이크업 진정 레이어 형성"),
        ("번들거림 프리 장벽", "오일 흡착 다크닝 방지 파우더 공법으로 12시간 톤업 지속성 제공")
    ]
    y_off = 350
    for title, desc in usps:
        draw.rectangle([470, y_off, 910, y_off + 70], fill=(255, 255, 255, 5), outline=(255, 255, 255, 15))
        draw.text((490, y_off + 12), title, font=get_font(14), fill=(255, 255, 255, 255))
        draw.text((490, y_off + 38), desc, font=get_font(11), fill=(148, 163, 184, 255))
        y_off += 90
        
    img.save("static/images/02_market_radar.png")

def create_step2():
    width, height = 1000, 650
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Header bar
    draw.rectangle([20, 20, 980, 80], fill=(30, 41, 59, 180), outline=(255, 255, 255, 20), width=1)
    draw.text((70, 39), "Step 2. VOC Insights (소비자 목소리 정량/정성 진단)", font=get_font(20), fill=(255, 255, 255, 255))
    
    # Left Input Column (Upload and raw box)
    draw.rectangle([50, 120, 420, 580], fill=(30, 41, 59, 100), outline=(255, 255, 255, 10), width=1)
    draw.text((80, 150), "정형/비정형 소비자 의견 입력", font=get_font(18), fill=(255, 255, 255, 255))
    
    # Text area Simulator
    draw.rectangle([80, 200, 390, 340], fill=(15, 23, 42, 255), outline=(255, 255, 255, 20), width=1)
    draw.text((95, 215), "화장이 전반적으로 너무 겉돌고", font=get_font(13), fill=(148, 163, 184, 255))
    draw.text((95, 240), "밀려서 쓸 수가 없네요. 다크닝도...", font=get_font(13), fill=(148, 163, 184, 255))
    
    # Buttons
    draw.rectangle([80, 360, 390, 410], fill=(16, 185, 129, 255), outline=None)
    draw.text((145, 372), "텍스트 분석 실행하기", font=get_font(15), fill=(255, 255, 255, 255))
    
    # Excel Upload area
    draw.rectangle([80, 440, 390, 540], fill=(255, 255, 255, 5), outline=(255, 255, 255, 15))
    draw.text((130, 470), "📁 EXCEL/CSV 파일 업로드", font=get_font(13), fill=(148, 163, 184, 255))
    draw.text((120, 495), "마우스로 드래그 앤 드롭 하세요.", font=get_font(11), fill=(100, 116, 139, 255))
    
    # Right Results Column
    draw.rectangle([450, 120, 950, 580], fill=(30, 41, 59, 180), outline=(255, 255, 255, 10), width=1)
    draw.text((490, 150), "VOC 피드백 및 고유 소구점 제안", font=get_font(20), fill=(52, 211, 153, 255))
    
    # Pain point Red label
    draw.text((490, 195), "✔ 도출된 핵심 소비자 Pain Point:", font=get_font(13), fill=(255, 255, 255, 255))
    draw.rectangle([490, 225, 910, 275], fill=(244, 63, 94, 20), outline=(244, 63, 94, 90))
    draw.text((510, 237), "🚨 제형/밀림: 화장 밀림 현상 발생 및 다크닝 잔존 (위험 지수: 4.5)", font=get_font(13), fill=(244, 63, 94, 255))
    
    # Selling Point Green recommendation
    draw.text((490, 310), "✔ AI 마케팅 소구점 처방 (클릭 시 3단계 카피연동):", font=get_font(13), fill=(255, 255, 255, 255))
    draw.rectangle([490, 340, 910, 390], fill=(16, 185, 129, 20), outline=(16, 185, 129, 120))
    draw.text((510, 352), "📢 🎯 \"메이크업 전 밀림 없는 가성비 초소량 속보습 비비크림\"", font=get_font(13), fill=(52, 211, 153, 255))
    
    # Star distribution
    draw.text((490, 430), "✔ 평점 분포 통계:", font=get_font(13), fill=(255, 255, 255, 255))
    stars = [("5★", 80), ("4★", 40), ("3★", 20)]
    y_star = 460
    for star, val in stars:
        draw.text((490, y_star), star, font=get_font(12), fill=(148, 163, 184, 255))
        draw.rectangle([530, y_star + 4, 750, y_star + 14], fill=(15, 23, 42, 255), outline=None)
        draw.rectangle([530, y_star + 4, 530 + val * 2, y_star + 14], fill=(16, 185, 129, 255), outline=None)
        draw.text((770, y_star), f"{val}%", font=get_font(12), fill=(255, 255, 255, 255))
        y_star += 30
        
    img.save("static/images/03_voc_insights.png")

def create_step3():
    width, height = 1000, 650
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Header bar
    draw.rectangle([20, 20, 980, 80], fill=(30, 41, 59, 180), outline=(255, 255, 255, 20), width=1)
    draw.text((70, 39), "Step 3. Copywriter (멀티채널 광고 카피라이팅)", font=get_font(20), fill=(255, 255, 255, 255))
    
    # Left Input Column (Selling Point display)
    draw.rectangle([50, 120, 450, 182], fill=(30, 41, 59, 100), outline=(255, 255, 255, 10), width=1)
    draw.text((70, 131), "선택된 핵심 마케팅 소구점", font=get_font(12), fill=(148, 163, 184, 255))
    draw.text((70, 149), "메이크업 전 밀림 없는 가성비 초소량 속보습 비비크림", font=get_font(13), fill=(255, 255, 255, 255))
    
    # Left Mobile simulator frame
    draw.rectangle([50, 200, 450, 580], fill=(30, 41, 59, 100), outline=(255, 255, 255, 10), width=1)
    draw.text((75, 215), "📱 Instagram 카드뉴스 슬라이드 시뮬레이터", font=get_font(14), fill=(167, 139, 250, 255))
    
    # Phone screen shape
    draw.rectangle([135, 250, 365, 520], fill=(2, 6, 23, 255), outline=(71, 85, 105, 255), width=3)
    draw.text((145, 260), "Cenciel_Official", font=get_font(8), fill=(148, 163, 184, 255))
    
    # Active slide content area
    draw.rectangle([145, 280, 355, 450], fill=(15, 23, 42, 255), outline=(139, 92, 246, 80), width=1)
    draw.text((155, 295), "Slide 1. 표지 타이틀", font=get_font(12), fill=(139, 92, 246, 255))
    # Write Korean card title
    draw.text((155, 335), "메이크업 전 밀림 ZERO!", font=get_font(13), fill=(255, 255, 255, 255))
    draw.text((155, 360), "하루 종일 들뜨지 않는 보습막", font=get_font(10), fill=(148, 163, 184, 255))
    
    # Interactive Dots
    draw.ellipse([240, 480, 244, 484], fill=(139, 92, 246, 255))
    draw.ellipse([249, 480, 253, 484], fill=(100, 116, 139, 255))
    draw.ellipse([258, 480, 262, 484], fill=(100, 116, 139, 255))
    
    # Right Results Area
    draw.rectangle([470, 120, 950, 580], fill=(30, 41, 59, 180), outline=(255, 255, 255, 10), width=1)
    
    # Horizontal tabs (Instagram, Naver Blog, Shorts Script)
    draw.rectangle([490, 140, 600, 175], fill=(139, 92, 246, 255), outline=None)
    draw.text((505, 149), "인스타그램", font=get_font(13), fill=(255, 255, 255, 255))
    
    draw.rectangle([610, 140, 720, 175], fill=(15, 23, 42, 255), outline=(255, 255, 255, 15))
    draw.text((630, 149), "네이버 블로그", font=get_font(13), fill=(148, 163, 184, 255))
    
    # Caption Preview
    draw.rectangle([490, 195, 920, 540], fill=(15, 23, 42, 255), outline=(255, 255, 255, 20))
    draw.text((510, 215), "✨ 화장 대참사 탈출! 밀림 없는 재생비비 꿀템 대공개 ✨", font=get_font(13), fill=(255, 255, 255, 255))
    draw.text((510, 255), "메이크업 전만 되면 밀리거나 떠서 화장 다 밀려나갔던 분들 주목!", font=get_font(12), fill=(148, 163, 184, 255))
    draw.text((510, 280), "센시엘 비비크림 하나면 겉돌거나 건조함 걱정 끝! 🌿 #파데프리", font=get_font(12), fill=(148, 163, 184, 255))
    
    img.save("static/images/04_copywriter.png")

if __name__ == "__main__":
    create_overview()
    create_step1()
    create_step2()
    create_step3()
    print("Mock screenshots generated successfully!")
