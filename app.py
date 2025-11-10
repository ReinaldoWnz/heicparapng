import streamlit as st
from PIL import Image
import io

# Importa suporte a HEIC
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    st.error("Instale o pacote 'pillow-heif' com: pip install pillow-heif")

# Configurações iniciais
st.set_page_config(page_title="Conversor HEIC para PNG", page_icon="🖼️", layout="centered")

st.title("🖼️ Conversor HEIC para PNG")
st.write("Envie suas fotos em formato `.heic` e baixe como `.png`.")

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha uma imagem HEIC", type=["heic"])

if uploaded_file:
    try:
        # Abre a imagem HEIC
        image = Image.open(uploaded_file)

        # Mostra prévia
        st.image(image, caption="Prévia da imagem", use_column_width=True)

        # Converte para PNG
        png_buffer = io.BytesIO()
        image.save(png_buffer, format="PNG")
        png_data = png_buffer.getvalue()

        # Download
        st.download_button(
            label="📥 Baixar como PNG",
            data=png_data,
            file_name=uploaded_file.name.replace(".heic", ".png"),
            mime="image/png"
        )

        st.success("Conversão concluída com sucesso ✅")

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
else:
    st.info("Envie uma imagem HEIC para começar.")
