import websocket
import json
import random
import string
import re
import pyttsx3
import time

# ============================================================
#  CONFIGURATION - Tweak these to your liking
# ============================================================

# How often to check the price (in seconds) 
CHECK_INTERVAL = 15

# Minimum % price change needed to trigger a commentary
PRICE_CHANGE_THRESHOLD = 0.0003  # 0.03% - BTC moves faster than Gold

# Voice speed (words per minute) - 145 is slower & clearer
VOICE_RATE = 145

# *** SET THIS TO THE INDEX OF YOUR MALE VOICE ***
# Run the STEP 1 check at the top to find the right number
# 0 = first voice, 1 = second voice, 2 = third voice etc.
VOICE_INDEX = 0

# TradingView symbol for BTC/USD (Binance)
TV_SYMBOL = "BINANCE:BTCUSDT"


# ============================================================
#  TRADINGVIEW WEBSOCKET DATA FETCHER
#  Connects as guest - no login, no API key needed
# ============================================================

def generate_session():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(12))
    return "qs_" + random_string


def prepend_header(st):
    return "~m~" + str(len(st)) + "~m~" + st


def construct_message(func, param_list):
    return json.dumps({"m": func, "p": param_list}, separators=(',', ':'))


def create_message(func, param_list):
    return prepend_header(construct_message(func, param_list))


def get_btc_price_tradingview():
    price = None
    ws = None

    try:
        headers = {
            'Origin': 'https://www.tradingview.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
        }

        ws = websocket.create_connection(
            'wss://data.tradingview.com/socket.io/websocket',
            header=headers,
            timeout=10
        )

        session = generate_session()

        ws.send(create_message("set_auth_token", ["unauthorized_user_token"]))
        ws.send(create_message("quote_create_session", [session]))
        ws.send(create_message("quote_set_fields", [
            session, "lp", "ch", "chp", "volume", "bid", "ask"
        ]))
        ws.send(create_message("quote_add_symbols", [session, TV_SYMBOL]))

        start_time = time.time()
        while time.time() - start_time < 8:
            try:
                result = ws.recv()

                if re.match(r'~m~\d+~m~~h~\d+$', result):
                    ws.send(result)
                    continue

                lp_match = re.search(r'"lp":([0-9]+\.?[0-9]*)', result)
                if lp_match:
                    price = float(lp_match.group(1))
                    if 1000 < price < 10000000:
                        break

            except websocket.WebSocketTimeoutException:
                break
            except Exception:
                break

    except Exception as e:
        print(f"  [Data Error] TradingView connection failed: {e}")
        return None
    finally:
        if ws:
            try:
                ws.close()
            except:
                pass

    return price


# ============================================================
#  COMMENTARY GENERATOR - BTC specific tips
# ============================================================

