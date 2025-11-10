import streamlit as st
from PIL import Image
import io
import zipfile
import time

# Suporte a HEIC
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    st.error("Instale o pacote 'pillow-heif' com: pip install pillow-heif")

# --- Configurações iniciais ---
st.set_page_config(page_title="Conversor HEIC → PNG", page_icon="🖼️", layout="centered")

st.title("🖼️ Conversor HEIC → PNG")
st.write("Envie **uma ou várias** imagens `.heic` e baixe todas convertidas em `.png` dentro de um arquivo ZIP.")

# Upload de múltiplos arquivos
uploaded_files = st.file_uploader(
    "Escolha suas imagens HEIC",
    type=["heic"],
    accept_multiple_files=True
)

if uploaded_files:
    total = len(uploaded_files)
    st.info(f"🔄 {total} arquivo(s) enviado(s). Iniciando conversão...")

    # Barra de progresso
    progress_bar = st.progress(0)
    status_text = st.empty()

    zip_buffer = io.BytesIO()
    converted_count = 0

    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for i, file in enumerate(uploaded_files):
            try:
                image = Image.open(file)
                png_buffer = io.BytesIO()
                image.save(png_buffer, format="PNG")

                png_filename = file.name.replace(".heic", ".png").replace(".HEIC", ".png")
                zipf.writestr(png_filename, png_buffer.getvalue())

                converted_count += 1
                progress = int((i + 1) / total * 100)
                progress_bar.progress(progress)
                status_text.text(f"✅ Convertendo ({i+1}/{total}) - {file.name}")

            except Exception as e:
                st.error(f"❌ Erro ao converter {file.name}: {e}")
                continue

            # Pequeno delay opcional pra suavizar o feedback visual
            time.sleep(0.05)

    # Exibir resumo
    st.success(f"🎉 Conversão concluída! {converted_count}/{total} arquivos convertidos com sucesso.")
    status_text.text("Pronto! Você pode baixar o arquivo ZIP abaixo 👇")

    # Finaliza o ZIP
    zip_buffer.seek(0)

    # Botão de download
    st.download_button(
        label="📦 Baixar todas em ZIP",
        data=zip_buffer,
        file_name="imagens_convertidas.zip",
        mime="application/zip"
    )
else:
    st.info("📂 Envie uma ou mais imagens HEIC para começar.")
