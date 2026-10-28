import psycopg

print("Testing connection...")

try:
    # We are hardcoding the URL exactly as it should be
    # Notice the %40 for the @ symbol
    conn = psycopg.connect(
        "postgresql://postgres.kcphopjpvtrllckyjnfd:Khanandkhan767%40@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
    )
    print("✅ CONNECTION SUCCESSFUL!")
    conn.close()
except Exception as e:
    print("❌ CONNECTION FAILED:", e)