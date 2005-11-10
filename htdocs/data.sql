DROP TABLE projects CASCADE;
DROP SEQUENCE project_ids;
DROP TABLE languages CASCADE;
DROP SEQUENCE language_ids;
DROP TABLE project_languages CASCADE;
DROP AGGREGATE comma(TEXT);
DROP FUNCTION comma_aggregate(TEXT,TEXT);

CREATE TABLE projects
(
  project_id INTEGER NOT NULL PRIMARY KEY DEFAULT NEXTVAL('project_ids'),
  name TEXT,
  lines INTEGER,
  cvsmodule TEXT,
  startdate TIMESTAMP,
  enddate TIMESTAMP,
  description TEXT
);

CREATE SEQUENCE project_ids INCREMENT 1 START 10;

CREATE TABLE languages
(
  language_id INTEGER NOT NULL PRIMARY KEY DEFAULT NEXTVAL('language_ids'),
  name TEXT
);

CREATE SEQUENCE language_ids INCREMENT 1 START 15;

CREATE TABLE project_languages
(
  project_id INTEGER NOT NULL,
  language_id INTEGER NOT NULL,
  PRIMARY KEY (project_id, language_id)
);

INSERT INTO languages (language_id, name) VALUES (1,'C++');
INSERT INTO languages (language_id, name) VALUES (2,'C#');
INSERT INTO languages (language_id, name) VALUES (3,'C');
INSERT INTO languages (language_id, name) VALUES (4,'Pascal (Delphi, Turbo Pascal)');
INSERT INTO languages (language_id, name) VALUES (5,'Python');
INSERT INTO languages (language_id, name) VALUES (6,'Java');
INSERT INTO languages (language_id, name) VALUES (7,'PHP');
INSERT INTO languages (language_id, name) VALUES (8,'Javascript');
INSERT INTO languages (language_id, name) VALUES (9,'CFML (Coldfusion)');
INSERT INTO languages (language_id, name) VALUES (10,'Procedural SQL (Postgres plpgsql)');
INSERT INTO languages (language_id, name) VALUES (11,'Procedural SQL (Microsoft T-SQL)');
INSERT INTO languages (language_id, name) VALUES (12,'Apple II Assembly');
INSERT INTO languages (language_id, name) VALUES (13,'Apple II BASIC');
INSERT INTO languages (language_id, name) VALUES (14,'MEL (Maya Scripting Language)');
INSERT INTO languages (language_id, name) VALUES (15,'Microsoft QuickBASIC');

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, lines, cvsmodule, startdate, enddate, description)
VALUES (1, 'QuickMan', 3000, 'quickman', '2001-11-28', '2001-12-03',
'<p>Quickman was an assignment for a robotics class that I worked on with 2 other people. The program drives a Pioneer mobile robot from a starting point to an ending point in a room filled with obstacles, trying to avoid collisions. The obstacle shapes and positions are given as input, and then the program plans an optimal path and follows it. Quickman is written in C++ and makes extensive use of the STL.</p>

<p>Quickman uses a commercial but freely available library called <a href="http://www.ai.sri.com/~konolige/saphira/">Saphira</a> that comes with a graphical robot simulator. There are makefiles for GCC under linux and solaris and a Metrowerks Codewarrior project file for windows. It uses features of C++ not supported by MS Visual C++ 6.</p>');

INSERT INTO project_languages (project_id, language_id) VALUES (1,1);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, lines, cvsmodule, startdate, enddate, description)
VALUES (2, 'Lost Cities Player', 2000, 'lost', '2001-11-12', '2001-11-16',
'<p>Written as a project for an AI class. It plays a card game called "Lost Cities" with 3 other players. I did very little testing on it, so I''m not sure how good it actually is, but I do like the design and strategies used.

The source is very well documented. It was written in Metrowerks Codewarrior for Windows. It also compiles with GCC and runs on linux and solaris (makefiles included).');

INSERT INTO project_languages (project_id, language_id) VALUES (2,1);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, lines, cvsmodule, startdate, enddate, description)
VALUES (3, 'Web Based Course Evaluation System (WCES)', 25000, 'wbes', '2001-11-12', NULL,
'WCES is a project of the Columbia University School of Engineering. Its lets administrators and professors create customized online surveys about courses and to be able to see and download graphical reports showing survey results. The site originally started as a software engineering project by a group of students. I  started working on it part-time for the university in the Fall 2000. Many new features have been added, and at this point almost all of the code is my own. The 25,000 line count is a bit inflated. About a quarter of that is just plain old HTML inside the PHP scripts. About half of it is solid PHP code (class and function definitions), and the rest consists of database schemas, postgres procedural sql (plpgsql) functions, a mini web-crawler written with Delphi, a COM authentication component written in Visual C++ with ATL, and leftover testing and prototype code.');

