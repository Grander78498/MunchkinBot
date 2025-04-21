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
	"name" varchar(255) NOT NULL,
	"description" varchar(255) NOT NULL,
	"image_path" varchar(255) NOT NULL,
	"action_group_id" bigint NOT NULL,
	"type_id" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Monster" (
	"card_id" bigint NOT NULL UNIQUE,
	"level" bigint NOT NULL,
	"treasure_count" bigint NOT NULL,
	"reward_level_count" bigint NOT NULL,
	"monster_type_id" bigint NOT NULL,
	PRIMARY KEY ("card_id")
);

CREATE TABLE IF NOT EXISTS "MonsterCombat" (
	"monster_id" bigint NOT NULL,
	"combat_id" bigint NOT NULL,
	"modifier" bigint NOT NULL,
	"treasure_count" bigint NOT NULL,
	"reward_level_count" bigint NOT NULL,
	PRIMARY KEY ("monster_id", "combat_id")
);

CREATE TABLE IF NOT EXISTS "PossibleGenders" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(64) NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Stats" (
	"card_id" bigint NOT NULL UNIQUE,
	"stats_type_id" bigint NOT NULL,
	PRIMARY KEY ("card_id")
);

CREATE TABLE IF NOT EXISTS "StatsType" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(255) NOT NULL UNIQUE,
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
	"price" bigint NOT NULL,
	"is_hireling" boolean NOT NULL,
	"item_type_id" bigint NOT NULL,
	"item_property_id" bigint NOT NULL,
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
	"has_death" boolean NOT NULL,
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

