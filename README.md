# Sistema de Autenticación en Flask - Aerolínea Auth ✈️

Este proyecto implementa un sistema de autenticación en Flask diseñado para una aerolínea. Incluye funcionalidades como registro de usuarios, inicio de sesión, recuperación de contraseña, y gestión de reservas de vuelos. Además, se han implementado características adicionales como confirmación de cuenta por correo y recuperación de contraseña mediante un enlace enviado al correo electrónico.

---

## **Características principales**

### **Registro de usuario con almacenamiento seguro de contraseña**
✔️ Implementado en `routes.py` en la ruta `/register/`.  
✔️ Las contraseñas se almacenan de forma segura utilizando `bcrypt`.

### **Inicio de sesión con validación de credenciales**
✔️ Implementado en `routes.py` en la ruta `/login/`.  
✔️ Se valida el correo y la contraseña utilizando `bcrypt` para comparar el hash.

### **Recuperación de contraseña**
✔️ Implementado en `routes.py` en las rutas `/reset_password` y `/reset_password/<token>`.  
✔️ Se envía un correo con un enlace para restablecer la contraseña.

### **Uso de sesiones (`flask.session`) para gestionar usuarios autenticados**
✔️ Implementado en `routes.py` con `Flask-Login` y el decorador `@login_required`.  
✔️ La sesión se mantiene activa por 1 minuto gracias al manejador `@routes.before_app_request`.

---

## **Bonificaciones**

### **Enviar un correo de confirmación al registrarse para activar la cuenta**
✔️ Implementado en `routes.py` en las rutas `/register/` y `/confirmar_cuenta/<token>`.  
✔️ Se utiliza `utils.py` para generar y verificar tokens de activación.

### **Enviar un correo con un enlace o código para la recuperación de contraseña**
✔️ Implementado en `routes.py` en la ruta `/reset_password`.  
✔️ Se utiliza `utils.py` para generar y verificar tokens de recuperación.

---

## **Criterios de evaluación**

### **Código funcional**
✔️ Todas las funcionalidades principales (registro, inicio de sesión, recuperación de contraseña) están implementadas y funcionales.

### **Buenas prácticas**
✔️ El proyecto está estructurado con Blueprints (`routes.py`).  
✔️ Se utilizan extensiones como `Flask-WTF` para formularios y validaciones.  
✔️ Las contraseñas se almacenan de forma segura con `bcrypt`.

### **Seguridad en contraseñas**
✔️ Las contraseñas se almacenan como hashes utilizando `bcrypt`.  
✔️ Se valida que las contraseñas tengan un mínimo de 8 caracteres.

### **Estructura del proyecto**
✔️ El proyecto está bien organizado con archivos separados para rutas, modelos, formularios y utilidades.  
✔️ Se utiliza un archivo `.env` para almacenar configuraciones sensibles como claves secretas y credenciales de correo.

---

## **Requisitos previos**

- Python 3.8 o superior.
- Entorno virtual configurado (opcional pero recomendado).
- SQLite (base de datos predeterminada).

---

## **Instalación**

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/aerolinea-auth.git
   cd aerolinea-auth





   python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


pip install flask

pip install -r requirements.txt


SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///database.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-correo@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicación
MAIL_DEFAULT_SENDER=tu-correo@gmail.com




flask db init
flask db migrate -m "Inicializar base de datos"
flask db upgrade




python main.py



---

### **2. Agregar un archivo `LICENSE`**
Incluye una licencia para que otros desarrolladores sepan cómo pueden usar tu proyecto. Por ejemplo, una licencia MIT:

#### Archivo `LICENSE`:
```plaintext
MIT License

Copyright (c) 2025 Alejandro Areiza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.