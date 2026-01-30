import streamlit as st
import random

# --- 1. AYARLAR VE SAHTE VERİ TABANI ---
st.set_page_config(page_title="AI Love Match", page_icon="💘", layout="wide")

# Gerçek bir uygulamada burası bir SQL veritabanı olurdu.
# Şimdilik "mock" (sahte) verilerle çalışıyoruz.
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


# --- 2. FONKSİYONLAR ---

def ai_bio_generator(name, interests):
    """
    Basit bir kural tabanlı yapay zeka simülasyonu.
    Gerçek uygulamada buraya Gemini veya GPT API bağlanır.
    """
    templates = [
        f"Selam ben {name}! {', '.join(interests)} konularına bayılırım. Benimle bu konuları konuşmaya ne dersin?",
        f"{name} burada! Hayat mottom: {interests[0]} ve {interests[-1]}.",
        f"Enerjik, {interests[0]} tutkunu ve {interests[1]} aşığı. Ben {name}, tanışalım mı?"
    ]
    return random.choice(templates)


def calculate_match_score(user_interests, candidate_interests):
    """
    İki kişinin ilgi alanlarını karşılaştırıp %0-100 arası skor üretir.
    """
    set_user = set(user_interests)
    set_candidate = set(candidate_interests)

    # Ortak ilgi alanlarını bul
    intersection = set_user.intersection(set_candidate)

    # Skor mantığı: Her ortak ilgi alanı 33 puan (Maks 100)
    score = len(intersection) * 33

    # Bonus: Tamamen alakasızsa bile %10 şans ver (Aşkın tesadüfleri!)
    if score == 0:
        score = 10
    if score > 100:
        score = 100

    return score, list(intersection)


# --- 3. ARAYÜZ TASARIMI (UI) ---

st.title("💘 AI Love Match: Yapay Zeka Destekli Eşleşme")

# Sol Panel: Kullanıcı Profili
with st.sidebar:
    st.header("Profilini Oluştur")
    my_name = st.text_input("Adın", "Misafir")
    my_gender = st.selectbox("Cinsiyetin", ["Erkek", "Kadın", "Belirtmek İstemiyorum"])
    target_gender = st.selectbox("Kimi Arıyorsun?", ["Kadın", "Erkek", "Herkes"])

    # İlgi Alanları
    all_interests = ["Yazılım", "Fitness", "Müzik", "Seyahat", "Kitap", "Sinema", "Oyun", "Sanat", "Yemek", "Kamp",
                     "Kahve", "Fotoğrafçılık"]
    my_interests = st.multiselect("İlgi Alanların (En az 1 tane seç)", all_interests, default=["Müzik", "Seyahat"])

    # AI Bio Butonu
    if st.button("✨ Yapay Zekaya Biyografi Yazdır"):
        if my_interests:
            generated_bio = ai_bio_generator(my_name, my_interests)
            st.success("YZ Senin İçin Yazdı:")
            st.info(f"Draft: {generated_bio}")
        else:
            st.warning("Lütfen önce ilgi alanı seç.")

# Ana Ekran: Eşleşmeler
st.header(f"Selam {my_name}, İşte Sana En Uygun Adaylar!")
st.write("Yapay zeka algoritmamız ilgi alanlarına göre uyumluluk analizi yapıyor...")
st.divider()

if not my_interests:
    st.warning("Eşleşmeleri görmek için sol taraftan ilgi alanlarını seçmelisin!")
else:
    # Eşleşme Mantığı
    matches = []
    for user in MOCK_USERS:
        # Cinsiyet Filtresi
        if target_gender != "Herkes" and user["gender"] != target_gender:
            continue

        score, common_tags = calculate_match_score(my_interests, user["interests"])
        user["score"] = score
        user["common"] = common_tags
        matches.append(user)

    # Skora göre sırala (Yüksekten düşüğe)
    matches = sorted(matches, key=lambda x: x["score"], reverse=True)

    # Eşleşmeleri Göster
    col1, col2, col3 = st.columns(3)

    for i, match in enumerate(matches):
        # Kartları 3 sütuna dağıt
        with [col1, col2, col3][i % 3]:
            st.image(match["img"], width=150)
            st.subheader(f"{match['name']}, {match['age']}")

            # Skor Barı
            st.progress(match["score"])
            st.caption(f"Uyum Skoru: %{match['score']}")

            st.write(
                f"**Ortak Noktalar:** {', '.join(match['common']) if match['common'] else 'Zıt kutuplar birbirini çeker!'}")
            st.button(f"Sohbet Et ({match['name']})", key=i)
            st.divider()