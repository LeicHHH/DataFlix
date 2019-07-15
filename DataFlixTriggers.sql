--Validar que los contenidos tengan una categoría asociada

CREATE OR REPLACE FUNCTION check_category() RETURNS TRIGGER
SET SCHEMA 'public' LANGUAGE plpgsql AS $$
    BEGIN
    IF NEW.id_categoria > 20 OR NEW.id_categoria < 1 THEN
        RAISE EXCEPTION 'Esta categoría no existe';
    END IF;
    RETURN NEW;
    END;
    $$;

CREATE TRIGGER check_category 
    BEFORE INSERT OR UPDATE ON clasificacion
    FOR EACH ROW EXECUTE PROCEDURE check_category();

--Validar que serie tenga temporada y capítulo

CREATE OR REPLACE FUNCTION check_cap() RETURNS TRIGGER
SET SCHEMA 'public' LANGUAGE plpgsql AS $$
    BEGIN
    CASE NEW.id_area = 1 WHEN NEW.numero_capítulo < 1 OR NEW.temporada < 1 THEN
        RAISE EXCEPTION 'Debes agregar número de temporada y capítulo';
    ELSE END CASE;
    RETURN NEW;
    END;
    $$;

CREATE TRIGGER check_cap
    BEFORE INSERT OR UPDATE ON contenido
    FOR EACH ROW EXECUTE PROCEDURE check_cap();

--Validar que no se use la misma contraseña

CREATE OR REPLACE FUNCTION check_contrasena() RETURNS TRIGGER
SET SCHEMA 'public' LANGUAGE plpgsql AS $$
    BEGIN
    IF NEW.contrasena = contrasena THEN
        RAISE EXCEPTION 'No puedes utilizar la misma contraseña';
    ELSE END IF;
    RETURN NEW;
    END;
    $$;

CREATE TRIGGER check_contrasena
    BEFORE INSERT OR UPDATE ON perfil
    FOR EACH ROW EXECUTE PROCEDURE check_contrasena();