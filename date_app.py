import streamlit as st
import google.generativeai as genai

# --- AYARLAR ---
st.set_page_config(page_title="AI Love Match", page_icon="💘", layout="wide")

# --- SAHTE VERİ TABANI ---
MOCK_USERS = [
    {"name": "Ayşe", "age": 22, "gender": "Kadın", "interests": ["Müzik", "Seyahat", "Kahve"],
     "img": "https://randomuser.me/api/portraits/women/44.jpg"},
    {"name": "Berk", "age": 24, "gender": "Erkek", "interests": ["Yazılım", "Oyun", "Fitness"],
     "img": "https://randomuser.me/api/portraits/men/32.jpg"},
    {"name": "Ceren", "age": 21, "gender": "Kadın", "interests": ["Sanat", "Fitness", "Fotoğrafçılık"],
     "img": "https://randomuser.me/api/portraits/women/65.jpg"},
    {"name": "Deniz", "age": 25, "gender": "Erkek", "interests": ["Müzik", "Kamp", "Yemek"],
     "img": "https://randomuser.me/api/portraits/men/85.jpg"},
    {"name": "Elif", "age": 23, "gender": "Kadın", "interests": ["Yazılım", "Kitap", "Sinema"],
     "img": "https://randomuser.me/api/portraits/women/22.jpg"},
]


# --- GEMINI AI FONKSİYONU ---
def get_gemini_response(api_key, name, interests, gender):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Sen bir flört uygulaması uzmanısın. Aşağıdaki kişi için çok havalı, 
        biraz flörtöz ve ilgi çekici kısa bir Instagram biyografisi yaz.

        İsim: {name}
        Cinsiyet: {gender}
        İlgi Alanları: {', '.join(interests)}

        Lütfen emojiler kullan ve samimi ol. Sadece biyografiyi yaz.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Hata: Anahtar yanlış olabilir. ({str(e)})"


# --- ARAYÜZ ---
st.title("💘 AI Love Match: Gerçek Yapay Zeka")

with st.sidebar:
    st.header("🔑 Önce Anahtarı Gir")
    api_key = st.text_input("Google API Key", type="password", help="aistudio.google.com adresinden alabilirsin")
    st.divider()

    st.header("Profilini Oluştur")
    my_name = st.text_input("Adın", "Misafir")
    my_gender = st.selectbox("Cinsiyetin", ["Erkek", "Kadın"])

    all_interests = ["Yazılım", "Fitness", "Müzik", "Seyahat", "Kitap", "Sinema", "Oyun", "Sanat", "Yemek"]
    my_interests = st.multiselect("İlgi Alanların", all_interests, default=["Müzik"])

    if st.button("✨ Yapay Zeka Biyografimi Yazsın!"):
        if not api_key:
            st.error("Lütfen önce en üstteki kutuya API Key yapıştır!")
        elif not my_interests:
            st.warning("İlgi alanı seçmelisin.")
        else:
            with st.spinner("Yapay zeka seni analiz ediyor..."):
                bio = get_gemini_response(api_key, my_name, my_interests, my_gender)
                st.success("İşte Senin Biyografin:")
                st.info(bio)

# Ana Ekran
if not my_interests:
    st.info("👈 Başlamak için soldan profilini doldur.")
else:
    st.subheader("Sana Uygun Adaylar")
    col1, col2, col3 = st.columns(3)
    for i, user in enumerate(MOCK_USERS):
        with [col1, col2, col3][i % 3]:
            st.image(user["img"], width=150)
            st.write(f"**{user['name']}, {user['age']}**")
            st.caption(", ".join(user["interests"]))
            st.divider()
