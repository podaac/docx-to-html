FROM nginx

# remove default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# replace with our own nginx.conf for production
COPY prod.nginx.conf /etc/nginx/conf.d/
