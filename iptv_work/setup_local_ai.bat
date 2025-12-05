@echo off
echo ========================================
echo Local AI Model Setup Script
echo ========================================
echo.

echo Checking if Ollama is installed...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama is not installed!
    echo.
    echo Please download and install Ollama from: https://ollama.com/download
    echo After installation, run this script again.
    pause
    exit /b 1
)

echo Ollama is installed!
echo.

echo Available models to download:
echo 1. Llama 3.2 3B (Small, ~2GB, Fast)
echo 2. Llama 3.2 7B (Medium, ~4GB, Better quality)
echo 3. Mistral 7B (Medium, ~4GB, Good balance)
echo 4. Phi-3 Mini (Small, ~2GB, Fast)
echo 5. DeepSeek R1 7B (Medium, ~4GB, Good for coding)
echo 6. Download all small models (3B variants)
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo Downloading Llama 3.2 3B...
    ollama pull llama3.2:3b
) else if "%choice%"=="2" (
    echo Downloading Llama 3.2 7B...
    ollama pull llama3.2:7b
) else if "%choice%"=="3" (
    echo Downloading Mistral 7B...
    ollama pull mistral:7b
) else if "%choice%"=="4" (
    echo Downloading Phi-3 Mini...
    ollama pull phi3:mini
) else if "%choice%"=="5" (
    echo Downloading DeepSeek R1 7B...
    ollama pull deepseek-r1:7b
) else if "%choice%"=="6" (
    echo Downloading all small models...
    ollama pull llama3.2:3b
    ollama pull phi3:mini
) else if "%choice%"=="7" (
    exit /b 0
) else (
    echo Invalid choice!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To use with Cursor:
echo 1. Make sure Ollama is running (it should start automatically)
echo 2. In Cursor Settings, add a custom model endpoint:
echo    - API URL: http://localhost:11434/v1/chat/completions
echo    - Model name: llama3.2:7b (or your chosen model)
echo.
echo To test locally, run: ollama run llama3.2:7b
echo.
pause








