# guitar_upload_automation.py
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatOpenAI

load_dotenv()

async def upload_guitar_to_suno(audio_file_path, extension_prompt="add drums and bass"):
    """Upload guitar file and extend it with AI"""
    
    profile_dir = str(Path.home() / ".suno_browser_profile")
    
    # Make sure the audio file exists
    if not Path(audio_file_path).exists():
        print(f"❌ Audio file not found: {audio_file_path}")
        return None
    
    agent = Agent(
        task=f"""
        I want to upload a guitar recording to Suno and extend it:
        
        1. Go to suno.com/create (I should already be logged in)
        2. Click the "Upload" button (I can see it in the interface)
        3. Upload this audio file: {audio_file_path}
        4. Make sure "Instrumental" is checked/enabled 
        5. In the song description area, enter: "Extend this guitar recording: {extension_prompt}"
        6. Click the generate/create button to start the AI extension
        7. Report when the generation has started
        
        Take your time and describe each step as you do it.
        """,
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        browser_session_config={
            "user_data_dir": profile_dir,
            "headless": False  # Keep visible so we can watch
        }
    )
    
    print(f"🎸 Uploading guitar file: {audio_file_path}")
    print(f"🎵 Extension prompt: {extension_prompt}")
    print("👀 Watch the browser - AI is working...")
    
    result = await agent.run()
    print("\n✅ Upload process complete!")
    print("Result:", result)
    
    return result

async def check_generation_status():
    """Check if the generation is complete and ready for download"""
    
    profile_dir = str(Path.home() / ".suno_browser_profile")
    
    agent = Agent(
        task="""
        Check the status of my Suno generation:
        
        1. Look at the current page for any completed tracks
        2. Check if generation is still in progress (loading/processing indicators)
        3. If I see a completed track with play button, that means it's done
        4. If completed, look for download options or ways to save the audio
        5. Report the status: "GENERATING", "COMPLETED", or "ERROR"
        6. If completed, describe how to download/save the result
        """,
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        browser_session_config={
            "user_data_dir": profile_dir,
            "headless": False
        }
    )
    
    print("🔍 Checking generation status...")
    result = await agent.run()
    print("Status check result:", result)
    
    return result

async def download_completed_track():
    """Download the completed track"""
    
    profile_dir = str(Path.home() / ".suno_browser_profile")
    
    agent = Agent(
        task="""
        Download my completed Suno track:
        
        1. Look for the most recent completed track
        2. Find download options (three-dot menu, download button, or right-click)
        3. Download the audio file
        4. Report when download is complete and where it was saved
        """,
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        browser_session_config={
            "user_data_dir": profile_dir,
            "headless": False
        }
    )
    
    print("💾 Downloading completed track...")
    result = await agent.run()
    print("Download result:", result)
    
    return result

async def complete_guitar_workflow(audio_file_path, extension_prompt="add drums and bass"):
    """Complete workflow: upload → wait → download"""
    
    print("🎸 Starting Complete Guitar Extension Workflow")
    print("=" * 50)
    
    # Step 1: Upload
    upload_result = await upload_guitar_to_suno(audio_file_path, extension_prompt)
    if not upload_result:
        return
    
    print("\n" + "=" * 50)
    print("⏳ Waiting for generation to complete...")
    print("💡 This usually takes 1-3 minutes")
    
    # Step 2: Wait and check status
    for attempt in range(12):  # Check every 30 seconds for 6 minutes
        await asyncio.sleep(30)
        
        print(f"\n🔍 Status check {attempt + 1}/12...")
        status_result = await check_generation_status()
        
        status_str = str(status_result).upper()
        if "COMPLETED" in status_str or "DONE" in status_str:
            print("🎉 Generation completed!")
            break
        elif "ERROR" in status_str or "FAILED" in status_str:
            print("❌ Generation failed")
            return
        else:
            print("⏳ Still generating... waiting 30 more seconds")
    else:
        print("⚠️ Timeout reached. Check Suno manually for your track.")
        return
    
    print("\n" + "=" * 50)
    
    # Step 3: Download
    download_result = await download_completed_track()
    
    print("\n🎉 Guitar extension workflow complete!")
    print("🎸 Your extended guitar track should be ready to jam with!")

async def quick_test_upload():
    """Quick test with a simple file"""
    
    # You'll need to put a real audio file here
    test_file = "./guitar-test.m4a"  # Change this to your guitar file
    
    if not Path(test_file).exists():
        print(f"❌ Please create a test file at: {test_file}")
        print("   Or change the path in the script to your guitar recording")
        return
    
    await upload_guitar_to_suno(test_file, "add rock drums and bass guitar")

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY in your .env file")
        return
    
    print("🎸 Suno Guitar Upload Automation")
    print("=" * 35)
    
    choice = input("""
What would you like to do?
1. Quick test upload (upload only)
2. Complete workflow (upload → wait → download)
3. Check status of current generation
4. Download completed track

Choice (1-4): """)
    
    if choice == "1":
        await quick_test_upload()
    elif choice == "2":
        audio_file = input("📁 Path to your guitar file: ")
        prompt = input("🎵 Extension prompt (or press Enter for default): ") or "add drums and bass"
        await complete_guitar_workflow(audio_file, prompt)
    elif choice == "3":
        await check_generation_status()
    elif choice == "4":
        await download_completed_track()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())