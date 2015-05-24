CREATE TABLE Utilisateur(
	id 					INT 		PRIMARY	KEY		NOT NULL,
	motDePasse			INT							NOT NULL,
	donneesBancaires	INT							NOT NULL,
	dateFinValidite		DATE						NOT NULL
);

CREATE TABLE Velo(
	id 					INT 		PRIMARY	KEY		NOT NULL,
	dateMiseService		DATE						NOT NULL,
	modele				CHAR(50)					NOT NULL,
	etat				BOOLEAN						NOT NULL
);

CREATE TABLE Station(
	id 					INT 		PRIMARY	KEY		NOT NULL,
	nom					CHAR(50)					NOT NULL,
	bornePayement		BOOLEAN						NOT NULL,
	capacite			INT							NOT NULL,
	xCoords				FLOAT						NOT NULL,
	yCoords				FLOAT						NOT NULL
);

CREATE TABLE Abonne(
	rfid				INT			PRIMARY KEY		NOT NULL,
	nom					CHAR(50)					NOT NULL,
	prenom				CHAR(50)					NOT NULL,
	telephone			CHAR(20)					NOT NULL,
	ville				CHAR(50)					NOT NULL,
	codePostal			INT							NOT NULL,
	rue					CHAR(50)					NOT NULL,
	numero				INT							NOT NULL,
	dateSouscription	DATE						NOT NULL,
	utilisateur			INT							NOT NULL,
	FOREIGN KEY(utilisateur) REFERENCES utilisateur(id)
);

CREATE TABLE Deplacement(
	velo				INT							NOT NULL,
	utilisateur			INT							NOT NULL,
	stationDepart		INT							NOT NULL,
	heureDepart			DATE						NOT NULL,
	stationArrivee		INT									,
	heureArrivee		DATE								,
	FOREIGN KEY(velo) REFERENCES Velo(id)					,
	FOREIGN KEY(utilisateur) REFERENCES Utilisateur(id)		,
	FOREIGN KEY(stationDepart) REFERENCES Station(id)		,
	FOREIGN KEY(stationArrivee) REFERENCES Station(id)		
);