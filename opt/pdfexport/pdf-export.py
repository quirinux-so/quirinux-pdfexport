import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter.font import Font
from pathlib import Path
import subprocess
import traceback
import tempfile
import shutil

class QuirinuxPDFExport(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Quirinux PDF Export")
        self.geometry("700x500")
        self.configure(bg="#f0f0f0")
        
        # Obtener la ruta del escritorio del usuario
        try:
            self.desktop_path = str(Path.home() / "Desktop")
            if not os.path.exists(self.desktop_path):
                # Intentar con la versión en español
                self.desktop_path = str(Path.home() / "Escritorio")
                if not os.path.exists(self.desktop_path):
                    self.desktop_path = str(Path.home())
        except Exception as e:
            self.desktop_path = os.path.expanduser("~")
            print(f"Error al obtener ruta del escritorio: {str(e)}")
        
        # Inicialización de variables
        self.file_path = tk.StringVar()
        self.output_format = tk.StringVar(value="docx")
        self.status = tk.StringVar(value="Listo para convertir")
        self.debug_info = tk.StringVar(value="")
        
        # Verificar dependencias
        self.check_dependencies()
        
        self.create_widgets()
    
    def check_dependencies(self):
        """Verificar si están instaladas las dependencias necesarias de Debian"""
        missing = []
        optional = []
        
        # Verificar poppler-utils (pdftotext, pdftocairo, etc.)
        try:
            subprocess.run(["pdftotext", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except FileNotFoundError:
            missing.append("poppler-utils")
        
        # Verificar pandoc
        try:
            subprocess.run(["pandoc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except FileNotFoundError:
            missing.append("pandoc")
        
        # Verificar imagemagick (util para procesamiento de SVG)
        try:
            subprocess.run(["convert", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except FileNotFoundError:
            optional.append("imagemagick")
            
        # Verificar gs (ghostscript)
        try:
            subprocess.run(["gs", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except FileNotFoundError:
            optional.append("ghostscript")
            
        # Verificar LibreOffice (para conversión DOC)
        try:
            subprocess.run(["libreoffice", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except FileNotFoundError:
            if self.output_format.get() == "doc":
                optional.append("libreoffice")

        # Verificar unoconv (alternativa para conversión DOC)
        try:
            subprocess.run(["unoconv", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except FileNotFoundError:
            if self.output_format.get() == "doc":
                optional.append("unoconv")
        
        if missing:
            warning_text = "\n".join(missing)
            messagebox.showwarning(
                "Dependencias faltantes",
                f"Las siguientes herramientas son necesarias para la conversión:\n{warning_text}\n\n"
                "Instálelas usando apt:\n"
                "sudo apt-get install poppler-utils pandoc"
            )
            
        if optional:
            opt_text = "\n".join(optional)
            messagebox.showinfo(
                "Dependencias opcionales",
                f"Las siguientes herramientas mejorarían la calidad de la conversión:\n{opt_text}\n\n"
                "Instálelas usando apt (opcionales):\n"
                "sudo apt-get install ghostscript imagemagick libreoffice unoconv"
            )
    
    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_font = Font(family="Helvetica", size=16, weight="bold")
        tk.Label(main_frame, text="Quirinux PDF Export", font=title_font, bg="#f0f0f0").pack(pady=(0, 10))
        
        # Información del autor
        tk.Label(main_frame, text="(c) Charlie Martínez - Quirinux, GPLv2", font=("Helvetica", 8), bg="#f0f0f0").pack(pady=(5, 0))
        
        # Frame para la selección de archivo
        file_frame = tk.LabelFrame(main_frame, text="Seleccionar archivo PDF", bg="#f0f0f0")
        file_frame.pack(fill=tk.X, pady=10)
        
        file_entry = tk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(file_frame, text="Examinar", command=self.select_file).pack(side=tk.RIGHT)
        
        options_frame = tk.LabelFrame(main_frame, text="Opciones de conversión", bg="#f0f0f0")
        options_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(options_frame, text="Formato de salida:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
        ttk.Radiobutton(options_frame, text="ODT", variable=self.output_format, value="odt").grid(row=0, column=1)
        ttk.Radiobutton(options_frame, text="DOC", variable=self.output_format, value="doc").grid(row=0, column=2)
        ttk.Radiobutton(options_frame, text="DOCX", variable=self.output_format, value="docx").grid(row=0, column=3)
        
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=15)
        
        ttk.Button(buttons_frame, text="Convertir", command=self.convert_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Abrir carpeta resultado", command=self.open_output_folder).pack(side=tk.LEFT, padx=5)
        
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=560, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=10)
        
        status_frame = tk.LabelFrame(main_frame, text="Estado", bg="#f0f0f0")
        status_frame.pack(fill=tk.X, pady=10)
        tk.Label(status_frame, textvariable=self.status, bg="#f0f0f0").pack(anchor=tk.W, pady=5)
        
        debug_label = tk.Label(status_frame, textvariable=self.debug_info, bg="#f0f0f0", fg="red", wraplength=650)
        debug_label.pack(anchor=tk.W, pady=5)
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo PDF", 
            filetypes=[("Archivos PDF", "*.pdf")], 
            initialdir=self.desktop_path
        )
        if file_path:
            self.file_path.set(file_path)
            self.status.set(f"Archivo seleccionado: {os.path.basename(file_path)}")
            self.debug_info.set("")
    
    def convert_file(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Seleccione un archivo PDF")
            return
        
        if not os.path.isfile(self.file_path.get()):
            messagebox.showerror("Error", "El archivo no existe")
            return
        
        self.progress.start()
        self.status.set("Iniciando conversión...")
        self.debug_info.set("")
        threading.Thread(target=self._convert_file_thread, daemon=True).start()
    
    def open_output_folder(self):
        """Abrir el explorador de archivos en la carpeta de destino"""
        if os.path.exists(self.desktop_path):
            try:
                if sys.platform == 'win32':
                    os.startfile(self.desktop_path)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', self.desktop_path], check=True)
                else:  # Linux
                    try:
                        subprocess.run(['xdg-open', self.desktop_path], check=True)
                    except:
                        subprocess.run(['gio', 'open', self.desktop_path], check=True)
                self.status.set(f"Carpeta abierta: {self.desktop_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la carpeta: {str(e)}")
        else:
            messagebox.showerror("Error", "No se encuentra la carpeta de destino")
    
    def _convert_file_thread(self):
        pdf_file = self.file_path.get()
        output_format = self.output_format.get()
        file_name = os.path.splitext(os.path.basename(pdf_file))[0]
        output_doc = os.path.join(self.desktop_path, f"{file_name}.{output_format}")
        
        self.after(0, self.status.set, f"Convirtiendo a {output_format.upper()}...")
        
        # Crear un directorio temporal con tempfile para mayor seguridad
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Archivos intermedios
                text_file = os.path.join(temp_dir, f"{file_name}.txt")
                html_file = os.path.join(temp_dir, f"{file_name}.html")
                markdown_file = os.path.join(temp_dir, f"{file_name}.md")
                svg_dir = os.path.join(temp_dir, "svg")
                os.makedirs(svg_dir, exist_ok=True)
                
                # Paso 1: Intentamos usar pdftocairo para convertir a SVG + extraer texto
                self.after(0, self.debug_info.set, "Convirtiendo PDF a SVG para mejor preservación del formato...")
                try:
                    # Primero extraemos el texto
                    cmd_text = ["pdftotext", "-layout", "-nopgbrk", pdf_file, text_file]
                    subprocess.run(cmd_text, check=True, capture_output=True, text=True)
                    
                    # Convertir cada página a SVG con pdftocairo
                    svg_base = os.path.join(svg_dir, f"{file_name}")
                    cmd_pdf_to_svg = ["pdftocairo", "-svg", pdf_file, svg_base]
                    result = subprocess.run(cmd_pdf_to_svg, capture_output=True, text=True)
                    
                    # Si la conversión a SVG fue exitosa, crear un HTML que combine texto y gráficos
                    if result.returncode == 0:
                        # Crear HTML con imágenes SVG incrustadas y texto
                        self.after(0, self.debug_info.set, "Generando HTML con contenido mixto (texto+gráficos)...")
                        
                        # Construir HTML
                        with open(html_file, 'w', encoding='utf-8') as html_out:
                            html_out.write("<!DOCTYPE html>\n<html>\n<head>\n")
                            html_out.write("<meta charset='utf-8'>\n")
                            html_out.write("<style>\n")
                            html_out.write("body { font-family: Arial, sans-serif; }\n")
                            html_out.write(".page { page-break-after: always; margin-bottom: 20px; }\n")
                            html_out.write(".svg-container { max-width: 100%; }\n")
                            html_out.write("</style>\n</head>\n<body>\n")
                            
                            # Obtener lista de archivos SVG generados
                            svg_files = sorted([f for f in os.listdir(svg_dir) if f.endswith('.svg')])
                            
                            # Dividir el texto en párrafos
                            with open(text_file, 'r', encoding='utf-8') as txt_in:
                                text_content = txt_in.read()
                            
                            # Si hay SVG, insertarlos
                            if svg_files:
                                for svg_file in svg_files:
                                    html_out.write(f"<div class='page'>\n")
                                    html_out.write(f"<div class='svg-container'>\n")
                                    # Incrustar SVG
                                    with open(os.path.join(svg_dir, svg_file), 'r', encoding='utf-8') as svg_in:
                                        svg_content = svg_in.read()
                                        html_out.write(svg_content)
                                    html_out.write("</div>\n</div>\n")
                            else:
                                # Si no hay SVG, usar solo el texto
                                paragraphs = text_content.split('\n\n')
                                for para in paragraphs:
                                    if para.strip():
                                        # Corregido: Se usa doble backslash para escapar \n en el método replace
                                        replaced_text = para.replace('\n', '<br>')
                                        html_out.write(f"<p>{replaced_text}</p>\n")
                            
                            html_out.write("</body>\n</html>")
                        
                        # Usar HTML generado para convertir al formato deseado
                        if os.path.exists(html_file) and os.path.getsize(html_file) > 0:
                            self.after(0, self.debug_info.set, "Convirtiendo HTML enriquecido al formato final...")
                            
                            # Convertir de HTML directamente al formato deseado
                            if output_format == "odt":
                                cmd_convert = ["pandoc", "-f", "html", "-t", "odt", "--standalone", 
                                              "--toc", "-o", output_doc, html_file]
                                subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                            elif output_format == "docx":
                                cmd_convert = ["pandoc", "-f", "html", "-t", "docx", "--standalone", 
                                              "--toc", "-o", output_doc, html_file]
                                subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                            elif output_format == "doc":
                                # Para DOC, primero convertimos a DOCX
                                docx_temp = os.path.join(temp_dir, f"{file_name}.docx")
                                cmd_to_docx = ["pandoc", "-f", "html", "-t", "docx", "--standalone", 
                                              "--toc", "-o", docx_temp, html_file]
                                
                                subprocess.run(cmd_to_docx, check=True, capture_output=True, text=True)
                                
                                # Ahora convertimos de DOCX a DOC usando LibreOffice si está disponible
                                try:
                                    # Verificar si LibreOffice está instalado
                                    subprocess.run(["libreoffice", "--version"], check=False, capture_output=True)
                                    
                                    # Usar LibreOffice para convertir
                                    cmd_convert = ["libreoffice", "--headless", "--convert-to", "doc", 
                                                 "--outdir", os.path.dirname(output_doc), docx_temp]
                                    
                                    subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                                    
                                    # Obtener el nombre generado por LibreOffice
                                    lo_output = os.path.join(os.path.dirname(output_doc), f"{file_name}.doc")
                                    if os.path.exists(lo_output):
                                        # Ya está en la ubicación correcta
                                        pass
                                    
                                except (FileNotFoundError, subprocess.CalledProcessError):
                                    # Si no está LibreOffice, intentar con unoconv
                                    try:
                                        subprocess.run(["unoconv", "--version"], check=False, capture_output=True)
                                        cmd_convert = ["unoconv", "-f", "doc", "-o", output_doc, docx_temp]
                                        subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                                    except (FileNotFoundError, subprocess.CalledProcessError):
                                        # Si también falla, copiamos el DOCX y lo renombramos (última opción)
                                        self.after(0, self.debug_info.set, "No se puede convertir directamente a DOC. Generando DOCX en su lugar...")
                                        shutil.copy2(docx_temp, output_doc.replace(".doc", ".docx"))
                                        self.after(0, self.debug_info.set, "Se ha generado un archivo DOCX en lugar de DOC")
                            
                            if os.path.exists(output_doc) and os.path.getsize(output_doc) > 0:
                                self.after(0, self.status.set, f"Conversión completada (Método SVG+HTML): {output_doc}")
                                self.after(0, self.debug_info.set, "")
                                self._success_message(output_doc)
                                return
                except Exception as e:
                    self.after(0, self.debug_info.set, f"Método SVG falló, probando método alternativo... {str(e)}")
                
                # Paso 2: Método tradicional con pdftotext para extraer el texto
                self.after(0, self.debug_info.set, "Extrayendo texto del PDF (método tradicional)...")
                
                # Extraer texto del PDF con mejor formato
                cmd_text = ["pdftotext", "-layout", "-nopgbrk", pdf_file, text_file]
                subprocess.run(cmd_text, check=True, capture_output=True, text=True)
                
                # Verificar que se extrajo contenido
                if os.path.getsize(text_file) == 0:
                    self.after(0, self.debug_info.set, "No se pudo extraer texto del PDF. Probando método alternativo...")
                    # Intentar con otro método de extracción
                    cmd_text_alt = ["pdftotext", pdf_file, text_file]
                    subprocess.run(cmd_text_alt, check=True, capture_output=True, text=True)
                
                # Convertir texto a markdown para mejor procesamiento
                self.after(0, self.debug_info.set, "Procesando texto...")
                cmd_to_md = ["pandoc", "-f", "plain", "-t", "markdown", "-o", markdown_file, text_file]
                subprocess.run(cmd_to_md, check=True, capture_output=True, text=True)
                
                # Aplicar conversión según formato requerido
                if output_format == "odt":
                    self.after(0, self.debug_info.set, "Generando ODT...")
                    cmd_convert = ["pandoc", 
                                  "-f", "markdown", 
                                  "-t", "odt", 
                                  "--standalone",
                                  "--toc",
                                  "-o", output_doc, 
                                  markdown_file]
                    subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                
                elif output_format == "docx":
                    self.after(0, self.debug_info.set, "Generando DOCX...")
                    cmd_convert = ["pandoc", 
                                  "-f", "markdown", 
                                  "-t", "docx", 
                                  "--standalone",
                                  "--toc",
                                  "-o", output_doc, 
                                  markdown_file]
                    subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                
                elif output_format == "doc":
                    self.after(0, self.debug_info.set, "Generando DOC (vía DOCX)...")
                    # Primero generamos un DOCX temporal
                    docx_temp = os.path.join(temp_dir, f"{file_name}.docx")
                    cmd_to_docx = ["pandoc", 
                                  "-f", "markdown", 
                                  "-t", "docx", 
                                  "--standalone",
                                  "--toc",
                                  "-o", docx_temp, 
                                  markdown_file]
                    
                    subprocess.run(cmd_to_docx, check=True, capture_output=True, text=True)
                    
                    # Ahora convertimos de DOCX a DOC usando LibreOffice si está disponible
                    try:
                        # Verificar si LibreOffice está instalado
                        subprocess.run(["libreoffice", "--version"], check=False, capture_output=True)
                        
                        # Usar LibreOffice para convertir
                        cmd_convert = ["libreoffice", "--headless", "--convert-to", "doc", 
                                     "--outdir", os.path.dirname(output_doc), docx_temp]
                        
                        # En este caso, LibreOffice guarda con el mismo nombre pero extensión doc
                        subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                        
                        # Obtener el nombre generado por LibreOffice
                        lo_output = os.path.join(os.path.dirname(output_doc), f"{file_name}.doc")
                        if os.path.exists(lo_output):
                            # Ya está en la ubicación correcta
                            pass
                        
                    except (FileNotFoundError, subprocess.CalledProcessError):
                        # Si no está LibreOffice, intentar con unoconv
                        try:
                            subprocess.run(["unoconv", "--version"], check=False, capture_output=True)
                            cmd_convert = ["unoconv", "-f", "doc", "-o", output_doc, docx_temp]
                            subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                        except (FileNotFoundError, subprocess.CalledProcessError):
                            # Si también falla, copiamos el DOCX y lo renombramos (última opción)
                            self.after(0, self.debug_info.set, "No se puede convertir directamente a DOC. Generando DOCX en su lugar...")
                            shutil.copy2(docx_temp, output_doc.replace(".doc", ".docx"))
                            self.after(0, self.debug_info.set, "Se ha generado un archivo DOCX en lugar de DOC")
                
                # Verificar si se generó el archivo y tiene contenido
                if os.path.exists(output_doc) and os.path.getsize(output_doc) > 0:
                    self.after(0, self.status.set, f"Conversión completada: {output_doc}")
                    self.after(0, self.debug_info.set, "")
                    self._success_message(output_doc)
                else:
                    # Si todavía falla, intentar un método de último recurso
                    self.after(0, self.debug_info.set, "Intentando método de rescate final...")
                    
                    # Para DOC y DOCX, probar con la ruta ODT → formato destino
                    temp_odt = os.path.join(temp_dir, f"{file_name}.odt")
                    cmd_to_odt = ["pandoc", "-f", "plain", "-t", "odt", "-o", temp_odt, text_file]
                    
                    try:
                        subprocess.run(cmd_to_odt, check=True, capture_output=True, text=True)
                        
                        if output_format == "doc":
                            # Para DOC, primero generamos un DOCX
                            docx_temp = os.path.join(temp_dir, f"{file_name}.docx")
                            cmd_to_docx = ["pandoc", "-f", "odt", "-t", "docx", "-o", docx_temp, temp_odt]
                            subprocess.run(cmd_to_docx, check=True, capture_output=True, text=True)
                            
                            # Luego intentamos convertir con LibreOffice
                            try:
                                subprocess.run(["libreoffice", "--version"], check=False, capture_output=True)
                                cmd_convert = ["libreoffice", "--headless", "--convert-to", "doc", 
                                             "--outdir", os.path.dirname(output_doc), docx_temp]
                                subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                            except (FileNotFoundError, subprocess.CalledProcessError):
                                # Si LibreOffice falla, intentamos unoconv
                                try:
                                    subprocess.run(["unoconv", "--version"], check=False, capture_output=True)
                                    cmd_convert = ["unoconv", "-f", "doc", "-o", output_doc, docx_temp]
                                    subprocess.run(cmd_convert, check=True, capture_output=True, text=True)
                                except (FileNotFoundError, subprocess.CalledProcessError):
                                    # Si todo falla, entregamos el DOCX
                                    shutil.copy2(docx_temp, output_doc.replace(".doc", ".docx"))
                                    self.after(0, self.debug_info.set, "No se pudo generar DOC. Se entrega DOCX.")
                        else:
                            # De ODT al formato final (DOCX u otro)
                            final_cmd = ["pandoc", "-f", "odt", "-t", output_format, "-o", output_doc, temp_odt]
                            subprocess.run(final_cmd, check=True, capture_output=True, text=True)
                        
                        # Verificar una última vez
                        output_to_check = output_doc
                        if output_format == "doc" and not os.path.exists(output_doc):
                            output_to_check = output_doc.replace(".doc", ".docx")
                            
                        if os.path.exists(output_to_check) and os.path.getsize(output_to_check) > 0:
                            self.after(0, self.status.set, f"Conversión completada (método alternativo): {output_to_check}")
                            self.after(0, self.debug_info.set, "")
                            self._success_message(output_to_check)
                        else:
                            raise Exception("No se pudo generar el archivo de salida.")
                    except Exception as e:
                        self.after(0, self.status.set, "Error: No se pudo completar la conversión")
                        self.after(0, self.debug_info.set, f"Error en la conversión: {str(e)}")
                    
            except Exception as e:
                self.after(0, self.status.set, f"Error inesperado: {str(e)}")
                self.after(0, self.debug_info.set, traceback.format_exc())
            
            finally:
                self.after(0, self.progress.stop)
    
    def _success_message(self, output_path):
        """Mostrar mensaje de éxito después de la conversión"""
        self.after(0, lambda: messagebox.showinfo(
            "Éxito", 
            f"Archivo convertido correctamente:\n{output_path}",
            detail="Para acceder al archivo, haga clic en 'Abrir carpeta resultado'"
        ))

if __name__ == "__main__":
    try:
        app = QuirinuxPDFExport()
        app.mainloop()
    except Exception as e:
        # Mostrar error crítico si falla la inicialización
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error crítico", f"Error al iniciar la aplicación:\n{str(e)}\n\n{traceback.format_exc()}")
            root.destroy()
        except:
            print(f"ERROR CRÍTICO: {str(e)}")
            print(traceback.format_exc())