import streamlit as st
from PIL import Image
import io
import zipfile

# Suporte a HEIC
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    st.error("Instale o pacote 'pillow-heif' com: pip install pillow-heif")

# --- Configurações iniciais ---
st.set_page_config(page_title="Conversor HEIC para PNG", page_icon="🖼️", layout="centered")

st.title("🖼️ Conversor HEIC → PNG")
st.write("Envie **uma ou várias** imagens `.heic` e baixe todas convertidas em `.png` num arquivo ZIP.")

# Upload de múltiplos arquivos
uploaded_files = st.file_uploader(
    "Escolha suas imagens HEIC", 
    type=["heic"], 
    accept_multiple_files=True
)

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for file in uploaded_files:
            try:
                image = Image.open(file)
                png_buffer = io.BytesIO()
                image.save(png_buffer, format="PNG")
                png_filename = file.name.replace(".heic", ".png").replace(".HEIC", ".png")
                zipf.writestr(png_filename, png_buffer.getvalue())
            except Exception as e:
                st.error(f"Erro ao converter {file.name}: {e}")

    # Exibir miniaturas das imagens
    st.subheader("Prévia das imagens convertidas:")
    cols = st.columns(min(3, len(uploaded_files)))
    for i, file in enumerate(uploaded_files):
        try:
            img = Image.open(file)
            with cols[i % len(cols)]:
                st.image(img, caption=file.name, use_column_width=True)
        except:
            pass

    # Finaliza o ZIP
    zip_buffer.seek(0)

    # Botão de download do ZIP
    st.download_button(
        label="📦 Baixar todas em ZIP",
        data=zip_buffer,
        file_name="imagens_convertidas.zip",
        mime="application/zip"
    )

    st.success("Conversão concluída com sucesso ✅")
else:
    st.info("Envie uma ou mais imagens HEIC para começar.")
