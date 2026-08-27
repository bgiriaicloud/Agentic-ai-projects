# Use lightweight node alpine image
FROM node:20-alpine

# Set working directory inside container
WORKDIR /usr/src/app

# Copy dependency manifests
COPY package*.json ./

# Install production dependencies
RUN npm ci --only=production

# Copy application source files
COPY src ./src

# Expose default application port
EXPOSE 8080

# Environment variables
ENV PORT=8080
ENV NODE_ENV=production

# Start application server
CMD ["node", "src/app.js"]
