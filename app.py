
import streamlit as st
import replicate
import os
from PIL import Image
import requests
from io import BytesIO

# Título da página
st.set_page_config(page_title="Lucas Img IA", layout="wide")

# Carregar API Token do secrets.toml
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Layout com duas colunas
col1, col2 = st.columns([1, 2])

with col1:
    st.title("Lucas Img IA")
    st.subheader("Preencha os campos abaixo para gerar uma imagem com IA:")

    prompt = st.text_area("Prompt (descrição da imagem):", height=150)
    negative_prompt = st.text_area("Negative Prompt (o que evitar na imagem):", height=100)

    style = st.radio("Escolha o estilo da imagem:", ["Realista", "Arte digital", "Fotorrealista", "Conceitual"])

    generate_button = st.button("🚀 Gerar Imagem")

with col2:
    image_container = st.empty()
    refresh_placeholder = st.empty()
    download_placeholder = st.empty()

if generate_button and prompt:
    with st.spinner("Gerando imagem..."):
        try:
            version_id = "7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"
            input_payload = {
                "prompt": f"{prompt}, estilo: {style}",
                "negative_prompt": negative_prompt,
                "width": 1024,
                "height": 576,
                "num_inference_steps": 30,
                "guidance_scale": 7
            }

            output = replicate.run(
                f"stability-ai/sdxl:{version_id}",
                input=input_payload
            )

            image_url = output[0]
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            with col2:
                image_container.image(img, caption="Imagem gerada com sucesso!", use_container_width=True)

                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("🔁 Refresh"):
                        st.experimental_rerun()
                with col_btn2:
                    st.download_button("⬇️ Download", data=response.content, file_name="imagem_gerada.png", mime="image/png")

        except Exception as e:
            st.error(f"Erro ao gerar imagem: {e}")
