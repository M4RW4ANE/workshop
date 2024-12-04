1.1) On cree la Base de Donnee
CREATE DATABASE Boutique

1.2) On cree les deux tables
On cree la Table Manufacturers
CREATE TABLE Manufacturers (Code INT PRIMARY KEY, Name VARCHAR(100) )

On cree la Table Products
CREATE TABLE Products ( Code INT PRIMARY KEY, Name VARCHAR(100), Price REAL, Manufacturer INT , FOREIGN KEY (Manufacturer) REFERENCES Manufacturers(Code) )

1.3) Insert dans la table Manufacturers  
INSERT INTO Manufacturers (Code, Name) VALUES (1,"Sony"),(2,"Creative Labs"),(3,"Hewlett-Packard"),(4,"Iomega"),(5,"Fujitsu"),(6,"Winchester")

1.4) Insérer dans la table Products
INSERT INTO Products (Code,Name,Price,Manufacturer) VALUES (1,"Hard drive",240,5) ,(2,"Memory",120,6) ,(3,"ZIP drive",150,4) ,(4,"Floppy disk",5,6), (5,"Monitor",240,1) ,(6,"DVD drive",180,2), (7,"CD drive",90,2), (8,"Printer",270,3) ,(9,"Toner cartridge",66,3) ,(10,"DVD burner",180,2)