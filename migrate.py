#!/usr/bin/env python3

import subprocess
import sys
import argparse

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error output: {e.stderr}")
        return False

def create_migration(message):
    print(f"Creating migration: {message}")
    command = f'alembic revision --autogenerate -m "{message}"'
    return run_command(command)

def apply_migrations():
    print("Applying migrations...")
    return run_command("alembic upgrade head")

def rollback_migration():
    print("Rolling back last migration...")
    return run_command("alembic downgrade -1")

def show_current_revision():
    print("Current database revision:")
    return run_command("alembic current")

def show_migration_history():
    print("Migration history:")
    return run_command("alembic history")

def main():
    parser = argparse.ArgumentParser(description="Database migration management")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create migration
    create_parser = subparsers.add_parser('create', help='Create a new migration')
    create_parser.add_argument('message', help='Migration message')
    
    # Apply migrations
    subparsers.add_parser('migrate', help='Apply pending migrations')
    
    # Rollback
    subparsers.add_parser('rollback', help='Rollback the last migration')
    
    # Current revision
    subparsers.add_parser('current', help='Show current database revision')
    
    # History
    subparsers.add_parser('history', help='Show migration history')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_migration(args.message)
    elif args.command == 'migrate':
        apply_migrations()
    elif args.command == 'rollback':
        rollback_migration()
    elif args.command == 'current':
        show_current_revision()
    elif args.command == 'history':
        show_migration_history()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
