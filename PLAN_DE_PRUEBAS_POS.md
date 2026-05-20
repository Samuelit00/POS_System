# Plan de Pruebas - Sistema POS XYZ

## 1. Informacion general

- Proyecto: POS XYZ (FastAPI + PostgreSQL + frontend web)
- Version evaluada: estado actual del repositorio
- Autor del plan: Samuel (equipo de proyecto)
- Fecha: 2026-03-17
- Base de referencia: buenas practicas de plan de pruebas (alcance, DoR/DoD, estrategia, entregables, dependencias, entorno, riesgos, roles)

## 2. Objetivos del plan

### 2.1 Objetivo general

Definir y ejecutar un proceso de pruebas funcionales para validar que el sistema POS XYZ cumpla con los requerimientos principales de autenticacion, gestion de usuarios, gestion de productos, ventas, inventario y dashboard, asegurando un comportamiento correcto y confiable para su uso academico.

### 2.2 Objetivos especificos

- Verificar el flujo de autenticacion (inicio y control de sesion) en condiciones validas e invalidas.
- Validar operaciones CRUD basicas de usuarios y productos desde API/UI.
- Comprobar que el registro de ventas actualiza correctamente el inventario.
- Confirmar reglas de negocio criticas, como bloqueo por stock insuficiente y validaciones de campos.
- Evaluar que las metricas del dashboard reflejen los datos operativos esperados.
- Detectar y documentar defectos por severidad para su correccion y seguimiento.
- Generar evidencia de ejecucion (casos, resultados y reporte final) para sustentar la calidad alcanzada.

## 3. Alcance

### 3.1 En alcance (que SI se probara)

- Login y control de sesion por token JWT.
- Acceso a paginas principales del sistema autenticado.
- CRUD basico de usuarios.
- CRUD basico de productos.
- Flujo de ventas con validacion de stock.
- Actualizacion de inventario despues de una venta.
- Consulta de ventas por listado y detalle.
- Carga de metricas del dashboard.
- Validaciones basicas de datos en API (campos obligatorios y reglas minimas).

### 3.2 Fuera de alcance (que NO se probara en esta fase)

- Pruebas de carga masiva y stress a nivel productivo.
- Pruebas de seguridad avanzadas tipo pentesting.
- Compatibilidad en multiples navegadores/OS en profundidad.
- Migraciones de base de datos y despliegue cloud.
- Pruebas de accesibilidad formal bajo normas WCAG completas.

## 4. Criterios de entrada y salida (DoR / DoD)

### 4.1 DoR (Definition of Ready) - Criterios de entrada

Antes de ejecutar pruebas, debe cumplirse:

- Repositorio clonado y dependencias instaladas.
- Entorno virtual activo y variables en archivo .env configuradas.
- Base de datos PostgreSQL disponible y conectada.
- Aplicacion inicia sin errores bloqueantes (uvicorn levanta correctamente).
- Usuario admin disponible para pruebas funcionales.
- Datos minimos de prueba cargados (al menos 3 productos y 1 usuario vendedor).
- Casos de prueba revisados y entendidos por quien ejecuta.

### 4.2 DoD (Definition of Done) - Criterios de salida

Las pruebas de una iteracion se consideran completas cuando:

- 100% de casos criticos ejecutados (login, venta, stock, dashboard).
- Al menos 90% de casos planificados ejecutados en total.
- 0 defectos criticos abiertos.
- Defectos altos con workaround documentado o corregidos.
- Evidencias guardadas (resultado de casos y hallazgos).
- Informe de cierre de pruebas emitido.

## 5. Estrategia de pruebas

Se aplicara una estrategia mixta, priorizando simplicidad y utilidad para aprendizaje:

- Pruebas manuales funcionales end-to-end desde UI.
- Pruebas de API basicas (Swagger/cliente HTTP) para validar codigos y respuestas.
- Pruebas de regresion ligera sobre flujos criticos luego de cada cambio.
- Pruebas exploratorias cortas para detectar errores no previstos.

### 5.1 Niveles/tipos de prueba

- Smoke test: validar que el sistema arranca y responde en rutas clave.
- Funcionales: validar reglas de negocio por modulo.
- Integracion: validar que frontend, API y DB trabajan en conjunto.
- Regresion: reejecutar casos criticos despues de cambios.

### 5.2 Priorizacion

- Prioridad Alta: login, crear venta, descuento de stock, consulta de ventas.
- Prioridad Media: CRUD de usuarios y productos, metricas dashboard.
- Prioridad Baja: detalles visuales menores en UI.

## 6. Entregables

Los entregables de pruebas seran:

- Plan de pruebas (este documento).
- Matriz de casos de prueba.
- Evidencias de ejecucion (capturas y/o logs breves).
- Registro de defectos (tabla simple: id, severidad, estado, descripcion).
- Reporte de avance (por ciclo).
- Reporte final de pruebas (resumen de cobertura, defectos y estado final).

## 7. Dependencias

Para ejecutar pruebas, se depende de:

- Python 3.8+.
- PostgreSQL 12+.
- Librerias del archivo requirements.txt.
- Variables de entorno correctas (DATABASE_URL, SECRET_KEY, etc.).
- Datos base validos para usuarios/productos/ventas.
- Disponibilidad local del servidor FastAPI.

