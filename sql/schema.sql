-- Création de la table
DROP TABLE IF EXISTS financial_data;

CREATE TABLE financial_data (
                                id SERIAL PRIMARY KEY,
                                month VARCHAR(7) NOT NULL,
                                department VARCHAR(50) NOT NULL,
                                budget NUMERIC(12,2),
                                actual NUMERIC(12,2),
                                variance NUMERIC(12,2),
                                variance_pct NUMERIC(8,2),
                                is_anomaly BOOLEAN DEFAULT FALSE,
                                anomaly_score NUMERIC(6,4)
);

CREATE INDEX idx_month ON financial_data(month);
CREATE INDEX idx_department ON financial_data(department);

-- Contrainte de cohérence
ALTER TABLE financial_data
    ADD CONSTRAINT chk_variance
        CHECK (variance = actual - budget OR variance IS NULL);