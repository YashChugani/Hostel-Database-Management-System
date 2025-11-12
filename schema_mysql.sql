USE hostel_db;

-- Drop existing tables if they exist (safe re-run)
DROP TABLE IF EXISTS MaintenanceRequests, Complaints, Fees, Allocations, Rooms, Staff, Hostels, Students, Visitors;

-- =====================================================
-- 1. STUDENTS
-- =====================================================
CREATE TABLE Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    StudentName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(15) NOT NULL UNIQUE,
    Address VARCHAR(255),
    DOB DATE,
    Gender ENUM('Male','Female','Others') NOT NULL,
    EnrollmentDate DATE DEFAULT (CURRENT_DATE),
    Course VARCHAR(100),
    Year INT CHECK (Year >= 1 AND Year <= 8)
);

-- =====================================================
-- 2. HOSTELS
-- =====================================================
CREATE TABLE Hostels (
    HostelID CHAR(1) PRIMARY KEY,
    HostelName VARCHAR(100) NOT NULL UNIQUE,
    Type ENUM('Boys','Girls','Co-ed') NOT NULL,
    WardenID INT UNIQUE
);

-- =====================================================
-- 3. STAFF
-- =====================================================
CREATE TABLE Staff (
    StaffID INT AUTO_INCREMENT PRIMARY KEY,
    StaffName VARCHAR(100) NOT NULL,
    Role ENUM('Warden','Security','Maintenance') NOT NULL,
    Phone VARCHAR(15) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    HireDate DATE DEFAULT (CURRENT_DATE),
    HostelID CHAR(1),
    FOREIGN KEY (HostelID) REFERENCES Hostels(HostelID)
);

ALTER TABLE Hostels
ADD CONSTRAINT fk_hostel_warden FOREIGN KEY (WardenID) REFERENCES Staff(StaffID);

-- =====================================================
-- 4. ROOMS
-- =====================================================
CREATE TABLE Rooms (
    RoomID INT AUTO_INCREMENT PRIMARY KEY,
    RoomNumber VARCHAR(10) NOT NULL,
    Floor INT,
    Capacity INT NOT NULL DEFAULT 2,
    Occupants INT NOT NULL DEFAULT 0,
    Status ENUM('Vacant','Partially Occupied','Full','Maintenance') DEFAULT 'Vacant',
    HostelID CHAR(1) NOT NULL,
    UNIQUE (HostelID, RoomNumber),
    FOREIGN KEY (HostelID) REFERENCES Hostels(HostelID),
    CHECK (Occupants >= 0 AND Occupants <= Capacity)
);

-- =====================================================
-- 5. ALLOCATIONS
-- =====================================================
CREATE TABLE Allocations (
    AllocationID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    RoomID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE CASCADE
);

-- =====================================================
-- 6. FEES
-- =====================================================
CREATE TABLE Fees (
    FeeID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    DueDate DATE NOT NULL,
    PaymentDate DATE,
    Status ENUM('Paid','Unpaid','Overdue') DEFAULT 'Unpaid',
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

-- =====================================================
-- 7. COMPLAINTS
-- =====================================================
CREATE TABLE Complaints (
    ComplaintID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    FiledDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Description TEXT NOT NULL,
    Status ENUM('Open','In-Progress','Resolved') DEFAULT 'Open',
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

-- =====================================================
-- 8. MAINTENANCE REQUESTS
-- =====================================================
CREATE TABLE MaintenanceRequests (
    RequestID INT AUTO_INCREMENT PRIMARY KEY,
    RoomID INT NOT NULL,
    RequestedBy INT NOT NULL,
    AssignedTo INT,
    RequestDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('Pending','Completed') DEFAULT 'Pending',
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID),
    FOREIGN KEY (RequestedBy) REFERENCES Students(StudentID),
    FOREIGN KEY (AssignedTo) REFERENCES Staff(StaffID)
);

-- =====================================================
-- 9. VISITORS
-- =====================================================
CREATE TABLE Visitors (
    VisitorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15),
    VisitDate DATE DEFAULT (CURRENT_DATE),
    Purpose VARCHAR(255),
    HostStudentID INT,
    FOREIGN KEY (HostStudentID) REFERENCES Students(StudentID)
);