def generate_commentary(price: float, change_pct: float, direction: str) -> str:
    change_display = f"{abs(change_pct * 100):.3f}%"
    price_display = f"{price:,.0f}"

    if direction == "UP":
        if change_pct > 0.01:
            tips = [
                (f"Bitcoin is going absolutely parabolic right now - up {change_display} in seconds!",
                 f"Price blasting through {price_display} dollars. Tip: on moves this explosive, wait for the first red candle before chasing. Do not FOMO in at the top."),
                (f"Massive pump on Bitcoin - up {change_display} and climbing hard!",
                 f"BTC hit {price_display}. Pro tip: whale buys drive these spikes. Check the order book depth. If bid walls are stacking, the move has legs."),
                (f"Bitcoin is on fire - surging {change_display} with serious momentum!",
                 f"Now at {price_display} dollars. Tip: high volume breakouts above round numbers like 70K or 80K are significant. Volume confirms the breakout is real."),
                (f"Explosive BTC candle - up {change_display} just like that!",
                 f"Price smashed to {price_display}. Remember: crypto moves 10 times faster than traditional markets. Trail your stop loss aggressively on runs like this."),
                (f"Bitcoin rockets {change_display} higher in one candle!",
                 f"Trading at {price_display}. Tip: check Bitcoin dominance. If dominance rises with the price, altcoins will likely follow soon after."),
            ]
        elif change_pct > 0.005:
            tips = [
                (f"Strong bullish candle on Bitcoin - {change_display} gained cleanly.",
                 f"Price at {price_display}. Tip: a sustained move above the 20-period moving average on the one-hour chart confirms short-term bullish control."),
                (f"Bitcoin pushing higher with conviction - up {change_display}.",
                 f"Now at {price_display} dollars. Pro tip: if Bitcoin is climbing while stock markets are flat or red, that is a very bullish signal for crypto."),
                (f"Nice upside momentum on BTC - {change_display} in the bag.",
                 f"Price reached {price_display}. Tip: watch the funding rate on perpetual futures. Positive and rising funding means traders are paying to stay long. That is healthy."),
                (f"Bulls stepping in hard on Bitcoin - up {change_display}.",
                 f"Currently at {price_display}. Remember: in a bull market, every dip is bought fast. This {change_display} move is exactly that behaviour."),
                (f"BTC climbing steadily - {change_display} to the upside.",
                 f"At {price_display} dollars. Tip: the previous all-time high acts as a magnet during bull runs. Once above it, price tends to accelerate fast."),
            ]
        else:
            tips = [
                (f"Bitcoin ticking up quietly - a modest {change_display} gain.",
                 f"Currently at {price_display}. Tip: accumulation looks exactly like this. Slow, boring, consistent buying. Do not ignore the small green candles."),
                (f"Small green candle on BTC - up {change_display}.",
                 f"Price at {price_display}. Pro tip: in ranging markets, buy near support and take profit near resistance. Do not force trades when Bitcoin is coiling."),
                (f"Bitcoin inching higher - {change_display} move.",
                 f"Sitting at {price_display}. Tip: a series of higher lows on the hourly chart is the earliest sign a new uptrend is starting. Watch for that pattern."),
                (f"Mild buying pressure on BTC - up {change_display}.",
                 f"Trading at {price_display}. Remember: Bitcoin often grinds up slowly then explodes. These small moves build the foundation for the next big candle."),
                (f"BTC edges up {change_display} - quiet but important.",
                 f"Price at {price_display}. Tip: check the weekly chart. Above the 50-week moving average, the long-term bias is always bullish regardless of daily noise."),
            ]
    else:  # DOWN
        if change_pct < -0.01:
            tips = [
                (f"Bitcoin getting absolutely destroyed right now - down {change_display} in seconds!",
                 f"Bears hammering BTC to {price_display}. Tip: do not catch a falling knife. Wait for a clear bounce candle with volume before thinking about buying the dip."),
                (f"Massive BTC sell-off - dropping {change_display} fast!",
                 f"Price collapsed to {price_display}. Pro tip: sharp drops often overshoot. The first bounce is usually a bull trap. Let the second test of lows confirm the bottom."),
                (f"Bitcoin in freefall - {change_display} wiped out in one candle!",
                 f"Now at {price_display} dollars. Remember: liquidation cascades cause these sudden drops. Check if a major support level just broke on the daily chart."),
                (f"Panic selling on Bitcoin - down {change_display} right now!",
                 f"BTC at {price_display}. Tip: fear drives crypto lower than it should go. Look for a bullish hammer candle on the hourly chart before re-entering. Stay patient."),
                (f"Bears obliterating Bitcoin - {change_display} drop in moments!",
                 f"Price crashed to {price_display}. Pro tip: check the long-to-short ratio on Binance. A ratio above 2 means most traders are still long, which means more pain is possible."),
            ]
        elif change_pct < -0.005:
            tips = [
                (f"Bitcoin losing ground fast - down {change_display}.",
                 f"Sellers stepping in at {price_display}. Watch the next hourly close. A close below the last swing low confirms bearish continuation."),
                (f"Bearish pressure building on BTC - down {change_display}.",
                 f"Price at {price_display}. Tip: a close below the 50-period moving average on the daily chart often triggers a wave of stop-loss hits. That accelerates the drop."),
                (f"Bitcoin sliding lower with intention - {change_display} drop.",
                 f"Now at {price_display} dollars. Pro tip: during crypto downtrends, funding rate flips negative as shorts dominate. That can trigger short squeeze bounces. Stay alert."),
                (f"Sellers in control on BTC - down {change_display}.",
                 f"Trading at {price_display}. Remember: every downtrend has relief bounces of 5 to 10 percent. Do not mistake those bounces for a full reversal without confirmation."),
                (f"Bitcoin under heavy pressure - dropping {change_display}.",
                 f"Price at {price_display}. Tip: compare BTC to Ethereum. If both fall equally it is a broad selloff. If only BTC drops, it is Bitcoin-specific news. Different strategies apply."),
            ]
        else:
            tips = [
                (f"A small dip on Bitcoin - {change_display} to the downside.",
                 f"Price easing to {price_display}. Tip: in strong uptrends, minor dips like this are prime buying opportunities. Check if the 9 EMA is holding on the 15-minute chart."),
                (f"Bitcoin pulls back slightly - down {change_display}.",
                 f"At {price_display} dollars. Pro tip: healthy corrections retrace 38 to 50 percent of the last move. Use Fibonacci retracement levels to find your entry zone."),
                (f"Minor selling on BTC - {change_display} lower.",
                 f"Price now {price_display}. Remember: one red candle does not make a reversal. Look at the bigger picture on the four-hour chart before making any decisions."),
                (f"BTC softens by {change_display} - minor pullback.",
                 f"Trading at {price_display}. Tip: if volume is low on this dip, it is likely just profit taking, not a real reversal. Big players are still holding their positions."),
                (f"Small pullback on Bitcoin - down {change_display}.",
                 f"Price at {price_display}. Pro tip: set a buy limit order at the nearest key support zone. Let the market come to your price. Chasing entries in crypto is costly."),
            ]

    line1, line2 = random.choice(tips)
    return f"{line1} {line2}"


