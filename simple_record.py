# fix_permission_override.py
import asyncio
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatOpenAI

load_dotenv()

def create_fresh_browser_profile():
    """Create a completely fresh browser profile with microphone permissions"""
    
    # Use a completely new profile directory
    fresh_profile = Path.home() / ".suno_fresh_profile"
    
    if fresh_profile.exists():
        import shutil
        shutil.rmtree(fresh_profile)
        print(f"🗑️ Removed old profile: {fresh_profile}")
    
    fresh_profile.mkdir()
    print(f"✅ Created fresh profile: {fresh_profile}")
    
    # Create preferences file with microphone allowed
    prefs_dir = fresh_profile / "Default"
    prefs_dir.mkdir()
    
    # Enhanced preferences with comprehensive media permissions
    preferences = {
        "profile": {
        },
        "webkit": {
            "webprefs": {
                "default_encoding": "UTF-8"
            }
        }
    }
    
    prefs_file = prefs_dir / "Preferences"
    with open(prefs_file, 'w') as f:
        json.dump(preferences, f, indent=2)
    
    print("✅ Created preferences with microphone allowed")
    return str(fresh_profile)

def get_working_browser_args():
    """Get browser arguments that actually work for microphone access"""
    return [
    
    ]

async def test_with_fresh_profile():
    """Test with completely fresh profile and proper flags"""
    
    fresh_profile = create_fresh_browser_profile()
    
    agent = Agent(
        task="""
        Test microphone with fresh profile and proper browser flags:
        
        1. Go to https://suno.com/create
        2. Look for the record/microphone button (usually a + or microphone icon)
        3. Click on "Audio" or "Record" option
        4. Try to start recording audio
        5. Report if you can successfully start recording
        6. If there are any permission prompts, accept them
        7. If recording starts, try to record for 2-3 seconds then stop
        8. Report the exact behavior and any errors you see
        
        The browser should now automatically allow microphone access.
        """,
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        browser_session_config={
            "user_data_dir": fresh_profile,
            "headless": False,
            "browser_args": get_working_browser_args()
        }
    )
    
    print("🆕 Testing with fresh browser profile and working flags...")
    result = await agent.run()
    print("✅ Fresh profile test result:", result)
    
    return result

async def test_without_browser_use():
    """Test by manually launching browser without Browser Use interference"""
    
    fresh_profile = create_fresh_browser_profile()
    
    print("🌐 Manual Browser Launch (No Browser Use)")
    print("=" * 45)
    print()
    print("1. Close any existing Chrome/Chromium windows")
    print("2. Run this command in terminal:")
    print()
    
    # Find Chrome path
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "google-chrome",
        "chromium-browser"
    ]
    
    chrome_path = None
    for path in chrome_paths:
        if Path(path).exists():
            chrome_path = path
            break
    
    if not chrome_path:
        chrome_path = "google-chrome"
    
    # Use the same working flags
    flags = " ".join([f'    {flag} \\' for flag in get_working_browser_args()])
    
    command = f'''"{chrome_path}" \\
    --user-data-dir="{fresh_profile}" \\
{flags}
    "https://suno.com/create"'''
    
    print(command)
    print()
    print("3. Test recording in the manually opened browser")
    print("4. Check if microphone permissions work without Browser Use")
    print()
    print("💡 This will show if Browser Use is causing the permission issues")

async def test_minimal_browser_use():
    """Test with Browser Use but minimal interference"""
    
    fresh_profile = create_fresh_browser_profile()
    
    agent = Agent(
        task="""
        Simple test with working browser flags:
        
        1. Go to https://suno.com/create
        2. Look for any audio/recording options
        3. Try to access the microphone/recording feature
        4. Report what happens - can you record audio?
        5. Test if the microphone icon shows as allowed (not blocked)
        
        Just focus on whether microphone access works.
        """,
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        browser_session_config={
            "user_data_dir": fresh_profile,
            "headless": False,
            "browser_args": get_working_browser_args()
        }
    )
    
    print("🔬 Testing with Browser Use + working flags...")
    result = await agent.run()
    print("✅ Minimal test result:", result)
    
    return result

