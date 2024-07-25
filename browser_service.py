from pyppeteer import launch

class BrowserService:
    def __init__(self):
        self.browser = None
        self.page = None

    async def initialize_browser(self):
        if not self.browser:
            try:
                self.browser = await launch(
                    executablePath='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                    headless=False,
                    args=['--ignore-certificate-errors', '--no-sandbox', '--disable-dev-shm-usage']
                )
                self.page = await self.browser.newPage()
                await self.page.setViewport({'width': 1280, 'height': 800})
                await self.page.setExtraHTTPHeaders({'Accept-Language': 'en-US,en;q=0.9'})
                await self.page.goto('http://localhost:8000', {'waitUntil': 'networkidle2'})
                await self.page.click('#join')
                await self.page.waitForSelector('video')
                await self.page.waitFor(2000)
            except Exception as e:
                print(f"Error initializing browser: {e}")
                self.browser = None
                self.page = None
                await self.close_browser()
                raise

    async def take_screenshot(self, video_output_path: str, map_output_path: str):
        await self.initialize_browser()

        # Take screenshot of the video element
        video_wrapper = await self.page.querySelector('#player-1000')
        video_element = await video_wrapper.querySelector('video')
        await video_element.screenshot({'path': video_output_path})

        # Take screenshot of the Mapbox map element
        map_element = await self.page.querySelector('#map')
        await map_element.screenshot({'path': map_output_path})

        return video_output_path, map_output_path

    async def data(self) -> dict:
        await self.initialize_browser()

        bot_data = await self.page.evaluate('''() => {
        return window.rtm_data;
        }''')

        return bot_data

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None