# ============================================================
#  SPEAK FUNCTION - Fresh engine every call, no echo
#  Uses VOICE_INDEX set at top of this file
# ============================================================

def speak(text: str):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', VOICE_RATE)
        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')

        if VOICE_INDEX < len(voices):
            engine.setProperty('voice', voices[VOICE_INDEX].id)
            print(f"  [Voice] Using: {voices[VOICE_INDEX].name}")
        else:
            print(f"  [Voice Warning] VOICE_INDEX {VOICE_INDEX} not found.")
            print(f"  [Voice Warning] Available: {[v.name for v in voices]}")
            print(f"  [Voice Warning] Change VOICE_INDEX at the top of this file.")

        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine

    except Exception as e:
        print(f"  [Voice Error] {e}")


# ============================================================
#  MAIN LOOP
# ============================================================

def main():
    print("=" * 55)
    print("  LIVE TRADING VIBE STREAM - BTC Commentator Bot")
    print("  Voice: Male | Echo: OFF | Engine: Fresh per call")
    print("  Data: TradingView WebSocket (BINANCE:BTCUSDT)")
    print("=" * 55)
    print(f"  Interval   : Every {CHECK_INTERVAL}s")
    print(f"  Threshold  : {PRICE_CHANGE_THRESHOLD * 100:.3f}% price change")
    print(f"  Voice Index: {VOICE_INDEX}  (change VOICE_INDEX at top if wrong)")
    print("=" * 55)
    print("  Waiting for first BTC price tick...")
    print()

    last_price = None
    fail_count = 0

    while True:
        try:
            current_price = get_btc_price_tradingview()

            if current_price is None:
                fail_count += 1
                print(f"  [Warning] Could not fetch BTC price. Retry {fail_count}/5...")
                if fail_count >= 5:
                    print("  [Error] Too many failures. Check your internet connection.")
                    print("  Retrying in 60 seconds...")
                    time.sleep(60)
                    fail_count = 0
                else:
                    time.sleep(CHECK_INTERVAL)
                continue

            fail_count = 0
            current_price = round(current_price, 2)

            if last_price is None:
                last_price = current_price
                print(f"  Starting BTC price locked in: ${current_price:,.2f}")
                time.sleep(CHECK_INTERVAL)
                continue

            change_pct = (current_price - last_price) / last_price
            direction = "UP" if change_pct >= 0 else "DOWN"

            print(f"  BTC: ${current_price:,.2f}  |  Change: {change_pct * 100:+.4f}%", end="")

            if abs(change_pct) >= PRICE_CHANGE_THRESHOLD:
                print(f"  <- TRIGGERING COMMENTARY ({direction})")
                print()

                commentary = generate_commentary(current_price, change_pct, direction)
                snippet = commentary[:80] + "..."
                print(f"  Script: \"{snippet}\"")
                print()

                print("  Speaking now...")
                print()
                speak(commentary)

                last_price = current_price
            else:
                print("  (below threshold, skipping)")

        except KeyboardInterrupt:
            print()
            print()
            print("  Bot stopped by user. Goodbye!")
            break
        except Exception as e:
            print()
            print(f"  [Unexpected Error] {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
