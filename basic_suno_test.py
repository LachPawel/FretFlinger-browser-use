# guitar_record_automation.py
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatOpenAI

load_dotenv()

async def start_guitar_recording(extension_prompt="add drums and bass"):
    """Start recording guitar directly in Suno"""
    
    profile_dir = str(Path.home() / ".suno_browser_profile")
    
    agent = Agent(
        task=f"""
        I want to set up guitar recording in Suno:
        
        1. Go to suno.com/create (I should already be logged in)
        2. I can see options: "Upload", "Record", and "song" buttons
        3. Click the "Record" button (the middle option, not Upload)
        4. This should open the recording interface with a red record button and timer
        5. Tell me when the recording interface is ready with the red button visible
        6. Don't start recording yet - just get to the recording interface
        
        Report when you can see the recording interface with the red record button.
        """,
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        browser_session_config={
            "user_data_dir": profile_dir,
            "headless": False
        }
    )
    
    print("🎸 Setting up recording interface...")
    result = await agent.run()
    print("Setup result:", result)
    
    return result

async def record_guitar_session(duration_seconds=30):
    """Record a guitar session for specified duration"""
    
    profile_dir = str(Path.home() / ".suno_browser_profile")
    
    agent = Agent(
        task=f"""
        Record a guitar session:
        
        1. I should see the recording interface with the red record button
        2. Click the red record button to start recording
        3. Tell me "RECORDING STARTED - PLAY YOUR GUITAR NOW!"
        4. Wait for exactly {duration_seconds} seconds
        5. Click the stop button to end recording
        6. Tell me "RECORDING STOPPED" when done
        7. Look for any "next" or "continue" buttons to proceed
        
        Be precise with timing and confirm each step.
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
    
    print(f"🔴 Starting {duration_seconds}-second recording session...")
    print("🎸 Get ready to play your guitar!")
    
    result = await agent.run()
    print("Recording result:", result)
    
    return result

async def set_extension_prompt_and_generate(extension_prompt="add drums and bass"):
    """Set the extension prompt and generate"""
    
    profile_dir = str(Path.home() / ".suno_browser_profile")
    
    agent = Agent(
        task=f"""
        Set up the AI extension for my guitar recording:
        
        1. I should now see options after recording (prompt field, settings, etc.)
        2. Make sure "Instrumental" is checked/enabled
        3. In the song description/prompt field, enter: "Extend this guitar recording: {extension_prompt}"
        4. Look for and click the generate/create button
        5. Confirm that generation has started
        6. Report when the AI is processing my guitar recording
        
        Take your time to find the right fields and buttons.
        """,
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        browser_session_config={
            "user_data_dir": profile_dir,
            "headless": False
        }
    )
    
    print(f"🎵 Setting extension prompt: '{extension_prompt}'")
    print("🚀 Starting AI generation...")
    
    result = await agent.run()
    print("Generation result:", result)
    
    return result

async def live_guitar_jam_session(duration=30, prompt="add rock drums and bass"):
    """Complete live guitar jam session"""
    
    print("🎸 Live Guitar Jam Session with AI")
    print("=" * 40)
    print(f"📝 Extension prompt: {prompt}")
    print(f"⏱️  Recording duration: {duration} seconds")
    
    # Step 1: Setup recording interface
    print("\n🔧 Step 1: Setting up recording...")
    setup_result = await start_guitar_recording()
    
    input("\n🎸 Recording interface ready! Press Enter when you're ready to record...")
    
    # Step 2: Record guitar
    print(f"\n🔴 Step 2: Recording for {duration} seconds...")
    record_result = await record_guitar_session(duration)
    
    # Step 3: Set prompt and generate
    print("\n🎵 Step 3: Setting up AI extension...")
    generate_result = await set_extension_prompt_and_generate(prompt)
    
    print("\n🎉 Guitar jam session started!")
    print("⏳ AI is now extending your guitar with backing instruments...")
    print("🎵 Check Suno for your completed track in a few minutes!")

async def manual_control_session():
    """Manual control - you tell the AI when to start/stop"""
    
    profile_dir = str(Path.home() / ".suno_browser_profile")
    
    print("🎸 Manual Guitar Recording Session")
    print("=" * 35)
    
    # Setup
    await start_guitar_recording()
    
    while True:
        action = input("""
🎛️  What do you want to do?
1. Start recording
2. Stop recording  
3. Set extension prompt and generate
4. Check status
5. Exit

Choice: """)
        
        if action == "1":
            agent = Agent(
                task="Click the red record button to start recording. Tell me when recording has started.",
                llm=ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
                browser_session_config={"user_data_dir": profile_dir, "headless": False}
            )
            result = await agent.run()
            print("🔴 Recording started:", result)
            
        elif action == "2":
            agent = Agent(
                task="Stop the current recording. Click the stop button and tell me when recording has stopped.",
                llm=ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
                browser_session_config={"user_data_dir": profile_dir, "headless": False}
            )
            result = await agent.run()
            print("⏹️ Recording stopped:", result)
            
        elif action == "3":
            prompt = input("🎵 Extension prompt: ") or "add drums and bass"
            await set_extension_prompt_and_generate(prompt)
            
        elif action == "4":
            agent = Agent(
                task="Check the current status - is anything recording, generating, or completed?",
                llm=ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
                browser_session_config={"user_data_dir": profile_dir, "headless": False}
            )
            result = await agent.run()
            print("📊 Status:", result)
            
        elif action == "5":
            break
        else:
            print("Invalid choice")

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY in your .env file")
        return
    
    print("🎸 Suno Guitar Recording Automation")
    print("=" * 40)
    
    choice = input("""
🎵 Choose your recording mode:

1. Quick 30-second jam (automatic)
2. Custom duration jam (automatic) 
3. Manual control (you control start/stop)
4. Just setup recording interface

Choice (1-4): """)
    
    if choice == "1":
        prompt = input("🎵 Extension prompt (or Enter for default): ") or "add rock drums and bass"
        await live_guitar_jam_session(30, prompt)
        
    elif choice == "2":
        duration = int(input("⏱️  Recording duration (seconds): "))
        prompt = input("🎵 Extension prompt (or Enter for default): ") or "add rock drums and bass"
        await live_guitar_jam_session(duration, prompt)
        
    elif choice == "3":
        await manual_control_session()
        
    elif choice == "4":
        await start_guitar_recording()
        print("✅ Recording interface ready! You can now record manually.")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())