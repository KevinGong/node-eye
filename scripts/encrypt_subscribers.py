#!/usr/bin/env python3
"""
Subscriber Data Encryption/Decryption Utility
Encryption password: 20260518

Usage:
  python encrypt_subscribers.py encrypt [json_file]    # Encrypt JSON to ENC
  python encrypt_subscribers.py decrypt [enc_file]     # Decrypt ENC to JSON
  python encrypt_subscribers.py add <email> <chain>    # Add subscriber
  python encrypt_subscribers.py remove <email>         # Remove subscriber
  python encrypt_subscribers.py list                   # List all subscribers
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Simple XOR encryption with password
PASSWORD = "20260518"

def xor_encrypt_decrypt(data: bytes, key: str) -> bytes:
    """XOR encryption/decryption (symmetric)"""
    key_bytes = key.encode('utf-8')
    result = bytearray()
    
    for i, byte in enumerate(data):
        result.append(byte ^ key_bytes[i % len(key_bytes)])
    
    return bytes(result)

def encrypt_json_to_file(json_data: dict, output_file: str):
    """Encrypt JSON data to file"""
    json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
    encrypted = xor_encrypt_decrypt(json_str.encode('utf-8'), PASSWORD)
    
    # Write as base64 for safe storage
    import base64
    with open(output_file, 'wb') as f:
        f.write(base64.b64encode(encrypted))
    
    print(f"✅ Encrypted data saved to {output_file}")

def decrypt_file_to_json(input_file: str) -> dict:
    """Decrypt file to JSON data"""
    import base64
    
    with open(input_file, 'rb') as f:
        encrypted = base64.b64decode(f.read())
    
    decrypted = xor_encrypt_decrypt(encrypted, PASSWORD)
    return json.loads(decrypted.decode('utf-8'))

def load_subscribers():
    """Load subscribers from encrypted file"""
    enc_file = Path(__file__).parent.parent / 'data' / 'subscribers.enc'
    
    if not enc_file.exists():
        return {'subscribers': []}
    
    try:
        return decrypt_file_to_json(str(enc_file))
    except Exception as e:
        print(f"⚠️  Failed to decrypt: {e}")
        return {'subscribers': []}

def save_subscribers(data: dict):
    """Save subscribers to encrypted file"""
    enc_file = Path(__file__).parent.parent / 'data' / 'subscribers.enc'
    encrypt_json_to_file(data, str(enc_file))

def add_subscriber(email: str, chain_id: str):
    """Add a new subscriber - Direct save without verification"""
    data = load_subscribers()
    
    # Check if already subscribed
    for sub in data['subscribers']:
        if sub['email'] == email:
            sub['chain_id'] = chain_id
            sub['updated_at'] = datetime.now().isoformat()
            save_subscribers(data)
            print(f"✅ Updated subscription for {email}")
            return True
    
    # Add new subscriber - Direct save, no verification needed
    data['subscribers'].append({
        'email': email,
        'chain_id': chain_id,
        'subscribed_at': datetime.now().isoformat(),
        'status': 'active'
    })
    
    save_subscribers(data)
    print(f"✅ Added subscriber: {email} ({chain_id})")
    return True

def remove_subscriber(email: str):
    """Remove a subscriber - Deprecated, unsubscribe disabled"""
    print("⚠️  Unsubscribe functionality is disabled")
    print("   Contact administrator to remove subscription")
    return None

def list_subscribers():
    """List all subscribers"""
    data = load_subscribers()
    
    print("\n📊 Subscriber List")
    print("=" * 60)
    print(f"Total subscribers: {len(data['subscribers'])}")
    print("=" * 60)
    
    for sub in data['subscribers']:
        print(f"  - {sub['email']} ({sub['chain_id']})")
        print(f"    Subscribed: {sub.get('subscribed_at', 'N/A')}")
        print(f"    Status: {sub.get('status', 'active')}")
    
    return data['subscribers']

def get_subscribers_for_chain(chain_id: str) -> list:
    """Get all subscribers for a specific chain"""
    data = load_subscribers()
    return [
        sub for sub in data['subscribers'] 
        if sub['chain_id'] == chain_id and sub.get('status') == 'active'
    ]

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'encrypt':
        json_file = sys.argv[2] if len(sys.argv) > 2 else 'subscribers.json'
        with open(json_file, 'r') as f:
            data = json.load(f)
        encrypt_json_to_file(data, json_file.replace('.json', '.enc'))
    
    elif command == 'decrypt':
        enc_file = sys.argv[2] if len(sys.argv) > 2 else 'subscribers.enc'
        data = decrypt_file_to_json(enc_file)
        print(json.dumps(data, indent=2))
    
    elif command == 'add':
        if len(sys.argv) < 4:
            print("Usage: python encrypt_subscribers.py add <email> <chain_id>")
            sys.exit(1)
        add_subscriber(sys.argv[2], sys.argv[3])
    
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("Usage: python encrypt_subscribers.py remove <email>")
            sys.exit(1)
        remove_subscriber(sys.argv[2])
    
    elif command == 'list':
        list_subscribers()
    
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
