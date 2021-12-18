CREATE TABLE pt_match_status
(
    mas_id   NUMERIC,
    mas_name VARCHAR(10),
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
    opp_last_name  VARCHAR(50),
    opp_first_name VARCHAR(50),
    CONSTRAINT pt_opponent_pk PRIMARY KEY (opp_id)
);