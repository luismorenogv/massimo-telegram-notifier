# Massimo Telegram Notifier

**Massimo Telegram Notifier** is a Python-based project that allows you to monitor the availability of specific products on Massimo Dutti's website. When the desired product size becomes available, the script sends a notification to a specified Telegram chat using a bot.

The script works in conjunction with GitHub Actions to perform hourly checks and can be modified to work with other websites by adjusting the web scraping logic.

## Features

- Automated hourly checks for product availability on Massimo Dutti.
- Sends instant notifications to a Telegram chat when the desired size becomes available.
- Easily configurable and adaptable to other websites.

## Requirements

- A Telegram bot token and chat ID.

### Obtaining the Telegram Bot Token and Chat ID

1. **Create a Telegram Bot:**
   - Open Telegram and search for the "BotFather" account.
   - Start a conversation with BotFather and use the `/newbot` command to create a new bot.
   - Follow the instructions to choose a name and username for your bot.
   - After creation, you will receive a **Bot Token**. Keep it safe.

2. **Add the Bot to Your Group:**
   - Create a new Telegram group or use an existing one.
   - Add your bot to the group.

3. **Promote the Bot to Admin:**
   - To ensure the bot can read all messages, promote it to admin status in the group.

4. **Obtain the Group Chat ID:**
   - Send any message in the group.
   - Use the following URL in your browser to get the updates, replacing `<YOUR_BOT_TOKEN>`:

     ```
     https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
     ```

   - Look for the `"chat"` object in the returned JSON. The `"id"` field will be your Group Chat ID.

## Setup and Configuration

1. **Fork the Repository:**
   - Fork this repository to your GitHub account.

2. **Edit the `config.py` File:**
   - Navigate to the `config.py` file in your forked repository on GitHub.
   - Click the pencil icon to edit the file.
   - Replace the placeholder values with your actual Telegram bot token, chat ID, product URLs, and desired product sizes.

    ```python
    # config.py

    # Bot telegram configuration
    TOKEN = 'your_telegram_bot_token_here'  # e.g., '123456789:ABCdefGhIJKlmnoPQRstuVWxYZ'
    CHAT_ID = 'your_chat_id_here'  # e.g., -1001234567890

    # List of desired products and sizes
    items = [
        ('https://www.massimodutti.com/product-page1', '42'),
        ('https://www.massimodutti.com/product-page2', 'XL')
    ]
    ```

3. **Commit Your Changes:**
   - After editing the `config.py` file, scroll down to the commit message box.
   - Write a brief commit message and click the "Commit changes" button to save your modifications to your forked repository.

4. **Enabling the Workflow:**

   If you fork this repository, the GitHub Actions workflow will be disabled by default. To enable it:

   - Go to the "Actions" tab in your forked repository.
   - You will see a message indicating that workflows are disabled.
   - Click the "Enable Workflow" button.
   - The workflow will now be enabled, and you can run it manually or let it run according to the schedule.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to discuss improvements.

If you find this project helpful, please consider giving it a ⭐! :)



