import streamlit as st
import yt_dlp
import os
import requests
from bs4 import BeautifulSoup
import base64

st.set_page_config(page_title="FLAC Downloader Pro", page_icon="🎵")

st.title("🎵 FLAC Downloader")
st.markdown("Baixe músicas em alta fidelidade (FLAC) a partir de links do YouTube, Spotify ou Apple Music.")

url = st.text_input("Cole o link da música aqui:", placeholder="https://...")

def get_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:file/flac;base64,{b64}" download="{os.path.basename(file_path)}">⬇️ Clique aqui para baixar o arquivo</a>'

if st.button("Processar e Baixar"):
    if url:
        with st.spinner("Extraindo áudio e convertendo... Isso pode levar um minuto."):
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'flac', 'preferredquality': '0'}],
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True
            }
            
            target_url = url
            if "music.apple.com" in url:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find('meta', property='og:title')['content']
                    target_url = f"ytsearch1:{title} audio"
                except: target_url = f"ytsearch1:{url}"

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(target_url, download=True)
                    if 'entries' in info: info = info['entries'][0]
                    file_name = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".flac"
                    
                    st.success(f"✅ Pronto: {info.get('title')}")
                    st.markdown(get_download_link(file_name), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro: {e}")
    else:
        st.warning("Por favor, insira um link.")
