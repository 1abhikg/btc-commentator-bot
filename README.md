Live Trading Commentator Bot — BTC & Gold (XAU/USD)
This is a real-time trading commentary bot built in Python, designed for live streamers and traders who want an automated voice assistant that tracks cryptocurrency and Gold price movements and speaks live commentary during streams.
The bot connects directly to TradingView's WebSocket feed to pull real-time BTC/USDT and XAU/USD price data with zero delay and no API key required. Every time the price moves beyond a set threshold, the bot automatically generates and speaks a trading tip or market commentary using the Windows built-in text-to-speech engine (pyttsx3), keeping your stream engaging and informative without any manual input.
Features:

Real-time price feed via TradingView WebSocket — no delays, no API key
Automatic voice commentary on every significant price movement
BTC and Gold bots included as separate scripts
Randomized commentary pool — tips never repeat back to back
Male voice optimized for stream clarity
Fresh engine reinitialization on every announcement — prevents the pyttsx3 freeze bug
Lightweight — runs smoothly on older hardware
Compatible with Windows 7 and Python 3.8

Trading Tips Covered in Commentary:
The bot speaks real trading insights including whale order book analysis, funding rate signals, liquidation cascade warnings, BTC dominance shifts, long/short ratio readings, Fibonacci retracement levels, support and resistance zones, and general market sentiment — all randomized and triggered automatically based on price movement size.
Built For:
This bot was built and tested on a Windows 7 machine running Python 3.8 with an Intel Core i7-4770 processor. It was specifically engineered to work around the onnxruntime DLL incompatibility that affects Windows 7, replacing the Kokoro ONNX voice engine with pyttsx3 as a fully local, zero-dependency alternative that works reliably on older systems.
Future Plans:
When upgraded to Windows 10 or 11, the bot can be switched to the Kokoro ONNX am_adam high-quality male voice using the included model.onnx and voices-v1.0.bin files — no code rewrite needed, just a single function swap.
