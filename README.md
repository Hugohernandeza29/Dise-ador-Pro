# Diseñador Pro

Primera versión funcional de un editor personal de piezas de Banco Amazonas, por capas y con Gellix integrada.

## Empezar sin instalar

1. En GitHub, pulsa **Code → Download ZIP**.
2. Extrae el ZIP en tu computadora.
3. Abre **index.html** con Chrome, Edge o Firefox.
4. Selecciona un texto del ejemplo y edítalo en el panel derecho. Arrastra los elementos para moverlos.

No requiere cuenta, servidor, conexión a Internet ni instalación de dependencias. Si el navegador de tu organización bloquea archivos HTML locales, utiliza un servidor local o un alojamiento web estático autorizado.

## Funciones disponibles

- Capas de texto Gellix, formas e imágenes PNG/JPG/WebP.
- Posición, dimensiones, proporciones, color, peso, cursiva y alineación.
- Duplicar, eliminar, reordenar, ocultar y bloquear capas.
- Deshacer y rehacer.
- Formatos de feed, historias, mailing, banner y banca digital.
- Guardado automático en el navegador y descarga de proyecto JSON con imágenes incorporadas.
- Abrir proyectos JSON y exportar PNG/JPG a resolución original, sin marcas de selección.

Usa **Guardar proyecto** para conservar una copia editable fuera del navegador. Borrar los datos del navegador elimina el guardado automático. La exportación PNG/JPG es una imagen plana; conserva también el JSON.

## Alcance de esta versión

Las imágenes importadas conservan sus elementos unidos: no se recuperan automáticamente las capas de un JPG o PNG. Los textos nuevos sí son editables. Puedes importar logos oficiales desde tu computadora; los logos originales no vienen incluidos. Todavía no hay generación con IA, eliminación de fondos ni publicación en redes. No se envían piezas ni fotografías a un servidor.

Consultar [criterios de marca](docs/criterios-de-marca.md). Los archivos Gellix aportados por el usuario están incorporados en el HTML para permitir su uso sin conexión; mantener su uso dentro del alcance autorizado por su licencia. Los PDF originales no están publicados en este repositorio.

## Desarrollo y validación

El editor utiliza HTML, CSS y JavaScript sin dependencias de ejecución ni proceso de compilación. Para servirlo localmente:

```sh
cd /workspace/Dise-ador-Pro
python3 -m http.server 8000 --bind 127.0.0.1
```

La prueba funcional `tests/smoke.py` requiere Python, Playwright y Chromium en `/usr/bin/chromium`:

```sh
python3 tests/smoke.py
```

Comprueba edición de texto, posiciones, capas, historial, proyectos, importación de imagen, proporciones, exportación PNG/JPG y persistencia. El script levanta su propio servidor temporal de prueba.
