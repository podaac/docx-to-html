FROM nginx

# remove default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# replace with our own nginx.conf
COPY dev.nginx.conf /etc/nginx/conf.d/