CREATE TABLE IF NOT EXISTS "MonsterType" (
	"id" serial NOT NULL UNIQUE,
	"name" bigint NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "ActionGroup" (
	"id" serial NOT NULL UNIQUE,
	"description" varchar(255) NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "ActionInGroup" (
	"action_id" bigint NOT NULL,
	"action_group_id" bigint NOT NULL,
	"number" bigint NOT NULL,
	PRIMARY KEY ("action_id", "action_group_id")
);

CREATE TABLE IF NOT EXISTS "Condition" (
	"id" serial NOT NULL UNIQUE,
	"value_id" bigint NOT NULL,
	"equal_id" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "EqualType" (
	"id" serial NOT NULL UNIQUE,
	"sign" varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "PossibleConditionType" (
	"id" serial NOT NULL UNIQUE,
	"name" bigint NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "PossibleConditionField" (
	"id" serial NOT NULL UNIQUE,
	"type_id" bigint NOT NULL,
	"name" varchar(255) NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "PossibleConditionValue" (
	"id" serial NOT NULL UNIQUE,
	"field_id" bigint NOT NULL,
	"name" varchar(255) NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "ActionCondition" (
	"action_id" bigint NOT NULL,
	"condition_id" bigint NOT NULL,
	PRIMARY KEY ("action_id", "condition_id")
);

CREATE TABLE IF NOT EXISTS "ItemCondition" (
	"item_id" bigint NOT NULL,
	"condition_id" bigint NOT NULL,
	PRIMARY KEY ("item_id", "condition_id")
);

CREATE TABLE IF NOT EXISTS "CreatureUpdate" (
	"action_id" bigint NOT NULL UNIQUE,
	"amount" bigint NOT NULL,
	"to_remove" boolean NOT NULL,
	PRIMARY KEY ("action_id")
);

CREATE TABLE IF NOT EXISTS "StatsChange" (
	"action_id" bigint NOT NULL UNIQUE,
	"amount" bigint NOT NULL,
	"positive" boolean NOT NULL,
	PRIMARY KEY ("action_id")
);

CREATE TABLE IF NOT EXISTS "ItemType" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "ItemProperty" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "CardsTransfer" (
	"action_id" bigint NOT NULL UNIQUE,
	"cards_count" bigint,
	"is_open" boolean,
	"giveaway" boolean NOT NULL,
	PRIMARY KEY ("action_id")
);

CREATE TABLE IF NOT EXISTS "CardsTransferCondition" (
	"cards_transdfer_id" bigint NOT NULL,
	"condition_id" bigint NOT NULL,
	PRIMARY KEY ("cards_transdfer_id", "condition_id")
);

CREATE TABLE IF NOT EXISTS "CardType" (
	"id" serial NOT NULL UNIQUE,
	"name" bigint NOT NULL UNIQUE,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "GameCard" (
	"id" serial NOT NULL UNIQUE,
	"card_id" bigint NOT NULL,
	"source_id" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "GameItem" (
	"card_id" bigint NOT NULL UNIQUE,
	"original_item_id" bigint NOT NULL,
	"bonus" smallint NOT NULL,
	"one_shot" boolean NOT NULL,
	"is_big" boolean NOT NULL,
	"price" bigint NOT NULL,
	PRIMARY KEY ("card_id")
);


ALTER TABLE "Munchkin" ADD CONSTRAINT "Munchkin_fk1" FOREIGN KEY ("user_id") REFERENCES "User"("tg_id");

ALTER TABLE "Munchkin" ADD CONSTRAINT "Munchkin_fk2" FOREIGN KEY ("game_id") REFERENCES "Game"("id");

ALTER TABLE "Munchkin" ADD CONSTRAINT "Munchkin_fk3" FOREIGN KEY ("gender_id") REFERENCES "PossibleGenders"("id");
ALTER TABLE "Game" ADD CONSTRAINT "Game_fk2" FOREIGN KEY ("group_id") REFERENCES "Group"("tg_id");
ALTER TABLE "Combat" ADD CONSTRAINT "Combat_fk1" FOREIGN KEY ("game_id") REFERENCES "Game"("id");
ALTER TABLE "MunchkinCombat" ADD CONSTRAINT "MunchkinCombat_fk0" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "MunchkinCombat" ADD CONSTRAINT "MunchkinCombat_fk1" FOREIGN KEY ("combat_id") REFERENCES "Combat"("id");
ALTER TABLE "Card" ADD CONSTRAINT "Card_fk4" FOREIGN KEY ("action_group_id") REFERENCES "ActionGroup"("id");

ALTER TABLE "Card" ADD CONSTRAINT "Card_fk5" FOREIGN KEY ("type_id") REFERENCES "CardType"("id");
ALTER TABLE "Monster" ADD CONSTRAINT "Monster_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Monster" ADD CONSTRAINT "Monster_fk4" FOREIGN KEY ("monster_type_id") REFERENCES "MonsterType"("id");
ALTER TABLE "MonsterCombat" ADD CONSTRAINT "MonsterCombat_fk0" FOREIGN KEY ("monster_id") REFERENCES "Monster"("card_id");

ALTER TABLE "MonsterCombat" ADD CONSTRAINT "MonsterCombat_fk1" FOREIGN KEY ("combat_id") REFERENCES "Combat"("id");

ALTER TABLE "Stats" ADD CONSTRAINT "Stats_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Stats" ADD CONSTRAINT "Stats_fk1" FOREIGN KEY ("stats_type_id") REFERENCES "StatsType"("id");

ALTER TABLE "MunchkinStats" ADD CONSTRAINT "MunchkinStats_fk0" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "MunchkinStats" ADD CONSTRAINT "MunchkinStats_fk1" FOREIGN KEY ("stats_id") REFERENCES "Stats"("card_id");
ALTER TABLE "Item" ADD CONSTRAINT "Item_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Item" ADD CONSTRAINT "Item_fk6" FOREIGN KEY ("item_type_id") REFERENCES "ItemType"("id");

ALTER TABLE "Item" ADD CONSTRAINT "Item_fk7" FOREIGN KEY ("item_property_id") REFERENCES "ItemProperty"("id");
ALTER TABLE "MunchkinItem" ADD CONSTRAINT "MunchkinItem_fk0" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "MunchkinItem" ADD CONSTRAINT "MunchkinItem_fk1" FOREIGN KEY ("item_id") REFERENCES "GameItem"("card_id");
ALTER TABLE "MunchkinCards" ADD CONSTRAINT "MunchkinCards_fk0" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "MunchkinCards" ADD CONSTRAINT "MunchkinCards_fk1" FOREIGN KEY ("card_id") REFERENCES "GameCard"("card_id");

ALTER TABLE "Turn" ADD CONSTRAINT "Turn_fk1" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");

ALTER TABLE "Turn" ADD CONSTRAINT "Turn_fk2" FOREIGN KEY ("turn_type_id") REFERENCES "TurnType"("id");



ALTER TABLE "AffectedMunchkin" ADD CONSTRAINT "AffectedMunchkin_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");

ALTER TABLE "AffectedMunchkin" ADD CONSTRAINT "AffectedMunchkin_fk1" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");
ALTER TABLE "InitiatedMunchkin" ADD CONSTRAINT "InitiatedMunchkin_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");

ALTER TABLE "InitiatedMunchkin" ADD CONSTRAINT "InitiatedMunchkin_fk1" FOREIGN KEY ("munchkin_id") REFERENCES "Munchkin"("id");
ALTER TABLE "AffectedMonster" ADD CONSTRAINT "AffectedMonster_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");

ALTER TABLE "AffectedMonster" ADD CONSTRAINT "AffectedMonster_fk1" FOREIGN KEY ("monster_id") REFERENCES "Monster"("card_id");


ALTER TABLE "ActionInGroup" ADD CONSTRAINT "ActionInGroup_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");

ALTER TABLE "ActionInGroup" ADD CONSTRAINT "ActionInGroup_fk1" FOREIGN KEY ("action_group_id") REFERENCES "ActionGroup"("id");
ALTER TABLE "Condition" ADD CONSTRAINT "Condition_fk1" FOREIGN KEY ("value_id") REFERENCES "PossibleConditionValue"("id");

ALTER TABLE "Condition" ADD CONSTRAINT "Condition_fk2" FOREIGN KEY ("equal_id") REFERENCES "EqualType"("id");


ALTER TABLE "PossibleConditionField" ADD CONSTRAINT "PossibleConditionField_fk1" FOREIGN KEY ("type_id") REFERENCES "PossibleConditionType"("id");
ALTER TABLE "PossibleConditionValue" ADD CONSTRAINT "PossibleConditionValue_fk1" FOREIGN KEY ("field_id") REFERENCES "PossibleConditionField"("id");
ALTER TABLE "ActionCondition" ADD CONSTRAINT "ActionCondition_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");

ALTER TABLE "ActionCondition" ADD CONSTRAINT "ActionCondition_fk1" FOREIGN KEY ("condition_id") REFERENCES "Condition"("id");
ALTER TABLE "ItemCondition" ADD CONSTRAINT "ItemCondition_fk0" FOREIGN KEY ("item_id") REFERENCES "Item"("card_id");

ALTER TABLE "ItemCondition" ADD CONSTRAINT "ItemCondition_fk1" FOREIGN KEY ("condition_id") REFERENCES "Condition"("id");
ALTER TABLE "CreatureUpdate" ADD CONSTRAINT "CreatureUpdate_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");
ALTER TABLE "StatsChange" ADD CONSTRAINT "StatsChange_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");


ALTER TABLE "CardsTransfer" ADD CONSTRAINT "CardsTransfer_fk0" FOREIGN KEY ("action_id") REFERENCES "Action"("id");
ALTER TABLE "CardsTransferCondition" ADD CONSTRAINT "CardsTransferCondition_fk0" FOREIGN KEY ("cards_transdfer_id") REFERENCES "CardsTransfer"("action_id");

ALTER TABLE "CardsTransferCondition" ADD CONSTRAINT "CardsTransferCondition_fk1" FOREIGN KEY ("condition_id") REFERENCES "Condition"("id");

ALTER TABLE "GameCard" ADD CONSTRAINT "GameCard_fk1" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "GameCard" ADD CONSTRAINT "GameCard_fk2" FOREIGN KEY ("source_id") REFERENCES "SourceType"("id");
ALTER TABLE "GameItem" ADD CONSTRAINT "GameItem_fk0" FOREIGN KEY ("card_id") REFERENCES "GameCard"("id");

ALTER TABLE "GameItem" ADD CONSTRAINT "GameItem_fk1" FOREIGN KEY ("original_item_id") REFERENCES "Item"("card_id");