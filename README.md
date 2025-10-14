# 🌿 Liser

**Liser** es una aplicación web para crear, organizar y compartir listas de productos curadas —llamadas **BagLists**—.  
Pensada para **creadores de contenido, influencers y amantes del orden visual**, Liser convierte tus recomendaciones en algo tan inspirador como útil.  

✨ _Piensa en Liser como una mezcla entre “mis favoritos”, “qué hay en mi mochila” y una vitrina interactiva de ideas._

---

## 🚀 Visión General

Liser permite a los usuarios:

- **Creadores** → Centralizar sus recomendaciones, compartirlas con su comunidad y monetizar mediante enlaces de afiliados.  
- **Seguidores** → Descubrir productos, inspirarse y crear sus propias listas de viaje, estudio o deseo.

Su enfoque combina lo **funcional y visual**, con una arquitectura robusta basada en Django y una interfaz simple hecha con Tailwind CSS.

---

## 🎯 Características Principales

### 👜 BagLists
El núcleo del proyecto. Cada lista pertenece a un usuario, tiene título, descripción y nivel de visibilidad (pública, privada, etc.).

### 🗂️ Secciones
Cada BagList puede dividirse en secciones temáticas como “Tecnología”, “Cuidado personal” o “Viaje”.

### 🛍️ Items
Cada producto dentro de una sección es un **Item**, con su propio snapshot de información.

### 📸 Snapshots de Producto
Cada vez que se añade un producto, se guarda una “foto” del título, precio, imagen y enlaces.  
Así, aunque el sitio original cambie, la información permanece intacta.

### 🏷️ Tags y Facetas
Sistema de etiquetas (#verano2024, #setup, #viaje) y facetas para filtrar por país, temporada o tipo de uso.

### ⚙️ Campos Personalizados
Cada creador puede añadir columnas propias a una sección (ej: “Peso (g)”, “Duración”, “Color favorito”).

### 💚 Interacción Social
Los usuarios pueden marcar BagLists e Items como favoritos.

---

## 🎨 Guía de Diseño (UI/UX)

El diseño actual usa **Tailwind CSS** directamente desde las plantillas Django.  
Funciona bien, pero está en proceso de unificación visual.

### Paletas de color
- **Verde/Natural** 🌿 → usada en el layout principal (sensación orgánica, fresca y amable).  
- **Azul/Corporativa** 💼 → usada en los bloques de datos (seriedad y aspecto “tech”).  

🧭 **Tarea pendiente**: unificar ambas en una sola paleta, tomando el verde como base y el azul como acento.

### Tipografía y Espaciado
- Tipografía actual: sans-serif por defecto.  
- Se recomienda definir una fuente de marca y establecer una escala de espaciado (múltiplos de 4 u 8px).

---

## ⚙️ Guía de Desarrollo

### Stack Tecnológico
- **Backend:** Django 5.2 (Python 3.11)  
- **Base de datos:** MySQL  
- **Frontend:** Tailwind CSS (vía CDN)  
- **Entorno:** Virtualenv (venv)

### Estructura del Proyecto

```plaintext
proyect_liser_ver2/
│
├─ accounts/      # Usuarios y perfiles
├─ catalog/       # Productos externos "canónicos"
├─ common/        # Modelos y utilidades base
├─ lists/         # BagLists, Secciones, Items, Snapshots, Tags...
├─ analytics/     # Preparado para analíticas (vistas, clics)
├─ api/           # Futura API REST
├─ templates/     # Plantillas HTML globales y parciales
└─ manage.py
```

### Modelos principales
- **BagList → Section → Item**: estructura jerárquica central.  
- **Item → Snapshot**: guarda los datos del producto.  
- **Tags, Facets y Campos personalizados**: amplían la flexibilidad del sistema.

---

## 🧭 Próximos Pasos

- 🌐 Dashboard de usuario ("Mis BagLists")  
- 📝 Páginas de creación/edición de BagLists  
- 🔍 Página de exploración pública con filtros por facetas y tags  
- 👤 Página de perfil de usuario  
- ⚡ Integrar un bundler (Vite o django-compressor) para compilar Tailwind y JS  
- 🧩 Componentizar elementos repetidos de la UI  

---

## 🛠️ Instalación y Configuración

1. Clona el repositorio:

   ```bash
   git clone https://github.com/excusasclub/liser_ver2.git
   cd liser_ver2
   ```

2. Crea y activa el entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En macOS/Linux
   venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta las migraciones:

   ```bash
   python manage.py migrate
   ```

5. Inicia el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

6. Abre tu navegador en [http://localhost:8000](http://localhost:8000) 🚀

---

## 📊 Estado Actual del Proyecto

| Área | Estado | Notas |
|------|---------|-------|
| **Backend (Django)** | ✅ Estable | Modelos y estructura funcional completa |
| **Frontend (Tailwind)** | ⚙️ En desarrollo | Necesita unificación visual y mejor UX |
| **Vistas (UI)** | 🧩 Parcial | Solo implementada la vista `baglist_detail` |
| **Analíticas y API** | ⏳ Pendiente | Estructura preparada, aún sin lógica activa |
| **Diseño visual y marca** | 🧠 En definición | Se está consolidando la identidad visual |

---

## 🤝 Contribuir

¡Nos encanta recibir ideas y aportes!  
Si tienes sugerencias de diseño, mejoras en el código o nuevas funcionalidades, abre un **issue** o crea un **pull request**.

---

## 💌 Contacto

**Liser** – una forma más humana de compartir lo que amas 💚  
_Síguenos, inspírate y crea tus propias BagLists._
