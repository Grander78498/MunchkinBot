CREATE TABLE IF NOT EXISTS "Card" (
	"id" serial NOT NULL UNIQUE,
	"name" varchar(255) NOT NULL,
	"description" varchar(255) NOT NULL,
	"image_path" varchar(255) NOT NULL,
	"action_group_id" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Item" (
	"card_id" bigint NOT NULL UNIQUE,
	"price" bigint NOT NULL,
	"bonus" bigint NOT NULL,
	"is_big" boolean NOT NULL,
	"is_hireling" boolean NOT NULL,
	"one_shot" boolean NOT NULL,
	"item_type_id" bigint NOT NULL,
	"item_property_id" bigint NOT NULL,
	PRIMARY KEY ("card_id")
);

CREATE TABLE IF NOT EXISTS "Monster" (
	"card_id" bigint NOT NULL UNIQUE,
	"level" bigint NOT NULL,
	"treasure_count" bigint NOT NULL,
	"reward_level_count" bigint NOT NULL,
	"monster_type_id" bigint NOT NULL,
	PRIMARY KEY ("card_id")
);

CREATE TABLE IF NOT EXISTS "MonsterType" (
	"id" serial NOT NULL UNIQUE,
	"name" bigint NOT NULL UNIQUE,
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

CREATE TABLE IF NOT EXISTS "ActionGroup" (
	"id" serial NOT NULL UNIQUE,
	"description" varchar(255) NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "1745172489" (

);

CREATE TABLE IF NOT EXISTS "ActionInGroup" (
	"action_id" bigint NOT NULL,
	"action_group_id" bigint NOT NULL,
	"number" bigint NOT NULL,
	PRIMARY KEY ("action_id", "action_group_id")
);

CREATE TABLE IF NOT EXISTS "Action" (
	"id" serial NOT NULL UNIQUE,
	"description" varchar(255) NOT NULL,
	"optional" boolean NOT NULL,
	"count" bigint NOT NULL,
	"has_death" boolean NOT NULL,
	PRIMARY KEY ("id")
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

ALTER TABLE "Card" ADD CONSTRAINT "Card_fk4" FOREIGN KEY ("action_group_id") REFERENCES "ActionGroup"("id");
ALTER TABLE "Item" ADD CONSTRAINT "Item_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Item" ADD CONSTRAINT "Item_fk6" FOREIGN KEY ("item_type_id") REFERENCES "ItemType"("id");

ALTER TABLE "Item" ADD CONSTRAINT "Item_fk7" FOREIGN KEY ("item_property_id") REFERENCES "ItemProperty"("id");
ALTER TABLE "Monster" ADD CONSTRAINT "Monster_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Monster" ADD CONSTRAINT "Monster_fk4" FOREIGN KEY ("monster_type_id") REFERENCES "MonsterType"("id");

ALTER TABLE "Stats" ADD CONSTRAINT "Stats_fk0" FOREIGN KEY ("card_id") REFERENCES "Card"("id");

ALTER TABLE "Stats" ADD CONSTRAINT "Stats_fk1" FOREIGN KEY ("stats_type_id") REFERENCES "StatsType"("id");



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