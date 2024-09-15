import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Cosine benzerliğine dayalı tahmin fonksiyonu
def tahmini_puani_hesapla(df, kullanici, urun, kullanici_benzerlikleri):
    diger_kullanici_puanlari = df[urun]
    puanlanmis_kullanicilar = diger_kullanici_puanlari[diger_kullanici_puanlari.notnull()].index

    pay = sum(kullanici_benzerlikleri[puanlanmis_kullanicilar] * diger_kullanici_puanlari[puanlanmis_kullanicilar])
    payda = sum(kullanici_benzerlikleri[puanlanmis_kullanicilar])

    if payda == 0:
        return None

    tahmini_puan = pay / payda
    return round(tahmini_puan, 2)

# Ana işlev
def tahmin_al(user_4_product_2, user_4_product_3):
    veriler = {
        'Ürün 1': [None, 6, 5, None],
        'Ürün 2': [5, 7, None, None],
        'Ürün 3': [8, None, 6, None],
        'Ürün 4': [None, 4, 8, None]
    }

    df = pd.DataFrame(veriler, index=['Kullanıcı 1', 'Kullanıcı 2', 'Kullanıcı 3', 'Kullanıcı 4'])

    # Kullanıcı 4'ün değerlendirme skorlarını ekleyelim
    df.loc['Kullanıcı 4', 'Ürün 2'] = user_4_product_2
    df.loc['Kullanıcı 4', 'Ürün 3'] = user_4_product_3

    # Boş değerleri 0 ile dolduralım
    doldurulmus_df = df.fillna(0)

    # Kullanıcılar arası benzerliği hesaplayalım
    kullanici_benzerligi = cosine_similarity(doldurulmus_df)
    kullanici_benzerlik_df = pd.DataFrame(kullanici_benzerligi, index=df.index, columns=df.index)

    # Tahmini puanı hesaplayalım
    kullanici_benzerlikleri = kullanici_benzerlik_df.loc['Kullanıcı 4']
    tahmini_puan = tahmini_puani_hesapla(df, 'Kullanıcı 4', 'Ürün 4', kullanici_benzerlikleri)

    return df, tahmini_puan

# Streamlit başlığı ve açıklama
st.title("Ürün Değerlendirme Tahmin Aracı")
st.write("""
Bu araç, diğer kullanıcıların değerlendirmelerine ve sizin verdiğiniz puanlara dayanarak **Ürün 4** için tahmini puanınızı hesaplar.
Tahmin edilen puan, diğer kullanıcıların benzerliklerine ve verdikleri puanlara göre belirlenir.
""")

# Kullanıcıdan puan girişi alalım
user_4_product_2 = st.slider("Ürün 2 için puanınızı girin:", 0, 10, 5)
user_4_product_3 = st.slider("Ürün 3 için puanınızı girin:", 0, 10, 5)

# Tahmini değerlendirme sonucunu gösterelim
if st.button('Tahmini Puanı Hesapla'):
    df, tahmini_puan = tahmin_al(user_4_product_2, user_4_product_3)

    if tahmini_puan:
        # Tahmin edilen puanı tabloya ekleyelim
        df.loc['Kullanıcı 4', 'Ürün 4'] = f"**{tahmini_puan} (Tahmin)**"
        
        # Tahmin edilen puan ile birlikte tabloyu gösterelim
        st.write("Tahmin edilen puanı içeren tablo:")
        st.table(df)

        # Ayrıntılı açıklama
        st.write(f"""
        **Tahmini Puanın Anlamı**:
        Tahmin edilen puan olan **{tahmini_puan}**, sizin diğer ürünler için verdiğiniz puanlar ile diğer kullanıcıların benzerliklerine dayanır.
        Bu benzerlik, kullanıcıların ürünler için verdikleri puanların ne kadar benzer olduğunu ölçer. Bu puan sizin bu ürünü ne kadar beğenebileceğinizin tahmin değeridir.
        
        Cosine benzerliği kullanılarak, her kullanıcının verdiği puanlar arasındaki benzerlik bulunur.
        Daha önce **Ürün 2** ve **Ürün 3** için verdiğiniz puanlar, diğer kullanıcıların aynı ürünlere verdiği puanlarla karşılaştırılır.
        Benzerlik ne kadar yüksekse, o kullanıcının değerlendirmeleri sizin tahmin edilen puanınıza o kadar çok katkı sağlar.
        """)
    else:
        st.warning("Tahmin yapılamadı. Daha fazla veri girmeniz gerekebilir.")
