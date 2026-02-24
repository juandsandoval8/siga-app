# 🎓 SIGA — Guía de Instalación y Despliegue
## Sistema Integral de Gestión del Aprendiz

---

## ✅ PASO 1 — Crear cuenta en GitHub (gratis)

1. Ve a **https://github.com**
2. Clic en **"Sign up"**
3. Pon tu email, crea contraseña, elige nombre de usuario
4. Verifica tu email
5. ¡Listo! Tienes GitHub.

---

## ✅ PASO 2 — Subir el código a GitHub

1. Inicia sesión en GitHub
2. Clic en el botón verde **"New"** (esquina superior izquierda)
3. Nombre del repositorio: `siga-app`
4. Selecciona **"Private"** (privado, solo tú lo ves)
5. Clic en **"Create repository"**
6. En la página siguiente, clic en **"uploading an existing file"**
7. Arrastra **todos los archivos** de la carpeta `siga_app` que te dieron
   - `app.py`
   - `database.py`
   - `requirements.txt`
   - carpeta `pages/` con sus archivos
   - carpeta `.streamlit/` con `config.toml`
   - `.gitignore`
8. Clic en **"Commit changes"** (botón verde)

---

## ✅ PASO 3 — Crear cuenta en Streamlit Cloud (gratis)

1. Ve a **https://share.streamlit.io**
2. Clic en **"Sign up"**
3. Selecciona **"Continue with GitHub"** (usa la cuenta que acabas de crear)
4. Autoriza Streamlit
5. ¡Ya tienes Streamlit Cloud!

---

## ✅ PASO 4 — Desplegar la app

1. En Streamlit Cloud, clic en **"New app"**
2. Selecciona tu repositorio: `siga-app`
3. Rama: `main`
4. Archivo principal: `app.py`
5. Clic en **"Deploy!"**
6. Espera 1-2 minutos ☕
7. **¡Tu app ya está en internet con una URL única!**

   Ejemplo de URL: `https://siga-app-tuusuario.streamlit.app`

---

## ✅ PASO 5 — Compartir con la segunda persona

1. Copia la URL de tu app
2. Envíasela por WhatsApp o email
3. Ella abre el link en su navegador
4. **¡Ambas pueden trabajar al mismo tiempo!** 🎉

> 💡 No necesitan instalar nada. Solo abrir el link en Chrome o Firefox.

---

## 🔄 ¿Cómo actualizar los datos entre las dos personas?

La app guarda todo en una base de datos compartida.  
Cuando una persona guarda un aprendiz → la otra lo ve al **presionar F5** (actualizar la página).

---

## 📋 Módulos disponibles en la app

| Módulo | Qué hace |
|--------|----------|
| 🏠 Dashboard | KPIs en tiempo real, gráficos de estado y riesgo |
| 👤 Aprendices | Registrar, editar, filtrar, importar desde Excel |
| 🏢 Empresas | Gestión de empresas aliadas y su cumplimiento |
| 📄 Documentos | Subir PDFs, Excel, imágenes y descargarlos |

---

## 📥 ¿Cómo importar tu Excel existente?

1. Ve al módulo **Aprendices**
2. Busca la sección **"📥 Importar desde Excel / CSV"**
3. Tu archivo Excel debe tener estas columnas exactas:

```
nombre | documento | programa | ficha | regional | estado | empresa | vinculacion | fecha_inicio | fecha_fin | instructor | riesgo | observaciones
```

4. Sube el archivo y clic en **"Importar todos los registros"**

---

## 🆘 Problemas comunes

| Problema | Solución |
|----------|----------|
| La app no carga | Espera 30 segundos, a veces "duerme" si no la usan por un rato |
| Error al importar Excel | Verifica que las columnas tengan exactamente los nombres indicados |
| No veo los cambios de mi compañera | Presiona F5 para actualizar |
| La app se ve lenta | Es gratis, tiene límites. Considera Streamlit Team si crece |

---

## 🚀 Próximos pasos (versión futura)

- ✅ Conectar con Supabase para persistencia total en la nube
- ✅ Agregar login con contraseña por usuario
- ✅ Alertas automáticas por email
- ✅ Panel de seguimiento con fechas límite

---

*Desarrollado para SENA Colombia · Sistema SIGA v1.0*
