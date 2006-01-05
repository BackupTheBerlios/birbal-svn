BEGIN;
CREATE TABLE "website_advertisements" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(250) NOT NULL,
    "date" timestamp with time zone NOT NULL,
    "expires" date NULL,
    "lead" varchar(250) NOT NULL,
    "photo" varchar(100) NULL,
    "matter" text NULL,
    UNIQUE ("title", "date")
);
CREATE TABLE "website_facilitys" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(250) NOT NULL,
    "type" varchar(2) NOT NULL,
    "layout" varchar(2) NOT NULL,
    "photo" varchar(100) NULL,
    "blurb" varchar(250) NULL,
    "matter" text NULL,
    "priority" integer NOT NULL,
    UNIQUE ("title", "type")
);
INSERT INTO "packages" ("label", "name") VALUES ('website', 'website');
INSERT INTO "content_types" ("name", "package", "python_module_name") VALUES ('advertisement', 'website', 'advertisements');
INSERT INTO "auth_permissions" ("name", "package", "codename") VALUES ('Can add advertisement', 'website', 'add_advertisement');
INSERT INTO "auth_permissions" ("name", "package", "codename") VALUES ('Can change advertisement', 'website', 'change_advertisement');
INSERT INTO "auth_permissions" ("name", "package", "codename") VALUES ('Can delete advertisement', 'website', 'delete_advertisement');
INSERT INTO "content_types" ("name", "package", "python_module_name") VALUES ('facility', 'website', 'facilitys');
INSERT INTO "auth_permissions" ("name", "package", "codename") VALUES ('Can add facility', 'website', 'add_facility');
INSERT INTO "auth_permissions" ("name", "package", "codename") VALUES ('Can change facility', 'website', 'change_facility');
INSERT INTO "auth_permissions" ("name", "package", "codename") VALUES ('Can delete facility', 'website', 'delete_facility');
COMMIT;
