"""
Environment setup script for Financial Sentiment Analyst Agent

This script helps users set up their environment and configure API keys.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print setup header."""
    print("=" * 60)
    print(" Financial Sentiment Analyst Agent - Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print(" Checking Python version...")
    
    if sys.version_info < (3, 9):
        print(" Python 3.9 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f" Python {sys.version.split()[0]} is compatible")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    print("\n Setting up virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print(" Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print(" Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError:
        print(" Failed to create virtual environment")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("\n Installing dependencies...")
    
    if os.name == 'nt':  
        pip_path = Path("venv/Scripts/pip")
    else: 
        pip_path = Path("venv/bin/pip")
    
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print(" Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(" Failed to install dependencies")
        return False

def setup_api_keys():
    """Help user set up API keys."""
    print("\n API Key Setup")
    print("You need to set up API keys for the following services:")
    print("1. Google AI (for Gemini API)")
    print("2. NewsAPI.org (for news articles)")
    print()
    
    google_key = os.getenv('GOOGLE_AI_API_KEY')
    news_key = os.getenv('NEWS_API_KEY')
    
    if google_key and news_key:
        print(" API keys are already configured in environment variables")
        return True
    
    print("Please set the following environment variables:")
    print()
    
    if not google_key:
        print(" GOOGLE_AI_API_KEY")
        print("   Get your key from: https://makersuite.google.com/app/apikey")
        print("   Example: export GOOGLE_AI_API_KEY='your_key_here'")
        print()
    
    if not news_key:
        print(" NEWS_API_KEY")
        print("   Get your key from: https://newsapi.org/register")
        print("   Example: export NEWS_API_KEY='your_key_here'")
        print()
    
    print("Alternatively, you can edit 'financial_agent/secrets.py' directly")
    print("and replace the placeholder values with your actual API keys.")
    
    return False

def create_env_file():
    """Create a .env file template."""
    print("\n Creating .env template...")
    
    env_content = """# Financial Sentiment Analyst Agent - Environment Variables
# Copy this file to .env and fill in your actual API keys

# Google AI API Key (for Gemini)
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# NewsAPI.org API Key
NEWS_API_KEY=your_news_api_key_here
"""
    
    with open(".env.template", "w") as f:
        f.write(env_content)
    
    print(" Created .env.template file")
    print("   Copy it to .env and fill in your API keys")

def run_tests():
    """Run the test suite."""
    print("\n Running tests...")
    
    if os.name == 'nt':  
        python_path = Path("venv/Scripts/python")
    else:  
        python_path = Path("venv/bin/python")
    
    try:
        result = subprocess.run([str(python_path), "test_data_fetch.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(" All tests passed!")
            return True
        else:
            print(" Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f" Failed to run tests: {e}")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Set up your API keys (see instructions above)")
    print("2. Activate the virtual environment:")
    if os.name == 'nt':  
        print("   venv\\Scripts\\activate")
    else:  
        print("   source venv/bin/activate")
    print()
    print("3. Run the application:")
    print("   streamlit run app.py")
    print()
    print("4. Open your browser to http://localhost:8501")
    print()
    print("For more information, see README.md")

def main():
    """Main setup function."""
    print_header()
    
    if not check_python_version():
        sys.exit(1)
    
    if not create_virtual_environment():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    api_keys_configured = setup_api_keys()
    
    create_env_file()
    
    if api_keys_configured:
        run_tests()
    
    print_next_steps()

if __name__ == "__main__":
    main()
