#!/usr/bin/env python3
"""
Quick verification script: connect to Chrome DevTools and check if a thread
was actually posted on @Cabral_Cripto's profile.

Usage:
    python verify_tweet_posted.py

Requires Chrome running with --remote-debugging-port=9222 and user logged into X.
"""

import asyncio
import sys

from pyppeteer import connect


async def main():
    browser = await connect(browserURL='http://127.0.0.1:9222')
    pages = await browser.pages()

    # Find profile tab or open one
    target = None
    for p in pages:
        if 'Cabral_Cripto' in p.url:
            target = p
            break

    if not target:
        # Create via requests shortcut
        import requests
        resp = requests.put(
            'http://127.0.0.1:9222/json/new?https://x.com/Cabral_Cripto'
        )
        if resp.status_code != 200:
            print("FAILED to open profile tab")
            await browser.disconnect()
            return

        # Reconnect to find the new tab
        await browser.disconnect()
        await asyncio.sleep(1)
        browser = await connect(browserURL='http://127.0.0.1:9222')
        pages = await browser.pages()
        for p in pages:
            if 'Cabral_Cripto' in p.url:
                target = p
                break

    if not target:
        print("FAILED: Could not open @Cabral_Cripto profile")
        await browser.disconnect()
        return

    await target.bringToFront()
    await asyncio.sleep(4)

    # Check for latest tweets
    tweets = await target.evaluate("""() => {
        const articles = document.querySelectorAll('article');
        const results = [];
        for (const a of articles) {
            const textEl = a.querySelector('[data-testid="tweetText"]');
            if (textEl) {
                results.push(textEl.innerText.substring(0, 120));
            }
        }
        return results;
    }""")

    print(f"\n📊 Latest tweets found: {len(tweets)}")
    for i, t in enumerate(tweets[:5]):
        print(f"\n  [{i+1}] {t}")
        print(f"       └─ {len(t)} chars")

    # Check for premium toast
    toasts = await target.evaluate("""() => {
        const statusEls = document.querySelectorAll('[role="status"]');
        const results = [];
        for (s of statusEls) {
            results.push(s.innerText || '');
        }
        return results;
    }""")

    if any('Premium' in t or 'upgrade' in t.lower() for t in toasts):
        print("\n⚠️  PREMIUM TOAST DETECTED! Some tweets may not have posted.")

    await browser.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
