- Question Number: 1
- Question Text: As shown in Figure 1, there is a box that generates a single output for two (2) inputs. The input in this box is either “Agree” or “Disagree,” and the output of “Agree” is generated only when both inputs are “Agree,” while in other cases the output of “Disagree” is generated. When three (3) inputs are entered into two (2) boxes as shown in Figure 2, which of the following is the correct description concerning the output?
  ![Q1 Figure 1 and 2](images/2025S_IP/page-03.png)
- Options: a) The output of “Agree” is generated at all times when one (1) or more inputs are “Agree.”, b) The output of “Agree” is generated at all times when two (2) or more inputs are “Agree.”, c) The output of “Disagree” is generated only when two (2) or more inputs are “Disagree.”, d) The output of “Agree” is generated only when all three (3) inputs are “Agree.”
- Correct Answer: d
- Category Tag: #BasicTheory

- Question Number: 2
- Question Text: Which of the following is the binary result of the multiplication of binary $1011_2$ and binary $101_2$?
- Options: a) $1111_2$, b) $10000_2$, c) $101111_2$, d) $110111_2$
- Correct Answer: d
- Category Tag: #BasicTheory

- Question Number: 3
- Question Text: The automation of the inspections performed by a quality controller is considered. By providing as training data 10,000 product images and the results of judgments by the quality controller about whether each product is defective or not, a machine learning model is created to judge whether a product is defective or not. The results of a test judgement by a machine learning model on 100 product images are as shown in the table. 

| Judgment by the quality controller | Defective (Model) | Not defective (Model) |
| :--- | :---: | :---: |
| **Defective** | 5 | 5 |
| **Not defective** | 15 | 75 |

When the ratio of the number of images that product is judged to be defective by the machine learning model out of the images that product is judged to be defective by the quality controller is deemed to be the recall rate, what is the recall rate in this test judgement?
- Options: a) 0.05, b) 0.25, c) 0.50, d) 0.80
- Correct Answer: c
- Category Tag: #BasicTheory

- Question Number: 4
- Question Text: When a six (6)-sided dice with the numbers 1 to 6 is thrown three (3) times, what is the probability of not getting any 1?
- Options: a) $\frac{1}{216}$, b) $\frac{5}{72}$, c) $\frac{91}{216}$, d) $\frac{125}{216}$
- Correct Answer: d
- Category Tag: #BasicTheory

- Question Number: 5
- Question Text: Which of the following is a term for a list of instructions to a computer that are written in a human-readable programming language?
- Options: a) PIN code, b) Source code, c) Binary code, d) Character code
- Correct Answer: b
- Category Tag: #BasicTheory

- Question Number: 6
- Question Text: The procedure `calculateElectricBill` receives electricity usage that accepts the units (non-negative value) and returns the amount of electricity bills. The pricing structure is given as: For the first 100 units, the cost is $10 per unit. Any units exceeding 100 are charged at $15 per unit. Which of the following is an appropriate piece of code to be inserted into `_______` in the program?

[Program]
```
○ integer: calculateElectricBill(integer: units)
  integer: payAmount ← 0
  if (units ≤ 100)
    payAmount ← units × 10
  else
    payAmount ← _______
  endif
  return payAmount
```
- Options: a) $(units - 100) \times 10 + 100 \times 15$, b) $(units - 100) \times 15 + 100 \times 10$, c) $units \times 15$, d) $units \times 15 + 100 \times 10$
- Correct Answer: b
- Category Tag: #BasicTheory

- Question Number: 7
- Question Text: A program uses loops to display results based on whether the cycle numbers are odd or even. The execution result of the program is shown below.
```
0+0+0+0
+++++++
2+2+2+2
+++++++
4+4+4+4
+++++++
6+6+6+6
```
Which of the following is an appropriate combination of pieces of code to be inserted into `___A___` through `___C___` in the program?

[Program]
```
integer: i, j
for (increase i from 0 to 6 by 1)
  for (increase j from 0 to 6 by 1)
    if (___A___)
      output ___B___
    else
      output ___C___
    endif
  endfor
  output a new line
endfor
```

| | A | B | C |
| :--- | :--- | :--- | :--- |
| a) | (i mod 2 ≠ 0) and (j mod 2 ≠ 0) | "+" | i |
| b) | (i mod 2 ≠ 0) and (j mod 2 ≠ 0) | i | "+" |
| c) | (i mod 2 = 0) and (j mod 2 = 0) | "+" | i |
| d) | (i mod 2 = 0) and (j mod 2 = 0) | i | "+" |
- Correct Answer: d
- Category Tag: #BasicTheory

- Question Number: 8
- Question Text: In the data structure called a queue that is suitable for performing first-in first-out (FIFO) processing, values are stored in the order of “8”, “1”, “6”, and “3”, and then two (2) values are removed consecutively. Which of the following is the last value that is removed?
- Options: a) 1, b) 3, c) 6, d) 8
- Correct Answer: a
- Category Tag: #BasicTheory

- Question Number: 9
- Question Text: As shown in Figure 1, there is a box that generates two (2) numerical values B1 and B2 when two (2) positive integers A1 and A2 are entered. B1 has the same value as A2, and B2 is the remainder of A1 divided by A2. In Figure 2, when two (2) boxes are connected, and 49 is entered as A1 and 11 is entered as A2 in the left box, what is the value of B2 generated from the right box?
  ![Q9 Figure 1 and 2](images/2025S_IP/page-07.png)
