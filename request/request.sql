
-- R1
SELECT * FROM Abonne WHERE ville='Ixelles' AND utilisateur IN (SELECT utilisateur FROM Deplacement WHERE stationDepart IN (SELECT id FROM Station WHERE nom='FLAGEY'));

-- R2
SELECT * FROM Utilisateur WHERE id IN (SELECT utilisateur FROM Deplacement GROUP BY utilisateur HAVING COUNT(*)>=2);

-- R3
SELECT D1.utilisateur U1,D2.utilisateur U2 FROM Deplacement D1 JOIN Deplacement D2 ON D1.stationDepart=D2.stationDepart AND D1.stationArrivee=D2.stationArrivee WHERE D1.stationDepart<>'None' AND D2.stationArrivee<>'None' AND D1.utilisateur<>D2.utilisateur;

-- R4
SELECT * FROM Deplacement D1 JOIN Deplacement D2 ON D1.velo=D2.velo WHERE D1.stationArrivee<>D2.stationDepart AND D1.stationArrivee<>'None' AND D2.stationDepart<>'None' AND D2.heureDepart>D1.heureArrivee;

-- R5


-- R6
SELECT stationArrivee,COUNT(*),COUNT(DISTINCT utilisateur) nbVelo FROM Deplacement GROUP BY stationArrivee HAVING stationArrivee<>'None' AND nBVelo>=10;