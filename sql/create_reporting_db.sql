USE reporting_db;
CREATE TABLE employee_kpis (
	id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20),
    date DATE,
    calls_handled INT,
    avg_call_time FLOAT,
    escalation_count INT,
    resolution_status VARCHAR(20)
);