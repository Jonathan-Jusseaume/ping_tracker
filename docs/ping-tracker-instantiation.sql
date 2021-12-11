CREATE TABLE pt_match_status
(
    mas_id   NUMERIC,
    mas_name VARCHAR(10),
    CONSTRAINT pt_match_status_pk PRIMARY KEY (mas_id)
);

INSERT INTO pt_match_status
VALUES (0, 'Victoire'),
       (1, 'Défaite');


CREATE TABLE pt_user
(

);