- Options: a) 1, b) 2, c) 4, d) 5
- Correct Answer: a
- Category Tag: #BasicTheory

- Question Number: 10
- Question Text: Which of the following is an appropriate combination of words that are inserted into A and B in the description below concerning the execution sequence of instructions in a computer?
  ![Q10 Instruction sequence](images/2025S_IP/page-07.png)
- Options: a) Decode, Read, b) Read, Decode, c) Read, Write, d) Write, Decode
- Correct Answer: b
- Category Tag: #ComputerSystems

- Question Number: 11
- Question Text: Which of the following is an appropriate description concerning the primary and secondary cache memory that a CPU is equipped with?
- Options: a) The primary cache memory has larger capacity than the secondary cache memory., b) The secondary cache memory is slower than the main memory in writing and reading., c) When the CPU reads data, it first accesses the primary cache memory, and then it accesses the secondary cache memory if the data is not available., d) All of the data that is required for a process needs to be present on the primary or secondary cache memory when a program starts.
- Correct Answer: c
- Category Tag: #ComputerSystems

- Question Number: 12
- Question Text: Which of the following is a type of device that is also used as a memory device in IoT devices, and has a lower power consumption and higher impact resistance than an HDD as it has memory media that is made of semiconductors and does not have any moving components?
- Options: a) DRM, b) DVD, c) HDMI, d) SSD
- Correct Answer: d
- Category Tag: #ComputerSystems

- Question Number: 13
- Question Text: Which of the following is the appropriate description concerning the performance of a CPU?
- Options: a) Between a 32-bit CPU and a 64-bit CPU, the length of data that a 64-bit CPU can process at once can be greater., b) The smaller the amount of cache memory in a CPU, the higher the processing speed of the CPU., c) In CPUs with the same structure, when the clock frequency is decreased, the processing speed increases., d) Between a dual core CPU and a quad core CPU, a dual core CPU can execute a greater number of processes simultaneously.
- Correct Answer: a
- Category Tag: #ComputerSystems

- Question Number: 14
- Question Text: Which of the following is an appropriate characteristic of a dual system?
- Options: a) It provides two (2) sets of systems that perform the same processing and checks the correctness of the processing by comparing the results. If one of the systems fails, it isolates the failed system and continues the processing., b) The same two (2) devices are used, so that the processing capability can be increased to double that of a simplex system., c) It provides a currently used system for performing online processing and also a backup system that is made on standby while performing batch processing. In the event of a failure in the currently used system, it switches to the backup system, starts the online processing on it, and continues the service., d) It connects multiple devices in series and configures them in such a way that the load of each function is distributed among them, so that processing capability is high. But if any one of the devices fails, it becomes unable to provide the service.
- Correct Answer: a
- Category Tag: #ComputerSystems

- Question Number: 15
- Question Text: Among the changes A through D in a client/server system, which of the following is the list that contains all and only the appropriate changes for reducing the response time?
- Options: a) A, B, C, b) A, D, c) B, C, d) C, D
- Correct Answer: b
- Category Tag: #ComputerSystems

- Question Number: 16
- Question Text: There is a web system that is composed of two (2) web servers and one (1) database server as shown in the figure. When the availability of each Web server is 0.8 and the availability of the Database server is 0.9, which of the following is the availability of this system rounded off to two (2) decimal places?
  ![Q16 Web system diagram](images/2025S_IP/page-10.png)
- Options: a) 0.04, b) 0.58, c) 0.86, d) 0.96
- Correct Answer: c
- Category Tag: #ComputerSystems

- Question Number: 17
- Question Text: Which of the following is an appropriate explanation of multitasking?
- Options: a) Several computers connected via a network work together to achieve a high performance system., b) Several processor cores composed of arithmetic circuits and other control circuits are implemented in a single CPU., c) The CPU processing time is allocated to several processes in turn so that the processes can be executed concurrently., d) The same processing is performed for multiple data items by executing a single instruction.
- Correct Answer: c
- Category Tag: #ComputerSystems

- Question Number: 18
- Question Text: The types of programs that are running when a PC is started are broadly classified into three (3) categories, namely BIOS (Basic Input Output System), OS, and resident application programs. Which of the following is the order of execution of the programs?
- Options: a) BIOS, OS, resident application programs, b) OS, BIOS, resident application programs, c) OS, resident application programs, BIOS, d) Resident application programs, BIOS, OS
- Correct Answer: a
- Category Tag: #ComputerSystems

- Question Number: 19
- Question Text: Multiple files stored on a hard disk are used in work, from Monday to Friday. In order to handle failure of the hard disk, the data is backed up to another hard disk after the end of each day’s work. When the backup has following conditions, what is the total time required (in minutes) to perform backups of data from Monday to Friday?

[Conditions for backups]
(1) There are 6,000 files used in work, each with a size of 3 Mbytes.
(2) In each day’s work, 1,000 files are modified. Modifications do not change the size of the files.
(3) Files are copied to the other hard disk at a speed of 10 Mbytes/second. One (1) file is backed up at a time; backup continues without interruption.
(4) From Monday to Thursday, only files modified that day are backed up. On Friday, all files are backed up, whether or not they have been modified.
- Options: a) 25, b) 35, c) 50, d) 150
- Correct Answer: c
- Category Tag: #ComputerSystems

