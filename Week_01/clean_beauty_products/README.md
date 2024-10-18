# Tira Beauty Clean Filter Extension

## Overview

The Tira Beauty Clean Filter Extension is a Chrome browser add-on designed to enhance your shopping experience on the Tira Beauty website. It automatically applies the "Clean" filter within the "Conscious" category, ensuring that you always view products that meet the "Clean" criteria.

## Features

- Automatically applies the "Clean" filter on Tira Beauty product pages
- Works across all product categories on the Tira Beauty website
- Easy to enable/disable with a single click
- Periodically checks and reapplies the filter if it's removed
- Seamlessly integrates with your browsing experience

## Installation

1. Download or clone this repository to your local machine.
2. Open Google Chrome and navigate to `chrome://extensions/`.
3. Enable "Developer mode" in the top right corner.
4. Click "Load unpacked" and select the directory containing the extension files.

## Usage

1. Click on the extension icon in your Chrome toolbar to open the popup.
2. Use the toggle switch to enable or disable the extension.
3. When enabled, the extension will automatically apply the "Clean" filter on Tira Beauty product pages.
4. The filter will be reapplied every 2 seconds if it's removed or when navigating between pages.

## Files

- `manifest.json`: Configuration file for the Chrome extension
- `popup.html`: HTML file for the extension's popup interface
- `popup.js`: JavaScript file handling the popup's functionality
- `content.js`: Main script that applies and maintains the "Clean" filter

## How It Works

The extension works by injecting a content script (`content.js`) into Tira Beauty web pages. This script:

1. Checks if the "Clean" filter is already applied.
2. If not applied, it locates the "Conscious" filter section and clicks on the "Clean" option.
3. Periodically checks (every 2 seconds) to ensure the filter remains applied.
4. Re-applies the filter when navigating between pages.

## Compatibility

This extension is designed to work specifically with the Tira Beauty website (https://www.tirabeauty.com/).

## Support

If you encounter any issues or have suggestions for improvements, please open an issue in this repository.

## License

[Include your chosen license here]

## Disclaimer

This extension is not officially affiliated with or endorsed by Tira Beauty. Use at your own discretion.
