CREATE TABLE IF NOT EXISTS "User" (
	"tg_id" bigint NOT NULL UNIQUE,
	"user_name" varchar(32) NOT NULL UNIQUE,
	"full_name" varchar(64) NOT NULL,
	PRIMARY KEY ("tg_id")
);

CREATE TABLE IF NOT EXISTS "Munchkin" (
	"id" serial NOT NULL UNIQUE,
	"user_id" bigint NOT NULL,
	"game_id" bigint NOT NULL,
	"gender_id" boolean NOT NULL,
	"number" bigint NOT NULL,
	"level" bigint NOT NULL,
	"strength" bigint NOT NULL,
	"luck" bigint NOT NULL,
	"runaway_bonus" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Game" (
	"id" serial NOT NULL UNIQUE,
	"on_going" boolean NOT NULL,
	"group_id" bigint NOT NULL,
	"current_player_number" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Combat" (
	"id" serial NOT NULL UNIQUE,
	"game_id" bigint NOT NULL,
	"difference" bigint NOT NULL,
	"munchkin_can_join" boolean NOT NULL,
	"monster_can_join" boolean NOT NULL,
	"is_active" boolean NOT NULL,
	"is_runaway" boolean NOT NULL,
	"time_to_think" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "MunchkinCombat" (
	"munchkin_id" bigint NOT NULL,
	"combat_id" bigint NOT NULL,
	"modifier" bigint NOT NULL,
	"runaway_bonus" bigint NOT NULL,
	"is_helping" boolean NOT NULL,
	PRIMARY KEY ("munchkin_id", "combat_id")
);

CREATE TABLE IF NOT EXISTS "Card" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(255) NOT NULL UNIQUE,
	"description" varchar(255) NOT NULL,
	"source_id" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Monster" (
	"card_id" bigint NOT NULL UNIQUE,
	"level" smallint NOT NULL,
	"strength" bigint NOT NULL,
	"treasure_count" smallint NOT NULL,
	"reward_level_count" smallint NOT NULL,
	"undead_type_id" smallint NOT NULL,
	PRIMARY KEY ("card_id")
);

CREATE TABLE IF NOT EXISTS "UndeadType" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(32) NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "MonsterCombat" (
	"monster_id" bigint NOT NULL,
	"combat_id" bigint NOT NULL,
	"modifier" bigint NOT NULL,
	PRIMARY KEY ("monster_id", "combat_id")
);

CREATE TABLE IF NOT EXISTS "PossibleGenders" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(64) NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Stats" (
	"card_id" bigint NOT NULL UNIQUE,
	"stats_type_id" smallint NOT NULL,
	PRIMARY KEY ("card_id")
);

CREATE TABLE IF NOT EXISTS "StatsType" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(20) NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "MunchkinStats" (
	"munchkin_id" bigint NOT NULL,
	"stats_id" bigint NOT NULL,
	PRIMARY KEY ("munchkin_id", "stats_id")
);

CREATE TABLE IF NOT EXISTS "Item" (
	"card_id" bigint NOT NULL UNIQUE,
	"bonus" smallint NOT NULL,
	"one_shot" boolean NOT NULL,
	"is_big" boolean NOT NULL,
	"is_weared" boolean NOT NULL,
	"condition_id" bigint NOT NULL,
	"related_item_id" bigint,
	PRIMARY KEY ("card_id")
);

CREATE TABLE IF NOT EXISTS "MunchkinItem" (
	"munchkin_id" bigint NOT NULL,
	"item_id" bigint NOT NULL,
	PRIMARY KEY ("munchkin_id", "item_id")
);

CREATE TABLE IF NOT EXISTS "MunchkinCards" (
	"munchkin_id" bigint NOT NULL,
	"card_id" bigint NOT NULL,
	"in_game" boolean NOT NULL,
	PRIMARY KEY ("munchkin_id", "card_id")
);

CREATE TABLE IF NOT EXISTS "Group" (
	"tg_id" bigint NOT NULL UNIQUE,
	"name" varchar(255) NOT NULL,
	PRIMARY KEY ("tg_id")
);