- Question Number: 20
- Question Text: Spreadsheet software is to be used to perform a calculation with the monthly sales data for each product shown in the worksheet below. When the expression `COUNTIF(B2:D2,">15000")` is entered in cell E2 and then copied to cell E3 and cell E4, which of the following is the value that is displayed in cell E4?

| | A | B | C | D | E |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Product name | January sales | February sales | March sales | Conditional count |
| **2** | Product A | 10,000 | 15,000 | 20,000 | |
| **3** | Product B | 5,000 | 10,000 | 5,000 | |
| **4** | Product C | 10,000 | 20,000 | 30,000 | |

- Options: a) 0, b) 1, c) 2, d) 3
- Correct Answer: c
- Category Tag: #TechnicalElements

- Question Number: 21
- Question Text: Which of the following is an Open Source Software (OSS) OS that is used in mobile devices such as smartphones and tablets?
- Options: a) Android, b) iOS, c) Safari, d) Windows
- Correct Answer: a
- Category Tag: #ComputerSystems

- Question Number: 22
- Question Text: In document creation software, spreadsheet software, and other such software, which of the following is a function that predefines and executes a series of operation procedures?
- Options: a) Autocomplete, b) Source code, c) Plug and play, d) Macro
- Correct Answer: d
- Category Tag: #ComputerSystems

- Question Number: 23
- Question Text: Which of the following is a space-saving server where computer components including the CPU, main memory, and storage are installed on a single circuit board and multiple circuit boards are mounted in racks?
- Options: a) DNS server, b) FTP server, c) Web server, d) Blade server
- Correct Answer: d
- Category Tag: #ComputerSystems

- Question Number: 24
- Question Text: Which of the following is a technology that projects things such as video made with computer graphics on to buildings, objects, and other such three-dimensional things, and produces a variety of visual effects?
- Options: a) Digital signage, b) Virtual reality, c) Projection mapping, d) Polygon
- Correct Answer: c
- Category Tag: #TechnicalElements

- Question Number: 25
- Question Text: Which of the following is a data format that can be used to compress both video and audio data?
- Options: a) BMP, b) GIF, c) JPEG, d) MPEG
- Correct Answer: d
- Category Tag: #TechnicalElements

- Question Number: 26
- Question Text: By joining tables “Employees in charge”, “Regions”, and “Customers” that are managed in a relational database, the table A that is shown below is obtained. Which of the following is the table “Customers” that is used for the joining? Here, a solid underline indicates a primary key and a dotted underline indicates a foreign key.
  ![Q26 Relational database tables](images/2025S_IP/page-13.png)
- Options: a) Table a, b) Table b, c) Table c, d) Table d
- Correct Answer: d
- Category Tag: #TechnicalElements

- Question Number: 27
- Question Text: Which of the following is an appropriate purpose of conducting data normalization when a relational database is constructed?
- Options: a) Providing redundancy to data in order to detect data errors, b) Eliminating data inconsistencies and duplications in order to make it easy to maintain and manage the data, c) Unifying the character code of data in order to improve data reliability and storage efficiency, d) Losslessly compressing data in order to improve access efficiency
- Correct Answer: b
- Category Tag: #TechnicalElements

- Question Number: 28
- Question Text: An “Employee” table and a “Department” table that are to be managed with a relational database were created on the basis of the conditions (i) through (v). Which of the following is the most appropriate primary key for the “Employee” table?

[Conditions]
(i) Each employee has one (1) employee number that is not duplicated.
(ii) There can be employees with the same first name and family name.
(iii) Each department has one (1) department code that is not duplicated.
(iv) Each department has multiple employees.
(v) Each employee belongs to only one (1) department.

- Options: a) “EmployeeNumber”, b) “EmployeeNumber” and “DepartmentCode”, c) “EmployeeName”, d) “DepartmentCode”
- Correct Answer: a
- Category Tag: #TechnicalElements

- Question Number: 29
- Question Text: Which of the following is the appropriate description concerning transaction processing?
- Options: a) Commit is the reversion of a database to the status prior to the start of the transaction when a transaction is not processed successfully., b) Exclusive control is the confirmation of the content of a database when a transaction is processed successfully., c) Rollback ensures that there are no inconsistencies in data when multiple transactions attempt to update data simultaneously., d) Log is a file that records transaction history of a database.
- Correct Answer: d
- Category Tag: #TechnicalElements

- Question Number: 30
- Question Text: Three (3) PCs and an Internet-capable TV (television) set are to be connected to the Internet by using a hub and a router that has a firewall function. Which of the following is an appropriate connection that enables the firewall function of the router to be used for all the traffic between the devices and the Internet? Here, “FW” in each figure indicates the firewall function.
  ![Q30 Firewall connections](images/2025S_IP/page-15.png)
- Options: a) a), b) b), c) c), d) d)
- Correct Answer: a
- Category Tag: #TechnicalElements

