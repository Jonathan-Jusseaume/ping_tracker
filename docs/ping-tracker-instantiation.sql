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
 - pt_match_is_valid: Vérifie que le match est valide
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


CREATE TABLE pt_user_stats
(
    uss_id                SERIAL  NOT NULL,
    uss_usr_id            INTEGER NOT NULL UNIQUE,
    uss_number_victory    INTEGER NOT NULL DEFAULT 0 CHECK ( uss_number_victory >= 0 ),
    uss_number_defeat     INTEGER NOT NULL DEFAULT 0 CHECK ( uss_number_defeat >= 0 ),
    uss_fifth_set_victory INTEGER NOT NULL DEFAULT 0 CHECK ( uss_fifth_set_victory >= 0 ),
    uss_fifth_set_defeat  INTEGER NOT NULL DEFAULT 0 CHECK ( uss_fifth_set_defeat >= 0 ),
    uss_decisive_victory  INTEGER NOT NULL DEFAULT 0 CHECK ( uss_decisive_victory >= 0 ),
    uss_decisive_defeat   INTEGER NOT NULL DEFAULT 0 CHECK ( uss_decisive_defeat >= 0 ),
    CONSTRAINT pk_uss_id PRIMARY KEY (uss_id),
    CONSTRAINT fk_uss_usr_id FOREIGN KEY (uss_usr_id) REFERENCES auth_user
);


CREATE FUNCTION stats_update()
    RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$$

DECLARE
    cur_stats CURSOR (id_usr INTEGER)
        FOR SELECT COUNT(*) AS count
            FROM pt_user_stats
            WHERE uss_usr_id = id_usr;
    rec_stats record;
BEGIN
    OPEN cur_stats(new.mat_usr_id);
    LOOP
        FETCH cur_stats INTO rec_stats;
        EXIT WHEN NOT found;
        IF rec_stats.count = 0 THEN
            INSERT INTO pt_user_stats(uss_usr_id) VALUES (new.mat_usr_id);
        END IF;
    END LOOP;
    IF new.mat_mas_id = 0 THEN
        IF old.mat_mas_id = 1 THEN
            UPDATE pt_user_stats
            SET uss_number_victory = uss_number_victory + 1,
                uss_number_defeat  = uss_number_defeat - 1
            WHERE uss_usr_id = new.mat_usr_id;
        ELSE
            UPDATE pt_user_stats
            SET uss_number_victory = uss_number_victory + 1
            WHERE uss_usr_id = new.mat_usr_id;
        END IF;


    END IF;
    IF new.mat_mas_id = 1 THEN
        IF old.mat_mas_id = 0 THEN
            UPDATE pt_user_stats
            SET uss_number_victory = uss_number_victory - 1,
                uss_number_defeat  = uss_number_defeat + 1
            WHERE uss_usr_id = new.mat_usr_id;
        ELSE
            UPDATE pt_user_stats
            SET uss_number_defeat = uss_number_defeat + 1
            WHERE uss_usr_id = new.mat_usr_id;
        END IF;

    END IF;

    CLOSE cur_stats;
    RETURN new;
END;
$$;


CREATE TRIGGER trigger_match
    AFTER INSERT OR UPDATE
    ON pt_match
    FOR EACH ROW
EXECUTE PROCEDURE stats_update();


CREATE FUNCTION stats_sets_update() RETURNS trigger
    LANGUAGE plpgsql
AS
$$
DECLARE
    cur_stats CURSOR (id_usr INTEGER)
        FOR SELECT COUNT(*) AS count
            FROM pt_user_stats
            WHERE uss_usr_id = id_usr;
    rec_stats record;
BEGIN
    /*
     On ajoute une ligne de statistiques si l'utilisateur n'en a pas
     */
    OPEN cur_stats((SELECT mat_usr_id FROM pt_match WHERE mat_id = new.set_mat_id));
    LOOP
        FETCH cur_stats INTO rec_stats;
        EXIT WHEN NOT found;
        IF rec_stats.count = 0 THEN
            INSERT INTO pt_user_stats(uss_usr_id)
            VALUES ((SELECT mat_usr_id FROM pt_match WHERE mat_id = new.set_mat_id));
        END IF;
    END LOOP;
    /*
     Cas où c'est un cinquième set et qu'on gagne
     */
    IF new.set_number = 5 AND new.set_score_user > new.set_score_opponent THEN
        /*
         Si pour le même set c'était l'opposant qui gagnait alors il faut nous enlever une défaite
         */
        IF old.set_score_user < old.set_score_opponent THEN
            UPDATE pt_user_stats
            SET uss_fifth_set_victory = uss_fifth_set_victory + 1,
                uss_fifth_set_defeat  = uss_fifth_set_defeat - 1
            WHERE uss_usr_id = (SELECT mat_usr_id FROM pt_match WHERE mat_id = new.set_mat_id);
            /*
             Sinon on rajoute juste une victoire
             */
        ELSE
            UPDATE pt_user_stats
            SET uss_fifth_set_victory = uss_fifth_set_victory + 1
            WHERE uss_usr_id = (SELECT mat_usr_id FROM pt_match WHERE mat_id = new.set_mat_id);
        END IF;
    END IF;
    /*
     Cas inverse où on est dans le cinquième set mais on perd
     */
    IF new.set_number = 5 AND new.set_score_user < new.set_score_opponent THEN
        /*
         Si pour le même set c'était nous qui gagnions alors il faut nous enlever une victoire
         */
        IF old.set_score_user > old.set_score_opponent THEN
            UPDATE pt_user_stats
            SET uss_fifth_set_victory = uss_fifth_set_victory - 1,
                uss_fifth_set_defeat  = uss_fifth_set_defeat + 1
            WHERE uss_usr_id = (SELECT mat_usr_id FROM pt_match WHERE mat_id = new.set_mat_id);
            /*
             Sinon on rajoute juste une victoire
             */
        ELSE
            UPDATE pt_user_stats
            SET uss_fifth_set_defeat = uss_fifth_set_defeat + 1
            WHERE uss_usr_id = (SELECT mat_usr_id FROM pt_match WHERE mat_id = new.set_mat_id);
        END IF;
    END IF;
    /*
     Cas où on a des points d'écarts
     */
    IF ABS(new.set_score_user - new.set_score_opponent) = 2 THEN
        /*
         Si c'est l'opposant qui gagne
         */
        IF new.set_score_user < new.set_score_opponent THEN
            UPDATE pt_user_stats
            SET uss_decisive_defeat = uss_decisive_defeat + 1
            WHERE uss_usr_id = (SELECT mat_usr_id FROM pt_match WHERE mat_id = new.set_mat_id);
            /*
             Sinon c'est nous qui gagnons
             */
        ELSE
            UPDATE pt_user_stats
            SET uss_decisive_victory = uss_decisive_victory + 1
            WHERE uss_usr_id = (SELECT mat_usr_id FROM pt_match WHERE mat_id = new.set_mat_id);
        END IF;
    END IF;

    CLOSE cur_stats;
    RETURN new;
END;
$$;


CREATE TRIGGER trigger_set
    AFTER INSERT OR UPDATE
    ON pt_set
    FOR EACH ROW
EXECUTE PROCEDURE stats_sets_update();