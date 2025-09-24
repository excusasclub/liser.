# Liser ver2

![Liser Logo](https://via.placeholder.com/150x50?text=Liser)

**Liser** es una aplicación web desarrollada en **Django 5.2** que permite a influencers, creadores de contenido y cualquier usuario organizar y compartir **listas de productos**, llamadas **BagLists**, de manera visual, atractiva y estructurada.  

Los seguidores pueden ver estas listas, inspirarse, guardar productos o añadirlos a sus propias listas. Para los creadores, Liser facilita la gestión y monetización de recomendaciones.

---

## Tabla de contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación y setup](#instalación-y-setup)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Modelos principales](#modelos-principales)
- [Administración](#administración)
- [GitHub](#github)
- [Contribución](#contribución)
- [Licencia](#licencia)

---

## Características

- Crear y gestionar **BagLists** (listas de productos) con secciones y items.
- Configurar visibilidad de cada BagList: privada, no listada, registrada o pública.
- Snapshots de productos externos para mantener historial de información.
- Etiquetas (Tags) para organizar listas.
- Favoritos: usuarios pueden marcar BagLists y productos como favoritos.
- Sistema de **facetas** (Facet) para filtrar BagLists por: país, temporada, uso, duración.
- Campos personalizados en secciones de BagList (SectionFieldDef) para organizar información específica de cada producto.
- Gestión de usuarios mediante perfil (Profile).
- Interfaz de administración de Django lista para usar.

---

## Tecnologías

- **Python 3.11**
- **Django 5.2**
- Base de datos **MySQL**  
  (conexión: `host=75.102.57.151`, `database=elclubdelaexcusa_liserdb`, `user=elclubdelaexcusa_pedrodch`)
- Entorno virtual: **venv**
- Control de versiones: **Git & GitHub**
- Frontend: Tailwind CSS para UI

---

## Instalación y setup

1. Clonar el repositorio:

```bash
git clone https://github.com/excusasclub/liser_ver2.git
cd liser_ver2
