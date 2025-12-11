# Sistema RAG de Consejos de Salud

Sistema de recuperación aumentada por generación (RAG) para proporcionar consejos de salud y mejores hábitos basados en documentos especializados.

## 📁 Estructura del Proyecto

```
health_RAG/
├── docs/                    # Carpeta para los documentos de salud
├── config.py               # Configuración del sistema
├── document_loader.py      # Carga y procesamiento de documentos
├── prompts.py              # Prompts personalizados
├── rag_system.py           # Sistema RAG principal
├── main.py                 # Aplicación principal
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## 🚀 Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Asegúrate de tener Ollama instalado y corriendo:**
   - Descarga Ollama desde: https://ollama.ai
   - Instala el modelo que usarás (por defecto: `gemma3:1b`):
   ```bash
   ollama pull gemma3:1b
   ```

3. **Coloca tus documentos en la carpeta `docs/`**

## 📚 Sobre los Documentos

### ¿Qué formato de nombres usar?

**Respuesta corta:** Cualquier nombre descriptivo funciona bien.

**Recomendaciones:**
- Puedes usar cualquier nombre que te resulte útil: `nutricion.pdf`, `ejercicio_fisico.txt`, `habitos_sueno.docx`, etc.
- El sistema detecta automáticamente el tipo de archivo por su extensión
- Los nombres descriptivos te ayudarán a identificar qué documentos se están usando en las respuestas

**Formatos soportados:**
- `.pdf` - Archivos PDF
- `.txt` - Archivos de texto plano
- `.md` - Archivos Markdown
- `.docx` - Documentos de Word

### Ejemplos de nombres útiles:
```
docs/
├── nutricion_basica.pdf
├── ejercicios_cardio.txt
├── habitos_sueno.md
├── salud_mental.docx
└── cualquier_nombre.pdf  # También funciona
```

## 🎯 Uso

### Ejecutar la aplicación:

```bash
python main.py
```

### Modo interactivo:

Una vez iniciado, puedes:
- Hacer preguntas sobre salud y hábitos
- Cambiar el número de documentos consultados escribiendo `docs N` (ej: `docs 6`)
- Escribir `salir` o `exit` para terminar

### Ejemplo de uso:

```
Tu pregunta: ¿Cuáles son los mejores hábitos para dormir bien?

Buscando información relevante...

============================================================
RESPUESTA:
============================================================
[La respuesta basada en tus documentos]

📚 Documentos consultados (4):
  1. habitos_sueno.md
  2. salud_mental.docx
  ...
```

## ⚙️ Configuración

Puedes modificar la configuración en `config.py`:

- `LLM_MODEL`: Modelo de Ollama a usar
- `RETRIEVER_K`: Número de documentos a recuperar por defecto
- `CHUNK_SIZE`: Tamaño de los chunks de texto
- `CHUNK_OVERLAP`: Solapamiento entre chunks

## 🔍 Cómo Funciona

1. **Carga de documentos:** El sistema carga todos los documentos de la carpeta `docs/`
2. **Procesamiento:** Divide los documentos en chunks más pequeños
3. **Indexación:** Crea un índice vectorial usando embeddings
4. **Búsqueda:** Cuando haces una pregunta, busca los documentos más relevantes
5. **Generación:** El LLM genera una respuesta basada en los documentos encontrados

## 📝 Notas

- El sistema solo usa información de los documentos proporcionados
- Si no encuentra información relevante, lo indicará claramente
- Puedes ajustar cuántos documentos consultar según la complejidad de tu pregunta
- Los documentos se cargan automáticamente al iniciar la aplicación

## 🛠️ Solución de Problemas

**Error: "No se encontraron documentos"**
- Asegúrate de tener archivos en la carpeta `docs/`
- Verifica que los archivos tengan una extensión soportada

**Error: "Modelo no encontrado"**
- Verifica que Ollama esté corriendo: `ollama list`
- Instala el modelo: `ollama pull gemma3:1b`

**Respuestas lentas:**
- Reduce el número de documentos consultados (`docs 2`)
- Usa un modelo más pequeño
- Reduce el `CHUNK_SIZE` en `config.py`





