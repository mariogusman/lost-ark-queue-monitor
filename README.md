# Lost Ark Queue Monitor

This special simple application monitors your position in the queue and sends updates to your Telegram via the @LostArkQueueChecker bot.
It was written in Python using a bunch of libraries while I was in the queue so nothing fancy.

### How it works:
- Takes a screenshot from the center your game screen (where the queue counter is)
- Uses Tesseract OCR to convert that small image into text and saves only the number to a string
- Builds a Telegram API call using your personal telegram user_id and sends the message to you containing your position on the queue.
- The main function is called at an adjustable interval. 
 
### TODO:
- Make it easier to install everything
- Move any user-adjustable settings to a config file
- Update the bot to give you some instructions/important details on the first run
- Edit some of the functions to work more safely and fail-proof
- Properly write this readme file
