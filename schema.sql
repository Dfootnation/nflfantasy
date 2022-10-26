 DROP IF TABLE EXISTS fantasy_score;


CREATE TABLE fantasy_score (
            playerid INTEGER PRIMARY KEY AUTOINCREMENT, 
            Week INTEGER, 
            Name VARCHAR, 
            Team VARCHAR, 
            Against VARCHAR, 
            Position VARCHAR, 
            Passing_yards INTEGER, 
            Passing_tds INTEGER, 
            Passing_int INTEGER, 
            Rushing_yards INTEGER, 
            Rushing_tds INTEGER, 
            Receiving_rec INTEGER, 
            Receiving_yards INTEGER, 
            Receiving_tds INTEGER, 
            Return_td INTEGER, 
            Misc_fumtd INTEGER, 
            Misc_2pt INTEGER, 
            Fum_lost INTEGER, 
            Fantasy_points DOUBLE
            );