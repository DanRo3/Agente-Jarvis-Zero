# 🚀 Proyecto Atlas: Un Compañero de IA Autónomo de Nueva Generación

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)![Tech Stack](https://img.shields.io/badge/tech-Python%20%7C%20React%20%7C%20Docker-blue)![License](https://img.shields.io/badge/license-MIT-lightgrey)

**Atlas** no es un chatbot. Es un framework para construir un **compañero digital autónomo** diseñado para integrarse profundamente en el ecosistema digital de un usuario. Su propósito es comprender, razonar, aprender y actuar para facilitar tareas, gestionar información y automatizar flujos de trabajo complejos de manera segura y personalizada.

---

## 📖 Tabla de Contenidos

1.  [**Visión y Filosofía**](#-visión-y-filosofía)
    - [El Problema a Resolver](#el-problema-a-resolver)
    - [El Protocolo MCP: El "USB-C" para la IA](#el-protocolo-mcp-el-usb-c-para-la-ia)
    - [Memoria Híbrida de Tres Niveles](#memoria-híbrida-de-tres-niveles)
2.  [**Arquitectura del Sistema**](#-arquitectura-del-sistema)
3.  [**Pila Tecnológica**](#-pila-tecnológica)
4.  [**Estructura del Proyecto**](#-estructura-del-proyecto)
5.  [**🚀 Primeros Pasos**](#-primeros-pasos)
    - [Prerrequisitos](#prerrequisitos)
    - [Guía de Instalación Rápida](#guía-de-instalación-rápida)
6.  [**🛠️ Flujo de Trabajo del Desarrollador**](#️-flujo-de-trabajo-del-desarrollador)
    - [Ejecutar la Aplicación](#ejecutar-la-aplicación)
    - [Gestionar Migraciones de la Base de Datos](#gestionar-migraciones-de-la-base-de-datos)
    - [Acceder a las Herramientas](#acceder-a-las-herramientas)
7.  [**⚙️ Configuración de Entorno**](#️-configuración-de-entorno)
    - [Variables del Backend](#variables-del-backend)
    - [Variables del Frontend](#variables-del-frontend)
8.  [**🗺️ Hoja de Ruta (Roadmap)**](#️-hoja-de-ruta-roadmap)
9.  [**🤝 Contribuciones**](#-contribuciones)

---

## 🔭 Visión y Filosofía

### El Problema a Resolver

Los asistentes de IA actuales son reactivos, transaccionales y carecen de memoria a largo plazo. No se adaptan al estilo, preferencias o necesidades únicas de un individuo. Atlas está diseñado para superar estas limitaciones.

### El Protocolo MCP: El "USB-C" para la IA

La piedra angular de la arquitectura es el **Model Context Protocol (MCP)**, un estándar que unifica la comunicación entre el agente y sus herramientas (servicios como Gmail, calendario, sistema de archivos, etc.).

- **Ventajas Clave:**
  - **Modularidad Extrema:** Añadir nuevas capacidades se reduce a implementar un nuevo "Servidor MCP" sin tocar el núcleo.
  - **Seguridad por Diseño:** Cada herramienta se ejecuta en su propio sandbox con permisos limitados.
  - **Interoperabilidad:** Fomenta un ecosistema de herramientas reutilizables.

### Memoria Híbrida de Tres Niveles

Para lograr una personalización real, Atlas utiliza un sistema de memoria sofisticado que imita la cognición humana.

| Nivel                  | Base de Datos  | Tipo de Memoria  | Propósito                                                            |
| :--------------------- | :------------- | :--------------- | :------------------------------------------------------------------- |
| **Nivel 1: Activo**    | **Redis**      | Corto Plazo      | Historial inmediato de la conversación para máxima fluidez.          |
| **Nivel 2: Semántico** | **Vector DB**  | Conceptual       | Almacena "recuerdos" como embeddings para búsquedas por significado. |
| **Nivel 3: Archivo**   | **PostgreSQL** | Factual y Perfil | Guarda transcripciones y el **Perfil de Usuario Evolutivo**.         |

---

## 🏛️ Arquitectura del Sistema

Atlas está construido sobre una arquitectura de microservicios orquestada por Docker Compose, garantizando una clara separación de responsabilidades y escalabilidad.

- **`Frontend`**: Una Single-Page Application (SPA) construida con **React (Vite + TypeScript)**. Es la cara de Atlas, proporcionando la interfaz de chat, el panel de monitoreo y la gestión de la cuenta.
- **`Backend`**: El cerebro de Atlas, una API de **Python (FastAPI)** que gestiona:
  - El **Agente Central** (ciclo ReAct con LangChain).
  - La autenticación de usuarios (OAuth2 con Google y JWT).
  - La comunicación en tiempo real a través de WebSockets.
  - La orquestación de las bases de datos.
- **`PostgreSQL`**: La base de datos relacional (Memoria de Nivel 3). Almacena de forma persistente los datos de usuarios, sesiones de chat y mensajes. Su esquema es gestionado por **Alembic**.
- **`Redis`**: La base de datos en memoria (Memoria de Nivel 1). Se utiliza para el caché y la gestión de la memoria a corto plazo de las conversaciones activas.

---

## 💻 Pila Tecnológica

| Área                | Tecnología                                  | Propósito                                            |
| :------------------ | :------------------------------------------ | :--------------------------------------------------- |
| **Backend**         | Python 3.11, FastAPI, SQLAlchemy, LangChain | API, lógica del agente, ORM                          |
| **Frontend**        | TypeScript, React 18, Vite, Tailwind CSS    | Interfaz de usuario reactiva y moderna               |
| **Bases de Datos**  | PostgreSQL 15, Redis 7, ChromaDB (futuro)   | Memoria factual, de corto plazo y semántica          |
| **Infraestructura** | Docker, Docker Compose                      | Contenerización y orquestación del entorno           |
| **Autenticación**   | OAuth2 (Google), JWT                        | Inicio de sesión seguro y gestión de sesiones        |
| **Migraciones**     | Alembic                                     | Control de versiones del esquema de la base de datos |

---

## 📁 Estructura del Proyecto

```
mi_agente_ia/
├── alembic/              # Scripts de migración de la base de datos
├── backend/
│   ├── app/              # Código fuente principal de la aplicación FastAPI
│   │   ├── api/          # Routers y dependencias de la API
│   │   ├── agent/        # Lógica del Agente (ReAct, Callbacks, etc.)
│   │   ├── core/         # Lógica central (seguridad, config)
│   │   ├── crud/         # Funciones de interacción con la base de datos
│   │   ├── db/           # Modelos SQLAlchemy y configuración de la DB
│   │   └── schemas/      # Modelos Pydantic para la validación de datos
│   ├── Dockerfile        # Define el contenedor del backend
│   └── requirements.txt  # Dependencias de Python
├── frontend/
│   ├── src/              # Código fuente principal de la aplicación React
│   │   ├── components/   # Componentes reutilizables de la UI
│   │   ├── context/      # Contexto de React (ej. AuthContext)
│   │   ├── pages/        # Componentes que representan páginas completas
│   │   └── services/     # Lógica de comunicación con la API
│   ├── Dockerfile        # Define el contenedor del frontend
│   └── package.json      # Dependencias de Node.js
├── docker-compose.yml    # Orquesta todos los servicios
└── README.md             # Este archivo
```

---

## 🚀 Primeros Pasos

### Prerrequisitos

- **Docker** y **Docker Compose** instalados y en ejecución.
- **Credenciales de Google OAuth** (consulta la sección de Configuración).

### Guía de Instalación Rápida

1.  **Clonar el Repositorio**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd mi_agente_ia
    ```

2.  **Configurar el Backend**
    Copia el archivo de ejemplo y rellena las variables de entorno.

    ```bash
    cp backend/.env.example backend/.env
    # Ahora edita backend/.env con tus claves y secretos
    ```

3.  **Configurar el Frontend**
    Copia el archivo de ejemplo y añade tu ID de cliente de Google.

    ```bash
    cp frontend/.env.example frontend/.env
    # Ahora edita frontend/.env con tu VITE_GOOGLE_CLIENT_ID
    ```

4.  **Construir y Ejecutar los Contenedores**
    Este comando construirá las imágenes de Docker y levantará toda la aplicación.
    ```bash
    docker-compose up --build
    ```
    - El **Frontend** estará disponible en `http://localhost:5173`.
    - La **API del Backend** estará disponible en `http://localhost:8000`.

---

## 🛠️ Flujo de Trabajo del Desarrollador

### Ejecutar la Aplicación

- Para iniciar todos los servicios en segundo plano: `docker-compose up -d`
- Para ver los logs en tiempo real de un servicio: `docker-compose logs -f backend`
- Para detener todos los servicios: `docker-compose down`

### Gestionar Migraciones de la Base de Datos

**Nunca modifiques la base de datos manualmente.** Usa Alembic para mantener el esquema sincronizado con tus modelos de SQLAlchemy.

**El ciclo de trabajo es:**

1.  **Modifica el Modelo:** Haz cambios en un archivo dentro de `backend/app/db/models.py`.

2.  **Genera el Script de Migración:**

    ```bash
    docker-compose run --rm backend alembic revision --autogenerate -m "Un mensaje descriptivo del cambio"
    ```

3.  **Aplica la Migración:**
    ```bash
    docker-compose run --rm backend alembic upgrade head
    ```

### Acceder a las Herramientas

- **Documentación Interactiva de la API (Swagger):** `http://localhost:8000/docs`
- **Conexión a PostgreSQL:** Puedes conectarte usando tus credenciales a `localhost:5432`.

---

## ⚙️ Configuración de Entorno

### Variables del Backend (`backend/.env`)```ini

# API de OpenAI (o cualquier otro LLM)

OPENAI_API_KEY="sk-..."

# Base de Datos PostgreSQL

DATABASE_URL="postgresql://danro:danrodev@postgres:5432/agente_db"

# Herramienta de Búsqueda

TAVILY_API_KEY="tvly-..."

# Credenciales de Google OAuth

GOOGLE_CLIENT_ID="..."
GOOGLE_CLIENT_SECRET="..."

# Configuración de JWT

JWT_SECRET_KEY="..."
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=43200

````

### Variables del Frontend (`frontend/.env`)```ini
# El prefijo VITE_ es obligatorio para que Vite las exponga al cliente
VITE_GOOGLE_CLIENT_ID="...apps.googleusercontent.com"
````

---

## 🗺️ Hoja de Ruta (Roadmap)

- **✅ Fase 1: Fundación (Q4 2025):**
  - Agente Central (ReAct) y Memoria Híbrida (PostgreSQL).
  - Autenticación de Usuarios con Google y JWT.
  - Primeras herramientas: Búsqueda en Internet.
- **◻️ Fase 2: Integración Externa (Q1 2026):**
  - Servidores MCP para `Email` y `Calendar`.
  - Perfil de Usuario Evolutivo y Prompt Dinámico.
- **◻️ Fase 3: Autonomía Local (Q2 2026):**
  - Servidor MCP para `FileSystem` con sandbox de seguridad.
- **◻️ Fase 4: Inteligencia Proactiva (Q3 2026):**
  - Motor de "triggers" para acciones basadas en eventos.

---

## 🤝 Contribuciones

Actualmente, el proyecto está en una fase inicial de desarrollo. Las contribuciones son bienvenidas. Por favor, abre un "issue" para discutir cambios importantes antes de enviar un "pull request".
