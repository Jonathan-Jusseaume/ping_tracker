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
    not_date    DATE         NOT NULL DEFAULT CURRENT_DATE,
    not_usr_id  INTEGER      NOT NULL,
    CONSTRAINT pt_notes_pk PRIMARY KEY (not_id),
    CONSTRAINT pt_notes_user_fk FOREIGN KEY (not_usr_id) REFERENCES auth_user
);

CREATE TABLE pt_match
(
    mat_id            SERIAL,
    mat_usr_id        INTEGER    NOT NULL,
    mat_mas_id        NUMERIC    NOT NULL DEFAULT 0,
    mat_opp_id        VARCHAR(7) NOT NULL,
    mat_rank_opponent NUMERIC    NOT NULL DEFAULT 500,
    mat_date          DATE       NOT NULL DEFAULT CURRENT_DATE,
    mat_comment       VARCHAR(500),
    CONSTRAINT pt_match_pk PRIMARY KEY (mat_id),
    CONSTRAINT pt_match_user_fk FOREIGN KEY (mat_usr_id) REFERENCES auth_user,
    CONSTRAINT pt_match_match_status_fk FOREIGN KEY (mat_mas_id) REFERENCES pt_match_status,
    CONSTRAINT pt_match_opp_id FOREIGN KEY (mat_opp_id) REFERENCES pt_opponent
);

CREATE TABLE pt_set
(
    set_id             SERIAL,
    set_mat_id         INTEGER NOT NULL,
    set_score_user     NUMERIC NOT NULL,
    set_score_opponent NUMERIC NOT NULL,
    set_number         NUMERIC NOT NULL,
    CONSTRAINT pt_set_pk PRIMARY KEY (set_id),
    CONSTRAINT pt_set_match_fk FOREIGN KEY (set_mat_id) REFERENCES pt_match
);

/*
 * Contraintes plus poussées:
 - pt_set_unique_match: Il ne peut pas y avoir deux sets identiques dans un même match
 - pt_set_number_between_1_and_5: Le set a un numéro entre 1 et 5
 - pt_set_is_valid: Le set est valide
 - pt_opponent_id_is_valid: Vérifie que la license fait bien 7 caractères
 */
ALTER TABLE pt_set
    ADD CONSTRAINT pt_set_unique_match UNIQUE (set_mat_id, set_number);

ALTER TABLE pt_set
    ADD CONSTRAINT pt_set_number_between_1_and_5 CHECK ( set_number >= 1 AND set_number <= 5 );

ALTER TABLE pt_set
    ADD CONSTRAINT pt_set_is_valid CHECK (
                    set_score_user >= 0
                AND set_score_opponent >= 0
                AND (set_score_user >= 11 OR set_score_opponent >= 11)
                AND (set_score_user >= 10 AND
                     set_score_opponent >= 10
                AND ABS(set_score_user - set_score_opponent) = 2
                        ) OR (
                            (set_score_user = 11 AND set_score_opponent < 10)
                            OR (set_score_user < 10 AND set_score_opponent = 11)
                        )
        );


ALTER TABLE pt_opponent
    ADD CONSTRAINT pt_opponent_id_is_valid CHECK ( LENGTH(opp_id) = 7 );

ALTER TABLE pt_match
    ADD CONSTRAINT pt_match_is_in_past CHECK ( mat_date <= CURRENT_DATE );