FROM python:3.10-slim-buster
WORKDIR /bot

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run the bot
CMD ["python", "bot.py"]