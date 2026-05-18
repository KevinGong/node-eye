#!/usr/bin/env python3
"""
Interactive Subscriber Management CLI

Usage:
  python manage_subscribers.py
  
Commands:
  list    - List all subscribers
  add     - Add new subscriber
  remove  - Remove subscriber
  export  - Export to JSON (for backup)
  import  - Import from JSON
  help    - Show this help
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from encrypt_subscribers import (
    load_subscribers, save_subscribers,
    add_subscriber, remove_subscriber
)

DATA_DIR = Path(__file__).parent.parent / 'data'

def print_menu():
    """Print interactive menu"""
    print("\n" + "=" * 50)
    print("📧 Node Eye Subscriber Management")
    print("=" * 50)
    print("1. List all subscribers")
    print("2. Add new subscriber")
    print("3. Remove subscriber")
    print("4. Export to JSON")
    print("5. Import from JSON")
    print("6. View statistics")
    print("0. Exit")
    print("=" * 50)

def list_subscribers_menu():
    """List all subscribers"""
    data = load_subscribers()
    subs = data.get('subscribers', [])
    
    print("\n" + "=" * 60)
    print(f"📊 Total Subscribers: {len(subs)}")
    print("=" * 60)
    
    if not subs:
        print("No subscribers yet")
        return
    
    # Group by chain
    by_chain = {}
    for sub in subs:
        chain = sub['chain_id']
        if chain not in by_chain:
            by_chain[chain] = []
        by_chain[chain].append(sub)
    
    for chain, chain_subs in by_chain.items():
        print(f"\n{chain.upper()} ({len(chain_subs)} subscribers):")
        for sub in chain_subs:
            print(f"  - {sub['email']}")
            print(f"    Added: {sub.get('subscribed_at', 'N/A')[:10]}")

def add_subscriber_menu():
    """Add new subscriber interactively"""
    print("\n➕ Add New Subscriber")
    print("-" * 40)
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email cannot be empty")
        return
    
    print("\nAvailable chains:")
    print("  1. bitcoin")
    print("  2. ethereum")
    print("  3. litecoin")
    print("  4. dogecoin")
    
    chain_choice = input("Chain (1-4 or name): ").strip().lower()
    
    chain_map = {
        '1': 'bitcoin',
        '2': 'ethereum',
        '3': 'litecoin',
        '4': 'dogecoin',
        'bitcoin': 'bitcoin',
        'ethereum': 'ethereum',
        'litecoin': 'litecoin',
        'dogecoin': 'dogecoin'
    }
    
    chain_id = chain_map.get(chain_choice, chain_choice)
    if not chain_id:
        print("❌ Invalid chain")
        return
    
    add_subscriber(email, chain_id)

def remove_subscriber_menu():
    """Remove subscriber interactively"""
    print("\n➖ Remove Subscriber")
    print("-" * 40)
    
    email = input("Email to remove: ").strip()
    if not email:
        print("❌ Email cannot be empty")
        return
    
    remove_subscriber(email)

def export_subscribers():
    """Export subscribers to JSON"""
    data = load_subscribers()
    
    output_file = DATA_DIR / f'subscribers_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported to {output_file}")

def import_subscribers():
    """Import subscribers from JSON"""
    print("\n📥 Import Subscribers")
    print("-" * 40)
    
    json_file = input("JSON file path: ").strip()
    
    if not Path(json_file).exists():
        print("❌ File not found")
        return
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Merge with existing
        existing = load_subscribers()
        existing_emails = {sub['email'] for sub in existing['subscribers']}
        
        imported_count = 0
        for sub in data.get('subscribers', []):
            if sub['email'] not in existing_emails:
                existing['subscribers'].append(sub)
                imported_count += 1
        
        save_subscribers(existing)
        print(f"✅ Imported {imported_count} new subscribers")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")

def view_statistics():
    """View subscription statistics"""
    data = load_subscribers()
    subs = data.get('subscribers', [])
    
    print("\n" + "=" * 60)
    print("📊 Subscription Statistics")
    print("=" * 60)
    
    print(f"Total Subscribers: {len(subs)}")
    
    # By chain
    by_chain = {}
    for sub in subs:
        chain = sub['chain_id']
        by_chain[chain] = by_chain.get(chain, 0) + 1
    
    print("\nBy Chain:")
    for chain, count in sorted(by_chain.items(), key=lambda x: -x[1]):
        print(f"  {chain}: {count}")
    
    # Recent subscriptions (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent = [
        sub for sub in subs
        if datetime.fromisoformat(sub.get('subscribed_at', '2000-01-01')) > seven_days_ago
    ]
    print(f"\nNew this week: {len(recent)}")

def main():
    """Main interactive loop"""
    print("\n👁️  Node Eye Subscriber Manager")
    
    while True:
        print_menu()
        choice = input("Enter choice (0-6): ").strip()
        
        if choice == '1':
            list_subscribers_menu()
        elif choice == '2':
            add_subscriber_menu()
        elif choice == '3':
            remove_subscriber_menu()
        elif choice == '4':
            export_subscribers()
        elif choice == '5':
            import_subscribers()
        elif choice == '6':
            view_statistics()
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == '__main__':
    from datetime import timedelta
    main()
