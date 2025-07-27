# Quirinux PDF Export

**Autor / Author:** Charlie Martínez – Quirinux GNU/Linux®  
**Licencia / License:** GPLv2.0

![Quirinux PDF Export Screenshot](https://github.com/user-attachments/assets/ee7c19ef-605e-4b35-b828-7b55f68e80ea)

---

## 🧭 Descripción general / Overview

**ES:**  
`Quirinux PDF Export` es una aplicación gráfica, multilingüe y sin conexión, diseñada para convertir archivos PDF en documentos editables como **ODT**, **DOC** o **DOCX**.  

Es especialmente útil para recuperar contenidos con formato complejo, mediante un sistema híbrido de conversión texto + SVG.

**EN:**  
`Quirinux PDF Export` is a graphical, multilingual, and offline application to convert PDF files into editable documents like **ODT**, **DOC**, or **DOCX**.  

It is especially useful for extracting content from complex PDFs using a hybrid text + SVG system.

---

## ✔️ Características / Features

**ES:**
- Conversión de PDF a ODT, DOC o DOCX  
- Conversión enriquecida con soporte para SVG, HTML y Markdown  
- Exportación directa al escritorio del usuario  
- Soporte para documentos con imágenes y diseño complejo  
- Interfaz amigable en varios idiomas  
- Detección automática de dependencias del sistema  
- Uso completamente offline (no requiere conexión)  
- Diseñada para sistemas basados en Debian

**EN:**
- Convert PDF to ODT, DOC or DOCX  
- Enhanced conversion using SVG, HTML and Markdown  
- Direct export to user's desktop  
- Supports complex layouts and embedded images  
- User-friendly multilingual interface  
- Automatically detects missing dependencies  
- Fully offline operation  
- Designed for Debian-based systems

---

## 📋 Requisitos / Requirements

**ES / EN:**  
Instalar las siguientes dependencias básicas / Install the following basic dependencies:

```bash
su root
apt install poppler-utils pandoc
```

**Dependencias opcionales recomendadas / Optional recommended dependencies:**

```bash
apt install ghostscript imagemagick libreoffice unoconv
```

---

## ▶️ Ejecución / How to Run

**ES / EN:**  
Clonar el repositorio y ejecutar la aplicación / Clone the repo and run the application:

```bash
git clone https://github.com/quirinux-so/quirinux-pdfexport.git
cd quirinux-pdfexport/opt/pdfexport
python3 pdf-export.py
```

---

## 📦 Instalación alternativa / Optional Installation (Quirinux)

**ES:**  
Disponible como paquete oficial `.deb` desde el repositorio de Quirinux o desde el Centro de Software.

**EN:**  
Available as an official `.deb` package via the Quirinux repository or Software Center.

**Comando / Command:**

    su root
    apt install quirinux-pdfexport

**Repositorio / Repository:**  
[https://repo.quirinux.org/pool/main/q/quirinux-pdfexport](https://repo.quirinux.org/pool/main/q/quirinux-pdfexport)

---

## ⚖️ Aviso legal / Legal Notice

**ES:**  
Este proyecto forma parte del ecosistema **Quirinux**, pero es compatible con cualquier distribución moderna de GNU/Linux.  
Distribuido bajo los términos de la licencia **GPLv2**.

**EN:**  
This project is part of the **Quirinux** ecosystem but remains compatible with any modern GNU/Linux distribution.  
Released under the terms of the **GPLv2 license**.

**Autor / Author:** Charlie Martínez  
📧 <cmartinez@quirinux.org>

**Más información / More information:**  
[https://www.quirinux.org/aviso-legal](https://www.quirinux.org/aviso-legal)
