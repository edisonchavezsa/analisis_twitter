
CREATE SCHEMA IF NOT EXISTS tweets DEFAULT CHARACTER SET utf8 ;
USE tweets ;

CREATE TABLE IF NOT EXISTS usuarios (
  id_usuarios INT NOT NULL AUTO_INCREMENT,
  id VARCHAR(150) NULL,
  usuario VARCHAR(250) NULL,
  lenguaje_usuario VARCHAR(150) NULL,
  resp_id_usuario VARCHAR(150) NULL,
  resp_pantalla_tweet VARCHAR(350) NULL,
  img_perfil_usuario VARCHAR(350) NULL,
  seguidores_por_usuario FLOAT NULL,
  user_friends_count FLOAT NULL,
  localizacion_publicacion VARCHAR(750) NULL,
  PRIMARY KEY (id_usuarios));

CREATE TABLE IF NOT EXISTS tweets (
  id_tweets INT NOT NULL AUTO_INCREMENT,
  tw_busqueda VARCHAR(150) NULL,
  texto VARCHAR(500) NULL,
  creado_en TIMESTAMP NULL,
  fecha TIMESTAMP NULL,
  coordenadas VARCHAR(250) NULL,
  fuente VARCHAR(350) NULL,
  direccion_url VARCHAR(350) NULL,
  entidades VARCHAR(350) NULL,
  is_rt TINYINT NULL,
  id_usuarios INT NOT NULL,
  PRIMARY KEY (id_tweets),
  FOREIGN KEY (id_usuarios) REFERENCES usuarios (id_usuarios));

CREATE TABLE IF NOT EXISTS datos (
  id_datos INT NOT NULL AUTO_INCREMENT,
  hashtag VARCHAR(150) NULL,
  usuario VARCHAR(150) NULL,
  direccion VARCHAR(350) NULL,
  id_tweets INT NOT NULL,
  PRIMARY KEY (id_datos),
  FOREIGN KEY (id_tweets) REFERENCES tweets (id_tweets));


