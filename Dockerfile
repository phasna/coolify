FROM php:8.2-apache

# Extension PDO MySQL pour la connexion à MariaDB
RUN docker-php-ext-install pdo pdo_mysql

# Configuration Apache pour éviter le 403
COPY apache-config.conf /etc/apache2/conf-available/chatlog.conf
RUN a2enconf chatlog

# Copie des fichiers de l'application (pas de volume = fichiers intégrés à l'image)
COPY index.php /var/www/html/
RUN echo 'Require all granted' > /var/www/html/.htaccess
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html
