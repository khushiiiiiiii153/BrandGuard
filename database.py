import sqlite3
import json
from datetime import datetime

DB_PATH = "data/brandguard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Brand Rules Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brand_rules (
            id TEXT PRIMARY KEY,
            category TEXT,
            rule_text TEXT,
            banned_terms TEXT,
            preferred_terms TEXT,
            severity TEXT
        )
    ''')
    
    # Claim Evidence Vault Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claim_vault (
            id TEXT PRIMARY KEY,
            claim_pattern TEXT,
            evidence_source TEXT,
            expiry_date TEXT,
            status TEXT
        )
    ''')
    
    # Submissions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            original_text TEXT,
            cleaned_text TEXT,
            status TEXT,
            creator_id TEXT,
            version INTEGER,
            created_at TEXT
        )
    ''')
    
    # Pre-populate sample rules
    cursor.execute('SELECT COUNT(*) FROM brand_rules')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO brand_rules VALUES (?, ?, ?, ?, ?, ?)
        ''', [
            ("R-001", "Terminology", "Avoid absolute claims without explicit backing.", "No.1,100% free,Best in India", "Leading,Verified", "High"),
            ("R-002", "Tone", "Maintain a professional, accessible, and supportive tone.", "cheap,guaranteed,insane", "affordable,assured,remarkable", "Medium"),
            ("R-003", "Hindi/Hinglish", "Do not use unverified absolute statements in local scripts.", "सबसे सस्ता,100% गारंटी,बिलकुल मुफ़्त", "किफायती,भरोसेमंद,आकर्षक ऑफर", "High")
        ])
        
        cursor.executemany('''
            INSERT INTO claim_vault VALUES (?, ?, ?, ?, ?)
        ''', [
            ("C-101", "30% faster", "Lab Benchmark Report Q3 2026", "2026-12-31", "Active"),
            ("C-102", "100% sugar-free", "Lab Audit Certificate #8821", "2026-05-01", "Expired")
        ])
        
    conn.commit()
    conn.close()

def get_rules():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, rule_text, banned_terms, preferred_terms, severity FROM brand_rules")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_claims():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, claim_pattern, evidence_source, expiry_date, status FROM claim_vault")
    rows = cursor.fetchall()
    conn.close()
    return rows