# wp-mapper
A Python-based WordPress mapper, a small content-discovery tool  that uses a local WordPress directory tree as a wordlist to enumerate a target site. For lab/authorized testing.

## 
## 1. Download and unpack a copy of WordPress: https://wordpress.org/download/ here: `/home/kali/Downloads/wordpress`
## 2. Local Wordpress with Docker:
```bash
mkdir wp-lab && cd wp-lab
```
### 2.1 Create docker-compose.yml:
```yaml
services:
  db:
    image: mysql:8.0
    command: --default-authentication-plugin=mysql_native_password
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wpuser
      MYSQL_PASSWORD: wppass
      MYSQL_ROOT_PASSWORD: rootpass
    volumes:
      - db_data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppass
    volumes:
      - wp_data:/var/www/html

volumes:
  db_data:
  wp_data:
```
## 3. Run: 
```bash
docker compose up -d
```
## 4. Then open http://localhost:8080 and finish the WP setup. You can test the mapper without registering/logging in. We are just testing if WP endpoints exist.

## 5. Run:
```bash
python mapper.py 
```
## 6. You are good, if you see something like this: 
#### OUTPUT:
```bash
/wp-comments-post.php
/wp-activate.php
/wp-cron.php
/readme.html
/wp-trackback.php
/wp-config-sample.php
/wp-load.php
/wp-login.php
/wp-mail.php
/wp-settings.php
/wp-blog-header.php
/wp-links-opml.php
/xmlrpc.php
/index.php
/wp-signup.php
/license.txt
/wp-includes/class-wp-block.php
...
/wp-content/plugins/akismet/class.akismet.php
/wp-content/plugins/akismet/readme.txt
/wp-content/plugins/akismet/index.php
/wp-content/plugins/akismet/.htaccess
/wp-content/plugins/akismet/class.akismet-widget.php
/wp-content/plugins/akismet/LICENSE.txt
/wp-content/plugins/akismet/class.akismet-rest-api.php
/wp-content/plugins/akismet/changelog.txt
/wp-content/plugins/akismet/wrapper.php
/wp-content/plugins/akismet/_inc/akismet.js
/wp-content/plugins/akismet/_inc/akismet-frontend.js
/wp-content/plugins/akismet/_inc/akismet-admin.js
/wp-content/plugins/akismet/_inc/img/akismet-refresh-logo.svg
/wp-content/plugins/akismet/_inc/img/arrow-left.svg
/wp-content/plugins/akismet/views/compatible-plugins.php
/wp-content/plugins/akismet/views/activate.php
```
We see full paths to .txt and .js files. Good! Our mapper is discovering directories and enumerating files under them. 

## 7. You can verify it using curl:
```bash
┌──(kali㉿kali)-[~]
└─$ curl -I http://localhost:8080/wp-content/plugins/akismet/changelog.txt
HTTP/1.1 403 Forbidden
Date: Fri, 13 Feb 2026 00:56:51 GMT
Server: Apache/2.4.66 (Debian)
Content-Type: text/html; charset=iso-8859-1

                                                                             
┌──(kali㉿kali)-[~]
└─$ curl -I http://localhost:8080/wp-content/plugins/akismet/_inc/akismet.js
HTTP/1.1 200 OK
Date: Fri, 13 Feb 2026 00:57:27 GMT
Server: Apache/2.4.66 (Debian)
Last-Modified: Wed, 29 Oct 2025 23:16:57 GMT
ETag: "3142-64254542a2c40"
Accept-Ranges: bytes
Content-Length: 12610
Vary: Accept-Encoding
Content-Type: text/javascript

                                                                             
┌──(kali㉿kali)-[~]
└─$ curl -I http://localhost:8080/wp-content/plugins/akismet/class.akismet-rest-api.php

HTTP/1.1 403 Forbidden
Date: Fri, 13 Feb 2026 00:59:01 GMT
Server: Apache/2.4.66 (Debian)
Content-Type: text/html; charset=iso-8859-1
```

## 8. Then press Enter to continue: 
```bash
.../wp-admin/js/widgets/media-video-widget.js
/wp-admin/js/widgets/media-gallery-widget.min.js
/wp-admin/js/widgets/text-widgets.min.js
/wp-admin/js/widgets/media-audio-widget.min.js
/wp-admin/js/widgets/media-image-widget.min.js
Press return to continue.
Spawning thread 0
Spawning thread 1
Spawning thread 2
Spawning thread 3
Spawning thread 4
Spawning thread 5
Spawning thread 6
Spawning thread 7
Spawning thread 8
Spawning thread 9
-+--+++++++++++++++++++++-++-++++++-+++++-+++-++++++++++--++++-++++-+++++++++++++-+-+-++++-+++++++++-+++-+++++-+++++++++--+++++++-+-++++-+-+++++--++++++++--+++---+++-++-+++--+++++++++-++++++--++--+++-+++++-+-+++-++++++-+++++++-+-++++--++++++++-+-++-++++-+++++++-+++-+++++-+++++++++++++++++++++++++++++-++++++----+++++++++-+++-+-++---+-----+-+-+--+-----------+-------+++++++++-++++-++-+++++++++++--+++++++-++++++++++------+----------------------------------+++---++-+---+------------------------+----------------------++++++++++++++++++------------------------+++-++++++++++-------------+-----------------------------------------+-------+------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-++++-+----+----------+-+-++++++--------+--------++-+-++++--+-++++++++++++++++--------------------------++++++---++++++++++++-+-+++++++-++++++++++++++++-------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-++-----+------------------+----------+------+++++++++-+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------+++++-------------++++++++++++-++++++++++++++++-++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-+-++--+--++-+--+-++-++++--++-++++----+++----++-+-+-+-+-+---++----+-+----+-+-+-+-++-+--++--+-+-+-+-----++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++done
```

## 8. Check the saved results:
```bash
cat myanswers.txt 
http://localhost:8080/readme.html
http://localhost:8080/wp-trackback.php
http://localhost:8080/wp-cron.php
http://localhost:8080/wp-load.php
http://localhost:8080/wp-mail.php
http://localhost:8080/wp-activate.php
http://localhost:8080/wp-login.php
http://localhost:8080/wp-links-opml.php
http://localhost:8080/wp-blog-header.php
http://localhost:8080/xmlrpc.php
http://localhost:8080/index.php
http://localhost:8080/wp-includes/class-wp-block.php
http://localhost:8080/license.txt
http://localhost:8080/wp-includes/class-wp-block-bindings-registry.php
http://localhost:8080/wp-includes/class-wp-block-pattern-categories-registry.php
http://localhost:8080/wp-includes/bookmark-template.php
http://localhost:8080/wp-signup.php
http://localhost:8080/wp-includes/script-modules.php
http://localhost:8080/wp-includes/class-wp-dependencies.php
http://localhost:8080/wp-includes/class-wp-http-encoding.php
```
