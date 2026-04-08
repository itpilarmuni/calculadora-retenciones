# Calculadora Fiscal Municipal — Pilar

App web para calcular retenciones ARBA / Ganancias / SUSS.  
Corre 100% en GitHub Pages (sin servidor).

---

## Estructura del repo

```
calculadora-fiscal/
├── index.html            ← app web (subir a GitHub Pages)
├── convert_to_sqlite.py  ← script Python para actualizar el padrón
└── README.md
```

---

## Configuración inicial (una sola vez)

### 1. Crear el repo en GitHub
1. Crear repo nuevo: `calculadora-fiscal` (puede ser privado o público)
2. Subir `index.html` y `README.md`
3. Ir a **Settings → Pages → Source: Deploy from a branch → main → / (root)**
4. GitHub te da la URL: `https://TU_USUARIO.github.io/calculadora-fiscal`

---

## Actualización mensual del padrón

### Paso 1 — Descargar ZIP de ARCA
Ir a: https://www.afip.gob.ar/genericos/cInscripcion/archivoCompleto.asp  
Descargar el ZIP del padrón completo.

### Paso 2 — Convertir a SQLite
1. Abrir `convert_to_sqlite.py` (doble click)
2. Seleccionar el ZIP descargado
3. Esperar que termine → genera `padron.sqlite` en la misma carpeta

### Paso 3 — Subir a GitHub Releases
1. Ir al repo en GitHub
2. Click en **Releases** (columna derecha) → **Draft a new release**
3. Tag version: `v2025-01` (el mes que corresponda)
4. Arrastrar `padron.sqlite` al área de archivos adjuntos
5. Click **Publish release**
6. Copiar la URL del archivo: botón derecho → Copiar dirección del enlace

### Paso 4 — Actualizar la URL en index.html (opcional)
Si querés que la página proponga la URL automáticamente, editar esta línea en `index.html`:
```
'https://github.com/TU_USUARIO/TU_REPO/releases/download/v1/padron.sqlite'
```
Reemplazarla por la URL del nuevo release.

---

## Cómo usan la app los empleados

1. Abrir la URL de GitHub Pages
2. Primera vez: click en **"Cargar SQLite"** o **"Cargar desde URL"**  
   → el padrón se guarda en el navegador automáticamente
3. Las próximas veces: la página ya tiene el padrón, listo para usar
4. Cuando hay padrón nuevo: volver a cargarlo con el mismo botón

---

## Nota sobre consulta ARBA
La consulta en tiempo real a padron.devos.com.ar no está disponible desde el navegador 
por restricciones CORS. Los usuarios deben verificar ARBA manualmente en ese sitio.
Para tener la alícuota correcta, usar los botones de override manual (1,5% / 2,5%).
