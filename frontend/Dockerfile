# --- Etapa 1: Build ---
# Usa la imagen oficial de Bun, que ya tiene el comando "bun" instalado
FROM oven/bun:1 AS builder

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de definición del proyecto.
# Nota: El archivo de lock se llama "bun.lockb"
COPY package.json bun.lock ./

# Instala las dependencias usando el comando bun que SÍ existe en esta imagen
# --frozen-lockfile asegura que se use exactamente lo que está en bun.lockb
RUN bun install --frozen-lockfile

# Copia el resto de los archivos de la aplicación
COPY . .

# Construye la aplicación para producción
RUN bun run build

# --- Etapa 2: Serve ---
# Usa una imagen de Nginx ligera para servir los archivos estáticos
FROM nginx:1.25-alpine

# Copia los archivos construidos de la etapa anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Expone el puerto 80
EXPOSE 80

# El comando por defecto de nginx se encarga de iniciar el servidor
CMD ["nginx", "-g", "daemon off;"]