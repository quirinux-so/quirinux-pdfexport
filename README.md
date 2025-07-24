
# <img width="32" alt="pdfexport" src="https://github.com/user-attachments/assets/5f307c4b-1c0f-4dad-8440-2886784e5f62" /> Quirinux PDF Export

(c) Charlie Martínez – Quirinux GNU/Linux, GPLv2  

<img width="449" height="339" alt="imagen" src="https://github.com/user-attachments/assets/ee7c19ef-605e-4b35-b828-7b55f68e80ea" />

## 🇪🇸 Español  
**Quirinux PDF Export** es una aplicación gráfica, multilingüe y offline para convertir archivos PDF en documentos editables (ODT, DOC o DOCX).  

Es especialmente útil para recuperar contenidos de PDFs con formato complejo, usando un sistema híbrido texto+SVG.  

✅ Características:

- Conversión de PDF a ODT, DOC o DOCX  
- Detección automática de dependencias del sistema  
- Conversión enriquecida usando SVG, HTML y Markdown  
- Soporte para documentos multiformato y con imágenes  
- Exportación directa al escritorio del usuario  
- Interfaz amigable y sin conexión a Internet  
- Para sistemas basados en Debian

🔧 Requisitos:

```bash
su root
apt install poppler-utils pandoc
```

📦 Dependencias opcionales recomendadas:

```bash
apt install ghostscript imagemagick libreoffice unoconv
```

▶️ Ejecutar la aplicación:

```bash
git clone https://github.com/quirinux-so/quirinux-pdfexport.git
cd quirinux-pdfexport/opt/pdfexport
python3 pdf-export.py
```

📦 Instalación en Quirinux (opcional):

```bash
su root
apt install quirinux-pdfexport
```

También disponible desde el **Centro de Software de Quirinux**.  
🔗 https://repo.quirinux.org/pool/main/q/quirinux-pdfexport/

### ⚠️ Aviso legal  
Este proyecto forma parte del ecosistema **Quirinux**, pero es compatible con cualquier distribución moderna de GNU/Linux.  

Publicado bajo licencia **GPLv2**.  

Autor: Charlie Martinez <cmartinez@quirinux.org>

ℹ️ Más información:  
🔗 [https://www.quirinux.org/aviso-legal](https://www.quirinux.org/aviso-legal)

---

## 🇬🇧 English  
**Quirinux PDF Export** is a graphical, multilingual, and offline tool to convert PDF files into editable documents (ODT, DOC, or DOCX).  

It’s especially useful for recovering structured content using hybrid text+SVG rendering.  

✅ Features:

- Convert PDF to ODT, DOC or DOCX  
- Auto-detects required system dependencies  
- Enhanced output using SVG, HTML and Markdown  
- Supports images and complex layout  
- Direct export to user desktop  
- Offline-friendly interface  
- For Debian bassed systems 

🔧 Requirements:

```bash
su root
apt install poppler-utils pandoc
```

📦 Optional recommended dependencies:

```bash
apt install ghostscript imagemagick libreoffice unoconv
```

▶️ Run the application:

```bash
git clone https://github.com/quirinux-so/quirinux-pdfexport.git
cd quirinux-pdfexport/opt/pdfexport
python3 pdf-export.py
```

📦 Install on Quirinux (optional):

```bash
su root
apt install quirinux-pdfexport
```

Also available from the **Quirinux Software Center**.  
🔗 https://repo.quirinux.org/pool/main/q/quirinux-pdfexport/

### ⚠️ Legal notice  
This project is part of the **Quirinux** ecosystem but compatible with any modern GNU/Linux distribution.  

Released under the **GPLv2 license**.  

Author: Charlie Martinez <cmartinez@quirinux.org>

ℹ️ More info:  
🔗 [https://www.quirinux.org/aviso-legal](https://www.quirinux.org/aviso-legal)