async def debug_permissions():
    """Debug what's happening with permissions in detail"""
    
    fresh_profile = create_fresh_browser_profile()
    
    agent = Agent(
        task="""
        Debug microphone permissions step by step:
        
        1. Go to chrome://settings/content/microphone
        2. Check if suno.com is listed and what its permission status is
        3. Go to https://suno.com/create
        4. Open Developer Tools (F12) 
        5. In the console, run this JavaScript:
           navigator.mediaDevices.getUserMedia({audio: true})
           .then(() => console.log('✅ Microphone access granted'))
           .catch(err => console.log('❌ Microphone error:', err))
        6. Click the lock/info icon in the address bar
        7. Check the site permissions for microphone
        8. Try to use the actual recording feature on Suno
        9. Report all findings in detail
        
        Give me the exact status of microphone permissions at each step.
        """,
        llm=ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        browser_session_config={
            "user_data_dir": fresh_profile,
            "headless": False,
            "browser_args": get_working_browser_args()
        }
    )
    
    print("🔍 Running detailed permission diagnosis...")
    result = await agent.run()
    print("✅ Debug results:", result)
    return result

def reset_all_profiles():
    """Reset all browser profiles we've created"""
    
    profiles = [
        Path.home() / ".suno_browser_profile",
        Path.home() / ".suno_fresh_profile"
    ]
    
    for profile in profiles:
        if profile.exists():
            import shutil
            shutil.rmtree(profile)
            print(f"🗑️ Deleted: {profile}")
    
    print("✅ All profiles reset")

async def test_comprehensive():
    """Run all tests to find what works"""
    
    print("🔬 Running comprehensive test suite...")
    print("=" * 50)
    
    # Reset everything first
    reset_all_profiles()
    await asyncio.sleep(1)
    
    print("\n1️⃣ Testing minimal Browser Use with working flags...")
    try:
        result1 = await test_minimal_browser_use()
        print(f"Result 1: {result1}")
    except Exception as e:
        print(f"Test 1 failed: {e}")
    
    print("\n" + "="*50)
    print("\n2️⃣ Testing fresh profile with enhanced permissions...")
    try:
        result2 = await test_with_fresh_profile()  
        print(f"Result 2: {result2}")
    except Exception as e:
        print(f"Test 2 failed: {e}")
    
    print("\n" + "="*50)
    print("\n3️⃣ Running permission diagnostics...")
    try:
        result3 = await debug_permissions()
        print(f"Result 3: {result3}")
    except Exception as e:
        print(f"Test 3 failed: {e}")
    
    print("\n" + "="*50)
    print("\n4️⃣ Manual browser instructions...")
    await test_without_browser_use()
    
    print("\n🎯 SUMMARY:")
    print("- The --use-fake-ui-for-media-stream flag should fix the issue")
    print("- If Browser Use still blocks it, try the manual browser approach")
    print("- Check the debug results for specific error messages")

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY in your .env file")
        return
    
    print("🔧 Fix Permission Override Issue - ENHANCED VERSION")
    print("=" * 55)
    print("\n🆕 NOW WITH WORKING BROWSER FLAGS!")
    print("The --use-fake-ui-for-media-stream flag should fix your issue.")
    
    choice = input("""
🎯 Choose your test approach:

1. Quick test with working flags (RECOMMENDED)
2. Manual browser launch (no Browser Use)  
3. Detailed permission debugging
4. Reset all profiles and start over
5. Comprehensive test (all of the above)

Choice (1-5): """)
    
    if choice == "1":
        await test_minimal_browser_use()
    elif choice == "2":
        await test_without_browser_use()
    elif choice == "3":
        await debug_permissions()
    elif choice == "4":
        reset_all_profiles()
        print("✅ All profiles reset. Try option 1 next.")
    elif choice == "5":
        await test_comprehensive()
    else:
        print("Invalid choice")
        return
    
    print("\n💡 If microphone still doesn't work:")
    print("   - Try option 2 (manual browser) to test without Browser Use")
    print("   - The issue might be browser_use itself overriding permissions")
    print("   - Check console output for specific error messages")

if __name__ == "__main__":
    asyncio.run(main())