from app.cli import create_domain

if __name__ == "__main__":
    for i in range(201):
        create_domain(f"criteo{i}.com", "ads", 1)
