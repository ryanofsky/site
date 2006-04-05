DROP TABLE projects CASCADE;
DROP SEQUENCE project_ids;
DROP TABLE languages CASCADE;
DROP SEQUENCE language_ids;
DROP TABLE project_languages CASCADE;

CREATE TABLE projects
(
  project_id INTEGER NOT NULL PRIMARY KEY DEFAULT NEXTVAL('project_ids'),
  name TEXT NOT NULL,
  repos TEXT,
  startdate DATE,
  enddate DATE,
  description TEXT NOT NULL
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
  lines INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (project_id, language_id)
);

INSERT INTO languages (language_id, name) VALUES (1,'C++');
INSERT INTO languages (language_id, name) VALUES (2,'C#');
INSERT INTO languages (language_id, name) VALUES (3,'C');
INSERT INTO languages (language_id, name) VALUES (4,'Pascal - Delphi, Turbo Pascal');
INSERT INTO languages (language_id, name) VALUES (5,'Python');
INSERT INTO languages (language_id, name) VALUES (6,'Java');
INSERT INTO languages (language_id, name) VALUES (7,'PHP');
INSERT INTO languages (language_id, name) VALUES (8,'Javascript');
INSERT INTO languages (language_id, name) VALUES (9,'CFML - Coldfusion');
INSERT INTO languages (language_id, name) VALUES (10,'Procedural SQL - Postgres plpgsql');
INSERT INTO languages (language_id, name) VALUES (11,'Procedural SQL - Microsoft T-SQL');
INSERT INTO languages (language_id, name) VALUES (12,'Apple II Assembly');
INSERT INTO languages (language_id, name) VALUES (13,'Apple II BASIC');
INSERT INTO languages (language_id, name) VALUES (14,'MEL - Maya Scripting Language');
INSERT INTO languages (language_id, name) VALUES (15,'Microsoft QuickBASIC');

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (1, 'QuickMan', 'quickman', '2001-11-28', '2001-12-03',
'<p>Quickman was an assignment for a robotics class that I worked on with 2 other people. The program drives a Pioneer mobile robot from a starting point to an ending point in a room filled with obstacles, trying to avoid collisions. The obstacle shapes and positions are given as input, and then the program plans an optimal path and follows it. Quickman is written in C++ and makes extensive use of the STL.</p>

<p>Quickman uses a commercial but freely available library called <a href="http://www.ai.sri.com/~konolige/">Saphira</a> that comes with a graphical robot simulator. There are makefiles for GCC under Linux and Solaris and a Metrowerks Codewarrior project file for windows. It uses features of C++ not supported by MS Visual C++ 6.</p>');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (1,1,1545);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (1,3,504);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (2, 'Lost Cities Player', 'lost', '2001-11-12', '2001-11-16',
'<p>Written as a project for an AI class. It plays a card game called "Lost Cities" with 3 other players. I did very little testing on it, so I''m not sure how good it actually is, but I do like the design and strategies used.</p>

<p>The source is very well documented. It was written in Metrowerks Codewarrior for Windows. It also compiles with GCC and runs on Linux and Solaris (makefiles included).</p>');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (2,1,1582);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (3, 'Web Based Course Evaluation System (WCES)', 'wces', '2000-11-12', '2003-06-01',
'<p>WCES is a project of the Columbia University School of Engineering. It''s a web site that lets administrators and professors create customized online surveys about courses and see reports showing survey results. The site originally started as a project for a software engineering class by a group of students I didn''t know. But it was picked up and used by the engineering school, which hired me in Fall 2000 to work on it part-time. Over time, I added many new features and reimplemented most of the preexisting functionality to make the system more flexible. At this point almost all of the code is my own, though I can''t take credit for most of the graphics and text on the site, and I also had a lot of help dealing with unix administration / server maintenance issues that came up during development.</p>

<p>The site is mostly implemented in PHP, but there''s also a big chunk of core logic written in procedural SQL. And there are a number of smaller components written in other languages, including 2 C++ Postgres extensions, a mini web-crawler written in Delphi, and a COM authentication component written in Visual C++ with ATL. </p>

<p>Since this is one of the biggest projects I''ve worked on, I''ve put up a demonstration copy of the site at <a href="http://wces.russ.yanofsky.org/">http://wces.russ.yanofsky.org/</a>.</p>');

-- sloc notes:
--   mapped .js extension to c_count to get javascript count
--   deleted include/VHGRAPH directory before counting
INSERT INTO project_languages (project_id, language_id, lines) VALUES (3,7,19310);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (3,10,3386);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (3,4,775);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (3,1,771);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (3,8,374);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (4, 'My Old Home Page', 'site_old', '2002-02-04', '2003-07-05',
'The original version of this website, a set of ASP.NET pages backed by a small Postgres database. The current version of the site is stored in a new repository and is written in Python.');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (4,2,211);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (5, 'EasyCRT/EasyGDI', 'easycrt', '1997-11-01', '1999-03-15',
'<p>EasyCRT and EasyGDI are libraries that work in Borland''s early releases of Turbo Pascal for Windows (circa 1992). I wrote them when I was a junior in my high school, where Turbo Pascal was the main programming language used in computer classes. EasyGDI is a procedural graphics library that wraps around the Windows GDI (graphics device interface), providing a simplified interface and adding new features like bitmap load and save routines. EasyCRT lets users to write graphical windows programs without dealing with complexities like callback functions, event loops, or class libraries. It is based on Borland''s Wincrt library, and it was used by students in my class and a few classes thereafter to write games. Both libraries come with documentation and sample programs. They have a homepage <a href="/easycrt/">here</a> and some documentation viewable <a href="/viewvc.py/easycrt/html/main.html">here</a>.</p>');

-- sloc notes:
--   deleted samples/stick directory before counting
--   had to modify really_is_pascal function in break_filelist because it
--     doesn't recognize half the pascal files as being pascal
INSERT INTO project_languages (project_id, language_id, lines) VALUES (5,4,3798);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (6, 'Ginyuu Calendar', NULL, '2001-03-25', '2001-04-13',
'This was a fun little project for a software engineering class. I was in a team with four other people and our job was to make a web-based calendar / scheduling component to integrate into a larger online education web site. We were required to implement it using ColdFusion 4 and Microsoft SQL Server. Coldfusion was frustrating to work with because it lacked a lot of basic language features like the ability to define functions. Another annoyance was lack of support for database cursors, meaning the only way to access a database result set was to use a looping construct built into the language, which restricted how you could process data. But our language requirements were really not that great, and in the end our web component had a polished, full-featured interface with a pretty clean implementation. There is no CVS repository but there is a copy of the project page <a href="/cs3156/integration/">here</a>. If free ColdFusion/MS-SQL hosting were to fall out of the sky, I would put up a demo too.');

-- sloc notes:
--   extracted 2001-05-02.zip and copied in schema.sql
--   deleted image/unused directory before counting
--   handled .js files with c_count and .cfm files with generic_count
INSERT INTO project_languages (project_id, language_id, lines) VALUES (6,9,1052);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (6,11,479);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (6,8,130);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (7, 'Twofish Javascript', NULL, '2000-02-25', '2000-03-06',
'In Spring 2000, I ported C implementations of Twofish and SHA-1 over to Javascript as a way of password-protecting the contents of static web pages (this was before I had done any server-side web programming). I never did implement the general password mechanism I was initially planning on, but I did get the encryption code working, and wrote a flexible test interface that can encrypt and decrypt messages, posted <a href="/twofish/twofish.html">here</a>.');

-- sloc notes:
--   handled .js files with c_count
--   copied and pasted contents of 2 <script> tags in twofish.html into a
--     separate .js file so that code would be counted, too
INSERT INTO project_languages (project_id, language_id, lines) VALUES (7,8,1319);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (8, 'ViewVC', NULL, '2001-07-22', NULL,
'<p>ViewVC (formerly ViewCVS) is an open source-project located <a href="http://www.viewvc.org">here</a>.</p>
<p>At the moment, I''m one of two active developers. The other one is <a href="http://www.cmichaelpilato.com/">C. Michael Pilato</a> and ViewVC''s original author is <a href="http://www.lyra.org/greg/">Greg Stein</a>. The features I originally contributed were support for Windows and support for Mod_Python. Since then I''ve done a lot of bug fixing and code reorganization. The 2,500 line count is a WAG (wild ass guess). The ViewVC sources are around 10,000 lines and I figure I''ve had my grubby hands on about a quarter of them.</p>');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (8,5,2500);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (9, 'rcsimport', 'rcsimport', '2006-01-26', '2006-03-05',
'Command line utility to generate rcs files using history from flat files. Pretty well documented and organized. Also has the ability to import whole directory trees and read project metadata from XML.');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (9,5,315);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (10, 'Doctor Database', NULL, '2002-03-29', '2002-04-02',
'Project for a database class to make a simple web application using Postgres and Java Servlets. Worked on with one other person. Demo and source code are available on a tomcat server I''ve got running at <a href="http://doc.russ.yanofsky.org:8080/">http://doc.russ.yanofsky.org:8080/</a>.');

-- sloc notes:
--   rm WEB-INF/classes/Base64.java
--   rm WEB-INF/classes/com/sdi/tools/mls/Main.java
INSERT INTO project_languages (project_id, language_id, lines) VALUES (10,6,2315);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (11, 'Buffer Manager', 'bufferman', '2002-04-09', '2002-04-30',
'Project for a database class to develop a disk caching algorithm and measure how well it worked by simulating database operations like lookups and joins on it with various sizes of data and adding up simulated hard disk access times. Code is some of the cleanest and best documented that I''ve written, but not useful outside of the context of the assignment. Worked on with one other person, though it was mostly a matter of me coding and him working on the paper.');

-- sloc notes:
--   rm -r boost
--   rm -r test/lib
INSERT INTO project_languages (project_id, language_id, lines) VALUES (11,1,989);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (11,5,350);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (12, 'cfree', 'cfree', '2003-12-09', NULL,
'Toy project containing a C++ implementation of some of Freenet''s cryptography and some ideas for a C++ asynchronous i/o framework.');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (12,1,1173);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (13, 'cvsimport', 'cvsimport', '2001-07-29', '2003-06-16',
'Command line utility to generate CVS repositories (complete with log messages, tags, and branches) from directory snapshots.');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (13,7,1658);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (14, 'cvsdate', 'cvsdate', '2001-10-05', '2001-10-06',
'Command line utility to alter commit times in a CVS repository based on last-modified timestamps in a CVS sandbox.');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (14,7,335);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (15, 'C++ Active Library for Device Driver Development', 'device', '2002-11-26', '2003-01-03',
'C++ template metaprogramming library that can take a description of a hardware device''s registers (through C++ typedef declarations) and provide a high-level interface for controlling the device. Supposed to make device driver development easier and less error-prone. Repository includes source code and a 6-page paper describing the project.');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (15,1,542);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (16, 'diffie', 'diffie', '2002-03-17', '2002-07-30',
'Toy project containing a flexible implementation of the DHIES asymmetric encryption algorithm for the Crypto++ library, plus a bunch of unfinished template metaprogramming code that was supposed to become a cool policy-based smart-pointer library.');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (16,1,1096);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (17, 'Iraq Net', 'net', '2005-07-06', '2005-10-03',
'Various scripts and configuration files used to manage a satellite internet gateway on a linux box I set up while deployed in Iraq. There are scripts that control <em>iptables</em> and <em>tc</em> to perform traffic control and nat, block unauthorized computers from accessing the internet, and redirect new computers attempting to access the internet to a web interface where they can register and instantly enable access. The web interface is implemented in Mod_Python and along with registration pages also includes utilities to check the status of the satellite connection and monitor bandwidth usage. Other interesting things in the repository include a small DNS proxy server written in Python and some scripts to deal with configuration files stored in Subversion repositories.');

INSERT INTO project_languages (project_id, language_id, lines) VALUES (17,3,233);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (17,5,2495);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (18, 'Rvalue references for G++', 'rref', '2005-05-26', NULL,
'Implementation of a proposed C++ language feature for G++ 4.x. More information is available at the <a href="/rref/">project homepage</a>. (Line counts produced by counting "+" lines in the GCC patch with sloc''s generic_count).');

-- sloc notes:
-- filterdiff -i '*.c' -i '*.h' < diff.txt | grep '^+[^+]' | generic_count ';' -
-- filterdiff -i '*.C' -x '*/overload.C' < diff.txt | grep '^+[^+]' | generic_count ';' -
-- filterdiff -i '*.py' < diff.txt | grep '^+[^+]' | generic_count ';' -
INSERT INTO project_languages (project_id, language_id, lines) VALUES (18,1,183);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (18,3,367);
INSERT INTO project_languages (project_id, language_id, lines) VALUES (18,5,140);

-------------------------------------------------------------------------------
INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (19, 'My Home Page', 'site', '2005-11-10', NULL,
'This web site, implemented in Python, backed by a Postgres database, and able to run either as a set of CGI scripts or in a Mod_Python environment. Uses the EZT template engine (from ViewVC), and an HTML widget framework I wrote based on the ones from my <em>WCES</em> (PHP) and <em>Doctor Database</em> (Java) web apps.');

-- sloc notes:
-- rm widgets/ezt.py
INSERT INTO project_languages (project_id, language_id, lines) VALUES (19,5,996);

-------------------------------------------------------------------------------
INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (20, 'Stickfighter', 'stick', '1997-12-18', '1998-01-23',
'<p>Fighter game written in Turbo Pascal for Windows as an assignment for a high school "Computer Math" class. This project was sort of a milestone for me, as my first foray into object-oriented and GUI programming. A good portion of the month I spent developing it went into puzzling over concepts like encapsulation and inheritance, and reading and re-reading the Turbo Pascal programmers'' guides to figure out how to make things happen with its windowing library. At the end of that period came a frantic programming effort to get menus and high scores screens working, implement game saving and loading, and tweak the gameplay and graphical intro screen into perfection before the assignment was due. It was pretty fun, and as the project went way beyond anything they were teaching in the class, I got a perfect grade too.</p>'); 

-- sloc notes:
--   checkout version_1_1, not incomplete HEAD
--   rm easygdi.pas
INSERT INTO project_languages (project_id, language_id, lines) VALUES (20,4,1928);

-------------------------------------------------------------------------------

INSERT INTO projects (project_id, name, repos, startdate, enddate, description)
VALUES (21, 'Tiger Compiler', 'tiger', '2003-02-12', '2002-05-07',
'Project for a compilers class to write an interpreter and MIPS compiler for a simple procedural language called "tiger" using Java and the ANTLR parser generator. Worked on with 2 other people and we all contributed about evenly (this was one of the few school projects I worked on with competent teammates). The code isn''t pretty or even fully functional, but it is the kind of hairy, mind-bending type of programming I truly enjoy working on.');

-- sloc notes:
--   just counted the code from HEAD, adding mapping from .g -> java.
--   The count is inflated because it includes code given to us by the
--   professor and also deflated because it doesn't include all the lexing and
--   parsing code we wrote for part 1 of the assignment. But it should be
--   in the right ballpark.
INSERT INTO project_languages (project_id, language_id, lines) VALUES (21,6,2148);

-------------------------------------------------------------------------------

ALTER TABLE project_languages ADD FOREIGN KEY (language_id) REFERENCES languages (language_id);
ALTER TABLE project_languages ADD FOREIGN KEY (project_id) REFERENCES projects (project_id);
