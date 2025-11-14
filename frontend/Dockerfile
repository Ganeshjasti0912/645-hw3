# Use official NGINX image
FROM nginx:latest

# Remove default NGINX website
RUN rm -rf /usr/share/nginx/html/*

# Copy your website files into container
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# NGINX automatically starts