- Question Number: 31
- Question Text: Which of the following is the appropriate role of a DNS in a network?
- Options: a) In response to a request from a client for the allocation of an IP address, it allocates an unused IP address from a pool of IP addresses., b) It receives a requests for file transfers from clients and transfers files to clients, and stores files that it receives from clients., c) It links domain names to IP addresses., d) It receives a request for retrieval from an e-mail recipient and transfers e-mail received by a mail server.
- Correct Answer: c
- Category Tag: #TechnicalElements

- Question Number: 32
- Question Text: Which of the following is an appropriate example of an IPv4 IP address that is assigned to a PC?
- Options: a) 00.00.11.aa.bb.cc, b) 050-1234-5678, c) 10.123.45.67, d) http://www.example.co.jp/
- Correct Answer: c
- Category Tag: #TechnicalElements

- Question Number: 33
- Question Text: Mr. A sent an e-mail to the three (3) people Mr. P, Mr. Q, and Mr. R. He entered Mr. P’s e-mail address in the To field, Mr. Q’s e-mail address in the CC field, and Mr. R’s e-mail address in the BCC field. Which of the following is the appropriate description concerning the three (3) recipients of the e-mail?
- Options: a) Mr. P and Mr. Q can see that the same e-mail was also sent to Mr. R., b) Mr. P cannot see that the same e-mail was also sent to Mr. Q., c) Mr. Q can see that the same e-mail was also sent to Mr. P., d) Mr. R cannot see that the same e-mail was also sent to Mr. P and Mr. Q.
- Correct Answer: c
- Category Tag: #TechnicalElements

- Question Number: 34
- Question Text: Which of the following is a technology that is used to make voice calls over the Internet by two (2) parties using the same application on their smartphones or other devices?
- Options: a) MVNO, b) NFC, c) NTP, d) VoIP
- Correct Answer: d
- Category Tag: #TechnicalElements

- Question Number: 35
- Question Text: Among descriptions A through D concerning how to conduct information security education to employees, which of the following contains all and only the appropriate descriptions?

A: The re-education of one who has committed an information security breach includes preventive actions to avoid the same fault being repeated.
B: One way to conduct it is to incorporate it in a training program for new employees.
C: It is restricted to employees in the information systems department.
D: It is conducted after an incident or an accident concerning information security as well as on a regular basis.

- Options: a) A, B, D, b) A, C, D, c) A, D, d) B, C
- Correct Answer: a
- Category Tag: #TechnicalElements

- Question Number: 36
- Question Text: Among the descriptions A through D of how to handle a contact list that includes customer names, addresses, and other information, which of the following contains all and only the appropriate descriptions in terms of personal information protection?

A: Even if a customer asks to check his/her own registration information, this cannot be disclosed on the grounds of information protection.
B: A list of all names and addresses is extracted from the contact list and is sent to all the customers to have them check for errors.
C: A CD-ROM that includes contact list data is to be shredded before it is discarded.
D: Contact list data is to be encrypted when it is stored in a file.

- Options: a) A, C, D, b) A, D, c) B, C, d) C, D
- Correct Answer: d
- Category Tag: #TechnicalElements

- Question Number: 37
- Question Text: Among the threats and vulnerabilities in information security, which of the following is a vulnerability?
- Options: a) Computer virus, b) Social engineering, c) Tapping of communications data, d) Inappropriate password management
- Correct Answer: d
- Category Tag: #TechnicalElements

- Question Number: 38
- Question Text: Which of the following is an appropriate disposal method for media that stores confidential information to ensure that information leakage does not occur?
- Options: a) CDs and DVDs are destroyed and then are disposed of., b) A PC is disposed of with its CPU being destroyed., c) USB memory is disposed of with its files and folders being deleted., d) Paper documentation is not reused as memo paper and is sealed in a confidential envelope and then is disposed of together with general trash.
- Correct Answer: a
- Category Tag: #TechnicalElements

- Question Number: 39
- Question Text: Which of the following is a term for software that encrypts files on a computer in order to make them unusable, and demands money or other valuables in exchange for the decryption key?
- Options: a) Keylogger, b) Ransomware, c) Rootkit, d) Worm
- Correct Answer: b
- Category Tag: #TechnicalElements

- Question Number: 40
- Question Text: Which of the following is an appropriate example of biometric authentication?
- Options: a) Authentication with a fingerprint, b) Authentication with a digital certificate, c) Authentication with a personal ID card, d) Authentication with a one-time password
- Correct Answer: a
- Category Tag: #TechnicalElements

- Question Number: 41
- Question Text: During the use of a PC in workplace, a message was displayed stating that antivirus software had detected a virus. Which of the following is an appropriate action that should be taken immediately?
- Options: a) Reboot of the PC, b) Notification to the workplace by e-mail from the PC, c) Disconnection of the PC from networks, d) Backup of files on the PC
- Correct Answer: c
- Category Tag: #TechnicalElements

- Question Number: 42
- Question Text: There is an IoT system that is composed of IoT devices and an IoT server that manages them. Which of the following is the appropriate combination of information security incidents (i) through (iii) in this system, and confidentiality, integrity, and availability that are compromised because of the incidents?

[Incident]
(i) An IoT device stopped working because its battery ran out.
(ii) Communication between the IoT devices and the IoT server was not encrypted, so an information leakage occurred.
(iii) Incorrect data was recorded because of a system fault.

