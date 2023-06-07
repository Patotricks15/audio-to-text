import streamlit as st
from pydub import AudioSegment
import speech_recognition as sr
import io
from docx import Document
import os


def mp3_to_text(mp3_file):
    # Carregar o arquivo MP3
    audio = AudioSegment.from_file(mp3_file, format="mp3")

    # Converter o áudio para WAV
    wav_data = io.BytesIO()
    audio.export(wav_data, format="wav")
    wav_data.seek(0)

    # Transcrição do áudio WAV
    r = sr.Recognizer()
    with sr.AudioFile(wav_data) as source:
        audio_text = r.record(source)

    return r.recognize_google(audio_text, language='pt-BR')

def gerar_docx(texto_transcrito):
    document = Document()
    paragraph = document.add_paragraph(texto_transcrito)
    document.save('transcricao.docx')

# Configurações da página do Streamlit
st.title("Transcrição de Áudio para DOCX")
st.write("Faça o upload de um arquivo MP3 para transcrição")

# Upload do arquivo MP3
audio_file = st.file_uploader("Selecione o arquivo MP3", type=["mp3"])

if audio_file is not None:
    # Transcrever o áudio e exibir o texto transcrito
    st.write("Transcrevendo o áudio...")
    texto_transcrito = mp3_to_text(audio_file)

    # Gerar o arquivo DOCX
    st.write("Gerando o arquivo DOCX...")
    gerar_docx(texto_transcrito)

    # Download do arquivo DOCX
    st.download_button("Clique aqui para baixar o arquivo DOCX", data=open('transcricao.docx', 'rb'), file_name="transcricao.docx")
