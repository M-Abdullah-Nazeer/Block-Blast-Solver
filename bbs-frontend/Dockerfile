FROM node:18

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy frontend code
COPY . .

# Set environment variable for API URL
# ENV NEXT_PUBLIC_API_URL="http://localhost:8000"

# Build for production
RUN npm run build

# Expose frontend port
EXPOSE 3000

# Start Next.js server
CMD ["npm", "start"]
