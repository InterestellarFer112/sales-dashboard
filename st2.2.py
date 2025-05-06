import pytesseract
from PIL import Image
import cv2
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import BytesIO
import re
# Configura la ruta de Tesseract si es necesario
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Carga la imagen
# image_path = "ruta_a_tu_imagen.jpg"
# image = cv2.imread(image_path)

# # Preprocesa la imagen (opcional)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convierte a escala de grises
# _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Binarización

# # Extrae texto usando pytesseract
# text = pytesseract.image_to_string(thresh)

# print("Texto extraído:")
# print(text)


st.set_page_config(page_title="OCR con Tesseract", page_icon=":guardsman:", layout="wide")
st.title("Eda Tool")


df = st.file_uploader("Sube una archivo", type=("csv", "xlsx", "png"))


if df:
    try:
    
            if df.name.endswith(".csv"):
                # Procesa el archivo CSV
                df = pd.read_csv(df)
                st.dataframe(df.head())
                numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
                categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()
                st.subheader(f"Tipos de columnas detectadas: {numericas}")
                st.write(f"Tipos de columnas detectadas: {categoricas}")


                st.subheader("Resumen estadístico")

                resume = df.describe(include="all").transpose()
                resume["missing values"] = df.isnull().sum()
                resume["%missing values"] = (resume["missing values"]/ len(df))*100
                st.write(resume)


        
            elif df.name.endswith("xlsx"):
                # df.name.endswith("xlsx")
                df = pd.read_excel(df)

                st.write("Archivo cargado correctamente ✅")
                numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
                categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()
                
                st.write(f"Tipos de columnas detectadas: {numericas}")

                st.write(f"Tipos de columnas detectadas: {categoricas}")


                st.subheader("Resumen estadistico ✅")

                resume = df.describe(include="all").transpose()
                resume["missing values"] =df.isnull().sum()
                resume["%missing values"] = (resume["missing values"]/len(df))*100
                st.write(resume)


            else:
                  df.name.endswith(".png")
                  #  Procesa la imagen con pytesseract
                  image = Image.open(df)
                  text = pytesseract.image_to_string(image)
                  st.write("Texto extraído de la imagen:")
                #   st.write(text)

                  numeros = re.findall(r"\b\d+\b", text)
                  nombres = re.findall(r"\b[A-Za-zÁÉÍÓÚÑáéíóúñ]{3,}\b", text)
                #   data_ocr = pd.DataFrame({"Nombres/Palabras": nombres[:len(numeros)]+[""]* (len(numeros)- len(nombres))if len(nombres)< len(numeros)else "nombres",
                #                            "Numeros": numeros[:len(nombres)]+[""]* (len(nombres)-len(numeros))if len(numeros)<len(nombres)else numeros})
                #   st.subheader("Información detectada en la Imagen: ")
                  max_len = max(len(nombres), len(numeros))

                  nombres_padded = nombres + [""] *(max_len - len(nombres))
                  numeros_padded = numeros + [""] *(max_len - len(numeros))

                  data_ocr = pd.DataFrame({"Nombres":nombres_padded,
                                           "Numeros": numeros_padded})
                  st.dataframe(data_ocr)

                  csv = data_ocr.to_csv(index=False).encode("utf-8")

                  st.download_button(label="Descargar Info de Imagen",
                                     data=csv,
                                     file_name="Info-Imagen.csv",
                                     mime="text/csv")
    except Exception as e:
        st.error(f"Error al procesar el archivo. Asegúrate de que sea un archivo CSV, XLSX o PNG.{e}")
        df = None
    if isinstance(df, pd.DataFrame):
            with st.expander(label="Graficos", icon="📊"):
                 st.write("Graficos")
                 for col in numericas:
                    fig, ax = plt.subplots(figsize=(10,5))
                    ax.hist(df[col].dropna(), bins=30,color="green")
                    ax.set_title(f"estadistica {col}")
                    ax.set_xlabel(col)
                    ax.set_ylabel("Frecuencia")
                    st.pyplot(fig)
                
                
                 st.write("Descargar Informe")

                 pdf = df.to_html()


                 st.download_button(
                    label="Descargar Informe",
                    data=pdf,
                    file_name="Informe.html",
                    mime="text/html"
                )

            with st.expander(label="Mas estadisticas",
                    icon="📊"):
                    st.write("Mediana: ")
                    st.dataframe(df[numericas].mean().round(2))
                    st.write("Moda: ")
                    st.dataframe(df[numericas].mode().round(2))
                    st.write("Varianza")
                    st.dataframe(df[numericas].var().round(2))
                    st.write("Curtosis")
                    st.dataframe(df[numericas].kurt().round(2))
                    st.write("Asimetría (Skewness):")
                    st.dataframe(df[numericas].skew().round(2))
# if __name__ == "__main__":
     