| | (i) | (ii) | (iii) |
| :--- | :--- | :--- | :--- |
| a) | Availability | Integrity | Confidentiality |
| b) | Availability | Confidentiality | Integrity |
| c) | Integrity | Availability | Confidentiality |
| d) | Confidentiality | Availability | Integrity |

- Options: a) a), b) b), c) c), d) d)
- Correct Answer: b
- Category Tag: #TechnicalElements

- Question Number: 43
- Question Text: In the activities of an organization that runs an ISMS on the basis of the PDCA cycle, improvements and corrective measures are decided from the results of monitoring of the risk management activities and other such information. In which process of the PDCA cycle is this activity performed?
- Options: a) P, b) D, c) C, d) A
- Correct Answer: d
- Category Tag: #TechnicalElements

- Question Number: 44
- Question Text: When risk treatment in risk management for information security is divided into the four (4) categories of risk avoidance, risk sharing, risk mitigation, and risk retention, which of the following is the appropriate explanation of risk sharing?
- Options: a) Halting activities that involve risk and fundamentally eliminating risk factors, for example, by not handling personal information, b) Implementing measures to reduce the probability of risk occurrence and reduce damage, such as distributing a data center over multiple locations that are geographically far away from each other in preparation for a disaster, c) Reducing damage that may occur when a risk materializes by transferring or distributing risk to a separate organization on the basis of an agreement, such as the purchasing of an insurance policy, d) If the probability of risk occurrence or the damage in the event of occurrence is considered to be small, recognizing the risk, and then accepting it without taking any particular measures
- Correct Answer: c
- Category Tag: #TechnicalElements

- Question Number: 45
- Question Text: Which of the following is an appropriate description concerning user authentication of a system?
- Options: a) A mechanism that achieves login to multiple servers, applications, and other such things with a single authentication is called challenge-response authentication., b) A mechanism that authenticates a user by using fingerprints, voice prints, and other characteristics of a body is called single sign-on., c) A code number that is used in order to authenticate a user of an information system is called a PIN., d) A method where, instead of the order of specific numbers or characters, the positions in a grid are memorized, and during authentication, a person enters the numbers and characters in the positions that he/she remembers in a grid that is displayed on the screen is called multi-factor authentication.
- Correct Answer: c
- Category Tag: #TechnicalElements

- Question Number: 46
- Question Text: Mr. A, a participant in system testing, has no access to the design of the internal structure of the system or software and prepares input data and output data to be used in verification of the transaction functions commonly used in the department. Which of the following is the testing technique that Mr. A is going to implement?
- Options: a) Inspection, b) Walk-through, c) Black-box testing, d) White-box testing
- Correct Answer: c
- Category Tag: #DevelopmentTechniques

- Question Number: 47
- Question Text: The processes of system development include system requirements definition, systems architecture design, system integration testing, and software acceptance. Which of the following is an activity that is performed in system requirements definition?
- Options: a) The party to which development is outsourced uses the software under the same conditions as the actual production environment in order to determine if it runs correctly., b) A system test plan is created, and a test environment is prepared., c) The functions and performance required of the system are clarified., d) A program is created and test results are reviewed according to the evaluation criteria.
- Correct Answer: c
- Category Tag: #DevelopmentTechniques

- Question Number: 48
- Question Text: What is the term for revising and changing programs after system development?
- Options: a) Computerization planning, b) System operation, c) Software maintenance, d) Requirements definition
- Correct Answer: c
- Category Tag: #DevelopmentTechniques

- Question Number: 49
- Question Text: Which of the following is the most appropriate description concerning the usability of RPA software when the quality characteristics of software are classified into portability, functional suitability, compatibility, usability, reliability, performance efficiency, security, and maintainability?
- Options: a) It operates even if the OS of the PC that RPA runs on changes., b) Automatic processing is executed at the time and on the conditions that are specified with RPA., c) Even if the version of the application software that is the subject of operation by RPA is upgraded, RPA will work with a simple change of the settings., d) People who have never used RPA can use it with only simple education.
- Correct Answer: d
- Category Tag: #DevelopmentTechniques

- Question Number: 50
- Question Text: Which of the following is the most appropriate case example of DevOps in software development?
- Options: a) The developer prepares a prototype of important functions, and evaluates its adequacy by measuring the performance together with the customer., b) The developer moves on to the next development phase only after it is judged that the current phase is complete, and handovers the system to the operation side only after the system test where users participating in a system test confirm the operability., c) The developer and the operator work in close cooperation and quickly proceed with the implementation and update of functions, etc., by using automation tools and other such tools., d) The programs are added one by one while fixed short-period cycles are repeated in order to expand the functions in the development of a system.
- Correct Answer: c
- Category Tag: #DevelopmentTechniques

- Question Number: 51
- Question Text: A system development project has more defects than the quality targets. In order to clarify the issues to prioritize for resolution, the number of defects for each cause is to be investigated and shown with a chart. Which of the following is an appropriate chart to use?
  ![Q51 Defect chart](images/2025S_IP/page-22.png)
- Options: a) a), b) b), c) c), d) d)
- Correct Answer: b
- Category Tag: #ProjectManagement