## 8. Entorno de pruebas

### 8.1 Ambiente

- Tipo: Local (desarrollo)
- Backend: FastAPI (uvicorn)
- Base de datos: PostgreSQL local
- Frontend: Templates + JS estatico

### 8.2 Configuracion sugerida

- URL aplicacion: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: /health
- Usuario inicial: admin@example.com (segun script local de admin)

### 8.3 Datos de prueba minimos

- Usuario admin (existente)
- 1 usuario vendedor
- 3 productos con stock > 0
- 1 producto con stock bajo (<10) para validar metrica

## 9. Gestion de riesgos

| Riesgo | Impacto | Probabilidad | Mitigacion |
|---|---|---|---|
| Fallo de conexion a DB | Alto | Media | Verificar .env, credenciales y servicio PostgreSQL antes de pruebas |
| Datos de prueba insuficientes | Medio | Alta | Definir dataset minimo y checklist previo |
| Defectos en flujo de venta/stock | Alto | Media | Priorizar pruebas de venta e inventario al inicio |
| Cambios de codigo durante pruebas | Medio | Media | Congelar version por ciclo corto y repetir regresion critica |
| Falta de tiempo academico | Alto | Alta | Priorizar casos criticos y reportar cobertura real |
| Conocimiento limitado en QA | Medio | Alta | Usar casos claros, plantillas simples y ejecucion guiada |

## 10. Roles y responsabilidades

| Rol | Responsable | Responsabilidades |
|---|---|---|
| QA Lead (academico) | Estudiante responsable | Definir plan, priorizar pruebas, consolidar reporte final |
| Tester funcional | Estudiante/equipo | Ejecutar casos, registrar evidencias y defectos |
| Desarrollador backend | Equipo dev | Corregir errores API/logica y apoyar analisis tecnico |
| Desarrollador frontend | Equipo dev | Corregir errores UI/flujo de usuario |
| Revisor (profesora/tutor) | Docente | Revisar calidad del plan y resultados reportados |

## 11. Casos de prueba base (resumen entendible)

| ID | Caso | Precondicion | Paso principal | Resultado esperado | Prioridad |
|---|---|---|---|---|---|
| CP-01 | Login exitoso | Usuario admin existe | Ingresar email y password validos | Acceso al dashboard y token guardado | Alta |
| CP-02 | Login fallido | Usuario existe | Ingresar password invalido | Mensaje de credenciales invalidas | Alta |
| CP-03 | Bloqueo por no autenticado | Sin token | Abrir ruta protegida | Redireccion a /login | Alta |
| CP-04 | Crear producto valido | Sesion activa | Crear producto con precio>0 y stock>=0 | Producto creado y visible en listado | Media |
| CP-05 | Crear producto invalido | Sesion activa | Enviar precio <= 0 | API/UI rechaza solicitud | Alta |
| CP-06 | Crear usuario duplicado | Email ya registrado | Intentar crear usuario con mismo email | Error por email registrado | Media |
| CP-07 | Venta con stock suficiente | Producto con stock >= cantidad | Registrar venta de producto | Venta creada y stock disminuye | Alta |
| CP-08 | Venta con stock insuficiente | Producto con stock < cantidad | Registrar venta excediendo stock | Error de stock insuficiente | Alta |
| CP-09 | Listar ventas por fecha | Hay ventas registradas | Consultar ventas con filtros | Retorna ventas dentro del rango | Media |
| CP-10 | Ver metricas dashboard | Datos cargados | Abrir dashboard | Muestra ventas hoy, ingresos, stock bajo, usuarios | Media |
| CP-11 | Health check | Servidor arriba | GET /health | Respuesta status ok | Alta |
| CP-12 | Eliminar producto | Producto existe | Eliminar producto desde UI/API | Producto removido del listado | Baja |

## 12. Flujo de ejecucion recomendado (simple)

1. Ejecutar smoke: CP-11, CP-01.
2. Ejecutar modulo productos: CP-04, CP-05, CP-12.
3. Ejecutar modulo usuarios: CP-06.
4. Ejecutar ventas e inventario: CP-07, CP-08, CP-09.
5. Ejecutar dashboard: CP-10.
6. Repetir CP-01, CP-07 y CP-10 como mini regresion final.

## 13. Criterios de severidad de defectos

- Critico: impide usar flujo principal (ejemplo: no se puede vender).
- Alto: afecta funcionalidad importante con impacto fuerte.
- Medio: afecta funcionalidad secundaria con workaround.
- Bajo: detalle visual o menor, sin bloquear operacion.

## 14. Formato minimo de reporte final

- Resumen ejecutivo (1 parrafo)
- Cobertura ejecutada (casos ejecutados vs planificados)
- Defectos por severidad
- Defectos abiertos/cerrados
- Riesgos remanentes
- Recomendacion de salida: Aprobado / Aprobado con observaciones / No aprobado

## 15. Notas para iteraciones futuras

- Agregar pruebas automatizadas de API para login, productos y ventas.
- Incluir pruebas de rendimiento de endpoint de ventas y dashboard.
- Mejorar validaciones de esquema para detalles de venta.
- Definir datos semilla consistentes para pruebas repetibles.
