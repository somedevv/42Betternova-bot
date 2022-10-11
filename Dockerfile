FROM python:3.10.7-alpine3.16
WORKDIR /bot

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run the bot
CMD ["python", "-u", "bot.py"]