- Question Number: 52
- Question Text: A system development project at a company is becoming delayed. In order to resolve the delay, the project leader proposes to project members that part of the planned work procedure be omitted. The project members are divided into those who think that this cannot be avoided and those who are opposed because the quality will decrease. From the perspective of ensuring quality in a project, which of the following is the most appropriate action for a project leader to take?
- Options: a) Discussing detailed measures against decrease in quality within the project, and building consensus as a project, b) Deciding whether to accept or reject a proposal with a majority decision by highly skilled people from among the project members, c) Proceeding as he/she proposed because he/she has the most experience, d) Replacing project members who cannot agree with his/her proposal
- Correct Answer: a
- Category Tag: #ProjectManagement

- Question Number: 53
- Question Text: In an arrow diagram that shows system development, if activities A and D are delayed for three (3) days in total, what is the delay in the entire project?
  ![Q53 Arrow diagram](images/2025S_IP/page-23.png)
- Options: a) 1, b) 2, c) 3, d) 4
- Correct Answer: a
- Category Tag: #ProjectManagement

- Question Number: 54
- Question Text: In a project team that is required to communicate information on a one-to-one basis, when the members increase from six (6) people to ten (10) people, by how many times does the number of paths that are required for communicating information increase?
- Options: a) 1.5, b) 2.5, c) 3, d) 6
- Correct Answer: c
- Category Tag: #ProjectManagement

- Question Number: 55
- Question Text: Which of the following is a method that organizes all of the activities to be performed in the project in a hierarchical structure?
- Options: a) CRM, b) ERP, c) PPM, d) WBS
- Correct Answer: d
- Category Tag: #ProjectManagement

- Question Number: 56
- Question Text: When a system development project is started, it is foreseen that the progress of the project may be affected by a large number of change requests for specification that come from users during the course of development. Which of the following is the most appropriate measure for ensuring that there is no deterioration in quality or delay in delivery date?
- Options: a) Declaring to the customer that change requests cannot be accepted after the completion of design, b) Shortening the test period by skipping tests when a delay occurs during the course of the project, c) Including in the plan that the implementation of a function will be called off if there are a large number of change requests, d) Reaching an agreement with the customer on what can be accepted as change requests and how to determine the priority of the accepted change requests
- Correct Answer: d
- Category Tag: #ProjectManagement

- Question Number: 57
- Question Text: The processes of project management include project cost management, project communications management, project resources management, project schedule management, and the like. In a system development project, which of the following is the most appropriate activity in project cost management when members are added for implementing a test?
- Options: a) Updating the mailing list, etc. so that information can be efficiently transmitted to the newly participating members, b) Requesting a vendor to provide training on the testing tool to the newly participating members, c) Adding tasks to be handled by the newly participating members, and changing the schedule, d) Estimating the personnel expenses of the newly participating members, and changing the plan
- Correct Answer: d
- Category Tag: #ProjectManagement

- Question Number: 58
- Question Text: Which of the following is an appropriate purpose for facility management concerning IT systems?
- Options: a) Optimization of IT service cost, b) Continuation of a company’s business in the event of a disaster, etc., c) Ensuring appropriate security for information assets, d) Overall maintenance of facilities and the environment for information processing
- Correct Answer: d
- Category Tag: #ServiceManagement

- Question Number: 59
- Question Text: Which of the following is the most appropriate activities of a service desk?
- Options: a) Eliminating root cause of incident., b) Installing updated software., c) Centralized management of changes., d) Handling and recording inquiries from users.
- Correct Answer: d
- Category Tag: #ServiceManagement

- Question Number: 60
- Question Text: Which of the following is the most appropriate interface that responds to the query from a user in an interactive and automated manner?
- Options: a) Recommendation, b) Chatbot, c) Escalation, d) FAQs
- Correct Answer: b
- Category Tag: #ServiceManagement

- Question Number: 61
- Question Text: In the PDCA cycle of service level management, which of the following is implemented as C (Check)?
- Options: a) Providing services on basis of SLA., b) Preparing service improvement plan., c) Agreeing upon desired quality., d) Monitoring and measuring provided services and preparing report.
- Correct Answer: d
- Category Tag: #ServiceManagement

- Question Number: 62
- Question Text: Which of the following is the appropriate combination of IT service management and the content of the SLA for a hosting service?
- Options: a) A: Availability, B: Capacity, C: Security, b) A: Availability, B: Security, C: Capacity, c) A: Capacity, B: Availability, C: Security, d) A: Security, B: Capacity, C: Availability
- Correct Answer: a
- Category Tag: #ServiceManagement

- Question Number: 63
- Question Text: In a company, which of the following is responsible for the establishment of IT governance?
- Options: a) Shareholders, b) Management, c) System auditor, d) Head of systems department
- Correct Answer: b
- Category Tag: #ManagementStrategy

- Question Number: 64
- Question Text: A food manufacturer is conducting business in accordance with food industry safety standards. Which of the following objectives of internal control corresponds to this action?
- Options: a) Effectiveness and efficiency of business, b) Reliability of financial reporting, c) Compliance with laws and regulations, d) Protection of assets
- Correct Answer: c
- Category Tag: #CorporateLegalAffairs