INSERT INTO project_languages (project_id, language_id) VALUES (3,1);
INSERT INTO project_languages (project_id, language_id) VALUES (3,7);
INSERT INTO project_languages (project_id, language_id) VALUES (3,10);
INSERT INTO project_languages (project_id, language_id) VALUES (3,4);
INSERT INTO project_languages (project_id, language_id) VALUES (3,8);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, lines, cvsmodule, startdate, enddate, description)
VALUES (4, 'My Home Page', 200, 'site', '2002-02-04', NULL,
'This website, a set of ASP.NET pages backed by a small postgres database running on win2k.');

INSERT INTO project_languages (project_id, language_id) VALUES (4,2);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, lines, cvsmodule, startdate, enddate, description)
VALUES (5, 'EasyCRT/EasyGDI', 4000, NULL, '1997-11-01', '1999-03-15',
'<p>EasyCRT and EasyGDI are libraries that work in Borland''s early releases of Turbo Pascal for windows (circa 1992). I wrote them when I was a junior in high school (1997-1998) and Turbo Pascal was the main programming language used in computer classes there. EasyGDI is a procedural graphics library that wraps around Windows GDI, providing simplified a interface and adding new features like bitmap load and save routines. EasyCRT lets users to write graphical windows programs without dealing with complexities like callback functions, event loops, or class libraries. It is based on Borland''s Wincrt library, and it was used by students in my class and a few classes thereafter to write games. Both libraries come with documentation and sample programs. There is a homepage at <a href="http://russ.hn.org/easycrt/">http://russ.hn.org/easycrt/</a></p>');

INSERT INTO project_languages (project_id, language_id) VALUES (5,4);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, lines, cvsmodule, startdate, enddate, description)
VALUES (6, 'Ginyuu Calendar', 1000, NULL, '2001-03-25', '2001-04-13',
'<a href="http://russ.hn.org/cs3156/">http://russ.hn.org/cs3156/</a></p>');

INSERT INTO project_languages (project_id, language_id) VALUES (6,9);
INSERT INTO project_languages (project_id, language_id) VALUES (6,11);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, lines, cvsmodule, startdate, enddate, description)
VALUES (7, 'Twofish Javascript', 1900, NULL, '2000-09-23', '2000-09-25',
'<a href="http://russ.hn.org/twofish/twofish.html">http://russ.hn.org/twofish/twofish.html</a>');

INSERT INTO project_languages (project_id, language_id) VALUES (7,8);
INSERT INTO project_languages (project_id, language_id) VALUES (7,3);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, lines, cvsmodule, startdate, enddate, description)
VALUES (8, 'ViewCVS', 800, NULL, '2001-07-22', NULL,
'Port of the <a href="http://viewcvs.sourceforge.net/">ViewCVS</a> web interface to windows. My original port is at <a href="http://russ.hn.org/viewcvs/">http://russ.hn.org/viewcvs/</a> which I released as a diff patch, as well as a self-installing standalone package. Since that release I''ve made a lot more changes, including another port to Python ASP (which runs <i>much</i> faster than Python CGI does), and support for ViewCVS''s <a href="http://www.mozilla.org/bonsai.html">Bonsai</a>-like features under windows. I hope to release another package with these features soon.');

INSERT INTO project_languages (project_id, language_id) VALUES (8,5);

-------------------------------------------------------------------------------

ALTER TABLE project_languages ADD FOREIGN KEY (language_id) REFERENCES languages (language_id);
ALTER TABLE project_languages ADD FOREIGN KEY (project_id) REFERENCES projects (project_id);

-- taken from postgres cookbook
-- http://www.brasileiro.net/postgres/cookbook/

CREATE FUNCTION comma_aggregate(text,text) RETURNS TEXT AS '
BEGIN
  IF (length($1) > 0 ) THEN
    RETURN $1 || '', '' || $2;
  ELSE
    RETURN $2;
  END IF;
END;
' LANGUAGE 'plpgsql';

CREATE AGGREGATE comma (basetype=text, sfunc=comma_aggregate, stype=text, initcond='');

