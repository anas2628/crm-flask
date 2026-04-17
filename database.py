import sqlite3

conn = sqlite3.connect('crm.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS customers (
            id integer PRIMARY KEY not null,
            name text,
            email text,
            phone text,
            notes text
        )""")
conn.commit()
def add_customers(name, email, phone, notes):
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute("INSERT INTO customers (name, email, phone, notes) VALUES(?,?,?,?)", (name, email, phone, notes))
    conn.commit()
    conn.close()
    
def get_all_customers():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM customers')
    result = c.fetchall()
    return result

def delete_customer(id):
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('DELETE FROM customers WHERE id=?', (id,))
    conn.commit()
    conn.close()
    
def update_customer(id,name,email,phone,notes):
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('UPDATE customers SET name = ?, email=?, phone=?, notes=? WHERE   id=?', (name,email,phone,notes,id))
    conn.commit()
    conn.close()
    
def get_customer(id):
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM customers WHERE id=?', (id,))
    result = c.fetchone()
    conn.close()
    return result

def search_customers(query):
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM customers WHERE name LIKE ?', ('%' + query + '%',))
    result = c.fetchall()
    conn.close()
    return result