- Question Number: 65
- Question Text: Which of the following is the most appropriate objective of an accounting audit?
- Options: a) To check risks are controlled., b) To check risk management is effective., c) To check work is implemented rationally., d) To check processing is performed without impropriety or errors in financial reports.
- Correct Answer: d
- Category Tag: #CorporateLegalAffairs

- Question Number: 66
- Question Text: Which of the following is an appropriate way to brainstorm?
- Options: a) Refrain from generating unrestrained ideas., b) Proceeding without blaming any member for improved ideas., c) Selecting ideas suitable to theme during session., d) Encouraging criticism to pursue quality.
- Correct Answer: b
- Category Tag: #ManagementStrategy

- Question Number: 67
- Question Text: What is the ratio in percentage of the profit result to the profit plan?
- Options: a) 77, b) 99, c) 110, d) 129
- Correct Answer: a
- Category Tag: #ManagementStrategy

- Question Number: 68
- Question Text: If risk assessment is divided into three (3) processes, which of the following is the third process besides risk identification and risk evaluation?
- Options: a) Risk transfer, b) Risk avoidance, c) Risk reduction, d) Risk analysis
- Correct Answer: d
- Category Tag: #ManagementStrategy

- Question Number: 69
- Question Text: Which of the following is the most appropriate term that describes withdrawing from business area A to strengthen area B?
- Options: a) Business environment, b) Business strategy, c) Management vision, d) Management philosophy
- Correct Answer: b
- Category Tag: #ManagementStrategy

- Question Number: 70
- Question Text: Which of the following is an expression that calculates operating profit?
- Options: a) (Gross profit) − (Selling, general, and administrative expense), b) (Sales) − (Cost of sales), c) (Current profits) + (Extraordinary profit) − (Extraordinary loss), d) (Current net profit before tax) − (Taxes)
- Correct Answer: a
- Category Tag: #CorporateLegalAffairs

- Question Number: 71
- Question Text: Which of the following is a chart suitable for displaying cumulative percentage in a line chart in descending order for determining priority?
- Options: a) PERT chart, b) Control chart, c) Cause and effect diagram, d) Pareto chart
- Correct Answer: d
- Category Tag: #ManagementStrategy

- Question Number: 72
- Question Text: Which of the following is a role that has direct responsibility for technology management?
- Options: a) CEO, b) CFO, c) COO, d) CTO
- Correct Answer: d
- Category Tag: #ManagementStrategy

- Question Number: 73
- Question Text: Which of the following is a corporate activity of compliance promotion?
- Options: a) Sharing sales know-how., b) Sharing customer information among departments., c) Sharing schedules and documents., d) Creating code of conduct based on ethics and ethical education.
- Correct Answer: d
- Category Tag: #CorporateLegalAffairs

- Question Number: 74
- Question Text: Which of the following is defined for information security management?
- Options: a) IEEE 802.3, b) ISO/IEC 27001, c) JPEG 2000, d) MPEG 1
- Correct Answer: b
- Category Tag: #CorporateLegalAffairs

- Question Number: 75
- Question Text: Which of the following is the most appropriate example of standardization in the manufacturing industry?
- Options: a) Daily workload balance., b) Common components and procedures are used., c) Optimum algorithm is selected., d) Production planning simplification.
- Correct Answer: b
- Category Tag: #CorporateLegalAffairs

- Question Number: 76
- Question Text: According to ISO 9000, which of the following is most appropriate as a product with good quality?
- Options: a) A product having no customer complaints and high satisfaction., b) A product produced in-house., c) A product designed using CAD/CAM., d) A product utilizing high quality materials.
- Correct Answer: a
- Category Tag: #CorporateLegalAffairs

- Question Number: 77
- Question Text: Which of the following is the most appropriate example of enhanced corporate governance?
- Options: a) Enhancing labor system for women., b) Purchasing another company., c) Increasing number of independent outside directors., d) Withdrawing from low profit business.
- Correct Answer: c
- Category Tag: #CorporateLegalAffairs

- Question Number: 78
- Question Text: Which of the following is the most appropriate term to express software provided at a set fee or for a certain period?
- Options: a) Activation, b) Adware, c) Subscription, d) Volume license
- Correct Answer: c
- Category Tag: #ManagementStrategy

- Question Number: 79
- Question Text: Which of the following is appropriate as measures to leverage strengths and overcome threats based on the SWOT analysis?
- Options: a) Extend retirement age., b) Procure funds at low interest., c) Research and develop electric automobiles., d) Strengthen sales capabilities.
- Correct Answer: c
- Category Tag: #ManagementStrategy

- Question Number: 80
- Question Text: Which of the following is an appropriate description concerning M&A?
- Options: a) Analysis of value chain., b) Increase in autonomy by dividing company., c) Reform of business processes., d) Acceleration of business deployment through corporate acquisition.
- Correct Answer: d
- Category Tag: #ManagementStrategy

- Question Number: 81
- Question Text: Which of the following is an appropriate explanation of 3C analysis?
- Options: a) Perspectives of customers, competitors, and company., b) Last purchase date, frequency, and amount., c) Elements of era, age, and generation., d) Groups in descending order of sales.
- Correct Answer: a
- Category Tag: #ManagementStrategy