CREATE TABLE IF NOT EXISTS "Turn" (
	"id" serial NOT NULL UNIQUE,
	"munchkin_id" bigint NOT NULL,
	"turn_type_id" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "TurnType" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "SourceType" (
	"id" serial NOT NULL UNIQUE,
	"name" bigint NOT NULL,
	"is_open" boolean NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Action" (
	"id" serial NOT NULL UNIQUE,
	"description" varchar(255) NOT NULL,
	"optional" boolean NOT NULL,
	"count" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "AffectedMunchkin" (
	"action_id" bigint NOT NULL,
	"munchkin_id" bigint NOT NULL,
	PRIMARY KEY ("action_id", "munchkin_id")
);

CREATE TABLE IF NOT EXISTS "InitiatedMunchkin" (
	"action_id" bigint NOT NULL,
	"munchkin_id" bigint NOT NULL,
	PRIMARY KEY ("action_id", "munchkin_id")
);

CREATE TABLE IF NOT EXISTS "AffectedMonster" (
	"action_id" bigint NOT NULL,
	"monster_id" bigint NOT NULL,
	PRIMARY KEY ("action_id", "monster_id")
);


ALTER TABLE "Munchkin" ADD CONSTRAINT "Munchkin_fk1" FOREIGN KEY ("user_id") REFERENCES "User"("tg_id");

ALTER TABLE "Munchkin" ADD CONSTRAINT "Munchkin_fk2" FOREIGN KEY ("game_id") REFERENCES "Game"("id");

ALTER TABLE "Munchkin" ADD CONSTRAINT "Munchkin_fk3" FOREIGN KEY ("gender_id") REFERENCES "PossibleGenders"("id");
ALTER TABLE "Game" ADD CONSTRAINT "Game_fk2" FOREIGN KEY ("group_id") REFERENCES "Group"("tg_id");
ALTER TABLE "Combat" ADD CONSTRAINT "Combat_fk1" FOREIGN KEY ("game_id") REFERENCES "Game"("id");
ALTER TABLE "MunchkinCombat" ADD CONSTRAINT "MunchkinCombat_fk0" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "MunchkinCombat" ADD CONSTRAINT "MunchkinCombat_fk1" FOREIGN KEY ("combat_id") REFERENCES "Combat"("id");
ALTER TABLE "Card" ADD CONSTRAINT "Card_fk3" FOREIGN KEY ("source_id") REFERENCES "SourceType"("id");
ALTER TABLE "Monster" ADD CONSTRAINT "Monster_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Monster" ADD CONSTRAINT "Monster_fk5" FOREIGN KEY ("undead_type_id") REFERENCES "UndeadType"("id");

ALTER TABLE "MonsterCombat" ADD CONSTRAINT "MonsterCombat_fk0" FOREIGN KEY ("monster_id") REFERENCES "Monster"("card_id");

ALTER TABLE "MonsterCombat" ADD CONSTRAINT "MonsterCombat_fk1" FOREIGN KEY ("combat_id") REFERENCES "Combat"("id");

ALTER TABLE "Stats" ADD CONSTRAINT "Stats_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Stats" ADD CONSTRAINT "Stats_fk1" FOREIGN KEY ("stats_type_id") REFERENCES "StatsType"("id");

ALTER TABLE "MunchkinStats" ADD CONSTRAINT "MunchkinStats_fk0" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "MunchkinStats" ADD CONSTRAINT "MunchkinStats_fk1" FOREIGN KEY ("stats_id") REFERENCES "Stats"("card_id");
ALTER TABLE "Item" ADD CONSTRAINT "Item_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Item" ADD CONSTRAINT "Item_fk6" FOREIGN KEY ("related_item_id") REFERENCES "Item"("card_id");
ALTER TABLE "MunchkinItem" ADD CONSTRAINT "MunchkinItem_fk0" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "MunchkinItem" ADD CONSTRAINT "MunchkinItem_fk1" FOREIGN KEY ("item_id") REFERENCES "Item"("card_id");
ALTER TABLE "MunchkinCards" ADD CONSTRAINT "MunchkinCards_fk0" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "MunchkinCards" ADD CONSTRAINT "MunchkinCards_fk1" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Turn" ADD CONSTRAINT "Turn_fk1" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "Turn" ADD CONSTRAINT "Turn_fk2" FOREIGN KEY ("turn_type_id") REFERENCES "TurnType"("id");



ALTER TABLE "AffectedMunchkin" ADD CONSTRAINT "AffectedMunchkin_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");

ALTER TABLE "AffectedMunchkin" ADD CONSTRAINT "AffectedMunchkin_fk1" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");
ALTER TABLE "InitiatedMunchkin" ADD CONSTRAINT "InitiatedMunchkin_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");

ALTER TABLE "InitiatedMunchkin" ADD CONSTRAINT "InitiatedMunchkin_fk1" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");
ALTER TABLE "AffectedMonster" ADD CONSTRAINT "AffectedMonster_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");

ALTER TABLE "AffectedMonster" ADD CONSTRAINT "AffectedMonster_fk1" FOREIGN KEY ("monster_id") REFERENCES "Monster"("card_id");