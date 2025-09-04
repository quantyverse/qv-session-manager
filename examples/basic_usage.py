#!/usr/bin/env python3
"""
Demo: SessionManager with qv-ollama-sdk

This example shows how to use the SessionManager to
persistently store and manage conversations.
"""

import os
import time
from datetime import datetime
from qv_session_manager.session_manager import SessionManager
from qv_ollama_sdk.domain.models import Conversation, MessageRole

def main():
    print("🚀 SessionManager Demo")
    print("=" * 50)
    
    # 1. Initialize SessionManager
    mgr = SessionManager(db_path="demo_sessions.db")
    print("✅ SessionManager initialized")
    
    # 2. Create new Conversation
    print("\n📝 Creating new conversation...")
    conv = Conversation(
        model_name="gemma2:2b", 
        title="Python Learning Help",
        metadata={"topic": "programming", "level": "beginner"}
    )
    
    # Add messages
    conv.add_system_message("You are a helpful Python tutor.")
    conv.add_user_message("Explain Python lists to me!")
    conv.add_assistant_message("Python lists are ordered, mutable collections. They are defined with [], e.g. my_list = [1, 2, 3].")
    conv.add_user_message("How do I add elements?")
    
    print(f"   Conversation ID: {conv.id}")
    print(f"   Title: {conv.title}")
    print(f"   Messages: {len(conv.messages)}")
    
    # 3. Save conversation
    print("\n💾 Saving conversation...")
    mgr.save_conversation(conv, conv.messages)
    print("✅ Saved!")
    
    # 4. List all conversations
    print("\n📋 All conversations:")
    all_convs = mgr.list_conversations()
    for i, c in enumerate(all_convs, 1):
        print(f"   {i}. {c['title']} (ID: {c['id'][:8]}...)")
    
    # 5. Search by text
    print("\n🔍 Search for 'lists':")
    found = mgr.search_conversations("lists")
    for c in found:
        print(f"   ✓ {c['title']} (found)")
    
    # 6. Load and continue conversation
    print("\n🔄 Load and continue conversation...")
    loaded_conv = mgr.load_conversation(str(conv.id))
    print(f"   Loaded: {loaded_conv.title}")
    print(f"   Model: {loaded_conv.model_name}")
    print(f"   Messages: {len(loaded_conv.messages)}")
    
    # Continue conversation
    loaded_conv.add_assistant_message("You can add elements with append(): my_list.append(4)")
    loaded_conv.add_user_message("And how do I remove elements?")
    
    # Save updated conversation
    mgr.save_conversation(loaded_conv, loaded_conv.messages)
    print("✅ Conversation extended and saved!")
    
    # 7. Demonstrate resume
    print("\n🎯 Resume conversation:")
    resumed = mgr.resume_conversation(str(conv.id))
    last_msg = resumed["last_message"]
    print(f"   Last message: '{last_msg['content'][:50]}...'")
    print(f"   Role: {last_msg['role']}")
    
    # 8. Time-based search
    print("\n⏰ Search for today's conversations:")
    today = datetime.now().strftime("%Y-%m-%d")
    recent = mgr.search_by_time(start=today)
    print(f"   Found: {len(recent)} conversation(s) from today")
    
    # 9. Create second demo conversation
    print("\n📝 Creating second conversation...")
    conv2 = Conversation(
        model_name="llama3",
        title="JavaScript Basics", 
        metadata={"topic": "web-dev", "level": "intermediate"}
    )
    conv2.add_user_message("What are arrow functions?")
    conv2.add_assistant_message("Arrow functions are a shorthand syntax for functions in JavaScript: const add = (a, b) => a + b;")
    
    mgr.save_conversation(conv2, conv2.messages)
    print("✅ Second conversation saved!")
    
    # 10. Final: Show all conversations
    print("\n📊 Final overview:")
    all_convs = mgr.list_conversations()
    for i, c in enumerate(all_convs, 1):
        created = c['created_at'][:10]  # Date only
        print(f"   {i}. {c['title']} (created: {created})")
    
    print(f"\n🎉 Demo completed! Database: demo_sessions.db")
    print(f"💡 You can open the file with an SQLite browser to view the data.")

if __name__ == "__main__":
    main() 