- Question Number: 82
- Question Text: Which of the following is an appropriate description concerning a balanced scorecard (BSC)?
- Options: a) Management technique from four viewpoints (financial, customer, business process, growth and learning)., b) View of corporate activities as chain of procurement to service., c) Technique to determine product combination., d) Evaluation of SWOT.
- Correct Answer: a
- Category Tag: #ManagementStrategy

- Question Number: 83
- Question Text: Which of the following is an appropriate organization formed through collaborative investment for R&D?
- Options: a) M&A, b) Cross-license, c) Joint venture, d) Spin-off
- Correct Answer: c
- Category Tag: #ManagementStrategy

- Question Number: 84
- Question Text: Which of the following is the most appropriate example of business improvement through SCM?
- Options: a) Sold over Internet., b) Sales info managed with database., c) Sales info sent to manufacturer over network for timely supply., d) Data gathered at headquarters for analysis.
- Correct Answer: c
- Category Tag: #ManagementStrategy

- Question Number: 85
- Question Text: Which of the following is the term for publishing interface specifications to permit access from external parties?
- Options: a) BPO, b) RPA, c) Open API, d) Technology management
- Correct Answer: c
- Category Tag: #ManagementStrategy

- Question Number: 86
- Question Text: Which of the following is a system that collects information at the time of sale?
- Options: a) ETC, b) GPS, c) POS, d) SCM
- Correct Answer: c
- Category Tag: #ManagementStrategy

- Question Number: 87
- Question Text: Which of the following is the most appropriate description concerning deep learning?
- Options: a) Integrates info between departments., b) Digital education/training., c) Sharing knowledge/knowhow., d) Computer identifies and learns characteristics by imitating neural circuits.
- Correct Answer: d
- Category Tag: #ManagementStrategy

- Question Number: 88
- Question Text: Which of the following is an appropriate effect of CAD?
- Options: a) Identifying material volume., b) Automating production processes., c) Managing production integratedly., d) Reusing design data and simplifying work.
- Correct Answer: d
- Category Tag: #ManagementStrategy

- Question Number: 89
- Question Text: Which of the following is the term for an automobile connected to the Internet?
- Options: a) Car sharing, b) Car navigation system, c) Connected car, d) Electric automobile
- Correct Answer: c
- Category Tag: #ManagementStrategy

- Question Number: 90
- Question Text: Which of the following is the appropriate name for a system using electronic tags for production orders?
- Options: a) Kanban system, b) Craft production system, c) Cell production system, d) Build-to-stock production system
- Correct Answer: a
- Category Tag: #ManagementStrategy

- Question Number: 91
- Question Text: Which of the following is the type of crowdfunding where profits are paid as dividends?
- Options: a) Loan-based, b) Donation-based, c) Purchase-based, d) Investment-based
- Correct Answer: d
- Category Tag: #ManagementStrategy

- Question Number: 92
- Question Text: Which mechanism displays images of past buildings on top of current scenery?
- Options: a) AR, b) GUI, c) VR, d) Metaverse
- Correct Answer: a
- Category Tag: #ManagementStrategy

- Question Number: 93
- Question Text: Which of the following is the most appropriate description concerning DFD?
- Options: a) Transitions of state., b) Relationships and data structure., c) Attributes and operations of components., d) Focuses on flow of data and relations with processing.
- Correct Answer: d
- Category Tag: #SystemStrategy

- Question Number: 94
- Question Text: Which of the following is the most appropriate term for large quantities of diverse forms of data?
- Options: a) Big data, b) Diversity, c) Core competence, d) Crowdfunding
- Correct Answer: a
- Category Tag: #ManagementStrategy

- Question Number: 95
- Question Text: Which of the following is the most appropriate explanation of the relation between business strategy and information systems strategy?
- Options: a) Created independently., b) IS strategy is created on basis of business strategy., c) Business strategy is created on basis of IS strategy., d) Strategies of different departments.
- Correct Answer: b
- Category Tag: #ManagementStrategy

- Question Number: 96
- Question Text: Which of the following is a term that represents practical verification of a new concept?
- Options: a) CRM, b) KPI, c) PoC, d) SLA
- Correct Answer: c
- Category Tag: #SystemStrategy

- Question Number: 97
- Question Text: Which of the following is the appropriate combination of terms for RFP?
- Options: a) A: Info system dept, B: Vendors, C: System requirements, b) A: Info system dept, B: User depts, C: System requirements, c) A: Vendor, B: Info system dept, C: System installation result, d) A: Vendor, B: User dept, C: System installation result
- Correct Answer: a
- Category Tag: #SystemStrategy

- Question Number: 98
- Question Text: Which of the following refers to goals for development to be achieved by 2030 by UN?
- Options: a) SDGs, b) SDK, c) SGA, d) SGML
- Correct Answer: a
- Category Tag: #ManagementStrategy

- Question Number: 99
- Question Text: Which process clarifies system functions and builds consensus on basis of computerization plan?
- Options: a) Planning process, b) Requirements definition process, c) Development process, d) Operation process
- Correct Answer: b
- Category Tag: #DevelopmentTechniques

- Question Number: 100
- Question Text: Which term expresses change using digital technology to create UX and business models that destroy existing structures?
- Options: a) Digital signage, b) Digital disruption, c) Digital divide, d) Digital transformation
- Correct Answer: b
- Category Tag: #ManagementStrategy
