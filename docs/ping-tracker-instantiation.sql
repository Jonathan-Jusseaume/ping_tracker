CREATE TABLE pt_match_status
(
    mas_id   NUMERIC,
    mas_name VARCHAR(10) NOT NULL,
    CONSTRAINT pt_match_status_pk PRIMARY KEY (mas_id)
);

INSERT INTO pt_match_status
VALUES (0, 'Victoire'),
       (1, 'Défaite');

CREATE FUNCTION do_not_change()
    RETURNS TRIGGER
AS
$$
BEGIN
    RAISE EXCEPTION 'Cannot modify table pt_match_status.
Contact the system administrator if you want to make this change.';
END;
$$
    LANGUAGE plpgsql;

CREATE TRIGGER no_change_trigger
    BEFORE INSERT OR UPDATE OR DELETE
    ON pt_match_status
EXECUTE PROCEDURE do_not_change();

CREATE TABLE pt_opponent
(
    opp_id         VARCHAR(7),
    opp_last_name  VARCHAR(50) NOT NULL,
    opp_first_name VARCHAR(50) NOT NULL,
    CONSTRAINT pt_opponent_pk PRIMARY KEY (opp_id)
);

CREATE TABLE pt_note
(
    not_id      SERIAL,
    not_content VARCHAR(500) NOT NULL,
    not_usr_id  INTEGER      NOT NULL,
    CONSTRAINT pt_notes_pk PRIMARY KEY (not_id),
    CONSTRAINT pt_notes_user_fk FOREIGN KEY (not_usr_id) REFERENCES auth_user
);