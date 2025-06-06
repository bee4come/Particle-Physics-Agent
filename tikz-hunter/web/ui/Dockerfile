# tikz-hunter/web/ui/Dockerfile
# Stage 1: Build the React application
FROM node:16-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:1.21-alpine

# Copy the build output from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for Nginx
EXPOSE 80

# When the container starts, Nginx will serve the files by default.
CMD ["nginx", "-g", "daemon off;"]